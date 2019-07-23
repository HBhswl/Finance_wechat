run:
	python manage.py runserver_plus --cert ssl.crt 0.0.0.0:8000
new:
	/usr/local/nginx/sbin/nginx -s reload
	uwsgi --ini uwsgi.ini
log:
	cat finance.log
