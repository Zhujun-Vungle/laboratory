

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
cqlsh:zj> insert into users(id,user_name) values(1,'petter') ;
cqlsh:zj> insert into users(id,user_name) values(2,'justin') ;
cqlsh:zj> select * from users
      ... ;

 id | user_name
----+-----------
  1 |    petter
  2 |    justin

cqlsh:zj> update users set user_name="zhujun" where id=1;
SyntaxException: <ErrorMessage code=2000 [Syntax error in CQL query] message="line 1:36 no viable alternative at input 'where' (update users set user_name=["zhuju]n" where...)">
cqlsh:zj> update users set user_name='zhujun' where id=1;
cqlsh:zj> select * from users;

 id | user_name
----+-----------
  1 |    zhujun
  2 |    justin

(2 rows)

cqlsh:zj> delete from users where id =1;
cqlsh:zj> select * from users;

 id | user_name
----+-----------
  2 |    justin

(1 rows)
```

