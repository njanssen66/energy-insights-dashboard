-- name: total_energy_by_region
SELECT 
    region, 
    SUM(kWh) AS total_energy_kWh,
    ROUND(AVG(temperature_2m_max), 2) AS avg_temperature
FROM energy_usage
GROUP BY region
ORDER BY total_energy_kWh DESC;

-- name: avg_kwh_per_device
SELECT 
    region, 
    ROUND(SUM(kWh) * 1.0 / SUM(devices), 2) AS avg_kWh_per_device,
    ROUND(AVG(temperature_2m_max), 2) AS avg_temperature
FROM energy_usage
GROUP BY region
ORDER BY avg_kWh_per_device DESC;

-- name: top_5_usage_days
WITH ranked_usage AS (
    SELECT 
        region, 
        date, 
        kWh,
        temperature_2m_max,
        ROW_NUMBER() OVER (PARTITION BY region ORDER BY kWh DESC) AS rank
    FROM energy_usage
)
SELECT 
    region, 
    date, 
    kWh,
    temperature_2m_max
FROM ranked_usage
WHERE rank <= 5
ORDER BY region, kWh DESC;

-- name: energy_growth_by_region
WITH first_last AS (
    SELECT 
        region, 
        MIN(date) AS start_date, 
        MAX(date) AS end_date
    FROM energy_usage
    GROUP BY region
),
start_vals AS (
    SELECT 
        fl.region, 
        eu.kWh AS start_kWh,
        eu.temperature_2m_max AS start_temperature
    FROM energy_usage eu
    JOIN first_last fl ON eu.region = fl.region AND eu.date = fl.start_date
),
end_vals AS (
    SELECT 
        fl.region, 
        eu.kWh AS end_kWh,
        eu.temperature_2m_max AS end_temperature
    FROM energy_usage eu
    JOIN first_last fl ON eu.region = fl.region AND eu.date = fl.end_date
)
SELECT 
    s.region, 
    s.start_kWh, 
    e.end_kWh,
    ROUND((e.end_kWh - s.start_kWh) * 100.0 / s.start_kWh, 2) AS percent_growth,
    s.start_temperature,
    e.end_temperature
FROM start_vals s
JOIN end_vals e ON s.region = e.region
ORDER BY percent_growth DESC;

-- name: kwh_temperature_correlation
SELECT 
    region,
    ROUND(
        (
            AVG(kWh * temperature_2m_max) - 
            AVG(kWh) * AVG(temperature_2m_max)
        ) / (
            SQRT(
                AVG(kWh * kWh) - POWER(AVG(kWh), 2)
            ) * 
            SQRT(
                AVG(temperature_2m_max * temperature_2m_max) - 
                POWER(AVG(temperature_2m_max), 2)
            )
        ), 3
    ) AS kwh_temperature_correlation
FROM energy_usage
GROUP BY region
HAVING 
    SQRT(AVG(kWh * kWh) - POWER(AVG(kWh), 2)) > 0 AND 
    SQRT(AVG(temperature_2m_max * temperature_2m_max) - POWER(AVG(temperature_2m_max), 2)) > 0
ORDER BY kwh_temperature_correlation DESC;