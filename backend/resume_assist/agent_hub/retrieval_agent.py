import logging
from typing import Dict, List, Tuple, Any

from resume_assist.agent_hub.base import Agent
from resume_assist.io.db.engine import neo4j_client
from resume_assist.utilities.embedding_utils import get_indexer_embedding

logger = logging.getLogger(__name__)


class RetrievalAgent(Agent):
    def retrieve(
        self,
        indexer_txt: str,
        node_type: str,
        max_chunk_size: int = 5,
        refined_filter: bool = True,
    ) -> List[str] | str:
        """job-summary based retreival"""
        chunks = self.step(indexer_txt, node_type)
        reranked_chunks = self.rerank(chunks)
        filtered_chunks = self.crude_filtering(reranked_chunks, max_chunk_size)
        if refined_filter:
            filtered_chunks = self.refined_filtering(filtered_chunks)
        return [chunk[0] for chunk in filtered_chunks]

    def step(self, indexer_str: str, node_type: str) -> List:
        indexer_embedding = get_indexer_embedding([indexer_str])[0]
        query = f"""
        MATCH (s:{node_type})
        WITH s, gds.similarity.cosine(s.embedding, $embedding) AS score
        RETURN s, score
        ORDER BY score DESC
        LIMIT 100
        """
        results = neo4j_client.query(query, {"embedding": indexer_embedding})
        return list(
            zip(
                [record["s"] for record in results],
                [record["score"] for record in results],
            )
        )

    def rerank(self, chunks: List) -> List:
        # TODO: add voyage's reranker -> update the query given the indexer_str as main source
        return chunks

    def crude_filtering(self, chunks: List, max_chunk_size: int) -> List:
        return chunks[:max_chunk_size]

    def refined_filtering(self, chunks: List) -> List:
        final_chunks = []
        for chunk, _ in chunks:
            label = chunk.get("label") or "unlabeled"
            if label == "success":
                final_chunks.append(chunk)
        return final_chunks

    def get_agent_name(self):
        return "retriever"
