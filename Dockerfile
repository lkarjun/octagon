FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN apt-get -y update

RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    git 

RUN cd ~ && \
    git clone https://github.com/davisking/dlib.git dlib/ && \
    cd dlib; mkdir build; cd build; cmake ..; cmake --build .

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./app /app/app
WORKDIR /app/

ENV PYTHONPATH=/app
EXPOSE 8000