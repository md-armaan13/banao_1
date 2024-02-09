# Banao



The "Banao" project is a delightful Django application designed to empower users login and Signup efficiently

Screenshots:

![Screenshot of Period/Grace dialog](/static/common/images/loginpage.png "Period/Grace Dialog")

##

![Screenshot of Cron dialog](/static/common/images/musicpage.png "Cron Dialog")


## Setting Up for Development

To set up Banao development environment:

* Install dependencies (Debian/Ubuntu):

  ```sh
  sudo apt update
  sudo apt install -y gcc python3-dev python3-venv libpq-dev libcurl4-openssl-dev libssl-dev
  ```

* Prepare directory for project code and virtualenv. Feel free to use a
  different location:

  ```sh
  mkdir -p ~/banao 
  cd ~/banao
  ```

* Prepare virtual environment
  (with virtualenv you get pip, we'll use it soon to install requirements):

  ```sh
  python3 -m venv venv
  source venv/bin/activate
  pip3 install wheel # make sure wheel is installed in the venv
  ```

* Check out project code:

  ```sh
  git clone https://github.com/md-armaan13/banao_1.git
  ```

* Install requirements (Django, ...) into virtualenv:

  ```sh
  pip install -r requirements.txt
  ```


* Now create the .env in the root and copy the Environment Variables From Gist [here](https://gist.github.com/md-armaan13/fc7ea90de2f59048daf02b1996b05439)

  ```sh
  https://gist.github.com/md-armaan13/fc7ea90de2f59048daf02b1996b05439
  ```




* Run development server:

  ```sh
  python manage.py runserver
  ```

The site should now be running at `http://localhost:8000`.
To access Django administration site, log in as a superuser, then
visit `http://localhost:8000/admin/`
* Defualt Login Credentials are:

  ```sh
  Email admin@gmail.com
  Pass  admin123
  ```

