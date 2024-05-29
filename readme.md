# url shortener in python

This project is an URL shortener written in python, using fastapi and postgres.  
It is a simple API allowing you to shorten an URL, get redirected from a shortcode and getting 
some stats about a specific one.

This project was developed and tested using Python 3.12.

## Setup the virtual environment

Make sure you do have `virtualenv` on your system first. If not, please install it from 
[https://virtualenv.pypa.io/en/latest/installation.html](https://virtualenv.pypa.io/en/latest/installation.html).

After cloning this repo and being in the project's folder, please follow those steps:

1. Create a virtual environment   
```bash
virtualenv venv
```

2. Activate it (linux and macos)  
```source ./venv/bin/activate```

3. Install the required dependencies  
```pip install -r requirement.txt```

**Note**: To exit the virtual environment and return to your normal terminal, just type `deactivate`.


## Run the app

You have 2 ways of running the app: using the `virtualenv` or `docker`.


