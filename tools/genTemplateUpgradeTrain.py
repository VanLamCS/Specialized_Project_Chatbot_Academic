import json
import os

# Đường dẫn đến thư mục chứa các file cần xử lý
input_folder = 'test/data'

# Đường dẫn đến thư mục để lưu các file đã xử lý
output_folder = 'test/upgradeData'
os.makedirs(output_folder, exist_ok=True)

# Lặp qua tất cả các file trong thư mục input_folder
for filename in os.listdir(input_folder):
  if filename.endswith('.json'):  # Chỉ xử lý các file có đuôi .json
    input_file_path = os.path.join(input_folder, filename)
    output_file_path = os.path.join(output_folder, filename)

    # Đọc dữ liệu từ file JSON
    with open(input_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Xử lý dữ liệu và tạo dữ liệu mới
    new_data = []
    for item in data['data']:
        obj = {
            "id": item['id'],
            "questions": [item['question']]
        }
        new_data.append(obj)

    # Ghi dữ liệu mới vào file JSON mới
    with open(output_file_path, 'w', encoding='utf-8') as new_json_file:
        json.dump(new_data, new_json_file, ensure_ascii=False, indent=2)
