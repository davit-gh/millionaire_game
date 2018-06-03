# Overview
A very crude version of the game "Who Wants To Be Millionaire" (No CSS and JS)

# Features

* 5 randomly chosen questions
* Add Questions and the related Answers from admin
* Login fields - First name, Last name, Password
* Only authenticated users can play the game
* Leaderboard shows the results ordered by descending points

# Deployment
The Django app is deployed on pythonanywhere.com for demonstration purposes. 

* App URL - [http://millionaire.pythonanywhere.com](http://millionaire.pythonanywhere.com/)
* Admin URL - [http://millionaire.pythonanywhere.com/admin](http://millionaire.pythonanywhere.com/admin)
* Admin Username - admin
* Admin Password - Admin123

# Add/modify Questions and Answers

When logged into the admin interface:

* Select "Questions" to create/edit question
	* Set question points
	* Add as many answers as needed by clicking on "Add another Answer"
	* Check that only one answer can be selected as correct 
* To see all the registered users and their earned highest points please navigate to "Profiles"

# Tests

Automatic tests are added for 'main' app in 'main/tests.py'. These tests cover user authentication scenarios including redirect checks. Tests can be run by
 
    ./manage.py test main
