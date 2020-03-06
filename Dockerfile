FROM python:3

ADD . /var/lib/simcd/

WORKDIR /var/lib/simcd/

RUN pip3 install flask python-gitlab

CMD [ "python", "./main.py" ]
