CREATE EXTENSION fuzzystrmatch; 	-- (soundex, levenshtein, metaphone)
CREATE EXTENSION pg_trgm;		-- (similarity , show_Trgm,…, %, <->)

CREATE TABLE product (
    product_id VARCHAR(255) PRIMARY KEY,
    title TEXT NOT NULL,
    price MONEY
);

CREATE TABLE user_profile (
    user_id VARCHAR(255) PRIMARY KEY,
    profile_name TEXT NOT NULL
);

CREATE TABLE review (
    review_id SERIAL PRIMARY KEY,
    product_id CHAR(10) REFERENCES product(product_id),
    user_id VARCHAR(255) REFERENCES user_profile(user_id),
    helpfulness VARCHAR(255),
    score DECIMAL(3, 1) NOT NULL,
    review_time TIMESTAMP NOT NULL,
    summary TEXT,
    review_text TEXT
);

--INDEXES

-- TRIGRAM
CREATE INDEX idx_trgm_title ON product USING gin(title gin_trgm_ops);

CREATE INDEX idx_trgm_title_review_text ON user_profile USING gin(profile_name gin_trgm_ops);

CREATE INDEX idx_trgm_summary_review_text ON review USING gin(summary gin_trgm_ops, review_text gin_trgm_ops);



-- others
CREATE INDEX idx_review_score ON review (score);
CREATE INDEX idx_product_price ON product (price);
CREATE INDEX idx_review_time ON review (review_time);


--CONFIGURATIONS

-- Create a new text search configuration named 'se56303'
CREATE TEXT SEARCH CONFIGURATION se56303 (copy=simple);

-- Assign the 'simple' dictionary to the token types
ALTER TEXT SEARCH CONFIGURATION se56303
    ALTER MAPPING FOR asciiword, word, numword, host WITH simple;
