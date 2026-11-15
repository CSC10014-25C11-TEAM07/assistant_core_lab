# Lab 05 – H2: Additional SQL Question

**Member:** Hân

## 1. Question

How many assistant responses used a backup path (`degraded = 1`)?

## 2. SQL Query

```sql
SELECT COUNT(*) AS degraded_count
FROM interaction
WHERE degraded = 1;
```

## 3. Actual Result

**Degraded responses: 38**

Database: `assistant.db`

Dataset: 300 seeded interactions.

## 4. Explanation

The query counts assistant interactions that used a backup response path.

The `degraded` column indicates whether a fallback was used. The condition `degraded = 1` selects these interactions, and `COUNT(*)` returns their total.

Out of 300 seeded interactions, 38 used a backup response, representing approximately **12.67%** of all interactions.

This result helps evaluate how frequently the assistant relies on fallback responses.