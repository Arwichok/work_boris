FROM python:3.10-alpine
WORKDIR /usr/src/api

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
CMD python -m app
EXPOSE 8080