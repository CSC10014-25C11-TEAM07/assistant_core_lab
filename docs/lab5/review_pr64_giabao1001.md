# PR #64 review - Bao04

Reviewed PR: [H1 and R2 by lkpnhat](https://github.com/CSC10014-25C11-TEAM07/assistant_core_lab/pull/64).
Author: `lkpnhat2514-glitch`; branch: `60-pyw4---phucnhat445`.
Reviewer: `giabao1001` (Bao04). Date: 2026-11-07.

Reviewed head: `6c1afec3acdc0b34e8e3d47d2ece32ba84ca3124`.
Base: `724c228f90436fba3fc4c03bf5900458d878ca50`, which already includes R1 from PR #49.

**Outcome: REQUEST_CHANGES**, submitted on the reviewed commit. [Submitted review](https://github.com/CSC10014-25C11-TEAM07/assistant_core_lab/pull/64#pullrequestreview-5812487742).

## Finding

**[P2] Q12 must order tied enrollment counts by course title.**

Location: [`lab05/practice/my_answers.sql:36`](https://github.com/CSC10014-25C11-TEAM07/assistant_core_lab/blob/6c1afec3acdc0b34e8e3d47d2ece32ba84ca3124/lab05/practice/my_answers.sql#L36).

Q12 requires descending enrollment counts, followed by ascending course title. The current query only sorts by the count. It passes the original fixture but can violate the title order when counts are equal.

Reproduction: load the original `school.sql` into an in-memory database, add course `('AAA10000', 'A first course', 3)`, and enroll students 1 through 5. Both this course and `Computational Thinking` have five enrollments. The current query returns `Computational Thinking` first; the required order places `A first course` first. See [reproduction evidence](evidence/pr64-6c1afec-q12-tie.txt).

Suggested correction:

```sql
ORDER BY COUNT(course_code) DESC, c.title ASC;
```

No blocking finding was identified in the R2 implementation itself: it selects feedback, sorts by `created_at DESC`, and applies the supplied limit correctly.

## Verification

All commands ran against an isolated archive of the exact reviewed commit; the author's branch was not modified.

| Check | Result | Evidence |
| --- | --- | --- |
| `python make_school_db.py` | Original fixture created | [Log](evidence/pr64-6c1afec-make-school-db.txt) |
| `python check.py` | **Score: 15/15** | [H1 log](evidence/pr64-6c1afec-h1.txt) |
| Original Assistant `python -m pytest -q` | **27 passed** | [Official suite](evidence/pr64-6c1afec-starter-official.txt) |
| Assistant plus Bao04's 19 independent feedback tests | **46 passed** | [Extended suite](evidence/pr64-6c1afec-starter-with-qa.txt) |
| Q12 title tie reproduction | **Ordering requirement violated** | [Synthetic case](evidence/pr64-6c1afec-q12-tie.txt) |

The extended suite covers valid/missing/incorrect API keys, empty feedback, timestamp ordering independent of insertion IDs, limits 0/1/2/100, feedback validation, database reads from a fresh Python process, and recreating the application/engine using the same SQLite file. This review did not run a real HTTP/Uvicorn restart cycle. The existing Starlette/AnyIO deprecation warning does not fail the suite.

## Integration note

The combined PR contains both H1 and R2. Under the team assignment, each member submits H1 separately and the Tech Lead selects only one H1 to merge. The submitted review asks the author to separate H1 from the R2 integration PR or coordinate the H1 selection with the Tech Lead before merging.

Re-review the updated commit after the Q12 fix. No PR was merged during this review.
