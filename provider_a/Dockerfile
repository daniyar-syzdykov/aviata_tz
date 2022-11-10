FROM python:3.10.4

WORKDIR /provider_a

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .


CMD ["python", "server.py"]
