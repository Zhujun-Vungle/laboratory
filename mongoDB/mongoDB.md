# mongodb

---

#### Introduction 

- Document Database
document is a data structure composed of field and value pairs. documents are similar to JSON objects. values can be another documents, arrays and arrays of documents.

    ![此处输入图片的描述][1]


 - CRUD
 

> Create or insert operations add new documents to a **collection**. If the collection does not currently exist, insert operations will create the collection.

##### insert example

```
> db.users.insert({name: "sue",age: 26, status: "A"})
WriteResult({ "nInserted" : 1 })
```
----
> Read operations retrieves documents from a collection; i.e. queries a collection for documents. MongoDB provides the following methods to read documents from a collection:
`db.collection.find()`

##### select example
```
> db.users.find({age: { $gt:18}})
{ "_id" : ObjectId("57e37bef0ad53fa1660e3736"), "name" : "sue", "age" : 26, "status" : "A" }
> db.users.find({age: { $gt:18}}).limit(5)
{ "_id" : ObjectId("57e37bef0ad53fa1660e3736"), "name" : "sue", "age" : 26, "status" : "A" }
```
##### about select
mongodb provide the db.collection.find() method to read documents from a collection. The method returns a cursor to matching documents. `db.collection.find( <query filter>, <projection> )`

> - a query filter to specify which documents to return.
> - a query projection to specifies which fields from the matching documents to return. The projection limits the amount of data that MongoDB returns to the client over the network.

