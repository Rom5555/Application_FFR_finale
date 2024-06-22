#FROM 3.10.8-slim-bullseye
FROM python:3.12

RUN apt -y update \
	&& apt install -y --no-install-recommends \
        apt-utils \
        net-tools \
		postgresql-client \
        libpq-dev \
        tzdata \
        nginx \
    && apt -y upgrade \
	&& rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    mkdir /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app
RUN python manage.py makemigrations
RUN python manage.py migrate

RUN ls -al

EXPOSE 8000

# permet de rassembler tous les éléments statics de chaque application dans un seul répertoire
# NB : en prduction, cette emplacement est l'"object storage" où django archive les éléments statics,
#      ainsi les containers instanciés par les pods kubernetes peuvent êtres remplacées "à la volée" sans
#      conséquence sur les fichiers statiques
# RUN python ./manage.py collectstatic --no-input

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "--timeout", "120", "application_FFR.wsgi"]