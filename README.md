# sports_events
Provides API for list, get match for betting

Built as Rest API, this uses `django-rest-framework` and `django`. Database used is `MySQL`. The app is documented with Swagger and redoc.


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


# Sample Images

## Swagger Documentation
![swagger](img/swagger.png)

## ReDoc Documentation
![redoc](img/redoc.png)


## List all Events
![list](img/list.png)
    

## Get Match by Id
![match](img/get-one.png)

## Search by Sport - FootFall
![s-fb](img/search.png)

## Search By Sport - Cricet
![s-cr](img/search-cricket.png)


## Ordering By startTime
![ord](img/ordering-time.png)

## Ordering , Search
![ord-s](img/ord-search.png)



## Update Odds
![update](img/update-odds.png)

## NewEvent
![new](img/new-event.png)

