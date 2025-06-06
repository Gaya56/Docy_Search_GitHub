#!/usr/bin/env python3
"""
Simple test for Step 3 integration
"""

print("🧪 Testing Step 3 Integration...")

try:
    print("1. Testing imports...")
    from memory.memory_manager import AsyncMemoryManager, TRACKING_AVAILABLE
    print(f"   ✅ AsyncMemoryManager imported")
    print(f"   ✅ TRACKING_AVAILABLE: {TRACKING_AVAILABLE}")
    
    print("2. Testing initialization...")
    import asyncio
    
    async def test():
        manager = AsyncMemoryManager()
        await manager.initialize()
        print(f"   ✅ Manager initialized")
        print(f"   ✅ Cost tracker: {manager.cost_tracker is not None}")
        return manager
    
    manager = asyncio.run(test())
    print("🎉 Step 3 Integration Test PASSED!")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
