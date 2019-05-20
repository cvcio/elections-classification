FROM python:3-slim

RUN mkdir /svc
COPY . /svc

WORKDIR /svc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 50051
CMD ["python", "server.py"]
