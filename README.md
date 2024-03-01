# HomeWeb

<a href="https://ko-fi.com/D1D4V03ZY"><img style="float: right;" src="https://ko-fi.com/img/githubbutton_sm.svg"></a>

A basic Flask server to host my modules on.

![Landing Page](sample_images/landing_page.png)
* Very basic interface. Shows available modules, click to navigate to the selected module. 
* Put your own wallpapers in the static/ folder labeled 'landing_page_wallpaper'. 
  * Accepts ['png','jpg','webp'] file types.

## Requirements
* Postgres Database installed
* Git (Included in one-click installation)
* Python 3.10.9 (Included in one-click installation)


## Features
* Automatically loads modules from the modules folder.
* Basic login/registration system (Can be disabled)

## Installation
For the one-click installer:
* Download the latest release, and put the contents in a new folder.
* Run the install_homeweb.bat to have Git and Python installed in a self-contained environment.
* If you wish to install any modules, follow the prompts within the install_homeweb.bat.

## Usage
* Run the provided `run_webserver.bat`

## Available Modules
* [ImageSorter](https://github.com/KJM-Code/ImageSorter)
  * Image Tagging/Searching module.
* [Users](https://github.com/KJM-Code/module_hw_user)
  * Simple user login/registration interface. Can replace with your own. 
  * If not installed, defaults to no login requirement.
  
## Launch Parameters
Here are the available parameters you can use when launching the server:

| Parameter                   | Default             | Description                                                                                                                                 | Type                |
|-----------------------------|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------|---------------------|
| disable_login               | False               | Disables login requirement for the server.                                                                                                  | Boolean             
| disable_user_registration   | False               | Disables user registration for the server.                                                                                                  | Boolean             
| port                        | 7070                | Port the server will run on.                                                                                                                | String              
| host                        | localhost           | Address that the server is hosted on.                                                                                  | String - IP Address 
| ssl_key                     | ""                  | \[optional\] location of your ssl key for HTTPS. full path required. ex: C:/Path/filename.key. Needs ssl_cert in conjunction with ssl_key.  | String - Path       
| ssl_cert                    | ""                  | \[optional\] location of your ssl cert for HTTPS. full path required. ex: C:/Path/filename.cert. Needs ssl_key in conjunction with ssl_cert. | String - Path       
| enable_csrf_protection      | True                | Enables CSRF Protection for the server.                                                                                                     | Boolean             
| csrf_time_limit             | 86400               | If CSRF Protection is enabled, sets the timeout for CSRF protected pages.                                                                   | Integer - Seconds   
| enable_info_logging         | False               | If enabled, displays routes and any accompanying information in the terminal.                                                               | Boolean             
| key_flask_secret_key        | 'FLASK_SECRET_KEY'  | Key used to get the flask_secret_key value from the system variables or .env file.                                                          | String              
| key_postgres_login_user     | 'POSTGRES_USER'     | Key used to get the postgres_login_user value from the system variables or .env file.                                                       | String              
| key_postgres_login_password | 'POSTGRES_PASSWORD' | Key used to get the postgres_login_password value from the system variables or .env file.                                                   | String              
| key_postgres_host           | 'POSTGRES_HOST'     | Key used to get the postgres_host value from the system variables or .env file.                                                             | String              
| key_postgres_port           | 'POSTGRES_PORT'     | Key used to get the postgres_port value from the system variables or .env file.                                                             | String              
| key_postgres_database       | 'POSTGRES_DATABASE' | Key used to get the postgres_database value from the system variables or .env file.                                                         | String              


