/* 
AIM: To analyse trends in the weekly fuel prices in the UK
ABBREVIATIONS INDEX:
ulsp_price - price of ultra low sulphur unleaded petrol pence per litre
ulsd_price - price of ultra low sulphur diesel pence per litre
ulsp_duty - duty on ultra low sulphur unleaded petrol pence per litre
ulsd_duty - duty on ultra low sulphur diesel pence per litre
ulsp_vat - VAT on ultra low sulphur unleaded petrol pence per litre
ulsd_vat - VAT on ultra low sulphur diesel pence per litre
    \
*/


DROP TABLE IF EXISTS fuel_prices;

CREATE TABLE fuel_prices (
    week_date DATE,
    ulsp_price NUMERIC,
    ulsd_price NUMERIC,
    ulsp_duty NUMERIC,
    ulsd_duty NUMERIC,
    ulsp_vat NUMERIC,
    ulsd_vat NUMERIC
);


COPY fuel_prices
FROM 'D:\Solar Energy Report\Data Analysis\Solar-Analysis\weekly_road_fuel_prices_200426.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

SELECT 
    week_date,
    ulsp_price,
    ulsd_price
    -- ulsp_duty AS duty,
    -- ulsp_vat AS vat,
    -- ulsp_price - (ulsp_duty + ulsp_vat) AS ulsp_raw_price,
    -- ulsd_price - (ulsd_duty + ulsd_vat) AS ulsd_raw_price
FROM fuel_prices
ORDER BY week_date;

