
Path | Correct | Abstain OK |P50 ms	| Max ms | 	Failed Cases
deterministic |	7/20 | 5/5	| 0.0 |	0.5 | E01 E02 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14 E15
retrieval |	16/20 |	4/5 | 0.0 |	0.1 | E13 E14 E15 E19
llm (stub) | 16/20 | 4/5 | 0.1 | 0.4 |E13 E14 E15 E19


**Three Sentences** 
1. For handbook questions, I would use the llm (RAG) path with the retrieval path as an automatic fallback when the model fails validation.
2. Unlike the deterministic path (which only answers fee and office questions and scores 7/20), the llm path answers 16/20 questions accurately from official document chunks while phrasing responses naturally and enforcing citation checks.
3. I would fix failure E14 ("can I take 32 credits") first by updating `tokenize` in `src/assistant_core/rag/index.py` to strip trailing `"s"` from plural words longer than four letters so `"credits"` matches `"credit"`.