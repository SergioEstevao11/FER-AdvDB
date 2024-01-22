import pymongo
import time

def main():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["ArtReviews"]  # Replace with your actual database name
    collection = db["Reviews"]  # Replace with your actual collection name
    
    #ex2
    # start_time = time.time()
    # distinct_scores = collection.distinct("review.score")
    # end_time = time.time()

    # print("Distinct Review Scores:", distinct_scores)
    # print("Query Execution Time:", end_time - start_time, "seconds")
   
    #3
    start_time = time.time()
    products_without_price = db.your_collection.count_documents({"product.price": "unknown"})
    end_time = time.time()

    print("Number of products without a defined price:", products_without_price)
    print("Query Execution Time:", end_time - start_time, "seconds")

    #4
    # start_time = time.time()
    # rated_1_reviews = db.your_collection.find({"review.score": "1.0"}).sort([("review.date", 1), ("_id", 1)])
    # count = rated_1_reviews.count()
    # penultimate_10 = rated_1_reviews.skip(count - 20).limit(10)
    # end_time = time.time()

    # for review in penultimate_10:
    #     print({
    #         "Product Name": review["product"]["title"],
    #         "Price": review["product"]["price"],
    #         "Review Date": review["review"]["date"]
    #     })

    # print("Query Execution Time:", end_time - start_time, "seconds")

    #5


    #6
if __name__ == "__main__":
    main()