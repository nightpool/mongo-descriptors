
from distutils.core import setup

setup(
    name='MongoDescriptors',
    version='0.1.0',
    author='Evan Gilgenbach',
    author_email='eg1290@gmail.com',
    py_modules=['mongo_descriptors'],
    url='https://github.com/nightpool/mongo-descriptors',
    license='LICENSE.txt',
    description='Some really basic descriptor-based utils for interacting with Mongo.',
    long_description=open('README').read(),
    install_requires=[
        "pymongo >= 2.0.0",
    ],
)

