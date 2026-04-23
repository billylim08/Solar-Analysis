/* 
AIM: To analyse trends in EV Charger installations in the UK.
*/

DROP TABLE IF EXISTS ev_chargers;

CREATE TABLE ev_chargers (
    week_date DATE,
    notes TEXT,
    region_code TEXT,
    region TEXT,
    metric TEXT,
    number_of_chargers NUMERIC
);

COPY ev_chargers
FROM 'D:\Solar Energy Report\Data Analysis\Solar-Analysis\uk_ev_chargers_clean.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

SELECT 
    week_date,
    number_of_chargers
FROM 
    ev_chargers
WHERE
    region = 'Northern Ireland'
        AND
    metric = 'EV chargers';
