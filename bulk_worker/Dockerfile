FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install -r bulk_requirements.txt

CMD ["python", "main.py"]
