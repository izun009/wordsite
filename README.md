# Wordsite

Wordsite is simple blog using Django and Wagtail CMS

## Setup with Virtualenv

Use the package manager [virtualenv](https://pypi.org/project/virtualenv/) to install.

```bash
virtualenv venv
```

## Installation


```bash
source venv/bin/activate
cd ~/yourdirectory
git clone https://github.com/izun009/wordsite.git
cd wordsite
pip install -r requirements.txt
```


## Usage

```bash
./manage.py makemigrations
./manage.py migrate
./manage.py createsupseruser
./manage.py runserver
```

## License
MIT License
