Bla
Claire Pritchard
October 2016

This is a Django chat application that makes use of websockets for updates and SSL/HTTPS to get profanity through
corporate web filters.
When websockets are not available (in Safari when using a self-signed certificate, for example), the page can still be
updated manually.
when javascript is not available (in Lynx, for example), the page can technically still be updated manually. 
However, constant questions about cookies and certificates made it unpleasant to use with Lynx (fix with a setting in Lynx?).
The "Chat like a pirate" feature was added for International Talk Like a Pirate Day but could be made into a more generic
chat filter.
The database used is SQLite.

Some packages used:
    django-websocket-redis
	Django REST framework

Django-sslserver was used to test the initial version on Windows, but when websockets were added it was necessary to switch to uWSGI on Linux 
(uWSGI is unavailable for Windows).

Before installing uwsgi install the following:
    build-essential python
    libpcre3 libpcre3-dev
    libssl-dev

Configuration:
start redis-server and uwsgi with
	sudo service redis-server start
	sudo -u <user> nohup uwsgi --ini uwsgi.ini

uwsgi.ini
=========
[uwsgi]
gevent = 100
http-websockets=True
module = bla.wsgi:application
static-map = /static=/path/to/staticdir
https = =0,mycert.crt,mycert.key,HIGH
shared-socket = 0.0.0.0:<port>
virtualenv = /path/to/virtualenv
master=True
