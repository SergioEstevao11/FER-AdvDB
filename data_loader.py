import re
import logging


# Text file containing the data
txt_file = 'data/Kindle_Store.txt'

# Output SQL file
sql_file = 'populate.sql'

# Open the output SQL file for writing
with open(sql_file, 'w') as output_file:
    with open(txt_file, 'r') as f:
        data = f.read()

    # Split the data into individual records based on blank lines
    records = re.split(r'\n\s*\n', data)

    for record in records:
        lines = record.strip().split('\n')
        product_data = {}
        review_data = {}

        for line in lines:
            if ":" not in line:
                print(f"Invalid line: {line}")
                continue
            key, value = line.split(": ", 1)
            if key.startswith("product/"):
                product_data[key] = value
            elif key.startswith("review/"):
                review_data[key] = value

        if 'product/productId' in product_data and 'review/userId' in review_data:
            insert_product_sql = f"INSERT INTO product (product_id, title, price) " \
                                f"VALUES ('{product_data.get('product/productId')}', " \
                                f"'{product_data.get('product/title')}', " \
                                f"'{product_data.get('product/price')}');\n"
            insert_review_sql = f"INSERT INTO review (product_id, user_id, profile_name, " \
                               f"helpfulness, score, review_time, summary, review_text) " \
                               f"VALUES ('{product_data.get('product/productId')}', " \
                               f"'{review_data.get('review/userId')}', " \
                               f"'{review_data.get('review/profileName')}', " \
                               f"'{review_data.get('review/helpfulness')}', " \
                               f"'{review_data.get('review/score')}', " \
                               f"to_timestamp('{review_data.get('review/time')}'::double precision), " \
                               f"'{review_data.get('review/summary')}', " \
                               f"'{review_data.get('review/text')}');\n"

            output_file.write(insert_product_sql)
            output_file.write(insert_review_sql)