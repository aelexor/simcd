FROM python:3

ADD . /var/lib/simcd/

WORKDIR /var/lib/simcd/

RUN pip3 install flask python-gitlab

EXPOSE 5000

CMD [ "python", "./main.py" ]