#####select example
```
db.users.insertMany(
  [
     {
       _id: 1,
       name: "sue",
       age: 19,
       type: 1,
       status: "P",
       favorites: { artist: "Picasso", food: "pizza" },
       finished: [ 17, 3 ],
       badges: [ "blue", "black" ],
       points: [
          { points: 85, bonus: 20 },
          { points: 85, bonus: 10 }
       ]
     },
     {
       _id: 2,
       name: "bob",
       age: 42,
       type: 1,
       status: "A",
       favorites: { artist: "Miro", food: "meringue" },
       finished: [ 11, 25 ],
       badges: [ "green" ],
       points: [
          { points: 85, bonus: 20 },
          { points: 64, bonus: 12 }
       ]
     },
     {
       _id: 3,
       name: "ahn",
       age: 22,
       type: 2,
       status: "A",
       favorites: { artist: "Cassatt", food: "cake" },
       finished: [ 6 ],
       badges: [ "blue", "red" ],
       points: [
          { points: 81, bonus: 8 },
          { points: 55, bonus: 20 }
       ]
     },
     {
       _id: 4,
       name: "xi",
       age: 34,
       type: 2,
       status: "D",
       favorites: { artist: "Chagall", food: "chocolate" },
       finished: [ 5, 11 ],
       badges: [ "red", "black" ],
       points: [
          { points: 53, bonus: 15 },
          { points: 51, bonus: 15 }
       ]
     },
     {
       _id: 5,
       name: "xyz",
       age: 23,
       type: 2,
       status: "D",
       favorites: { artist: "Noguchi", food: "nougat" },
       finished: [ 14, 6 ],
       badges: [ "orange" ],
       points: [
          { points: 71, bonus: 20 }
       ]
     },
     {
       _id: 6,
       name: "abc",
       age: 43,
       type: 1,
       status: "A",
       favorites: { food: "pizza", artist: "Picasso" },
       finished: [ 18, 12 ],
       badges: [ "black", "blue" ],
       points: [
          { points: 78, bonus: 8 },
          { points: 57, bonus: 7 }
       ]
     }
  ]
)
```
```
// Select All
db.users.find({}) ==== db.users.find()
> db.users.find({}).limit(1)
{ "_id" : ObjectId("57e37bef0ad53fa1660e3736"), "name" : "sue", "age" : 26, "status" : "A" }
```
##### select filter
```
Sample
{
  <field1>: <value1>,
  <field2>: { <operator>: <value> },
  ...
}

> db.users.find({status: "A"})
{ "_id" : ObjectId("57e37bef0ad53fa1660e3736"), "name" : "sue", "age" : 26, "status" : "A" }
{ "_id" : 2, "name" : "bob", "age" : 42, "type" : 1, "status" : "A", "favorites" : { "artist" : "Miro", "food" : "meringue" }, "finished" : [ 11, 25 ], "badges" : [ "green" ], "points" : [ { "points" : 85, "bonus" : 20 }, { "points" : 64, "bonus" : 12 } ] }
{ "_id" : 3, "name" : "ahn", "age" : 22, "type" : 2, "status" : "A", "favorites" : { "artist" : "Cassatt", "food" : "cake" }, "finished" : [ 6 ], "badges" : [ "blue", "red" ], "points" : [ { "points" : 81, "bonus" : 8 }, { "points" : 55, "bonus" : 20 } ] }
{ "_id" : 6, "name" : "abc", "age" : 43, "type" : 1, "status" : "A", "favorites" : { "food" : "pizza", "artist" : "Picasso" }, "finished" : [ 18, 12 ], "badges" : [ "black", "blue" ], "points" : [ { "points" : 78, "bonus" : 8 }, { "points" : 57, "bonus" : 7 } ] }
```
###### query fiter documentation
```
> db.users.find({status: {$in:["P","D"]}})

{ "_id" : 1, "name" : "sue", "age" : 19, "type" : 1, "status" : "P", "favorites" : { "artist" : "Picasso", "food" : "pizza" }, "finished" : [ 17, 3 ], "badges" : [ "blue", "black" ], "points" : [ { "points" : 85, "bonus" : 20 }, { "points" : 85, "bonus" : 10 } ] }
{ "_id" : 4, "name" : "xi", "age" : 34, "type" : 2, "status" : "D", "favorites" : { "artist" : "Chagall", "food" : "chocolate" }, "finished" : [ 5, 11 ], "badges" : [ "red", "black" ], "points" : [ { "points" : 53, "bonus" : 15 }, { "points" : 51, "bonus" : 15 } ] }
{ "_id" : 5, "name" : "xyz", "age" : 23, "type" : 2, "status" : "D", "favorites" : { "artist" : "Noguchi", "food" : "nougat" }, "finished" : [ 14, 6 ], "badges" : [ "orange" ], "points" : [ { "points" : 71, "bonus" : 20 } ] }

//Although you can express this query using the $or operator, use the $in operator rather than the $or operator when performing equality checks on the same field.

// AND
db.users.find( { status: "A", age: { $lt: 30 } } )
> db.users.find( { status: "A", age: { $lt: 30 } } )
{ "_id" : ObjectId("57e37bef0ad53fa1660e3736"), "name" : "sue", "age" : 26, "status" : "A" }
{ "_id" : 3, "name" : "ahn", "age" : 22, "type" : 2, "status" : "A", "favorites" : { "artist" : "Cassatt", "food" : "cake" }, "finished" : [ 6 ], "badges" : [ "blue", "red" ], "points" : [ { "points" : 81, "bonus" : 8 }, { "points" : 55, "bonus" : 20 } ] }

//OR

> db.users.find(
... {
...  $or:[{status: "A"},{age: {$lt:30}}]
... }
... )
{ "_id" : ObjectId("57e37bef0ad53fa1660e3736"), "name" : "sue", "age" : 26, "status" : "A" }
{ "_id" : 1, "name" : "sue", "age" : 19, "type" : 1, "status" : "P", "favorites" : { "artist" : "Picasso", "food" : "pizza" }, "finished" : [ 17, 3 ], "badges" : [ "blue", "black" ], "points" : [ { "points" : 85, "bonus" : 20 }, { "points" : 85, "bonus" : 10 } ] }
{ "_id" : 2, "name" : "bob", "age" : 42, "type" : 1, "status" : "A", "favorites" : { "artist" : "Miro", "food" : "meringue" }, "finished" : [ 11, 25 ], "badges" : [ "green" ], "points" : [ { "points" : 85, "bonus" : 20 }, { "points" : 64, "bonus" : 12 } ] }
{ "_id" : 3, "name" : "ahn", "age" : 22, "type" : 2, "status" : "A", "favorites" : { "artist" : "Cassatt", "food" : "cake" }, "finished" : [ 6 ], "badges" : [ "blue", "red" ], "points" : [ { "points" : 81, "bonus" : 8 }, { "points" : 55, "bonus" : 20 } ] }
{ "_id" : 5, "name" : "xyz", "age" : 23, "type" : 2, "status" : "D", "favorites" : { "artist" : "Noguchi", "food" : "nougat" }, "finished" : [ 14, 6 ], "badges" : [ "orange" ], "points" : [ { "points" : 71, "bonus" : 20 } ] }
{ "_id" : 6, "name" : "abc", "age" : 43, "type" : 1, "status" : "A", "favorites" : { "food" : "pizza", "artist" : "Picasso" }, "finished" : [ 18, 12 ], "badges" : [ "black", "blue" ], "points" : [ { "points" : 78, "bonus" : 8 }, { "points" : 57, "bonus" : 7 } ] }
> 

db.users.find(
   {
     status: "A",
     $or: [ { age: { $lt: 30 } }, { type: 1 } ]
   }
)

// query on embedded document
db.users.find( { favorites: { artist: "Picasso", food: "pizza" } } )
> db.users.find( { favorites: { food: "pizza" } } )
> db.users.find( { favorites: { artist: "Picasso"} } )
> db.users.find( { favorites: { food: "pizza" } } )
> db.users.find( { favorites: { artist: "Picasso", food: "pizza" } } )
{ "_id" : 1, "name" : "sue", "age" : 19, "type" : 1, "status" : "P", "favorites" : { "artist" : "Picasso", "food" : "pizza" }, "finished" : [ 17, 3 ], "badges" : [ "blue", "black" ], "points" : [ { "points" : 85, "bonus" : 20 }, { "points" : 85, "bonus" : 10 } ] }
>
// equality match on Fields on embedded document
> db.users.find({"favorites.artist":"Picasso"})
{ "_id" : 1, "name" : "sue", "age" : 19, "type" : 1, "status" : "P", "favorites" : { "artist" : "Picasso", "food" : "pizza" }, "finished" : [ 17, 3 ], "badges" : [ "blue", "black" ], "points" : [ { "points" : 85, "bonus" : 20 }, { "points" : 85, "bonus" : 10 } ] }
{ "_id" : 6, "name" : "abc", "age" : 43, "type" : 1, "status" : "A", "favorites" : { "food" : "pizza", "artist" : "Picasso" }, "finished" : [ 18, 12 ], "badges" : [ "black", "blue" ], "points" : [ { "points" : 78, "bonus" : 8 }, { "points" : 57, "bonus" : 7 } ] }
> db.users.find({"favorites.food":"Pizza"})
> db.users.find({"favorites.food":"pizza"})
{ "_id" : 1, "name" : "sue", "age" : 19, "type" : 1, "status" : "P", "favorites" : { "artist" : "Picasso", "food" : "pizza" }, "finished" : [ 17, 3 ], "badges" : [ "blue", "black" ], "points" : [ { "points" : 85, "bonus" : 20 }, { "points" : 85, "bonus" : 10 } ] }
{ "_id" : 6, "name" : "abc", "age" : 43, "type" : 1, "status" : "A", "favorites" : { "food" : "pizza", "artist" : "Picasso" }, "finished" : [ 18, 12 ], "badges" : [ "black", "blue" ], "points" : [ { "points" : 78, "bonus" : 8 }, { "points" : 57, "bonus" : 7 } ] }

// query on an Array
// exactly
db.users.find( { badges: [ "blue", "black" ] } )
> db.users.find( { badges: ["black","blue"] } )
{ "_id" : 6, "name" : "abc", "age" : 43, "type" : 1, "status" : "A", "favorites" : { "food" : "pizza", "artist" : "Picasso" }, "finished" : [ 18, 12 ], "badges" : [ "black", "blue" ], "points" : [ { "points" : 78, "bonus" : 8 }, { "points" : 57, "bonus" : 7 } ] }
> db.users.find( { badges: ["blue","black"] } )
{ "_id" : 1, "name" : "sue", "age" : 19, "type" : 1, "status" : "P", "favorites" : { "artist" : "Picasso", "food" : "pizza" }, "finished" : [ 17, 3 ], "badges" : [ "blue", "black" ], "points" : [ { "points" : 85, "bonus" : 20 }, { "points" : 85, "bonus" : 10 } ] }
// Arrays with position
> db.users.find( { "badges.0": "black" } )
{ "_id" : 6, "name" : "abc", "age" : 43, "type" : 1, "status" : "A", "favorites" : { "food" : "pizza", "artist" : "Picasso" }, "finished" : [ 18, 12 ], "badges" : [ "black", "blue" ], "points" : [ { "points" : 78, "bonus" : 8 }, { "points" : 57, "bonus" : 7 } ] }
> db.users.find( { "badges.1": "black" } )
{ "_id" : 1, "name" : "sue", "age" : 19, "type" : 1, "status" : "P", "favorites" : { "artist" : "Picasso", "food" : "pizza" }, "finished" : [ 17, 3 ], "badges" : [ "blue", "black" ], "points" : [ { "points" : 85, "bonus" : 20 }, { "points" : 85, "bonus" : 10 } ] }
{ "_id" : 4, "name" : "xi", "age" : 34, "type" : 2, "status" : "D", "favorites" : { "artist" : "Chagall", "food" : "chocolate" }, "finished" : [ 5, 11 ], "badges" : [ "red", "black" ], "points" : [ { "points" : 53, "bonus" : 15 }, { "points" : 51, "bonus" : 15 } ] }

// match
db.users.find( { badges: "black" } )
...


In conclusion , dot can be used in embeded structure to specify which parameter will be match.  And every move start fro the most out embrace.
```

