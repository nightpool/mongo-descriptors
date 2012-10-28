import pymongo

class Db(object):
	"""A Descriptor class for storing a db. (actually a collection)
		name is a string, the name of the colection.
		root is a string, the actual database.
		root defaults to local"""
	def __init__(s, name=None, db=None, root="local"):		
		s._db = db
		s.name=name
		s.root=root
		if not name and not db:
			raise ValueError("Need either a db object to base off of or a name")
	def __get__(s, inst, cls):
		"""Alias for get()"""
		return s.get()
	def __set__(s,inst,val):
		"""Changes the db to specified db.
			If the value is a tuple, then the name and the root are set from indices 0 and 1 respectively.
			If the value is an instance of pymongo.database.Collection or sub-classes, then the root and the name are set from that Collection
			Else the value is cast as a string, and interpreted as the name."""			
		if isinstance(val, pymongo.database.Collection):
			s._db = val
			return
		s._db = None
		if isinstance(val, basestring):		#This is so we don't accidently set name and root to the first 2 chars of a string
			s.name=val
			return
		else:
			try:
				s.name=str(val[0])
				s.root=str(val[1])
			except KeyError:
				s.name=str(val)
	def get(s):
		"""Get the db. Returns the db instance"""
		if s._db:
			return s._db
		con=pymongo.Connection()
		db=con[s.root][s.name]
		return db

class CatDict(dict):
	"""A small modification to dict that supports concatenation :)"""
	def __add__(s, other):
		ret=s.copy()
		ret.update(other)
		return ret

class MongoI(object):
	"""A Descriptor that represents one property in a mongo document.
	Requires the instance to have an attribute db, which is a pymongo.Database and an attribute oi which is the value in the _id of the document
	Suggested use is in model classes that represent a type of document
	If name is omitted, it represents a CatDict of the document. Using CatDict with this allows you to do things like
		x+={"some_prop": stuff}	 	#X being a MongoI with no name (i.e. MongoI()) in a object.
	to add some_prop to the mongo Document.
		Name is the name of the property.
		typ is a callable that is called on the return object to standardise it. for example, int"""
	def __init__(s,name=None,typ=None,default=None):
		s.name=name
		s.default=default
		if typ and not default:
			s.default = typ()
		s.typ=typ
	def __get__(s, inst, cls):
		if s.name==None:
			return CatDict(inst.db.find_one(inst.oi))
		else:
			try:
				ret=inst.db.find_one(inst.oi)[s.name]
			except KeyError:
				ret=s.default
			if not s.typ==None:
				ret=s.typ(ret)
			return ret
	def __set__(s, inst, val):
		if s.name==None:
			new=dict(val)
			new['_id']=inst.oi  	#just some sanity checking here...
		else:
			new=inst.db.find_one(inst.oi)
			if not s.typ==None:
				val=s.typ(val)
			new[s.name]=val
		#print new
		inst.db.save(new)
	def __delete__(s,inst):
		if s.name==None:
			inst.db.remove({'_id':s.oi})
			return
		new = inst.db.find_one(inst.oi)
		try:
			del new[s.name]
		except KeyError:
			pass
		inst.db.save(new)

class test(object):
	"""Just a simple test object that tests most of the features. Its in no way exhaustive, and if you find a bug, please tell me."""
	db=Db("test", root="local")
	blank=MongoI("stuff")
	de=MongoI("de", default = "ww")
	tnd=MongoI("tnd", int)
	twd=MongoI("twd", int, default = 2)
	raw=MongoI()
	def __init__(s, oi):
		s.oi=oi
		if s.db.find_one(oi)==None:
			s.db.insert({"_id":oi})