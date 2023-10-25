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


--ex4 -> update the configuration 

-- Alter the "se56303" configuration to modify the behavior of word and asciiword tokens
ALTER TEXT SEARCH CONFIGURATION se56303
    DROP MAPPING FOR word, asciiword; -- Remove stop words

-- Assign the 'simple' dictionary for unrecognized words
ALTER TEXT SEARCH CONFIGURATION se56303
    ALTER MAPPING FOR asciiword, word WITH simple;

-- Assign the 'english_stem' dictionary for recognized English words (normalize)
ALTER TEXT SEARCH CONFIGURATION se56303
    ALTER MAPPING FOR asciiword WITH english_stem;

--ex5 -> dictionary configuration

-- Create the 'se56303Syn' text search dictionary
CREATE TEXT SEARCH DICTIONARY se56303Syn (
	TEMPLATE = synonym,
	SYNONYMS = se56303syn
);

-- Create a text search configuration using the 'se56303' configuration as a template
CREATE TEXT SEARCH CONFIGURATION se56303Syn (COPY = se56303);

-- Set the 'se56303Syn' dictionary for word and asciiword token types
ALTER TEXT SEARCH CONFIGURATION se56303Syn
    ALTER MAPPING FOR asciiword, word WITH se56303Syn;


--ex6
-- Change the behavior of 'ferUserName' text search configuration for word and asciiword tokens

ALTER TEXT SEARCH CONFIGURATION se56303
    ALTER MAPPING FOR asciiword, word
    WITH se56303Syn, english_stem;

--ex7

SELECT review_text
FROM review
WHERE to_tsvector('se56303', review_text) @@ to_tsquery('se56303', 'awesomeness & hell & good');


SELECT review_text
FROM review
WHERE to_tsvector('se56303', review_text) @@ phraseto_tsquery('se56303', 'daring to dream');


SELECT review_text
FROM review
WHERE to_tsvector('se56303', review_text) @@ tsquery_phrase(to_tsquery('bound'), to_tsquery('darkness'), 2)
   
--ex8
SELECT
	ts_rank_cd(
		setweight(to_tsvector('se56303', p.title), 'A')   ||
        setweight(to_tsvector('se56303', r.summary), 'A') ||
        setweight(to_tsvector('se56303', r.review_text), 'C'),
		to_tsquery('se56303', 'woman & across')
	) AS relevance,
    r.review_id,
	p.title,
    r.summary,
    r.review_text
FROM review r
JOIN product p ON r.product_id = p.product_id
WHERE r.review_id = 214324;

--ex9

SELECT *
FROM (
    SELECT
    	(LENGTH(LOWER(r.review_text)) - LENGTH(REPLACE(LOWER(r.review_text), LOWER('good'), ''))) / LENGTH(LOWER('good')) AS occurrences,
		ts_rank_cd(
			setweight(to_tsvector('se56303', r.review_text), 'A'),
			to_tsquery('se56303', 'good')
		) AS relevance,
		r.review_id,
		p.title,
		r.summary,
		r.review_text
	FROM review r
	JOIN product p ON r.product_id = p.product_id
	WHERE to_tsvector('se56303', r.review_text) @@ to_tsquery('se56303', 'good')
	ORDER by relevance DESC
) subquery;



SELECT *
FROM (
    SELECT
    	LENGTH(LOWER(r.review_text)) AS length,
		ts_rank_cd(
			setweight(to_tsvector('se56303', r.review_text), 'A'),
			to_tsquery('se56303', 'good')
		) AS relevance,
		r.review_id,
		p.title,
		r.summary,
		r.review_text
	FROM review r
	JOIN product p ON r.product_id = p.product_id
	WHERE to_tsvector('se56303', r.review_text) @@ to_tsquery('se56303', 'good')
	ORDER by relevance DESC
) subquery;

--ex10

SELECT 
	levenshtein('darkness', a.title) as distance_darkness_source,
	levenshtein(a.title, 'darkness') as distance_darkness_target,
	a.title AS title_1 
FROM product a
WHERE levenshtein('darkness', a.title) != 0
ORDER by distance_darkness_source, distance_darkness_target ASC


SELECT 
	levenshtein('darkness', a.title, 8,4,2) as distance_darkness_source,
	levenshtein(a.title, 'darkness', 8,4,2) as distance_darkness_target,
	a.title AS title_1 
FROM product a
WHERE levenshtein(a.title,'darkness', 8,4,2) != 0 and levenshtein('darkness', a.title, 8,4,2) != 0
ORDER by distance_darkness_source, distance_darkness_target ASC



--ex11

alter table review add column idx_review tsvector
generated always as (
    setweight(to_tsvector('se56303', coalesce(summary,'')), 'A') ||
    setweight(to_tsvector('se56303', coalesce(review_text,'')), 'B')
) stored;


CREATE INDEX ON review USING GIST (idx_review);


-- Index
EXPLAIN ANALYZE
SELECT * FROM review
WHERE idx_review @@ to_tsquery('darkness');

-- No index
EXPLAIN ANALYZE
SELECT * FROM review
WHERE review_text @@ to_tsquery('darkness');