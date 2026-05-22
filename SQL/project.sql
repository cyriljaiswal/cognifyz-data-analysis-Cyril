CREATE DATABASE restaurant_db;

CREATE TABLE restaurant (
    restaurant_id INT PRIMARY KEY,
    restaurant_name VARCHAR(100),
    country_code INT,
    city VARCHAR(50),
    address VARCHAR(200),
    locality VARCHAR(100),
    locality_verbose VARCHAR(150),
    longitude FLOAT,
    latitude FLOAT,
    cuisines VARCHAR(200),
    average_cost_for_two INT,
    currency VARCHAR(50),
    has_table_booking BOOLEAN,
    has_online_delivery BOOLEAN,
    is_delivering_now BOOLEAN,
    switch_to_order_menu BOOLEAN,
    price_range INT,
    aggregate_rating FLOAT,
    rating_color VARCHAR(20),
    rating_text VARCHAR(20),
    votes INT
);

SELECT * FROM restaurant;


-- fix boolean 

ALTER TABLE restaurant
ALTER COLUMN has_table_booking TYPE BOOLEAN USING (has_table_booking = 'Yes'),
ALTER COLUMN has_online_delivery TYPE BOOLEAN USING (has_online_delivery = 'Yes'),
ALTER COLUMN is_delivering_now TYPE BOOLEAN USING (is_delivering_now = 'Yes'),
ALTER COLUMN switch_to_order_menu TYPE BOOLEAN USING (switch_to_order_menu = 'Yes');




-- LEVEL 1 TASKS/QUESTIONS 


--  L1 Task 1: Top Cuisines
--  Splits multi-cuisine strings and counts each cuisine

CREATE OR REPLACE VIEW v_l1_top_cuisines AS
WITH split_cuisines AS (
    SELECT
        TRIM(unnest(string_to_array(cuisines, ','))) AS cuisine
    FROM restaurant
    WHERE cuisines IS NOT NULL
),
cuisine_counts AS (
    SELECT
        cuisine,
        COUNT(*) AS restaurant_count
    FROM split_cuisines
    GROUP BY cuisine
),
total AS (
    SELECT SUM(restaurant_count) AS grand_total FROM cuisine_counts
)
SELECT
    c.cuisine,   
    c.restaurant_count,
    ROUND((c.restaurant_count * 100.0) / t.grand_total, 2) AS percentage
FROM cuisine_counts c, total t
ORDER BY restaurant_count DESC;



--  L1 Task 2: City Analysis
--  Restaurant count per city + avg rating per city

CREATE OR REPLACE VIEW v_l1_city_analysis AS
SELECT
    city,
    COUNT(*)                              AS restaurant_count,
    ROUND(AVG(aggregate_rating)::NUMERIC, 2) AS avg_rating
FROM restaurant
GROUP BY city
ORDER BY restaurant_count DESC;



--  L1 Task 3: Price Range Distribution

CREATE OR REPLACE VIEW v_l1_price_range AS
WITH counts AS (
    SELECT
        price_range,
        COUNT(*) AS restaurant_count
    FROM restaurant
    GROUP BY price_range
),
total AS (SELECT SUM(restaurant_count) AS grand_total FROM counts)
SELECT
    c.price_range,
    CASE c.price_range
        WHEN 1 THEN 'Budget'
        WHEN 2 THEN 'Affordable'
        WHEN 3 THEN 'Mid-range'
        WHEN 4 THEN 'Premium'
    END AS price_label,
    c.restaurant_count,
    ROUND((c.restaurant_count * 100.0) / t.grand_total, 2) AS percentage
FROM counts c, total t
ORDER BY price_range;



--  L1 Task 4: Online Delivery
--  % of restaurants offering delivery + avg rating comparison

CREATE OR REPLACE VIEW v_l1_online_delivery AS
WITH counts AS (
    SELECT
        has_online_delivery,
        COUNT(*)                                 AS restaurant_count,
        ROUND(AVG(aggregate_rating)::NUMERIC, 2) AS avg_rating
    FROM restaurant
    GROUP BY has_online_delivery
),
total AS (SELECT SUM(restaurant_count) AS grand_total FROM counts)
SELECT
    CASE c.has_online_delivery WHEN TRUE THEN 'With Delivery' ELSE 'Without Delivery' END AS delivery_status,
    c.restaurant_count,
    ROUND((c.restaurant_count * 100.0) / t.grand_total, 2) AS percentage,
    c.avg_rating
FROM counts c, total t
ORDER BY has_online_delivery DESC;



-- LEVEL 2 TASKS/QUESTIONS 


--  L2 Task 1: Restaurant Ratings
--  Rating distribution + average votes

