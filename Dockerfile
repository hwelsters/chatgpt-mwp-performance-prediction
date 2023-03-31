FROM python:3.7.9

WORKDIR /app

RUN python -m pip install nltk==3.8.1
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader averaged_perceptron_tagger

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["python", "src/run.py"]