[Query and Projection Operators][2]



- UPDATE
![update][3]
> db.collection.update()
db.collection.updateOne() New in version 3.2
db.collection.updateMany() New in version 3.2
db.collection.replaceOne() New in version 3.2

```
// prototype
db.collection.update(
   <query>,
   <update>,
   {
     upsert: <boolean>,
     multi: <boolean>,
     writeConcern: <document>
   }
)

```
- DELETE
> **db.collection.remove()**	
Delete a single document or all documents that match a specified filter.
**db.collection.deleteOne()**	
Delete at most a single document that match a specified filter even though multiple documents may match the specified filter.
**db.collection.deleteMany()**	
Delete all documents that match a specified filter.


－ BULKWRITE
> The **db.collection.bulkWrite()** method provides the ability to perform bulk insert, update, and remove operations. MongoDB also supports bulk insert through the db.collection.insertMany().

-SQL
![Screen Shot 2016-09-22 at 4.28.56 PM.png-146.9kB][4]
![Screen Shot 2016-09-22 at 4.30.11 PM.png-92.8kB][5]

```
// data
> db.orders.insert({
...   cust_id: "abc123",
...   ord_date: ISODate("2012-11-02T17:04:11.102Z"),
...   status: 'A',
...   price: 50,
...   items: [ { sku: "xxx", qty: 25, price: 1 },
...            { sku: "yyy", qty: 25, price: 1 } ]
... })
WriteResult({ "nInserted" : 1 })
```

