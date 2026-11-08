-- Lab 5 Part F: write your queries for the assistant database here.
-- Q1 requests per intent
SELECT intent, COUNT(*) AS requests
FROM interaction
GROUP BY intent
ORDER BY requests DESC, intent;

-- Q2 average latency per intent
SELECT intent, ROUND(AVG(latency_ms), 1) AS avg_latency_ms
FROM interaction
GROUP BY intent
ORDER BY avg_latency_ms DESC, intent;

-- Q3 topics with the most thumbs-down (JOIN feedback with interaction)
-- Exclude NULL topics: those interactions are not associated with a handbook topic.
SELECT i.topic, COUNT(*) AS thumbs_down
FROM interaction i
JOIN feedback f ON f.request_id = i.request_id
WHERE f.rating = -1 AND i.topic IS NOT NULL
GROUP BY i.topic
ORDER BY thumbs_down DESC, i.topic;

-- H2: What percentage of answers used a backup path?
-- All interactions form the denominator; COALESCE gives 0% for an empty database.
SELECT COUNT(*) AS total_answers,
       COALESCE(SUM(CASE WHEN degraded = 1 THEN 1 ELSE 0 END), 0) AS backup_answers,
       ROUND(COALESCE(100.0 * SUM(CASE WHEN degraded = 1 THEN 1 ELSE 0 END)
                      / NULLIF(COUNT(*), 0), 0.0), 2) AS backup_percent
FROM interaction;
