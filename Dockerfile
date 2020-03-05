FROM python:3.7.3-slim

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt 

COPY . /app

# ENV VIEW_ID $VIEW_ID
ENV KEY_FILE_LOCATION "client_secrets.json"

EXPOSE 8050

CMD ["python", "app.py"]
