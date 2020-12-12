# Bidster

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
Bidster is a website where people can puublish items for sale for a limited time. Other people can place bids on offers while they are active.

### Unregistered users
Unregistered users can browse and search through all published offers.

### Registered users
Users can browse and search through all published offers. In addition they can publish new offers and can place bids on offers from other users.

### Admins
Admins have the same rights as users. In addtition they have access to the admin panel and can edit most of the information for offers, bids and users.
Categories for offers canot be deleted from the admin panel.
	
## Technologies
Project is created with:
* Django 3.1.3
* Celery 5.0.3
* PostgreSQL 13
	
## Setup
The project is setup to work with a local PostgreSQL database on default port.
The message broker for Celery is configured to be a local instance of RabbitMQ.

Running the project:

```
$ make sure the message broker is running
$ activate venv
$ cd into the main folder
$ pip install -r requirements.txt - will install dependencies
$ celery -A bidster worker -l info - will start the celery service
$ *celery -A bidster worker --pool=solo -l info - will start the celery service(for Windows)
$ python manage.py runserver - will start the server
```
