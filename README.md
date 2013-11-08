boricide
========

requirements
--------------
 - in /var/www/boricide/, execute 'virtualenv .'
 - pip install -r requirements.txt
 - a2enmod wsgi headers

WSGI set up: apache vhost example
--------------

WSGIPythonHome /home/javad/boricide/

NameVirtualHost showshows.net
<VirtualHost showshows.net>
    ServerName showshows.net
    ServerAlias www.showshows.net

    Alias /static/     /home/javad/boricide/static/

    Header set Access-Control-Allow-Origin "*"
    Header set Access-Control-Allow-Headers "accept, authorization, origin, Content-Type"
    Header set Access-Control-Allow-Methods "POST, PUT, PATCH, DELETE, GET"

    WSGIPassAuthorization On
    WSGIScriptAlias / /home/javad/boricide/boricide/wsgi.py
</VirtualHost>

getting it up and running
---------------

 - set above vhost in apache configuration (replacing '/home/javad/boricide/' with project directory, and 'boricide' virtual host name as necessary)
 - set boricide/local_settings.py accordingly
 - ./manage.py syncdb
 - ./manage.py collectstatic

