import psycopg2
from psycopg2.extras import execute_values

# Define your PostgreSQL connection parameters
db_params = {
    "host": "localhost",
    "database": "KindleReviews",
    "user": "user_1",
    "password": "test123"
}

# Function to read data from a .txt file
def read_data_from_file(file_path):
    with open(file_path, "r") as file:
        lines = file.read().split('\n\n')  # Assuming each entry is separated by two newlines
        data = []
        for entry in lines:
            entry_data = {}
            for line in entry.split('\n'):
                if ":" not in line:
                    print(f"Invalid line: {line}")
                    continue
                key, value = line.split(': ', 1)
                # Check and replace "unknown" with None for the "price" field
                if key == "product/price" and value == "unknown":
                    value = None
                entry_data[key] = value
            data.append(entry_data)
        return data

# Load data from the .txt file
data = read_data_from_file("data/Kindle_Store.txt")

# Establish a connection to the PostgreSQL database using a context manager
with psycopg2.connect(**db_params) as conn:
    with conn.cursor() as cur:
        for item in data:
            product_id = item.get("product/productId")
            title = item.get("product/title")
            price = item.get("product/price")

            if product_id is None:
                continue

            # Check if the product_id already exists
            cur.execute("SELECT product_id FROM product WHERE product_id = %s", (product_id,))
            existing_product = cur.fetchone()

            if existing_product is None:
                # Insert the product data into the 'product' table
                cur.execute(
                    "INSERT INTO product (product_id, title, price) VALUES (%s, %s, %s)",
                    (product_id, title, price)
                )

            # Insert review data into the 'review' table
            cur.execute(
                """
                INSERT INTO review (product_id, user_id, profile_name, helpfulness, score, review_time, summary, review_text)
                VALUES (%s, %s, %s, %s, %s, to_timestamp(%s), %s, %s)
                """,
                (
                    product_id,
                    item.get("review/userId"),
                    item.get("review/profileName"),
                    item.get("review/helpfulness"),
                    item.get("review/score"),
                    item.get("review/time"),
                    item.get("review/summary"),
                    item.get("review/text"),
                ),
            )

    # Commit the changes to the database
    conn.commit()

print("Data loaded successfully.")
