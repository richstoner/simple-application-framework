Install Instructions
--------------------

The current version of this framework requires several manual steps to provision a remote host. These steps could be
aggregated into a single superscript. By keeping them discrete, it provides the user with a better understanding of
what is being installed where.


Step 0: Setup a remote machine
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You, the target audience, should be comfortable in creating a new virtual machine, either on the cloud or in vagrant. Once started, you will need to configure the appropriate host name, default user, and associated authentication mechanisms. Currently this framework supports vagrant, AWS, and digital ocean.


Step 1: Provision the machine with core components
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You will need to have a local installation of fabric, a python module that allows us to run the remote
commands. To install fabric, follow instructions from here: http://www.fabfile.org/

*All of the following commands should be run from the `manage` folder*

**1) Verify a working fabric installation and get a list of available commands:**

:code:`fab --list`

	This should return a long list of commands available through fabric


**2) Verify your host settings are correct**

:code:`fab provider:do info`

	This should return a list of server stats, including ubuntu release #


**3) Save this information to a local variable to simplify the fabric calls**

:code:`fab provider:do info save`

	We now have a file (last.ini) with the most recent working settings. We can now run the equivalent command:

:code:`fab last info`

	And get the same result as before.

**4) Run the standard updates via apt**

:code:`fab last update:v`

	This command introduces the verbose flag. Most commands will surpress their output unless a value is passed with their call. Here we pass ':v'. This actual value is ignored, we simply test for absense or presence of.


**5) Install some base tools and configure them**

What you'll have when done: build-essential, subversion, git, unzip, supervisor

:code:`fab last installBase:v installNginx:v`

:code:`fab last rsync`

:code:`fab last configureNginx:v`

:code:`fab last configureSupervisor:v`

:code:`fab last restartAll:`

You should now be able to visit the host domain.

Going to http://hostdomain:9999 should land you at the Supervisor control panel.


Step 2: Install additional components
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1) Install a database (mongodb)

:code:`fab last installMongoDB:v`


2) Install a task queue (RabbitMQ)

:code:`fab last installRabbitMQ:v`




Step 3: Add components for python apps
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following commands will add the remaining components needed to host multiple python web applications with a common set of share modules. We use anaconda (https://store.continuum.io/cshop/anaconda/) to handle package management (with pip as needed).

1) We'll create a user & home directory to store the python distribution

:code:`fab last addUser:flaskuser`

2) Install miniconda (the anaconda base installer)

:code:`fab last user:flaskuser installConda:v`

	This command introduces the user:<username> inline parameter. It works how you'd expect it to work.

3) Install python dependencies like OpenCV, numpy, scipy, flask, etc

:code:`fab last user:flaskuser installPythonCore:v`


We now have everything we need to run apps!





Step 4: Adding an app from git and running
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**What is an app (in this context)?**

An app bundle is a directory containing key configuration files and all necessary source code & resources. You'll notice the requirements.txt, nginx.conf, supervisor.conf in the repo above. The management framework takes this information and uses it to deploy individual applications. Each application is managed via the supervisord http interface for simplicity.

A simple app: https://github.com/richstoner/simple_app

A complex app: https://github.com/richstoner/isic_annotator

Installation of an app is done by pointing the hosting framework to a git repository and giving the app a name.


**We'll use the simple app for this example.**


*Still running commands from `manage`*


1) Register the app with the framework

:code:`fab last addApp:appname=simple,giturl=https://github.com/richstoner/simple_app.git`

2) Enable the app

This links the nginx & supervisor config files, and installs any additional python dependencies via pip

:code:`fab last enableApp:simple`

You can now start this app via the supervisor configuration, available at http://hostdomain:9999


**To update the app from git after enabled:**

:code:`fab last updateApp:simple`

:code:`fab last restartAll` (this could be more elegant!)



Have a look at the config files. An ideal next step would be to build a skeleton generator for the nginx/supervisor configuration files. 

