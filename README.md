Name: Pubcrawler
Link: https://github.com/AAGlasgow/pubcrawler
Author: AAGlasgow
Version: 1.0
Created: 12/03/2015
Modified: 26/03/2015

Description
===========

A platform where users can exchange their favourite pubcrawls and rate them.

Details
===========

Pubcrawler is a Django powered web application which uses a very user-friendly interface to allow a wide variety of users to create pubcrawls and share them with others online.
The user can also search for pubcrawls by the name of the crawl, city or by the name of a certain pub.
Clicking on a crawl will bring up a Google Maps page which will show them the fastest route between the pubs and the distance.

The user can also rate other people's pubcrawls by clicking the like button.
They can also write reviews for crawls.

Users have to create an account for a lot of functionality to be available.
They should click on the Register button on the Navbar. Then enter the relevant details. 

Requirements
=============

Django Web Framework ver. 1.7
Pillow
django-registration-redux
django-bootstrap-toolkit

Installation
=============

In your specified workspace open a console and type the following lines:
	
	$ pip install -U django==1.7
	$ pip install pillow
	$ pip install django-registration-redux
	$ pip install django-bootstrap-toolkit  

After this create a local repository and clone it from the remote repository.
Navigate to the project using:
	cd pubcrawler
Then work on your virtual enviroment:
	workon <envname>
Then type the following line:
	python manage.py runserver
And type the link given into the address bar of your favourite browser.

Compatibility
=============

There are no known compatibility issues. It should work on all latest versions of Google Chrome, Internet Explorer and Mozilla Firefox. 

Known Bugs
==========




Authors
=============

Adam Fleming
Vladimir Nikolov
David Fröhlingsdorf
Calum Young
