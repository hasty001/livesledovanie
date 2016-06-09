from setuptools import setup

setup(name='sledovanie',
      version='1.0',
      description='live sledovanie app',
      author='hasty',
      author_email='info@cestasnp.sk',
      url='http://livesledovanie.eu/',

      install_requires=['flask==0.10.1','flask-login==0.2.7','sqlalchemy==0.9.8','flask-sqlalchemy==2.0', 'MarkupSafe'],
      #install_requires=['flask==0.10.1','flask-login==0.2.7','sqlalchemy==0.9.8','flask-sqlalchemy==2.0', 'MarkupSafe'],
     )