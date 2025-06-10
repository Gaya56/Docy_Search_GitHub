"""
Optimized memory manager with embeddings and activity tracking.
Consolidated sync/async operations with shared functionality.
"""

import json
import numpy as np
import os
import asyncio
from typing import List, Dict, Optional, Any, Union
from datetime import datetime
from .sqlite_memory import SQLiteMemory, AsyncSQLiteMemory

# Import modules with graceful fallback
try:
    import sys
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir) if parent_dir not in sys.path else None
    from docy_search.activity_tracker import activity_tracker
    from docy_search.memory.cost_tracker import CostTracker
    TRACKING_AVAILABLE = True
except ImportError:
    activity_tracker, CostTracker, TRACKING_AVAILABLE = None, None, False

try:
    from openai import OpenAI, AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OpenAI, AsyncOpenAI, OPENAI_AVAILABLE = None, None, False


class EmbeddingMixin:
    """Shared embedding functionality for sync and async operations."""
    
    def __init__(self):
        self.embedding_cache = {}
        self.openai_client = None
        self.cost_tracker = None
        
        # Initialize OpenAI client if available
        if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            client_class = AsyncOpenAI if hasattr(self, '_async') else OpenAI
            self.openai_client = client_class(api_key=os.getenv("OPENAI_API_KEY"))
            
        # Initialize cost tracker if available
        if TRACKING_AVAILABLE and CostTracker:
            self.cost_tracker = CostTracker()
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between embeddings."""
        if not embedding1 or not embedding2:
            return 0.0
        
        vec1, vec2 = np.array(embedding1), np.array(embedding2)
        dot_product = np.dot(vec1, vec2)
        norm1, norm2 = np.linalg.norm(vec1), np.linalg.norm(vec2)
        
        return dot_product / (norm1 * norm2) if norm1 and norm2 else 0.0
    
    def _format_memories(self, memories: List[Dict]) -> str:
        """Format memories for display."""
        if not memories:
            return "No previous interactions found."
        
        formatted = []
        for mem in memories:
            timestamp = mem.get('timestamp', 'Unknown time')
            content = mem.get('content', '')
            formatted.append(f"[{timestamp}] {content}")
        
        return "\n".join(formatted)


class MemoryManager(EmbeddingMixin):
    """Synchronous memory manager with embedding support."""
    
    def __init__(self, db_path: str = "data/memories.db", model=None):
        super().__init__()
        self.db = SQLiteMemory(db_path)
        self.model = model
        self.async_manager = AsyncMemoryManager(db_path, model)
        
        status = "✅ Embeddings enabled" if self.openai_client else "ℹ️ Embeddings disabled"
        print(f"{status} (OpenAI)")
    
    def save_memory_async(self, **kwargs) -> int:
        """Save memory asynchronously (fire-and-forget for UI responsiveness)."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(self.async_manager.save_memory(**kwargs))
                return 0  # Return dummy ID immediately
            else:
                return asyncio.run(self.async_manager.save_memory(**kwargs))
        except RuntimeError:
            return self.save_memory(**kwargs)
    
    def save_memory(self, user_id: str, content: str, metadata: Optional[Dict[str, Any]] = None, 
                   category: str = "tool_recommendation") -> int:
        """Save memory with generated embedding."""
        embedding = self._generate_embedding(content) if self.openai_client else None
        
        if metadata is None:
            metadata = {}
        metadata['created_at'] = datetime.now().isoformat()
        
        return self.db.save_memory(
            user_id=user_id, content=content, embedding=embedding, 
            metadata=metadata, category=category
        )
    
    def _generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding using OpenAI API."""
        if not self.openai_client:
            return None
        
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=text[:8000]
            )
            return response.data[0].embedding
        except Exception:
            return None  # Silently fail - embeddings are optional
    
    def retrieve_memories(self, user_id: str, query: Optional[str] = None, 
                         limit: int = 5, category: Optional[str] = None) -> str:
        """Retrieve formatted memories for a user."""
        memories = self.db.get_memories(user_id, limit=limit, category=category)
        return self._format_memories(memories)
    
    def find_similar_memories(self, user_id: str, query_embedding: List[float],
                             threshold: float = 0.7, limit: int = 5) -> List[Dict[str, Any]]:
        """Find memories similar to query embedding."""
        all_memories = self.db.get_memories(user_id, limit=100)
        
        scored_memories = []
        for memory in all_memories:
            if memory.get('embedding'):
                similarity = self.calculate_similarity(query_embedding, memory['embedding'])
                if similarity >= threshold:
                    memory['similarity_score'] = similarity
                    scored_memories.append(memory)
        
        return sorted(scored_memories, key=lambda x: x['similarity_score'], reverse=True)[:limit]
    
    def clear_user_memories(self, user_id: str) -> int:
        """Clear all memories for a user."""
        return self.db.clear_user_memories(user_id)


class AsyncMemoryManager(EmbeddingMixin):
    """Asynchronous memory manager with embedding support and lifecycle management."""
    
    def __init__(self, db_path: str = "data/memories.db", model=None):
        self._async = True  # Flag for EmbeddingMixin
        super().__init__()
        self.async_db = AsyncSQLiteMemory(db_path)
        self.model = model
        self._initialized = False
    
    async def initialize(self):
        """Initialize the database and check embedding availability."""
        if not self._initialized:
            await self.async_db.initialize_database()
            self._initialized = True
            
            status = "✅ Embeddings enabled" if self.openai_client else "ℹ️ Embeddings disabled"
            print(f"{status} (OpenAI)")
    
    async def save_memory(self, user_id: str, content: str, metadata: Optional[Dict[str, Any]] = None,
                         category: str = "tool_recommendation") -> int:
        """Save memory with generated embedding asynchronously."""
        await self.initialize()
        
        embedding = await self._generate_embedding_with_retry(content) if self.openai_client else None
        
        if metadata is None:
            metadata = {}
        metadata['created_at'] = datetime.now().isoformat()
        
        return await self.async_db.save_memory(
            user_id=user_id, content=content, embedding=embedding,
            metadata=metadata, category=category
        )
    
    async def _generate_embedding_with_retry(self, text: str, max_retries: int = 3) -> Optional[List[float]]:
        """Generate embedding with retry logic, activity tracking, and cost logging."""
        if not self.openai_client:
            return None
        
        activity_id = None
        if TRACKING_AVAILABLE and activity_tracker:
            activity_id = await activity_tracker.start_activity("generate_embedding", {
                "text_length": len(text), "model": "text-embedding-3-small", "max_retries": max_retries
            })
        
        for attempt in range(max_retries):
            try:
                # Update progress
                if activity_id:
                    await activity_tracker.update_activity(
                        activity_id, progress=(attempt + 1) / max_retries * 0.8,
                        details={"attempt": attempt + 1, "max_retries": max_retries}
                    )
                
                # Generate embedding
                response = await self.openai_client.embeddings.create(
                    model="text-embedding-3-small", input=text[:8000]
                )
                
                # Track cost
                cost_info = {"tokens": 0, "cost": 0.0}
                if self.cost_tracker:
                    cost_info = await self.cost_tracker.log_embedding_cost(text[:8000])
                
                # Complete activity
                if activity_id:
                    summary = f"Generated embedding: {cost_info['tokens']} tokens, ${cost_info['cost']:.6f}"
                    await activity_tracker.complete_activity(activity_id, summary)
                
                return response.data[0].embedding
                
            except Exception as e:
                if attempt == max_retries - 1:
                    error_msg = f"Failed after {max_retries} attempts: {str(e)}"
                    if activity_id:
                        await activity_tracker.complete_activity(activity_id, error_msg)
                    return None
                    
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                if activity_id:
                    await activity_tracker.update_activity(
                        activity_id, progress=(attempt + 1) / max_retries * 0.5,
                        details={"attempt": attempt + 1, "error": str(e), "retrying": True}
                    )
        
        return None
    
    async def retrieve_memories(self, user_id: str, query: Optional[str] = None,
                               limit: int = 5, category: Optional[str] = None) -> str:
        """Retrieve formatted memories for a user asynchronously."""
        await self.initialize()
        memories = await self.async_db.get_memories(user_id, limit=limit, category=category)
        return self._format_memories(memories)
    
    async def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between embeddings."""
        return super().calculate_similarity(embedding1, embedding2)
    
    async def find_similar_memories(self, user_id: str, query_embedding: List[float],
                                   threshold: float = 0.7, limit: int = 5) -> List[Dict[str, Any]]:
        """Find memories similar to query embedding asynchronously."""
        all_memories = await self.async_db.get_memories(user_id, limit=100)
        
        scored_memories = []
        for memory in all_memories:
            if memory.get('embedding'):
                similarity = await self.calculate_similarity(query_embedding, memory['embedding'])
                if similarity >= threshold:
                    memory['similarity_score'] = similarity
                    scored_memories.append(memory)
        
        return sorted(scored_memories, key=lambda x: x['similarity_score'], reverse=True)[:limit]
    
    async def clear_user_memories(self, user_id: str) -> int:
        """Clear all memories for a user asynchronously."""
        return await self.async_db.clear_user_memories(user_id)
    
    async def perform_memory_maintenance(self) -> Dict[str, int]:
        """Perform memory lifecycle maintenance (compression/archival)."""
        await self.initialize()
        compressed = await self.async_db.compress_old_memories(days_threshold=30)
        archived = await self.async_db.archive_old_memories(days_threshold=90)
        return {'compressed': compressed, 'archived': archived}
    
    async def get_user_memory_stats(self, user_id: str) -> Dict[str, int]:
        """Get memory statistics for a user."""
        return await self.async_db.get_memory_stats(user_id)
