# Rent my house -  Fourth Milestone Project

This project is a simplified version of a booking website, where users can add their own houses to be rentes, or rent a already added one.

## UX

The UX for this project is clear and simple. Navigations are quite easy and smooth for users. The application is intuitive to use and has information on it presented well.

    - As a user I want to be able to create an account.
    - As a user I can choose if i am a tenant or a owner
    - As a user a can add/change details on my account
	- As a user I want to see a list of properties available to rent
	
	- As a tenant I can rent one or more properties on specific dates
	- As a tenant I can see a list of my bookings

	- As a owner I can add my property
	- As a owner I can edit or remove my property

## Features 


* Navbar - Bootstrap Navbar allows user to for quickly move around the app with help of bootstrap predefined classes.

* Alert Messages - Allows message returned to user about a bid that has taken effect in the web app.

* Images - Django ImageField attribute are used to store images in models. Images are hosted on AWS3 Bucket to allow hosting on cloud servers. 

* Forms - Allows user to sign in and sign up. 
* 
* StripeJS - StripeJS payment used is to take payment from the web app from only an auction winner.

* Profile - Allows user to view thier details when signed into the app.


### Possible feature to implement 

* more property images
* more details for owner about rentings


# [Live Demo Here](http://milestone4-radu.herokuapp.com/)

### External sites used 

