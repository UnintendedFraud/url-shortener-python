# url shortener in python

This project is an URL shortener written in python, using fastapi and postgres.  
It is a simple API allowing you to shorten an URL, get redirected from a shortcode and getting 
some stats about a specific one.

This project was developed and tested using Python 3.12.

## Requirements

- Python 3+
- Postgres installed on the machine, with the ability to execute `pg_config`
- `virtualenv` and / or `docker`

## Setup the virtual environment

Make sure you do have `virtualenv` on your system first. If not, please install it from 
[https://virtualenv.pypa.io/en/latest/installation.html](https://virtualenv.pypa.io/en/latest/installation.html).

After cloning this repo and being in the project's folder, please follow those steps:

1. Create a virtual environment   
```bash
virtualenv venv
```

2. Activate it (linux and macos)  
```bash
source ./venv/bin/activate
```

3. Install the required dependencies  
```bash
pip install -r requirement.txt
```


## Run the app

You have 2 ways of running the app: using the `virtualenv` or `docker`. 

In both scenarios, you will want to look at the `.env` (normally wouldn't push that but for the 
sake of the exercice I did, it makes it simpler) and make sure the right `DATABASE_URL` is uncommented.

### Running inside docker

No setup is necessary, you don't even need to be inside the virtual environment.  
Simply make sure that inside the `.env` file, the docker's `DATABASE_URL` is uncommented.

Then simply run:
```bash 
docker-compose up --build 
```

This will create everything you need and allow you to access the API through 
[http://0.0.0.0:8000](http://0.0.0.0:8000).

### Running locally in the virtual environment

**1. Update .env with your own database**

First, you need to make sure your postgres database is setup properly and running, then update the `.env` file 
with your local database credentials (by default is my own local information, lots of default values):
```bash 
# docker
# DATABASE_URL=postgresql://test_user:test_password@db:5432/shortener_db

# local
DATABASE_URL=postgresql://<username>:<password>@<addr>:<port>/<database_name>
```

**2. Create the required table**

Run the following script:
```bash 
python app/db/init_db.py 
```
This will create the table with the right schema.

**3. Run the app**

Then you can run the app with this command:
```bash 
fastapi run 
```

You can go try the app using the `/docs` url highlighted: [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs) or 
any other way you wish.

To test a working scenario of the `GET /<shortcode>` endpoint, I suggest typing the full endpoint directly to 
the browser to be redirected as expected.

## Running the tests

For those you need to be inside the virtual environment. Then simply run:
```bash 
pytest
```
