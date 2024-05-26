# url shortener in python

## setup

- add `.env` file with the postgres url
- init DB / explain why models and init are in the same file (didn't know how to not do that)

## model 

everything is one table for simplicity as per required, instead of having 2 tables which would probably 
be better in a real scenario


## shortcode generation
chose the easiest solution as per the requirement again

2 other solutions stand out:
- using the hash of the url and taking the first 6 characters (or the last probably better), regardless 
still a risk of getting the same shortcode so not really better than what I chose 

- it looks like the most reliable way to generate guarantee unique code would be to increment a number in our 
DB and hash that in base 62, but since in the requirement people can send their own shortcode, this will not 
guarantee it either
