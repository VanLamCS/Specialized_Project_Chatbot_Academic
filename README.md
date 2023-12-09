# CHATBOT HỖ TRỢ TƯ VẤN HỌC VỤ CHO SINH VIÊN TRƯỜNG ĐẠI HỌC BÁCH KHOA

## Mục lục

1. [Mô tả đề tài](#mô-tả-đề-tài)
2. [Các liên kết](#các-liên-kết)
3. [Cách thực thi code](#cách-thực-thi-code)
   1. [Yêu cầu](#các-liên-kết)
      1. [Cách cài transformers](#cách-cài-transformers-4320dev0)
      2. [Cách cài torch](#cách-cài-torch)
   2. [Cách train mô hình](#cách-train-mô-hình)
   3. [Cách run server](#cách-run-server)
4. [Thành viên nhóm](#thành-viên-nhóm)
5. [Giảng viên hướng dẫn](#giảng-viên-hướng-dẫn)

## Mô tả đề tài

Những năm gần đây số lượng sinh viên nhập học Trường Đại học Bách Khoa đã và đang tăng rất đáng kể. Thông thường một Giáo viên Chủ nhiệm phải quản lý có khi lên đến cả trăm sinh viên trong một khoá. Mặc dù đã có sự hỗ trợ từ các nhân viên giáo vụ Khoa và các phòng ban nhưng việc giải quyết các vấn đề liên quan đến học vụ cho sinh viên còn nhiều hạn chế và quy trình làm việc kéo dài. Nhận thấy khó khăn đó, đề tài hướng đến việc xây dựng chatbot có thể hỗ trợ tư vấn trả lời hoặc gợi ý cho một số câu hỏi liên quan đến học vụ của sinh viên Trường một cách tự động tối ưu quy trình xử lý các vấn đề học vụ, tiết kiệm thời gian và nhân lực. Cụ thể hơn, chatbot sẽ được tích hợp một mô hình Học Sâu được thiết kế và huấn luyện dựa trên bộ dữ liệu câu hỏi-câu trả lời xây dựng từ các quy định quy chế về học vụ được đăng công khai trên website Trường.

## Các liên kết

- [Confluence](https://chatbotacademic.atlassian.net/l/cp/4DYmj5mV)

## Cách thực thi code

### Yêu cầu

- Python 3.10.x
- Transformers 4.32.0.dev0

#### Cách cài Transformers 4.32.0.dev0

- Bước 1: Chạy câu lệnh:

```bash
git clone --single-branch --branch fast_tokenizers_BARTpho_PhoBERT_BERTweet https://github.com/datquocnguyen/transformers.git
```

- Bước 2: Chạy câu lệnh:

```bash
pip install -e transformers
```

#### Cách cài torch

Theo sự hướng dẫn của [PyTorch](https://pytorch.org/)
Cài torch với cuda:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

Cài torch không cuda:

```bash
pip install torch torchvision torchaudio
```

### Cách train mô hình

#### Bước 1: Clone repository

#### Bước 2: Cài các thư viện cần thiết trong requirements.txt

```bash
pip install -r requirements.txt
```

Bên cạnh đó, install thêm transformers như hướng dẫn trên.

#### Bước 3: Chuẩn bị data (train data, validation data) bằng cách chạy file `data.py` trong `src`

```bash
python src/data.py
```

#### Bước 4: Cấu hình các thông số train trong file `src/constants.py`

```python
PRETRAIN_MODEL = "vinai/phobert-base-v2"
BATCH_SIZE = 8
MAX_ANSWER_LENGTH = 200
MAX_LENGTH = 256
STRIDE = 128
N_BEST = 20
MODEL_LIMIT = 700
DEVICE = "cuda"
```

#### Bước 5: Thực thi `src/train.py`

```bash
python src/train.py
```

### Cách run server

#### Bước 1: Đảm bảo đã train và có mô hình `pytorch_model.bin` và file `config.json` trong `checkpoints`

#### Bước 2: Thực thi `src/server.py`

```bash
python src/server.py
```

## Thành viên nhóm

- [Hồ Ngọc An](https://github.com/hoan7902)
- [Lê Văn Lâm](https://github.com/vanlamcs)
- [Trần Văn Tài](https://github.com/tranvantai2905)

## Giảng viên hướng dẫn

- [TS. Nguyễn Tiến Thịnh](https://github.com/thinhcse)
- [ThS. Băng Ngọc Bảo Tâm](#giảng-viên-hướng-dẫn)
