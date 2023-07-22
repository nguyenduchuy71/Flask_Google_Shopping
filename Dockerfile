FROM python:3.7-alpine

WORKDIR /app

COPY . .

RUN python3 -m pip install --upgrade pip

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 3000

CMD ["python", "app.py"]
