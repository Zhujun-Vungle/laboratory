

####a bite of cassendra 


try cql in cqlsh
```
cqlsh> SELECT cluster_name, listen_address FROM system.local; 

 cluster_name | listen_address
--------------+----------------
 Test Cluster |     172.17.0.2

(1 rows)
```
```
cqlsh> use zj;
cqlsh:zj> 
cqlsh:zj> CREATE TABLE users ( id int, user_name varchar, PRIMARY KEY(id));
```
