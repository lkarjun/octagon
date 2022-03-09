FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

RUN apt-get -y update && apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN pip3 install --upgrade pip && \
    git clone https://github.com/davisking/dlib.git && \
    cd dlib/ && \
    python3 setup.py install

COPY requirements.txt /app/requirements.txt

# COPY Pipfile /app/Pipfile
# COPY Pipfile.lock /app/Pipfile.lock

# RUN pip install pipenv && pipenv sync
RUN pip install -r /app/requirements.txt

# COPY ./app /app
WORKDIR /app
COPY ./app .
EXPOSE 5000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]