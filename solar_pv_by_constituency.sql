---------------- DOMESTIC CONSTITUENCY ----------------
DROP TABLE IF EXISTS solar_domestic_by_constituency;

CREATE TABLE solar_domestic_by_constituency (
    constituency_code TEXT PRIMARY KEY,
    constituency_name TEXT,
    country TEXT,
    country_region TEXT,
    installed_capacity_mw NUMERIC,
    number_of_installations BIGINT
);

COPY solar_domestic_by_constituency
FROM 'D:/Solar Energy Report/Data Analysis/Solar-Analysis/solar_domestic_by_constituency.csv'
DELIMITER ','
CSV HEADER;


-- Quick sanity check after load
SELECT country, COUNT(*) AS n_constituencies,
       ROUND(SUM(installed_capacity_mw), 1) AS total_mw,
       SUM(number_of_installations) AS total_installs
FROM solar_domestic_by_constituency
GROUP BY country
ORDER BY total_mw DESC;


-- Heat-map-ready view
CREATE OR REPLACE VIEW solar_domestic_constituency_map AS
SELECT 
    constituency_code,
    constituency_name,
    country,
    country_region,
    installed_capacity_mw,
    number_of_installations,

    -- Average domestic system size (kW)
    ROUND(
        ((installed_capacity_mw * 1000.0) / NULLIF(number_of_installations, 0))::numeric,
        2
    ) AS avg_system_kw,

    -- Share of UK total (%)
    ROUND(
        (100.0 * installed_capacity_mw 
             / SUM(installed_capacity_mw) OVER ())::numeric,
        3
    ) AS uk_capacity_share_pct,

    -- National ranks (1 = highest)
    RANK() OVER (ORDER BY installed_capacity_mw DESC)   AS rank_capacity_uk,
    RANK() OVER (ORDER BY number_of_installations DESC) AS rank_count_uk,

    -- Country-level ranks
    RANK() OVER (PARTITION BY country ORDER BY installed_capacity_mw DESC) 
        AS rank_capacity_within_country,

    -- Percentile across the UK (0–100)  -- this one needed the cast
    ROUND(
        (100.0 * PERCENT_RANK() OVER (ORDER BY installed_capacity_mw))::numeric, 
        1
    ) AS pct_capacity_uk

FROM solar_domestic_by_constituency
ORDER BY installed_capacity_mw DESC;