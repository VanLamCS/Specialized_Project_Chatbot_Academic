

def flat_dataset(data):
    newData = []
    for dataItem in data:
        item = {'title': dataItem['title'], 'context': dataItem['context']}
        for qa in dataItem['qas']:
            for q in qa['question']:
                item['question'] = q
                item['answers'] = {
                    'text': [qa['answer']['text']],
                    'answer_start': [qa['answer']['answer_start']],
                    'answer_end': [qa['answer']['answer_end']],
                }
                newData.append(item)
    return newData