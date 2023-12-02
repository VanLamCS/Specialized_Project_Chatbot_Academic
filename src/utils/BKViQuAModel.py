import numpy as np
import torch
from torch import nn
from transformers import AutoModelForQuestionAnswering, BartphoTokenizerFast
from datasets import Dataset, DatasetDict
import uuid
from get_contexts import get_all_contexts, get_contexts_by_key

# import sys
# import os

# current_dir = os.path.dirname(os.path.abspath(__file__))
# checkpoints_dir = os.path.abspath(os.path.join(current_dir, "../checkpoints"))

# sys.path.append(checkpoints_dir)


class ViQuADModel:
    def __init__(
        self,
        device="cuda",
        checkpoints="checkpoints",
        n_best=20,
        max_length=256,
        max_answer_length=200,
        stride=128,
        mode_limit=700,
    ):
        self.device = torch.device(device)
        self.checkpoints = checkpoints

        self.n_best = n_best
        self.max_length = max_length
        self.max_answer_length = max_answer_length
        self.stride = stride

        self.model = AutoModelForQuestionAnswering.from_pretrained(self.checkpoints)
        self.model = nn.DataParallel(self.model)
        self.tokenizer = BartphoTokenizerFast.from_pretrained("vinai/phobert-base-v2")
        self.model.to(self.device)
        self.mode_limit = mode_limit

    def create_dataset(self, contexts):
        context_length = len(contexts)
        context_ids = []
        for i in contexts:
            new_id = uuid.uuid4()
            context_ids.append(str(new_id))

        return Dataset.from_dict({"context": contexts, "id": context_ids})

    def pre_dataset(self, question, contexts):
        new_column = [question] * len(contexts)
        qa_dataset = contexts.add_column("question", new_column)
        return qa_dataset

    def pre_map_dataset(self, dataset, preprocess_dataset):
        return dataset.map(
            preprocess_dataset,
            batched=True,
            remove_columns=dataset.column_names,
            load_from_cache_file=False,
        )

    def preprocess_dataset(self, examples):
        questions = [q.strip() for q in examples["question"]]
        inputs = self.tokenizer(
            questions,
            examples["context"],
            max_length=self.max_length,
            truncation="only_second",
            stride=self.stride,
            return_overflowing_tokens=True,
            return_offsets_mapping=True,
            padding="max_length",
        )

        sample_map = inputs.pop("overflow_to_sample_mapping")
        example_ids = []

        for i in range(len(inputs["input_ids"])):
            sample_idx = sample_map[i]
            example_ids.append(examples["id"][sample_idx])

            sequence_ids = inputs.sequence_ids(i)
            offset = inputs["offset_mapping"][i]
            inputs["offset_mapping"][i] = [
                o if sequence_ids[k] == 1 else None for k, o in enumerate(offset)
            ]

        inputs["example_id"] = example_ids
        inputs["overflow_to_sample_mapping"] = sample_map
        return inputs

    def query_model(self, eval_set_for_model, length):
        i = 0

        start_logits = []
        end_logits = []
        while i <= length:
            start = i
            i += self.mode_limit
            if i < length:
                end = i
            else:
                end = length
            print("Batched at %s index to %s index, all: %s" % (start, end - 1, length))

            batch = {
                k: eval_set_for_model[k][start:end].to("cuda")
                for k in eval_set_for_model.column_names
            }

            with torch.no_grad():
                outputs = self.model(**batch)
                start_logits.append(outputs["start_logits"])
                end_logits.append(outputs["end_logits"])

        start_logits = torch.cat(start_logits, dim=0)
        end_logits = torch.cat(end_logits, dim=0)

        start_logits = start_logits.detach().cpu().numpy()
        end_logits = end_logits.detach().cpu().numpy()
        return start_logits, end_logits

    def exact_answer(
        self,
        all_contexts,
        start_logits,
        end_logits,
        overflow_to_sample_mapping,
        eval_mapped_dataset,
    ):
        answers = []

        for index in range(len(start_logits)):
            start_logit = start_logits[index]
            end_logit = end_logits[index]

            offsets = eval_mapped_dataset["offset_mapping"][index]
            context = all_contexts[overflow_to_sample_mapping[index]]["context"]

            start_indexes = np.argsort(start_logit)[-1 : -self.n_best - 1 : -1].tolist()
            end_indexes = np.argsort(end_logit)[-1 : -self.n_best - 1 : -1].tolist()

            for start_index in start_indexes:
                for end_index in end_indexes:
                    # Skip answers that are not fully in the context
                    if offsets[start_index] is None or offsets[end_index] is None:
                        continue

                    # Skip answers with a length that is either < 0 or > max_answer_length.
                    if (
                        end_index < start_index
                        or end_index - start_index + 1 > self.max_answer_length
                    ):
                        continue

                    answers.append(
                        {
                            "text": context[
                                offsets[start_index][0] : offsets[end_index][1]
                            ],
                            "logit_score": start_logit[start_index]
                            + end_logit[end_index],
                        }
                    )
        best_answer = max(answers, key=lambda x: x["logit_score"])

        return best_answer

    def forward(self, question, context_key):
        contexts = get_contexts_by_key(context_key)
        context_dataset = self.create_dataset(contexts)

        dataset = self.pre_dataset(question, context_dataset)
        eval_mapped_dataset = self.pre_map_dataset(dataset, self.preprocess_dataset)

        overflow_to_sample_mapping = eval_mapped_dataset["overflow_to_sample_mapping"]
        eval_set_for_model = eval_mapped_dataset.remove_columns(
            ["example_id", "offset_mapping", "overflow_to_sample_mapping"]
        )

        eval_set_for_model.set_format("torch")
        length = eval_set_for_model.num_rows

        start_logits, end_logits = self.query_model(eval_set_for_model, length)
        answer = self.exact_answer(
            context_dataset,
            start_logits,
            end_logits,
            overflow_to_sample_mapping,
            eval_mapped_dataset,
        )
        return answer
