# Simple Application Framework

An easy way to deploy and manage python-based processes. Once setup, it's trivial to deploy a flask application to the host, handling nginx + supervisor + pip configuration along the way.

#### source

frontend -> angular.js application provisioned with yeoman

server -> flask app

manage -> provisioning tools



#### structure on server

/vagrant -> a clone of this directory.

/home/flaskuser/miniconda/envs/server -> python virtual environment

/home/flaskuser/flaskapp -> place flask application here

 app would consist of folder, configuration settings, and asset folders (static/templates)


/home/flaskuser/celerytasks -> place processing tasks here


