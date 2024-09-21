TODO:
1. Prompt Studio (with good UI) for personalized prompts: https://github.com/anthropics/prompt-eng-interactive-tutorial/blob/master/Anthropic%201P/09_Complex_Prompts_from_Scratch.ipynb
2. Agent-based architecture
    ReviewerAgent
    KeywordExtractorAgent
    RetrievalAgent
        - configurable voyage ai embedding
        - advanced retrieval setting: https://neo4j.com/developer-blog/advanced-rag-strategies-neo4j/?utm_source=Google&utm_medium=PaidSearch&utm_campaign=Evergreen&utm_content=AMS-Search-SEMCE-DSA-None-SEM-SEM-NonABM&utm_term=&utm_adgroup=DSA&gad_source=1&gclid=Cj0KCQjw1qO0BhDwARIsANfnkv9m8jLeuv0b2Ny0PEFPZQLvg3Hkr6uRrCz5zKDgyhj91Jeq7QjaZLQaAtfXEALw_wcB
    FormatterAgent
    RendererAgent -> if two pages rendered -> give error -> suggest sections to remove
3. Langfuse integration
4. Setup cheaper inference engine
5. testing
6. Guardrail
7. Prompt Optimization: 
8. Caching -> cost saving



Steps:
- Enable modification-based graph relationship (section modified from xxx)

TODO:
- Fix $id matching bug --> should be by $resumeId + $itemId