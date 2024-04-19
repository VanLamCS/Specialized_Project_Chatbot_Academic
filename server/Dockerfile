FROM ubuntu:22.04

ENV PORT=5000
ENV JWT_SECRET_KEY=
ENV MONGO_URI=
ENV DEVICE=cuda:0
ENV EMBEDDING_MODEL_ID=bkai-foundation-models/vietnamese-bi-encoder
ENV DOCS_PATH=./dataset
ENV MAX_NEW_TOKENS=1024
ENV LLM_API_SERVICE_URL=https://ws.gvlab.org/fablab/ura/llama/api/generate_stream

RUN apt-get update

RUN apt-get install -y python3 python3-pip

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "app.py" ]