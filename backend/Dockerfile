FROM python:3.11
WORKDIR app
RUN apt-get update && apt-get upgrade -y
RUN apt-get install tesseract-ocr -y
RUN apt-get install tesseract-ocr-rus -y
RUN apt-get install -y chromium
RUN apt-get install -y chromium-driver
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN ls
COPY . .
EXPOSE 8080
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]