# steps to build a server

    fab provider:do info save
    fab last info
    fab last addUser:flaskuser
    fab last update:v
    fab last installBase:v
    fab last installNginx:v
    fab last installRabbitMQ:v
    fab last configureSupervisor:v
    fab last startNginx:v
    fab last configureNginx:v
    fab last installMongoDB:v

    fab last user:flaskuser installConda:v
    fab last user:flaskuser testConda:v
    fab last user:flaskuser installAnaconda:v
    fab last rsync

