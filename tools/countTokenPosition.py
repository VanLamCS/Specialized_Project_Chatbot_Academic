from transformers import AutoTokenizer, AutoModelForQuestionAnswering

tokenizer = AutoTokenizer.from_pretrained("hoang14/viettel-phobert-finetune-viquad")
# tokenizer = AutoTokenizer.from_pretrained("duyduong9htv/phobert-qa-finetuned-viet-qa")
model = AutoModelForQuestionAnswering.from_pretrained("hoang14/viettel-phobert-finetune-viquad")

def countTokenPosition(context, ans): 
  contextTokens = tokenizer(context)["input_ids"]
  ansTokens = tokenizer(ans)["input_ids"]
  ansTokens = ansTokens[1:len(ansTokens) - 1]
  lenContextTokens = len(contextTokens)
  lenAnsTokens = len(ansTokens)
  if lenAnsTokens > lenContextTokens:
    return (-1 ,-1)
  for i in range(lenContextTokens - lenAnsTokens):
    if contextTokens[i] == ansTokens[0]:
      isFind = True
      for j in range(lenAnsTokens):
        if ansTokens[j] != contextTokens[i + j]:
          isFind = False
      if isFind:
        return (i, i + len(ansTokens))
  return (-1, -1)
