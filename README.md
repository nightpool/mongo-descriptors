Mongo Descriptors
=================

Some really basic descriptor-based utils for interacting with Mongo. Specifically, It's made for model classes, that represent documents or types of documents.

Example:
```python
import bson
from mongo-descriptors import MongoI, Db

class Doc(object):
	db=Db()
	some_prop=MongoI("some_prop")					# Note that if you try to get this before assigning 
													# to it, you'll get an error. (Unless of course the 
													# document already exists in the database)

	an_int_prop=MongoI("an_int_prop", typ=int)		# Applies int() before returning and submitting.

	another_prop=MongoI("another_prop", default=0)	# If the property isn't in the database, it returns
													# value provided by default. This doesn't affect 
													# the value stored in the database in any way.

	oi=bson.ObjectId()								# The instance is required to have a attribute oi 
													# which stores the _id of the document reffered to.

	raw=MongoI()									# This gets and stores a raw dict that represents
													# the object. You can't overwrite the _id like this.

													# I mentioned earlier that it returned a dict. 
													# This isn't strictly true. It actually returns a 
													# CatDict, which supports concatination.
													# This leads itself to examples like the following.

x=Doc()
x.raw+={"foo":"bar"}								# Note that foo does not actually get added as a
													# property to the object. Just to the database.
```