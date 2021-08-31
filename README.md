# STEPS TO EXECUTION
1. create new virtual environment  <br />
2. Install the requirements by pip install -r requirements.txt  <br />
3. Edit the database details in settings.py file  <br />
4. Edit the SECRET_KEY and other config() datas in settings.py with your own django project datas.  <br />
5. Create a new database and migrate using python manage.py migrate  <br />
6. Collect all the static files using python manage.py collectstatic  <br />
7. Finally python manage.py runserver  <br />