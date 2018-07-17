FROM jupyterhub/jupyterhub

MAINTAINER Sergey Emelyanov <karagabul@gmail.com>

ADD ./requirements.txt /var/tmp/requirements.txt
RUN python3 -m pip install -r /var/tmp/requirements.txt

# Create oauthenticator directory and put necessary files in it
RUN mkdir /srv/oauthenticator
WORKDIR /srv/oauthenticator
ENV OAUTHENTICATOR_DIR /srv/oauthenticator

ADD ./jupyterhub_config.py jupyterhub_config.py
ADD ./addusers.sh /srv/oauthenticator/addusers.sh
ADD ./userlist /srv/oauthenticator/userlist
RUN chmod 700 /srv/oauthenticator

CMD ["sh", "/srv/oauthenticator/addusers.sh"]
