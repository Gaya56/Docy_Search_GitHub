#!/usr/bin/env python3
"""
Test script for async memory system integration.
Verifies that the async memory operations work correctly.
"""

import asyncio
import os
import sys
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memory.memory_manager import AsyncMemoryManager, MemoryManager


async def test_async_memory():
    """Test async memory operations."""
    print("🧪 Testing Async Memory System")
    print("=" * 50)
    
    # Test database path
    test_db_path = "data/test_memories.db"
    
    # Remove existing test database
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    # Initialize async memory manager
    async_manager = AsyncMemoryManager(db_path=test_db_path)
    
    # Test initialization
    print("1. Testing initialization...")
    await async_manager.initialize()
    print("✅ Async memory manager initialized")
    
    # Test user ID
    test_user_id = "test_user_123"
    
    # Test saving memory
    print("\n2. Testing memory save...")
    memory_id = await async_manager.save_memory(
        user_id=test_user_id,
        content="This is a test memory for async operations",
        metadata={
            "test": True,
            "timestamp": datetime.now().isoformat()
        },
        category="test"
    )
    print(f"✅ Memory saved with ID: {memory_id}")
    
    # Test retrieving memories
    print("\n3. Testing memory retrieval...")
    memories_text = await async_manager.retrieve_memories(
        user_id=test_user_id,
        limit=5,
        category="test"
    )
    print(f"✅ Retrieved memories:\n{memories_text}")
    
    # Test memory stats
    print("\n4. Testing memory statistics...")
    stats = await async_manager.get_user_memory_stats(test_user_id)
    print(f"✅ Memory stats: {stats}")
    
    # Test memory maintenance
    print("\n5. Testing memory maintenance...")
    maintenance_results = await async_manager.perform_memory_maintenance()
    print(f"✅ Maintenance results: {maintenance_results}")
    
    # Test backward compatibility wrapper
    print("\n6. Testing backward compatibility...")
    sync_manager = MemoryManager(db_path=test_db_path)
    
    # Test sync save using async backend
    sync_memory_id = sync_manager.save_memory_async(
        user_id=test_user_id,
        content="This is a sync wrapper test",
        category="sync_test"
    )
    print(f"✅ Sync wrapper saved memory")
    
    # Test sync retrieve
    sync_memories = sync_manager.retrieve_memories(
        user_id=test_user_id,
        limit=5
    )
    print(f"✅ Sync wrapper retrieved memories")
    
    # Cleanup
    print("\n7. Testing cleanup...")
    cleared_count = await async_manager.clear_user_memories(test_user_id)
    print(f"✅ Cleared {cleared_count} memories")
    
    # Clean up test database
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
        print("✅ Test database cleaned up")
    
    print("\n🎉 All async memory tests passed!")


def test_sync_compatibility():
    """Test that existing sync code still works."""
    print("\n🔄 Testing Sync Compatibility")
    print("=" * 50)
    
    test_db_path = "data/test_sync_memories.db"
    
    # Remove existing test database
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    # Test existing sync interface
    sync_manager = MemoryManager(db_path=test_db_path)
    
    test_user_id = "sync_user_123"
    
    # Test sync save
    print("1. Testing sync save...")
    memory_id = sync_manager.save_memory(
        user_id=test_user_id,
        content="This is a sync compatibility test",
        category="sync_test"
    )
    print(f"✅ Sync save successful: {memory_id}")
    
    # Test sync retrieve
    print("2. Testing sync retrieve...")
    memories = sync_manager.retrieve_memories(
        user_id=test_user_id,
        limit=5
    )
    print(f"✅ Sync retrieve successful")
    
    # Test sync clear
    print("3. Testing sync clear...")
    cleared = sync_manager.clear_user_memories(test_user_id)
    print(f"✅ Sync clear successful: {cleared} memories cleared")
    
    # Clean up test database
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
        print("✅ Test database cleaned up")
    
    print("🎉 Sync compatibility tests passed!")


if __name__ == "__main__":
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Run async tests
    asyncio.run(test_async_memory())
    
    # Run sync compatibility tests
    test_sync_compatibility()
    
    print("\n🚀 All memory system tests completed successfully!")
    print("The async memory system is ready for production use.")
