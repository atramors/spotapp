FROM python:3.9.13

# setting working directory in our container
WORKDIR /app

# install requirements
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

CMD ["uvicorn", "spotapp:app", "--port", "80", "--host", "0.0.0.0"]