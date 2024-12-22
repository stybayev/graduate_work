FROM --platform=linux/amd64 python:3.10-slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /movie_service
COPY requirements.txt /movie_service
RUN /usr/local/bin/python -m pip install --upgrade pip

RUN apt-get update -y
RUN apt-get install gcc -y
RUN apt-get install postgresql-client -y
RUN pip install -r requirements.txt
COPY . /movie_service
RUN chmod +x /movie_service/utils/init.sh
ENTRYPOINT ["/movie_service/utils/init.sh"]
COPY main.py /
CMD python /main.py

