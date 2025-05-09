FROM nginx:latest

WORKDIR / app

COPY nginx.conf /etc/nginx/nginx.conf
COPY html/ /usr/share/nginx/html/
COPY .env .
COPY requirements.txt ./
COPY . .



RUN mkdir -p /app/media

EXPOSE 80
