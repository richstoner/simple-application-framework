# Simple Application Framework

An easy way to deploy and manage python-based processes. Once setup, it's trivial to deploy a flask application to the host, handling nginx + supervisor + pip configuration along the way.

Check out the helloworld app as an example: 

[https://github.com/richstoner/simple-application-framework/tree/master/server/apps/helloworld](https://github.com/richstoner/simple-application-framework/tree/master/server/apps/helloworld)




#### folder structure

server -> python apps and tasks

manage -> provisioning tools




#### structure on server

/vagrant -> a clone of this directory. rsync'able with fabric

/home/{{user}}/miniconda/envs/server -> python virtual environment