CREATE OR REPLACE VIEW v_l2_rating_distribution AS
SELECT
    CASE
        WHEN aggregate_rating = 0          THEN 'Not Rated'
        WHEN aggregate_rating < 2.0        THEN '0-2 (Poor)'
        WHEN aggregate_rating < 3.0        THEN '2-3 (Average)'
        WHEN aggregate_rating < 3.5        THEN '3-3.5 (Good)'
        WHEN aggregate_rating < 4.0        THEN '3.5-4 (Very Good)'
        WHEN aggregate_rating < 4.5        THEN '4-4.5 (Excellent)'
        ELSE                                    '4.5-5 (Outstanding)'
    END AS rating_range,
    COUNT(*)                                 AS restaurant_count,
    ROUND(AVG(votes)::NUMERIC, 0)            AS avg_votes
FROM restaurant
GROUP BY rating_range
ORDER BY MIN(aggregate_rating);

-- Separate view: just the average votes number
CREATE OR REPLACE VIEW v_l2_avg_votes AS
SELECT ROUND(AVG(votes)::NUMERIC, 0) AS avg_votes_overall
FROM restaurant;


--  L2 Task 2: Cuisine Combinations
--  Most common cuisine combos + their avg rating

CREATE OR REPLACE VIEW v_l2_cuisine_combinations AS
SELECT
    cuisines                                 AS cuisine_combination,
    COUNT(*)                                 AS restaurant_count,
    ROUND(AVG(aggregate_rating)::NUMERIC, 2) AS avg_rating
FROM restaurant
WHERE cuisines IS NOT NULL
  AND cuisines LIKE '%,%'
GROUP BY cuisines
ORDER BY restaurant_count DESC;



--  L2 Task 3: Geographic Analysis
--  Lat/Long + rating for map visual

CREATE OR REPLACE VIEW v_l2_geographic AS
SELECT
    restaurant_id,
    restaurant_name,
    city,
    latitude,
    longitude,
    aggregate_rating,
    rating_color,
    votes
FROM restaurant
WHERE latitude IS NOT NULL
  AND longitude IS NOT NULL
  AND latitude  <> 0
  AND longitude <> 0;



--  L2 Task 4: Restaurant Chains
--  Restaurants with same name appearing 2+ times = chain

CREATE OR REPLACE VIEW v_l2_restaurant_chains AS
SELECT
    restaurant_name,
    COUNT(*)                                 AS outlet_count,
    ROUND(AVG(aggregate_rating)::NUMERIC, 2) AS avg_rating,
    SUM(votes)                               AS total_votes
FROM restaurant
GROUP BY restaurant_name
HAVING COUNT(*) >= 2
ORDER BY outlet_count DESC;



-- LEVEL 3 TASKS/QUESTIONS 


--  L3 Task 1: Votes Analysis
--  Highest/lowest votes + correlation with rating

CREATE OR REPLACE VIEW v_l3_votes_analysis AS
SELECT
    restaurant_id,
    restaurant_name,
    votes,
    aggregate_rating,
    city
FROM restaurant
ORDER BY votes DESC;

-- Top 10 most voted
CREATE OR REPLACE VIEW v_l3_top10_votes AS
SELECT restaurant_name, votes, aggregate_rating, city
FROM restaurant
ORDER BY votes DESC;

-- Bottom 10 least voted
CREATE OR REPLACE VIEW v_l3_bottom10_votes AS
SELECT restaurant_name, votes, aggregate_rating, city
FROM restaurant
WHERE votes > 0
ORDER BY votes ASC;


--  L3 Task 2: Price Range vs Online Delivery & Table

CREATE OR REPLACE VIEW v_l3_price_vs_services AS
SELECT
    price_range,
    CASE price_range
        WHEN 1 THEN 'Budget'
        WHEN 2 THEN 'Affordable'
        WHEN 3 THEN 'Mid-range'
        WHEN 4 THEN 'Premium'
    END AS price_label,
    COUNT(*)                                                          AS total_restaurants,
    SUM(CASE WHEN has_online_delivery  THEN 1 ELSE 0 END)            AS with_online_delivery,
    SUM(CASE WHEN has_table_booking    THEN 1 ELSE 0 END)            AS with_table_booking,
    ROUND(AVG(CASE WHEN has_online_delivery THEN 1.0 ELSE 0 END) * 100, 1) AS delivery_pct,
    ROUND(AVG(CASE WHEN has_table_booking   THEN 1.0 ELSE 0 END) * 100, 1) AS booking_pct
FROM restaurant
GROUP BY price_range
ORDER BY price_range;



-- Run these to confirm all views are created

SELECT * FROM v_l1_top_cuisines LIMIT 5;
SELECT * FROM v_l1_city_analysis LIMIT 5;
SELECT * FROM v_l1_price_range lIMIT 5;
SELECT * FROM v_l1_online_delivery LIMIT 5;
SELECT * FROM v_l2_rating_distribution LIMIT 5;
SELECT * FROM v_l2_avg_votes;
SELECT * FROM v_l2_cuisine_combinations LIMIT 5;
SELECT * FROM v_l2_geographic LIMIT 5;
SELECT * FROM v_l2_restaurant_chains LIMIT 5;
SELECT * FROM v_l3_votes_analysis LIMIT 5;
SELECT * FROM v_l3_top10_votes LIMIT 10;
SELECT * FROM v_l3_bottom10_votes LIMIT 10;
SELECT * FROM v_l3_price_vs_services;