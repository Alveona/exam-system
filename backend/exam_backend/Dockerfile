FROM python:latest

COPY ./requirements.txt /var/www/app/
RUN pip3 install -r /var/www/app/requirements.txt

# add (the rest of) our code
COPY ./ /var/www/app/
WORKDIR /var/www/app/
CMD bash /var/www/app/server_start.sh
# CMD ["python3", "/var/www/app/manage.py", "makemigrations"]
# CMD ["python3", "/var/www/app/manage.py", "migrate"]
# CMD ["python3", "/var/www/app/manage.py", "runserver"]