[mongo-sql comparison][7]

![Screen Shot 2016-09-22 at 4.46.16 PM.png-212.4kB][6]

- TEXT SEARCH
```
db.stores.insert(
...    [
...      { _id: 1, name: "Java Hut", description: "Coffee and cakes" },
...      { _id: 2, name: "Burger Buns", description: "Gourmet hamburgers" },
...      { _id: 3, name: "Coffee Shop", description: "Just coffee" },
...      { _id: 4, name: "Clothes Clothes Clothes", description: "Discount clothing" },
...      { _id: 5, name: "Java Shopping", description: "Indonesian goods" }

...    ]
... )
BulkWriteResult({
	"writeErrors" : [ ],
	"writeConcernErrors" : [ ],
	"nInserted" : 5,
	"nUpserted" : 0,
	"nMatched" : 0,
	"nModified" : 0,
	"nRemoved" : 0,
	"upserted" : [ ]
})
> 
> db.stores.createIndex( { name: "text", description: "text" } )
{
	"createdCollectionAutomatically" : false,
	"numIndexesBefore" : 1,
	"numIndexesAfter" : 2,
	"ok" : 1
}
> 
> 
> db.stores.find( {
... $text: {
... $search: "java coffee shop" }})
{ "_id" : 5, "name" : "Java Shopping", "description" : "Indonesian goods" }
{ "_id" : 1, "name" : "Java Hut", "description" : "Coffee and cakes" }
{ "_id" : 3, "name" : "Coffee Shop", "description" : "Just coffee" }
> 
```



  [1]: https://docs.mongodb.com/manual/_images/crud-annotated-document.png
  [2]: https://docs.mongodb.com/manual/reference/operator/query/
  [3]: https://docs.mongodb.com/manual/_images/crud-annotated-mongodb-update.png
  [4]: http://static.zybuluo.com/ZeoJun/rsjro299rutioea6o0yk50cm/Screen%20Shot%202016-09-22%20at%204.28.56%20PM.png
  [5]: http://static.zybuluo.com/ZeoJun/044g9lr7luw3kzywakioctgb/Screen%20Shot%202016-09-22%20at%204.30.11%20PM.png
  [6]: http://static.zybuluo.com/ZeoJun/9hw9l8lq9vuzxyvtm9ecduz0/Screen%20Shot%202016-09-22%20at%204.46.16%20PM.png
  [7]: https://docs.mongodb.com/manual/reference/sql-aggregation-comparison/
