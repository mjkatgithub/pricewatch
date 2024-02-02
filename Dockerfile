#Zugrundeliegendes Image
#FROM python:3.9-slim
FROM python:3.10.11-slim

WORKDIR /app

# aktuellen verzeichnisses in /app
ADD . /app

#installieren der requirements
RUN pip install --trusted-host pypi.python.org -r requirements.txt

#Port 80 veroeffentlichen
EXPOSE 80

CMD ["python", "priceWatch.py"]
