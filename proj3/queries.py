import pymongo

def main():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["ArtReviews"]  # Replace with your actual database name
    collection = db["Reviews"]  # Replace with your actual collection name

    #Count the number of documents in the collection
    count = collection.count_documents({})
    print(f"Total documents in the collection: {count}")

    # Retrieve and print a few documents to verify
    sample_documents = collection.find().limit(5)
    for doc in sample_documents:
        print(doc)

    collection_stats = db.command("collstats", "Reviews")

    avg_doc_size = collection_stats.get("avgObjSize")
    total_data_size = collection_stats.get("size")
    disk_space_used = collection_stats.get("storageSize")

    print(f"Average Document Size: {avg_doc_size} bytes")
    print(f"Total Data Size: {total_data_size} bytes")
    print(f"Disk Space Used: {disk_space_used} bytes")

if __name__ == "__main__":
    main()