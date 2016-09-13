# Amazon Redshift

sth special

# Amazon Redshift

sth special

#### Create

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

#### 编码格式


----------

>  ![Screen Shot 2016-09-13 at 3.27.45 PM.png-209.8kB][1]

- raw encoding 
> default storage method, data stored in raw uncompressed.

- Byte-Dictionary Encoding
> the dictionary contains up to **256** one-byte values that are stored as indexes to the orign data values. not always effective when used with VARCHAR column. 

- Delta Encoding
> useful for **datetime** columns.  compress data by record difference between data. such as 1...10, the first will be stored as a 4-byte integer, next 9 will each be stored as a byte with the value 1, indicating that it is one greater than the previous one. 
> - DELTA records diff as 1-byte values
> - DELTA32K records diff as 2-byte values




![Screen Shot 2016-09-13 at 3.52.00 PM.png-115.4kB][2]



- LZO Encoding 
> high compression ratio with good performance. work well for CHAR and VARCHAR that store very long strings.

- Mostly Encoding
> useful when the data type for a column is larger than most of the stored values require(like numbers). you can compress the majority of the values in the column to a smaller standard storage size. The remaining are stored in their raw form. 
> work with the following data types
> - SMALLINT/INT2(16-bit) 
> - INTEGER/INT (32-bit)
> - BIGINT/INT8 (64-bit)
> - DECIMAL/NUMERIC (64-bit)

![Screen Shot 2016-09-13 at 4.12.11 PM.png-81.6kB][3]
![Screen Shot 2016-09-13 at 4.24.59 PM.png-144kB][4]

- Runlength Encoding
> Runlength encoding replaces a repeated consecutively value with a token consists of the value and a count. this is suit for table in which data values repeated conscutively. 
>  do not recommend applying runlength encoding on any column that is designated as a sort key. 

![Screen Shot 2016-09-13 at 4.35.45 PM.png-129.8kB][5]


- Text255 and Text32k Encodings
> Text255 and text32k encodings are useful for compressing **VARCHAR** columns in which the **same words recur often**. A separate dictionary of unique words is created for each block of column values on disk. (An Amazon Redshift disk block occupies 1 MB.) The dictionary contains the first 245 unique words in the column. 


  [1]: http://static.zybuluo.com/ZeoJun/d3dhux61k5aif3z3pyjj1cmc/Screen%20Shot%202016-09-13%20at%203.27.45%20PM.png
  [2]: http://static.zybuluo.com/ZeoJun/hacyexn4u7u8cifd8bc8me8e/Screen%20Shot%202016-09-13%20at%203.52.00%20PM.png
  [3]: http://static.zybuluo.com/ZeoJun/bv1rkoly8s0vrp0xvbdxij9l/Screen%20Shot%202016-09-13%20at%204.12.11%20PM.png
  [4]: http://static.zybuluo.com/ZeoJun/uzfyg8be9sg6qagdb9pchf6p/Screen%20Shot%202016-09-13%20at%204.24.59%20PM.png
  [5]: http://static.zybuluo.com/ZeoJun/mioe3fmzt4oizyt19ccj0ko9/Screen%20Shot%202016-09-13%20at%204.35.45%20PM.png
