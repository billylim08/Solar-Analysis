/* 
AIM: To analyse trends in Solar Capacity and Count by Region in the UK, NI, and GB (TOTAL)
DATA SOURCE: https://www.gov.uk/government/statistics/solar-photovoltaics-deployment    
*/

DROP TABLE IF EXISTS solar_capacity_by_region;

CREATE TABLE solar_capacity_by_region (
    region TEXT,
    date DATE,
    btw_0_and_4_kw NUMERIC,
    btw_4_and_10_kw NUMERIC,
    btw_10_and_50_kw NUMERIC,
    btw_50kw_and_5_mw NUMERIC,
    btw_5_and_25_mw NUMERIC,
    more_than_25_mw NUMERIC,
    total NUMERIC
);

COPY solar_capacity_by_region
FROM 'D:/Solar Energy Report/Data Analysis/Solar-Analysis/solar_capacity_gb.csv'
DELIMITER ','
CSV HEADER;

SELECT 
    date,
    -- btw_0_and_4_kw ,
    -- btw_4_and_10_kw ,
    -- btw_10_and_50_kw ,
    -- btw_50kw_and_5_mw ,
    -- btw_5_and_25_mw ,
    -- more_than_25_mw ,
    total 
FROM solar_capacity_by_region
WHERE date >= '2010-01-01';