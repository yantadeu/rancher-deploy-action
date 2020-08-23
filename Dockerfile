FROM ubuntu-latest

RUN apt update
RUN apt -y install clang-format-9 python3
RUN python -m pip install --upgrade pip
RUN update-alternatives --install /usr/bin/clang-format clang-format /usr/bin/clang-format-9 100
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 100

ADD . /usr/src/app
WORKDIR /usr/src/app

RUN pip install -r requirements.txt