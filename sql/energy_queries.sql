-- name: total_energy_by_region
SELECT region, SUM(kWh) AS total_energy_kWh
FROM energy_usage
GROUP BY region
ORDER BY total_energy_kWh DESC;

-- name: avg_kwh_per_device
SELECT region, ROUND(SUM(kWh) * 1.0 / SUM(devices), 2) AS avg_kWh_per_device
FROM energy_usage
GROUP BY region
ORDER BY avg_kWh_per_device DESC;

-- name: top_5_usage_days
WITH ranked_usage AS (
  SELECT 
    region, 
    date, 
    kWh,
    ROW_NUMBER() OVER (PARTITION BY region ORDER BY kWh DESC) AS rank
  FROM energy_usage
)
SELECT region, date, kWh
FROM ranked_usage
WHERE rank <= 5;

-- name: energy_growth_by_region
WITH first_last AS (
    SELECT region, MIN(date) AS start_date, MAX(date) AS end_date
    FROM energy_usage
    GROUP BY region
),
start_vals AS (
    SELECT fl.region, eu.kWh AS start_kWh
    FROM energy_usage eu
    JOIN first_last fl ON eu.region = fl.region AND eu.date = fl.start_date
),
end_vals AS (
    SELECT fl.region, eu.kWh AS end_kWh
    FROM energy_usage eu
    JOIN first_last fl ON eu.region = fl.region AND eu.date = fl.end_date
)
SELECT s.region, s.start_kWh, e.end_kWh,
       ROUND((e.end_kWh - s.start_kWh) * 100.0 / s.start_kWh, 2) AS percent_growth
FROM start_vals s
JOIN end_vals e ON s.region = e.region
ORDER BY percent_growth DESC;
