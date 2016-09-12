# Amazon Redshift

sth special

- Create

```
CREATE [ [LOCAL ] { TEMPORARY | TEMP } ] TABLE 
[ IF NOT EXISTS ] table_name
( { column_name data_type [column_attributes] [ column_constraints ] 
  | table_constraints
  | LIKE parent_table [ { INCLUDING | EXCLUDING } DEFAULTS ] } 
  [, ... ]  )
[ BACKUP { YES | NO } ]
[table_attribute]

where column_attributes are:
  [ DEFAULT default_expr ]
  [ IDENTITY ( seed, step ) ] 
  [ ENCODE encoding ] 
  [ DISTKEY ]
  [ SORTKEY ]

and column_constraints are:
  [ { NOT NULL | NULL } ]
  [ { UNIQUE  |  PRIMARY KEY } ]
  [ REFERENCES reftable [ ( refcolumn ) ] ] 

and table_constraints  are:
  [ UNIQUE ( column_name [, ... ] ) ]
  [ PRIMARY KEY ( column_name [, ... ] )  ]
  [ FOREIGN KEY (column_name [, ... ] ) REFERENCES reftable [ ( refcolumn ) ] 

and table_attributes are:
  [ DISTSTYLE { EVEN | KEY | ALL } ] 
  [ DISTKEY ( column_name ) ]
  [ [COMPOUND | INTERLEAVED ] SORTKEY ( column_name [, ...] ) ]
```
- LOCAL is useless
- table name which start with # is temp table, the temp table is automatically dropped at the end of the session in which it is created. `create table #temp(id int);`
- enforces a limit of 9,900 tables per cluster among temp table(created by user or amazon).
- Optionally, the table name can be qualified with the database and schema name. In the following example, the database name is tickit , the schema name is public, and the table name is test.`create table tickit.public.test (c1 int);`
- IDENTITY Clause that specifies that the column is an IDENTITY column. An IDENTITY column contains unique auto-generated values. 
- DISTKEY Keyword that specifies that the column is the distribution key for the table. Only one column in a table can be the distribution key. 
- SORTKEY sort key for table, can define a maximum of 400 sortkey in one table. When data is loaded into the table, the data is sorted by one or more columns that are designated as sort keys.
- UNIQUE
- PRIMARY KEY
- LIKE parent_table [ { INCLUDING | EXCLUDING } DEFAULTS ] A clause that specifies an existing table from which the new table automatically copies column names, data types, and NOT NULL constraints. The new table and the parent table are decoupled, and any changes made to the parent table are not applied to the new table. 
- DISTSTYLE { EVEN | KEY | ALL } Defines the data distribution style for the whole table. Amazon Redshift distributes the rows of a table to the compute nodes according the distribution style specified for the table.

 > - EVEN: The data in the table is spread evenly across the nodes in a cluster in a round-robin distribution. 
 > - KEY: The data is distributed by the values in the DISTKEY column. when you set the join columns as distkey, the join will be more efficiency
 > - ALL: distribute entire table to every node. kind of spark brodcast table.
