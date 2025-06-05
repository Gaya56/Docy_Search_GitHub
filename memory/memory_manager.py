"""
Memory manager for handling embeddings and similarity search.
Wraps SQLiteMemory with AI-powered memory operations.
"""

import json
import numpy as np
import os
from typing import List, Dict, Optional, Any
from datetime import datetime
from .sqlite_memory import SQLiteMemory


class MemoryManager:
    """Manages memory operations with embedding support."""
    
    def __init__(self, db_path: str = "data/memories.db", model=None):
        """Initialize memory manager.
        
        Args:
            db_path: Path to SQLite database
            model: AI model instance (used for future extensions)
        """
        self.db = SQLiteMemory(db_path)
        self.model = model
        self.embedding_cache = {}
        
        # Check embedding availability
        if os.getenv("OPENAI_API_KEY"):
            print("✅ Embeddings enabled (OpenAI)")
        else:
            print("ℹ️ Embeddings disabled (no OpenAI API key)")
    
    def save_memory(self,
                    user_id: str,
                    content: str,
                    metadata: Optional[Dict[str, Any]] = None,
                    category: str = "tool_recommendation") -> int:
        """Save memory with generated embedding.
        
        Args:
            user_id: User identifier
            content: Memory content
            metadata: Optional metadata
            category: Memory category
            
        Returns:
            Memory ID
        """
        # Generate embedding if available
        embedding = self._generate_embedding(content)
        
        # Add timestamp to metadata
        if metadata is None:
            metadata = {}
        metadata['created_at'] = datetime.now().isoformat()
        
        return self.db.save_memory(
            user_id=user_id,
            content=content,
            embedding=embedding,
            metadata=metadata,
            category=category
        )
    
    def _generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding using OpenAI API when available."""
        # Check for OpenAI API key
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            return None
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=text[:8000]  # Limit text length
            )
            return response.data[0].embedding
        except Exception:
            # Silently fail - embeddings are optional
            return None
    
    def retrieve_memories(self, 
                         user_id: str,
                         query: Optional[str] = None,
                         limit: int = 5,
                         category: Optional[str] = None) -> str:
        """Retrieve formatted memories for a user.
        
        Args:
            user_id: User identifier
            query: Optional query for similarity search
            limit: Maximum memories to return
            category: Optional category filter
            
        Returns:
            Formatted string of relevant memories
        """
        memories = self.db.get_memories(user_id, limit=limit, category=category)
        
        if not memories:
            return "No previous interactions found."
        
        # Format memories for context
        formatted = []
        for mem in memories:
            timestamp = mem.get('timestamp', 'Unknown time')
            content = mem.get('content', '')
            formatted.append(f"[{timestamp}] {content}")
        
        return "\n".join(formatted)
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between embeddings."""
        if not embedding1 or not embedding2:
            return 0.0
        
        # Convert to numpy arrays
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        # Cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def find_similar_memories(self,
                             user_id: str,
                             query_embedding: List[float],
                             threshold: float = 0.7,
                             limit: int = 5) -> List[Dict[str, Any]]:
        """Find memories similar to query embedding.
        
        Args:
            user_id: User identifier
            query_embedding: Query embedding vector
            threshold: Similarity threshold
            limit: Maximum results
            
        Returns:
            List of similar memories with similarity scores
        """
        all_memories = self.db.get_memories(user_id, limit=100)
        
        # Calculate similarities
        scored_memories = []
        for memory in all_memories:
            if memory.get('embedding'):
                similarity = self.calculate_similarity(query_embedding, memory['embedding'])
                if similarity >= threshold:
                    memory['similarity_score'] = similarity
                    scored_memories.append(memory)
        
        # Sort by similarity and return top results
        scored_memories.sort(key=lambda x: x['similarity_score'], reverse=True)
        return scored_memories[:limit]
    
    def clear_user_memories(self, user_id: str) -> int:
        """Clear all memories for a user."""
        return self.db.clear_user_memories(user_id)
