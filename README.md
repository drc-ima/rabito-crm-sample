# Rabito CRM Sample by Moon Labs
A practice project for Rabito CRM Solution. This solution is a work in progress built with Python django and [AdminLTE 3 Template](https://adminlte.io).

## Setup
The first thing to do is to clone the repository:
```sh
$ git clone https://github.com/drc-ima/rabito-crm-sample.git
$ cd rabito-crm-sample
```

Create a virtual environment to install dependencies and activate it:
```sh
$ virtualenv venv
$ source venv/bin/activate
```

Then install the dependencies:
```sh
(venv)$ pip install -r requirements.txt
```
Note the (venv) in front of the prompt. this indicates that this terminal session operates in a virtual environment set up by `virtualenv`.

Onces `pip` has finished downloading the dependencies:
```sh
(venv)$ python manage.py runserver
```

Now navigate to `http://127.0.0.1:8000/` in your browser to run the django server.
