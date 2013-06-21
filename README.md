boricide
========

requirements
--------------

 - apt-get install python-django python-tastypie libapache2-mod-wsgi
 - a2enmod wsgi headers

WSGI set up: apache vhost example
--------------
    NameVirtualHost boricide
    <VirtualHost boricide>
        ServerName boricide
        Alias /static/admin/ /var/www/boricide/admin/
    
        Header set Access-Control-Allow-Origin "*"
        Header set Access-Control-Allow-Headers "accept, authorization, origin"
    
        WSGIPassAuthorization On
        WSGIScriptAlias / /var/www/boricide/boricide/wsgi.py
    </VirtualHost>

