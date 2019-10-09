#SIMPLE "REST API / CRUD" APP WITH FLASK
```
Simple flask application that stores students with their name, lastname and age.
Database = MONGODB
CACHE = REDIS with ReJSON module loaded.
```
####INSTALLATION & PREP
```
1. Pull from git https://github.com/dript0hard/REST-API-FLASK
2. Install required packages to run the app.
$apt-get install mongodb
$apt-get install redis-server redis-cli
$python3.7 -m pip install --user --upgrade setuptools wheel        
$python3.7 -m pip install -r requirements.txt 

After these steps make shure to have installed ReJSON module for redis-server.

$git clone https://github.com/RedisJSON/RedisJSON.git
$apt-get install build-essential
To build the module, run make in the project's directory.
```
####RUNING THE APP
```
$redis-server --loadmodule path_to/RedisJSON/src/rejson.so
$redis-cli --raw
$mongo
$use students
$export FLASK_APP=students2
$export FLASK_ENV=development
$flask run
$python3.7 wsgi.py <port number>
```
####ROUTES AND SENDING REQUESTS
```
    Endpoint                 Methods             Rule
-----------------------  ------------------  -----------------------
views.get_post           GET, POST           /students
views.update_delete_get  DELETE, GET, PATCH  /students/<string:id>

In this example the module httpie is used you can use POSTMAN to test

$http -j POST :5000/students name=test lastname=test age=1
$http GET :5000/students
$http GET :5000/students/{copied id from second request}
$http -j PATCH :5000/students/{copied id from second request} name=test1 lastname=test1 age=2
$http DELETE :5000/students/{copied id from second request}
```
####WHAT I LEARNED
``` 
1.Creating a REST API that can be implemeted in CRUD web app.
2.Basics of the FLASK framework.
3.Wrapping the pyredis and pymongo module functions as needed to work with the database and cache.
4.Making python modules installable with setuptools.
```
