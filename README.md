boricide
========

requirements
--------------
(from ubuntu 13.04)
 - apt-get install python-django python-tastypie libapache2-mod-wsgi
 - a2enmod wsgi headers

WSGI set up: apache vhost example
--------------
    NameVirtualHost boricide
    <VirtualHost boricide>
        ServerName boricide
        Alias /static/admin/ /var/www/boricide/static/admin/
    
        Header set Access-Control-Allow-Origin "*"
        Header set Access-Control-Allow-Headers "accept, authorization, origin"
    
        WSGIPassAuthorization On
        WSGIScriptAlias / /var/www/boricide/boricide/wsgi.py
    </VirtualHost>

getting it up and running
--------------

 - set above vhost in apache configuration (replacing '/var/www/boricide' with project directory, and 'boricide' virtual host name as necessary)
 - set boricide/local_settings.py accordingly
 - ./manage.py syncdb
 - ./manage.py collectstatic

