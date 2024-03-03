import json
import datasets
from constants import *

logger = datasets.logging.get_logger(__name__)

class BKViQuADConfig(datasets.BuilderConfig):
    def __init__(self, **kwargs):
        super(BKViQuADConfig, self).__init__(**kwargs)

class ViQuAD(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        BKViQuADConfig(
            name="plain_text",
            version=datasets.Version("2.0.0", ""),
            description="Plain text",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description="BKViQuAD2.0",
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers": datasets.features.Sequence(
                        {
                            "text": datasets.Value("string"),
                            "answer_start": datasets.Value("int64"),
                        }
                    ),
                }
            ),
        )

    def _split_generators(self, dl_manager):
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": DATASET_FOLDER + "/merge_dataset/new_train.json"}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": DATASET_FOLDER+ "/merge_dataset/validation.json"}),
        ]

    def _generate_examples(self, filepath):
        logger.info("generating examples from = %s", filepath)
        key = 0
        with open(filepath, encoding="utf-8") as f:
            squad = json.load(f)
        
        for qa in squad["data"]:
            if len(qa["answers"]["answer_start"]) >= 1:
                yield key, {
                    "id": qa["id"],
                    "context": qa["context"],
                    "question": qa["question"],
                    "title": qa["title"],
                    "answers": {
                        "answer_start": [qa["answers"]["answer_start"][0]],
                        "text": [qa["answers"]["text"][0]]
                    }
                }
                key += 1
