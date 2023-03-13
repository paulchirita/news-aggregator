# News Aggregator web application

Create a superuser and fill in the required data:

`python manage.py createsuperuser`

The superuser can be used to log in to the Django API interface.

After you created a superuser, we can populate the database with dummy data.

For populating the database with dummy data run the following commands:

`python manage.py makemigrations`

`python manage.py migrate`

`python populate_database.py`

If you get conflicts from the dummy data creation, delete `db.sqlite3` and all the files inside `mainAPP/migrations/` and re-run all 3 commands above.