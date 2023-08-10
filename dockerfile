FROM python:3.11.4-bookworm

# Install Node.js
RUN apt-get update && apt-get install -y nodejs

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 7788

CMD ["python", "main.py"]