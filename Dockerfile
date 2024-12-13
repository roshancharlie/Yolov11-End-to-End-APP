FROM python:3.10-slim

WORKDIR /object-detection

COPY requirements.txt /object-detection/

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . /object-detection/

EXPOSE 8080 8081

CMD ["sh", "-c", "python3 api.py & python3 interface.py"]
