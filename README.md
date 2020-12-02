# sports_events
Provides API for list, get match for betting

Built as Rest API, this uses `django-rest-framework` and `django`. Database used is `MySQL`.


# Setup
## Pre Requirements
- MySQL to be installed
- Database to be created. If not use,

        CREATE DATABASE IF NOT EXISTS spectate_888;

 All requirements needed are listed under `requirements.txt`. To install

    pip install -r requirements.txt
    
# Starting the server
To start the Django WSGI engine,
    
    python manage.py runserver

# Testing 
To test the app,

    python manage.py test
    
This runs all the testcases defined in all the apps, defined in `tests.py` in each app.

    
