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

# Function to insert or retrieve a user based on user_id
def get_or_insert_user(conn, user_id, profile_name):
    with conn.cursor() as cur:
        # Check if the user already exists
        cur.execute("SELECT user_id FROM user_profile WHERE user_id = %s", (user_id,))
        existing_user = cur.fetchone()

        if not existing_user:
            # Insert the user data into the 'user' table
            cur.execute("INSERT INTO user_profile (user_id, profile_name) VALUES (%s, %s)", (user_id, profile_name))
        
        return user_id

# Function to load data into the database
def load_data(data):
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            for item in data:
                product_id = item.get("product/productId")
                title = item.get("product/title")
                price = item.get("product/price")
                user_id = item.get("review/userId")
                profile_name = item.get("review/profileName")

                if product_id is None:
                    continue

                # Insert or retrieve the user based on user_id
                user_id = get_or_insert_user(conn, user_id, profile_name)

                # Check if the product_id already exists
                cur.execute("SELECT product_id FROM product WHERE product_id = %s", (product_id,))
                existing_product = cur.fetchone()

                if not existing_product:
                    # Insert the product data into the 'product' table
                    cur.execute(
                        "INSERT INTO product (product_id, title, price) VALUES (%s, %s, %s)",
                        (product_id, title, price)
                    )

                # Insert review data into the 'review' table
                cur.execute(
                    """
                    INSERT INTO review (product_id, user_id, helpfulness, score, review_time, summary, review_text)
                    VALUES (%s, %s, %s, %s, to_timestamp(%s), %s, %s)
                    """,
                    (
                        product_id,
                        user_id,
                        item.get("review/helpfulness"),
                        item.get("review/score"),
                        item.get("review/time"),
                        item.get("review/summary"),
                        item.get("review/text"),
                    ),
                )

        conn.commit()

if __name__ == "__main__":
    data = read_data_from_file("data/Kindle_Store.txt")
    load_data(data)

    print("Data loaded successfully.")
