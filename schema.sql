CREATE EXTENSION fuzzystrmatch; 	-- (soundex, levenshtein, metaphone)
CREATE EXTENSION pg_trgm;		-- (similarity , show_Trgm,…, %, <->)

CREATE TABLE product (
    product_id CHAR(10) PRIMARY KEY,
    title TEXT NOT NULL,
    price MONEY -- You can use an appropriate data type for price
);

CREATE TABLE review (
    review_id SERIAL PRIMARY KEY, -- You can use a serial for a unique identifier
    product_id CHAR(10) REFERENCES product(product_id),
    user_id VARCHAR(255) NOT NULL,
    profile_name TEXT,
    helpfulness VARCHAR(10), -- Assuming it's in the format "X/Y"
    score DECIMAL(3, 1) NOT NULL, -- Decimal with one decimal place
    review_time TIMESTAMP NOT NULL, -- Storing as a timestamp
    summary TEXT,
    review_text TEXT
);