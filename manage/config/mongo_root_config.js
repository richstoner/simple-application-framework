db.createUser(
   {
     user: "root",
     pwd: "##SAFROOTPASS##",
     roles:
       [
         { role: "readWrite", db: "config" },
         "clusterAdmin"
       ]
   }
);

