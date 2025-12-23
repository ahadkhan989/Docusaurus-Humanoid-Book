"""
Simple test script to verify the application structure without requiring environment variables
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Temporarily set environment variables for testing
os.environ.setdefault('OPENAI_API_KEY', 'test-key')
os.environ.setdefault('QDRANT_URL', 'https://test.qdrant.io')
os.environ.setdefault('QDRANT_API_KEY', 'test-key')
os.environ.setdefault('DATABASE_URL', 'postgresql://test:test@localhost:5432/test')

try:
    from app.main import app
    print("✓ Application imported successfully")

    # Check if routes are registered
    routes = [route.path for route in app.routes]
    print("✓ Registered routes:")
    for route in routes:
        print(f"  - {route}")

    # Check if the main services can be imported
    from app.services.rag_service import rag_service
    from app.services.database import db_service
    from app.services.vector_store import vector_store_service
    print("✓ All services imported successfully")

    print("\n✓ Application structure is correct!")
    print("To run the application, set the required environment variables and execute:")
    print("  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")

except Exception as e:
    print(f"✗ Error importing application: {e}")
    import traceback
    traceback.print_exc()