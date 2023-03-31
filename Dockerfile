FROM python:3.7.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["python", "src/run.py"]