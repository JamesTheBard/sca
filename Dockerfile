FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.8

COPY ./app /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN flask db upgrade
