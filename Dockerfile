FROM python:3.12-alpine
WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000

COPY . .

RUN ["python", "init.py"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

