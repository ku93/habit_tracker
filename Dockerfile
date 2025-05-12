FROM python:3.13-slim

WORKDIR / app

COPY .env .
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

RUN mkdir -p /app/media

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]