#Datebase Prep
db.getCollection('arbeitsagentur').dropIndexes()

db.getCollection('arbeitsagentur').createIndex( { "hashId": 1 }, { unique: true } )

#Clean up bad entries