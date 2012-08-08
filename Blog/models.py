# models.py
# Store the database schema.

# Raw SQL or an abstraction layer? I'd go with raw SQL to keep things simple, and then use psycopg2 to access the stuff.
# Can also go with Mongo-DB. Gives a chance to learn Mongo, and besides, the data is stored in files in Mondo as well.