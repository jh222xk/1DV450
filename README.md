TOERH
===========
Webbramverk - 1DV450

[![Build Status](https://travis-ci.org/jh222xk/toerh.svg?branch=master)](https://travis-ci.org/jh222xk/toerh)

# Run the application

## Get the project
First of all clone this repository: `git clone https://github.com/jh222xk/toerh.git`

## Dependencies
[Python version >= 3.0](https://www.python.org/downloads/)

Latest version of [pip](https://pip.pypa.io/en/latest/installing.html)

Check `requirements.txt` for more dependencies

### Install dependencies
To install all the requirements for this project just run: `pip install -r requirements.txt`.
(given that you have Python and pip installed).

## Database
To get the database up and running with the latest migrations and so on just type:
* `python manage.py syncdb`
* `python manage.py makemigrations`
* `python manage.py migrate`

and then the database should be just fine.

## Run it
locate to `path/to/toerh/` then just run Python's built-in server using the command: `python manage.py runserver` and the application will be served at `http://localhost:8000/`

# Using the API
First of you need to register an account. After that sign in and create a new token.

After successfully set up your account and your token you can make requests as follows:

``curl -X GET http://127.0.0.1:8000/api/v1/positions/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'``