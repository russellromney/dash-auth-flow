FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install -r requirements.txt

CMD ["gunicorn", "--workers","3","app:server", "-b", "0.0.0.0:8080"]

