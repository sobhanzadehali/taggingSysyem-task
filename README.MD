## tagging system task

clone project:
```bash
> git clone https://github.com/sobhanzadehali/taggingSysyem-task
```
change direction to folder where docker compose file exists.

compose up:
```bash
> docker compose up
```
migrate and create new superuser:
```bash
> docker compose exec taggingsystem sh -c "python manage.py migrate"

> docker compose up exec taggingsystem sh -c "python manage.py createsuperuser"
```
then fill the prompt to create a new superuser.

now view api documentation in this url:
```
localhost:8000/api/docs/
```
