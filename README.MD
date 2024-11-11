## tagging system task

clone project:
```bash
git clone https://github.com/sobhanzadehali/taggingSysyem-task
```
make sure to create an `.env` file beside`manage.py` containing something like bellow:
```env
DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=hello_django_dev
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432
```

change direction to folder where docker compose file exists.

compose up:
```bash
docker compose up
```
migrate and create new superuser:
```bash
docker compose exec taggingsystem sh -c "python manage.py migrate"
```
```bash
docker compose up exec taggingsystem sh -c "python manage.py createsuperuser"
```
then fill the prompt to create a new superuser.

now view api documentation in this url:
```
localhost:8000/api/docs/
```
