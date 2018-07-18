FROM jupyterhub/jupyterhub

MAINTAINER Sergey Emelyanov <karagabul@gmail.com>

ADD ./jupyterhub/requirements.txt /var/tmp/requirements.txt
RUN python3 -m pip install -r /var/tmp/requirements.txt

# Create oauthenticator directory and put necessary files in it
RUN mkdir /srv/oauthenticator
WORKDIR /srv/oauthenticator
ENV OAUTHENTICATOR_DIR /srv/oauthenticator

ADD ./jupyterhub/jupyterhub_config.py jupyterhub_config.py
ADD ./jupyterhub/addusers.sh /srv/oauthenticator/addusers.sh
ADD ./jupyterhub/userlist /srv/oauthenticator/userlist
ADD ./jupyterhub/MANUAL.ipynb /vat/tmp/MANUAL.ipynb
RUN chmod 700 /srv/oauthenticator


ADD ./packages/ /var/tmp/packages
ARG pg_user
ARG pg_password
ARG pg_host
ARG pg_db
RUN cd /var/tmp/packages/models && \
    POSTGRES_USER=$pg_user \
    POSTGRES_PASSWORD=$pg_password \
    POSTGRES_HOST=$pg_host \
    POSTGRES_DB=$pg_db \
    python setup.py install

CMD ["sh", "/srv/oauthenticator/addusers.sh"]
