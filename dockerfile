FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean

WORKDIR /app

RUN apt-get update && apt-get install -y git && apt-get clean

COPY requirements.txt /app/

RUN pip install --upgrade pip

RUN pip3 install git+https://github.com/vijaytakbhate2002/sentiment_prediction_python_package.git

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV FLASK_APP=app
EXPOSE 8000
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]