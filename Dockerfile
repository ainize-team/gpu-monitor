FROM ubuntu:18.04
ENV PYTHONUNBUFFERED TRUE

RUN apt-get update && \ 
    apt remove python-pip  python3-pip && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    ca-certificates \
    g++ \
    python3.8 \
    python3.8-dev \
    python3.8-distutils \
    python3.8-venv \
    python3-venv \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && cd /tmp \
    && curl -O https://bootstrap.pypa.io/get-pip.py \
    && python3.8 get-pip.py

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1 \ 
    && update-alternatives --install /usr/local/bin/pip pip /usr/local/bin/pip3.8 1

RUN python3.8 -m venv /home/venv
ENV PATH="/home/venv/bin:$PATH"
RUN python -m pip install -U pip setuptools

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt && rm requirements.txt

COPY /app /app
WORKDIR /app

CMD ["python", "-u", "app.py"]
