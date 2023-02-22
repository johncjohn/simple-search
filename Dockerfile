FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary
COPY . /code/
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host", "0.0.0.0"]
