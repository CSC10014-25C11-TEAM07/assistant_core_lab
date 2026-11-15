# Lab 5 — Data model worksheet

## 1. Critique the bad schema (sql/bad_schema.sql)
| # | Problem | Why it hurts | Fix |
|---|---|---|---|
| 1 | `id` has no primary-key or uniqueness constraint. | Duplicate or NULL IDs make it impossible to identify a record reliably. | Give every entity a primary key; make `interaction.request_id` unique. |
| 2 | Real names, phone numbers and full messages are stored indefinitely. | They can expose personal details even though the analytics features do not need them. | Omit these fields; store a salted session hash and minimal interaction metadata. |
| 3 | `feedback` stores a comma-separated list. | Individual ratings cannot be reliably validated, joined, timestamped or counted. | Put each rating in a separate `feedback` row, linked to `interaction.request_id`. |
| 4 | `latency` is text such as `120ms`; `time` uses an ambiguous local format. | Numerical averages and chronological sorting become unreliable. | Use numeric `latency_ms` and consistently generated UTC `created_at` timestamps. |
| 5 | Sessions, interactions and feedback are mixed together without foreign keys. | Data is duplicated and feedback can reference no identifiable answer. | Separate `chat_session`, `interaction` and `feedback`; declare their foreign keys and check interaction existence before saving feedback. SQLite foreign-key enforcement must be enabled per connection if relying on database enforcement. |
| 6 | `intent` is uncontrolled free text. | `fee`, `Fee` and `tuition` split one category into misleading groups. | The supplied application derives intent from its router enum. For stronger database protection, add a CHECK constraint or an intent reference table in a future migration; the current schema has neither. |

Additional observations: the bad schema lacks outcome flags (`resolved`, `degraded`), useful topic IDs, and indexes. The supplied design stores these metadata fields and indexes intent, session, creation time and feedback request IDs. Migration 001 constrains ratings to -1/0/1; the API also validates ratings. Tables created directly by SQLModel currently rely on API validation for ratings.

## 2. Store or not? (privacy-aware storage)
| Data | Store? | Form (raw / hashed / aggregated / none) | Retention | Reason |
|---|---|---|---|---|
| raw user message | No | none | Do not persist | May contain personal information; not required for the lab's analytics. |
| session id | Yes, indirectly | salted SHA-256 hash, truncated to 16 hexadecimal characters by the supplied implementation | Proposed: 30 days, then delete session-linked records or retain only aggregate counts | Counts sessions without keeping the original ID; keep the salt secret. Hashes are pseudonymous identifiers and can still link activity. |
| intent, latency, topic | Yes | raw metadata; aggregates for longer-term trends | Proposed: 30 days per interaction, then keep monthly aggregates for 1 year | Supports performance, resolution and topic analysis without raw questions. |
| feedback rating | Yes | one numeric value per feedback row | Proposed: 30 days linked to a request, then aggregate | Measures satisfaction and identifies problematic topics. |
| feedback comment | Optional | raw, at most 500 characters; advise users to omit personal information | Proposed: 30 days, then delete | Can explain a rating, but may itself contain personal details. The starter does not redact comments. |
| student name / phone | No | none | Do not persist | None of the lab features needs these identifiers. |

These retention periods are design proposals, not implemented deletion jobs or requirements stated by the tutorial. When implementing cleanup, remove dependent feedback and interactions before their session records.

## 3. Product questions → fields
| Product question | Fields needed | Table(s) | Query sketch |
|---|---|---|---|
| Most failed intent? | `intent`, `resolved` | `interaction` | `SELECT intent, COUNT(*) AS failures FROM interaction WHERE resolved = 0 GROUP BY intent ORDER BY failures DESC, intent;` |
| Average response time by intent? | `intent`, `latency_ms` | `interaction` | `SELECT intent, ROUND(AVG(latency_ms), 1) AS avg_latency_ms FROM interaction GROUP BY intent ORDER BY avg_latency_ms DESC, intent;` |
| Top unresolved topics? | `topic`, `resolved` | `interaction` | `SELECT topic, COUNT(*) AS unresolved FROM interaction WHERE resolved = 0 AND topic IS NOT NULL GROUP BY topic ORDER BY unresolved DESC, topic;` |

The seed script marks only `unknown` interactions unresolved, and these have NULL topics, so the last query can correctly return no rows on the supplied seed data. Failures can also be compared as percentages when intent volumes differ.

## 4. ER diagram
Completed Mermaid diagram: [../starter/docs/data-model.md](../starter/docs/data-model.md).
