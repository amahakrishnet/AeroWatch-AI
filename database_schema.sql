-- 1. TABLES SETUP
CREATE OR REPLACE TABLE `air_quality_data.sensor_data` (
    station_id STRING,
    station_name STRING,
    city_name STRING,
    timestamp TIMESTAMP,
    pm25 FLOAT64,
    latitude FLOAT64,
    longitude FLOAT64
);

CREATE OR REPLACE TABLE `air_quality_data.imd_rainfall_forecast` (
    year INT64,
    forecast_percentage_of_lpa FLOAT64,
    category STRING
);

CREATE OR REPLACE TABLE `air_quality_data.citizen_reports` (
    report_id STRING,
    timestamp TIMESTAMP,
    latitude FLOAT64,
    longitude FLOAT64,
    neighborhood STRING,
    ai_pollution_category STRING,
    ai_severity_rating INT64,
    ai_summary_en STRING,
    status STRING
);

CREATE OR REPLACE TABLE `air_quality_data.india_census_data` (
    district_name STRING,
    population INT64
);

-- 2. REAL DATA INGESTION (IMD 2024)
INSERT INTO `air_quality_data.imd_rainfall_forecast` (year, forecast_percentage_of_lpa, category)
VALUES (2024, 122.0, 'Above Normal');

-- 3. THE ANALYTICAL VIEWS (The "Brain")
CREATE OR REPLACE VIEW `air_quality_data.v_neighborhood_hotspots` AS
WITH sensor_latest AS (
    SELECT city_name, station_name, pm25, latitude, longitude 
    FROM `air_quality_data.sensor_data`
    QUALIFY ROW_NUMBER() OVER(PARTITION BY station_name ORDER BY timestamp DESC) = 1
),
citizen_summary AS (
    SELECT neighborhood, AVG(ai_severity_rating) as avg_severity, COUNT(*) as report_count,
    ANY_VALUE(latitude) as lat, ANY_VALUE(longitude) as lon
    FROM `air_quality_data.citizen_reports` GROUP BY neighborhood
)
SELECT 
    s.city_name, COALESCE(c.neighborhood, s.station_name) as specific_location,
    s.pm25 as sensor_aqi, COALESCE(c.avg_severity, 0) as citizen_ai_severity,
    CASE 
        WHEN s.pm25 > 150 AND COALESCE(c.avg_severity, 0) > 7 THEN 'ACTION: DEPLOY WATER CANNON'
        WHEN s.pm25 > 150 THEN 'ACTION: SMOG ALERT'
        ELSE 'STABLE'
    END as municipal_action_plan,
    s.latitude, s.longitude, COALESCE(c.report_count, 0) as total_citizen_reports
FROM sensor_latest s
LEFT JOIN citizen_summary c ON s.city_name = c.neighborhood;

-- 4. AI PREDICTION MODEL (BigQuery ML)
CREATE OR REPLACE MODEL `air_quality_data.pm25_prediction_model`
OPTIONS(model_type='ARIMA_PLUS', time_series_timestamp_col='timestamp', time_series_data_col='pm25') AS
SELECT timestamp, pm25 FROM `air_quality_data.sensor_data`;