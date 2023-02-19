FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get update && \
    apt-get install -y libpq-dev && \
    pip install psycopg2

COPY . /code/
CMD python app.py
