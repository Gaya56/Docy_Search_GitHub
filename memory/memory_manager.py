"""
Memory manager for handling embeddings and similarity search.
Wraps SQLiteMemory with AI-powered memory operations.
Supports both sync and async operations for backward compatibility.
"""

import json
import numpy as np
import os
import asyncio
from typing import List, Dict, Optional, Any
from datetime import datetime
from .sqlite_memory import SQLiteMemory, AsyncSQLiteMemory

# Import activity tracking and cost tracking modules
try:
    import sys
    import os
    # Add parent directory to path for imports
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    from activity_tracker import activity_tracker
    from memory.cost_tracker import CostTracker
    TRACKING_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Activity/Cost tracking not available: {e}")
    activity_tracker = None
    CostTracker = None
    TRACKING_AVAILABLE = False

try:
    from openai import OpenAI, AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class MemoryManager:
    """Manages memory operations with embedding support.
    
    Enhanced with async capabilities while maintaining backward compatibility.
    """
    
    def __init__(self, db_path: str = "data/memories.db", model=None):
        """Initialize memory manager.
        
        Args:
            db_path: Path to SQLite database
            model: AI model instance (used for future extensions)
        """
        self.db = SQLiteMemory(db_path)
        self.async_manager = AsyncMemoryManager(db_path, model)
        self.model = model
        self.embedding_cache = {}
        
        # Check embedding availability
        if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            print("✅ Embeddings enabled (OpenAI)")
        else:
            print("ℹ️ Embeddings disabled (no OpenAI API key)")
    
    def save_memory_async(self, **kwargs) -> int:
        """Save memory asynchronously (fire-and-forget for UI responsiveness)."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we're in an async context, schedule the task
                task = asyncio.create_task(self.async_manager.save_memory(**kwargs))
                return 0  # Return dummy ID immediately
            else:
                # Run in new event loop
                return asyncio.run(self.async_manager.save_memory(**kwargs))
        except RuntimeError:
            # Fallback to sync operation
            return self.save_memory(**kwargs)
    
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
        # Generate embedding if model available
        embedding = None
        if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            try:
                # Generate real embedding using OpenAI API
                embedding = self._generate_embedding(content)
            except Exception as e:
                print(f"Warning: Could not generate embedding: {e}")
        
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
        # Check for OpenAI API key and availability
        if not OPENAI_AVAILABLE or not os.getenv("OPENAI_API_KEY"):
            return None
        
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=text[:8000]  # Limit text length
            )
            return response.data[0].embedding
        except Exception as e:
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


class AsyncMemoryManager:
    """Async memory manager with embedding support and lifecycle management."""
    
    def __init__(self, db_path: str = "data/memories.db", model=None):
        """Initialize async memory manager.
        
        Args:
            db_path: Path to SQLite database
            model: AI model instance (used for future extensions)
        """
        self.async_db = AsyncSQLiteMemory(db_path)
        self.model = model
        self.embedding_cache = {}
        self._initialized = False
        
        # Initialize cost tracker if available
        self.cost_tracker = None
        if TRACKING_AVAILABLE and CostTracker:
            self.cost_tracker = CostTracker()
        
        # Initialize OpenAI client if available
        self.openai_client = None
        if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            self.openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def initialize(self):
        """Initialize the database and check embedding availability."""
        if not self._initialized:
            await self.async_db.initialize_database()
            self._initialized = True
            
            # Check embedding availability
            if self.openai_client:
                print("✅ Embeddings enabled (OpenAI)")
            else:
                print("ℹ️ Embeddings disabled (no OpenAI API key)")
    
    async def save_memory(self,
                         user_id: str,
                         content: str,
                         metadata: Optional[Dict[str, Any]] = None,
                         category: str = "tool_recommendation") -> int:
        """Save memory with generated embedding asynchronously.
        
        Args:
            user_id: User identifier
            content: Memory content
            metadata: Optional metadata
            category: Memory category
            
        Returns:
            Memory ID
        """
        # Ensure initialized
        await self.initialize()
        
        # Generate embedding if available with retry logic
        embedding = None
        if self.openai_client:
            embedding = await self._generate_embedding_with_retry(content)
        
        # Add timestamp to metadata
        if metadata is None:
            metadata = {}
        metadata['created_at'] = datetime.now().isoformat()
        
        return await self.async_db.save_memory(
            user_id=user_id,
            content=content,
            embedding=embedding,
            metadata=metadata,
            category=category
        )
    
    async def _generate_embedding_with_retry(self, text: str, max_retries: int = 3) -> Optional[List[float]]:
        """Generate embedding using OpenAI API with retry logic, activity tracking, and cost logging."""
        if not self.openai_client:
            return None
        
        # Track activity start (if available)
        activity_id = None
        if TRACKING_AVAILABLE and activity_tracker:
            activity_id = await activity_tracker.start_activity("generate_embedding", {
                "text_length": len(text),
                "model": "text-embedding-3-small",
                "max_retries": max_retries
            })
        
        for attempt in range(max_retries):
            try:
                # Update activity progress (if available)
                if TRACKING_AVAILABLE and activity_tracker and activity_id:
                    await activity_tracker.update_activity(
                        activity_id, 
                        progress=(attempt + 1) / max_retries * 0.8,  # 80% for API call
                        details={"attempt": attempt + 1, "max_retries": max_retries}
                    )
                
                # Generate embedding
                response = await self.openai_client.embeddings.create(
                    model="text-embedding-3-small",
                    input=text[:8000]  # Limit text length
                )
                
                # Track cost after successful API call (if available)
                cost_info = {"tokens": 0, "cost": 0.0}
                if self.cost_tracker:
                    cost_info = await self.cost_tracker.log_embedding_cost(text[:8000])
                
                # Complete activity with success (if available)
                if TRACKING_AVAILABLE and activity_tracker and activity_id:
                    summary = f"Generated embedding: {cost_info['tokens']} tokens, ${cost_info['cost']:.6f}, text preview: '{text[:50]}...'"
                    await activity_tracker.complete_activity(activity_id, summary)
                
                return response.data[0].embedding
                
            except Exception as e:
                if attempt == max_retries - 1:
                    # Final failure
                    error_msg = f"Failed after {max_retries} attempts: {str(e)}"
                    if TRACKING_AVAILABLE and activity_tracker and activity_id:
                        await activity_tracker.complete_activity(activity_id, error_msg)
                    print(f"Warning: Could not generate embedding: {error_msg}")
                    return None
                    
                # Wait with exponential backoff before retry
                await asyncio.sleep(2 ** attempt)
                if TRACKING_AVAILABLE and activity_tracker and activity_id:
                    await activity_tracker.update_activity(
                        activity_id,
                        progress=(attempt + 1) / max_retries * 0.5,  # 50% progress on failures
                        details={"attempt": attempt + 1, "error": str(e), "retrying": True}
                    )
        
        return None
    
    async def retrieve_memories(self, 
                               user_id: str,
                               query: Optional[str] = None,
                               limit: int = 5,
                               category: Optional[str] = None) -> str:
        """Retrieve formatted memories for a user asynchronously.
        
        Args:
            user_id: User identifier
            query: Optional query for similarity search
            limit: Maximum memories to return
            category: Optional category filter
            
        Returns:
            Formatted string of relevant memories
        """
        # Ensure initialized
        await self.initialize()
        
        memories = await self.async_db.get_memories(user_id, limit=limit, category=category)
        
        if not memories:
            return "No previous interactions found."
        
        # Format memories for context
        formatted = []
        for mem in memories:
            timestamp = mem.get('timestamp', 'Unknown time')
            content = mem.get('content', '')
            formatted.append(f"[{timestamp}] {content}")
        
        return "\n".join(formatted)
    
    async def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
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
    
    async def find_similar_memories(self,
                                   user_id: str,
                                   query_embedding: List[float],
                                   threshold: float = 0.7,
                                   limit: int = 5) -> List[Dict[str, Any]]:
        """Find memories similar to query embedding asynchronously."""
        all_memories = await self.async_db.get_memories(user_id, limit=100)
        
        # Calculate similarities
        scored_memories = []
        for memory in all_memories:
            if memory.get('embedding'):
                similarity = await self.calculate_similarity(query_embedding, memory['embedding'])
                if similarity >= threshold:
                    memory['similarity_score'] = similarity
                    scored_memories.append(memory)
        
        # Sort by similarity and return top results
        scored_memories.sort(key=lambda x: x['similarity_score'], reverse=True)
        return scored_memories[:limit]
    
    async def clear_user_memories(self, user_id: str) -> int:
        """Clear all memories for a user asynchronously."""
        return await self.async_db.clear_user_memories(user_id)
    
    async def perform_memory_maintenance(self) -> Dict[str, int]:
        """Perform memory lifecycle maintenance (compression/archival)."""
        await self.initialize()
        
        # Compress old memories (30+ days, low access)
        compressed = await self.async_db.compress_old_memories(days_threshold=30)
        
        # Archive very old memories (90+ days, very low access)
        archived = await self.async_db.archive_old_memories(days_threshold=90)
        
        return {
            'compressed': compressed,
            'archived': archived
        }
    
    async def get_user_memory_stats(self, user_id: str) -> Dict[str, int]:
        """Get memory statistics for a user."""
        return await self.async_db.get_memory_stats(user_id)