* [Bootstrap](https://getbootstrap.com/) - A web framework used 
* [W3 Schools](https://www.w3schools.com/html/default.asp) - Help & tips 
* [Stackoverflow](https://stackoverflow.com/) - Help & tips
* [Django](https://www.djangoproject.com/) - The web framework used
* [Fontawesome](https://favicon.io/) - Fontawesome
* [Stripe JS](https://stripe.com/ie) - Stripe API used

### Frameworks/API used 

* [Bootstrap 3.3.7](https://getbootstrap.com/docs/3.3/getting-started/)
* [JQuery 3.2.1](https://jquery.com/download/)
* [Stripe](https://stripe.com/ie)
* [Django](https://www.djangoproject.com/)


## Custom Fonts 

I used fonts from **@googleapis CSS 'Montserrat'** to create difference in headers, paragraph, span and written styles.

## Technologies used


* HTML - Was used with a Jinja Template to display data stored in backend. [HTML](https://djangobook.com/)

* CSS3 - Was used for styling the web app. [CSS3](http://www.css3.info/)

* JQuery & JavaScript - Was used to allow payment, showing countdown and payment button to function smoothly. [Jquery](https://jquery.com/)

* Sqlite3 - SQLite3 was used to store database and retrieve data via the backend. [SQLite3](https://www.sqlite.org/)

* Python - Was used to route and retrieve backend database schema from SQLite3. [Python](Lecture Notes)

* Django - Produces very useful packages like Auth, Admin Jinja, Bootstrap Forms, Classes and Attributes that can be used to make the application more functional. [Django](https://www.djangoproject.com/)

* AWS3 BUCKET - Using amazon cloud based server to store images and static files. [Amazon](https://aws.amazon.com/s3/)

* AWS3 IAM - Used to manage access to our S3 storages. By providing us with ID and KEY to use. [Amazon](https://aws.amazon.com/iam/)

* Heroku - Was used to deploy application to run on any every technological devices. [Heroku](https://heroku.com/)

* Stripe JS - For easy payment when user select paynow option on all screen sizes [Stripe](https://stripe.com/ie)

* Fontawesome - Used to improve UX when viewing the top of the webpage. [Fontawesome](https://fontawesome.com/)

* Bootstrap Classes - To trigger more styles and reduce CSS over-styling. [Bootstrap](https://getbootstrap.com/)

* PostgresSQL - To allow the storage of database in sqlite before it can be used in Heroku as a database. [PostgresSQL](https://www.postgresql.org/) 

* Bootstrap datepicker ([GitHub - uxsolutions/bootstrap-datepicker: A datepicker for twitter bootstrap (@twbs)](https://github.com/uxsolutions/bootstrap-datepicker))

## Testing

+ Tested on **Chrome** 
+ Tested on **IE**
+ Tested on  **Android**
+ Tested on  **Samsung S6 - S9**
+ Tested on **Iphone**
+ Tested on **Firefox**
+ Tested on **Opera** 
+ Tested on **Safari**


## Deployment

### AWS3 Deployment Process

Created a new Amazon account and connect to amazon service **AWS3** account are cloud based serve where 
the project media and static files will be stored .
At first, we locate **S3** on amazon service then we create a bucket. While creating the bucket on **S3**,
the note that public access must be all switched off to allow access for users.

Once we've created the bucket, we now can now click on it's properties and enable the **Static Website Hosting** option, 
so it can serve the purpose of hosting our static files, you will need to imput an **index.html** and **error.html** before saving.
Then we go into the created bucket **Permissions** and click into **CORS configuration**, this part already have a prefilled default config,
All that is needed is just to write the default code and save the config.

Then we go into the **bucket policy** to allows access to the contents across all web 
and inside this we will put in here some code including  arn address displayed at the top of the heading.
Then we go into amazon **IAM** to allow identity and access management of our stored files and folder.
In the **IAM** service, we add a new group for our application and then we set the policies to **ALL**
Then it generates a downloadable zip file containing **ID and KEY** for us to use for the newly added group. 
This **ID and KEY** as to be stored in an environment variable.

This then allows us to into our terminal window and install some settings
**Boto3**
**Django Storages**

### GitHub Deployment

Created a new repositories on **Github** where the project will be deployed unto at each commit.
At first, use a **git remote** command to link project with new repo.
Then use the **git push -u origin master** command to push codes and every change into new repo

Using the CLI in terminal to call **git init** to start git initialization on the project.
This allows a file/files to be added to the Github repo by calling a **git add** command.
Then any added file/files is being commited with a **git commit -m "commit message"** command.
Afterwards, the file is been pushed with **git push** where Github username + password is required.

### Heroku Deployment

Created a new app on **Heroku** where the app is hosted live.
At first, to allow **Heroku** locate application we login into the CLI using ** heroku login -i** command.
You will be requested to imput username and password for **Heroku** account. 
After which you can request **Heroku Apps** via CLI. 

Knowing the apps you need to pass deployment into then we can use **heroku git:remote -a <app>** 
to allow Git automatically update deployment in Heroku. 
Once this has been remotely passed . 
To host the app unto heroku pass the IP and PORT config to match the route **__main__** config.

To **allow PostgresSQL**, we have to go into our newly created app and click into **resources** inside here you can type **PostgresSQL** 
and add as an add on, it should prompt up on your screen choose the **hobby dev free** and click on **provision**.
Once you allow **PostgresSQL** it will generate a **DATABASE_URL** in the heroku settings.

Now we need to install in production terminal **dj-database-url** and **psycopg2**
Then we run a **migrate** to to update our new **PostgresSQL** database and since this is new in Heroku, all data imputed will be erased.
Which means we need to **createsuperuser** from terminal and add our contents again,
Our new production database is ready. So we can rebuild all our projects again.

To allow git to push to heroku the command **git push heroku master** must be called for a final **push**.
For a succefull and healthy push it is best adviced to have the **requirement.txt** and **Procfile** 
files installed or updated. 

### HTML, CSS, JQuery, JavaScript, Python(Django Framework)

All my mark up is **HTML valid**
All my styling is **CSS valid**
All my syntax is **JavaScript syntactically valid**
All my routing, views and urls is **Django valid**

### Credits

*	This project was based on the Boutique Ado and Ecommerce mini projects in the Django module of the Code Institute Full Stack Developer Course.

*	Guidance on the models, forms and views were obtained from the projects, queries on Slack and tutor support.


### Media

*	Images used in this site are from Google Images.