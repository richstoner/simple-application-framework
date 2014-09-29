//db.addUser({ user : "girder", pwd : "##SAFGIRDERPASS##",  roles:[ "userAdminAnyDatabase", "readWrite" ] });

db.createUser( { "user" : "girder",
                 "pwd": "##SAFGIRDERPASS##",
                 "roles" : [ { role: "clusterAdmin", db: "admin" },
                             { role: "readAnyDatabase", db: "admin" },
                             "readWrite"
                             ] });