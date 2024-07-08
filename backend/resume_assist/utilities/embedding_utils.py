from typing import List

import voyageai


def get_indexer_embedding(texts: List[str]) -> List[List]:
    vo_client = voyageai.Client()
    results = vo_client.embed(texts, model="voyage-2", input_type="query")
    return results.embeddings
