# ESD-Tuition-Matching
This repository contains the codes that are used for developing a Tuition Matching Web Application as part of a school module project of creating an enterprise solution using microservices architecture.

1.	Run WAMP/MAMP server. 
2.	Run Docker Desktop.
3.	Create a working folder.
4.	Unzip the .zip file into the working folder. You should have the following:
●	img
○	favicon.png
○	tutee_logo.png
○	tutor_logo.png
●	amqp.reqs.txt
●	amqp_setup.py
●	assignment.Dockerfile
●	assignment.py
●	assignment.sql
●	check_tutee.html
●	check_tutor.html
●	docker-compose.yml
●	http.reqs.txt
●	index_tutee.html
●	index_tutor.html
●	invokes.py
●	manage_assignment.Dockerfile
●	manage_assignment.py
●	notification.Dockerfile
●	notification.py
●	telebot.py
●	tutee.Dockerfile
●	tutee.py
●	tutee.sql
●	tutor.Dockerfile
●	tutor.py
●	tutor.sql
5.	Go to http://localhost/phpmyadmin,  enter “root” in the username field and leave password field empty.
6.	Use the following .sql files: “tutee.sql”, “tutor.sql”, and “assignment.sql”, to create and populate the databases in WampServer.
7. Allow remote access to the databases by creating a new user "is213" under "User Account" at WampServer and set the "Hostname" field to "Any Host" and the "Password" field as "No Password".
8.	Access our telegram bot through this link :http://t.me/tuitionmatch_bot. Enter any message to our telegram bot. 
9.	Open a terminal, navigate to the working directory and run the following command python telebot.py. Take note of your telegram chat id that is printed on the terminal. 
10.	Change the telegram chat id of the tutee/tutor (that you are choosing to test) to your own telegram chat id in the tutee/tutor databases.  
11.	Similarly, update the current email address for the same tutee/tutor (that you are choosing to test) to your own email address in the tutee/tutor databases.
12.	In the VSCode terminal, install the SendGrid package using pip install sendgrid.
13.	In your current working directory, start a new terminal to build the container and images by using docker-compose up.
14.	Check on Docker Desktop to ensure the container and various images are running
15.	Open the index_tutor.html and index_tutee.html files to start using our service with the tutee/tutor you have chosen for testing. 
