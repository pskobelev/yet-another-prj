FROM python:3.12-alpine

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . code
WORKDIR /code

EXPOSE 8000
ENTRYPOINT ["python", "superapp/manage.py"]
CMD ["runserver", "0.0.0.0:8000"]