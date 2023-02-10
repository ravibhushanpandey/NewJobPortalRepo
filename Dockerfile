FROM python:3

WORKDIR /app

COPY . .

RUN pip install -r newreqirement.txt



CMD ["python3", "manage.py", "runserver", "0.0.0.0:8001"]
