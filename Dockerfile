FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install  -r requirements.txt

COPY . .

RUN chmod +x manage.py
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
