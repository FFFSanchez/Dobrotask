FROM python:3.9.10

WORKDIR /app

COPY requirements.txt .

RUN pip install gunicorn==20.1.0 && pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "dobrotask.wsgi"]