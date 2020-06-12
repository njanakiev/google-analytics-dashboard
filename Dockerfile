FROM python:3.7.3-slim

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt 

ARG VIEW_ID

COPY utils /app/utils
COPY app.py /app

EXPOSE 8050

CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server"]
