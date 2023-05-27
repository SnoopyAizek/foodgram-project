FROM python:3.11-slim

RUN mkdir /app

COPY requirements.txt /app

RUN python3 -m pip install --upgrade pip && pip3 install -r /app/requirements.txt --no-cache-dir

COPY . /app

WORKDIR /app

CMD python3 manage.py migrate && python3 manage.py load_ingredients -fp /app/data && python3 manage.py collectstatic && gunicorn foodgram.wsgi:application --bind 0:8000