#!/usr/bin/env python3
"""
Debug script to test the RAG service logic directly
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set test environment variables
os.environ.setdefault('OPENAI_API_KEY', 'test-key')
os.environ.setdefault('QDRANT_URL', 'https://test.qdrant.io')
os.environ.setdefault('QDRANT_API_KEY', 'test-key')
os.environ.setdefault('DATABASE_URL', 'postgresql://test:test@localhost:5432/test')

# Mock the vector store and embedding services to avoid external dependencies
from unittest.mock import AsyncMock, MagicMock

# Read the rag_service file to understand the current system prompts
with open('app/services/rag_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("Current system prompt in general chat (around line 190):")
start_idx = content.find('"content": f"You are a helpful assistant', content.find('line 190', 0))
if start_idx == -1:
    # Search more broadly
    start_idx = content.find('You are a helpful assistant')
    if start_idx != -1:
        # Find the start of the string assignment
        quote_start = content.rfind('"content": f"', 0, start_idx)
        if quote_start != -1:
            # Find the end of this string (next unescaped quote not followed by closing bracket)
            end_idx = start_idx
            brace_count = 0
            in_string = True
            i = quote_start

            # Find the whole assignment
            while i < len(content):
                if content[i:i+12] == '"content": f"' and i == quote_start:
                    i += 11
                elif content[i] == '{' and i > 0 and content[i-1] != '\\':
                    brace_count += 1
                elif content[i] == '}' and i > 0 and content[i-1] != '\\':
                    brace_count -= 1
                elif content[i] == '"' and brace_count == 0 and i > 0 and content[i-1] != '\\':
                    # This might be the end, but need to make sure it's the end of the content value
                    # Look for comma or closing bracket after
                    j = i + 1
                    while j < len(content) and content[j] in [' ', '\n', '\t']:
                        j += 1
                    if content[j] in [',', '}', ']']:
                        end_idx = j
                        break
                i += 1

            snippet = content[quote_start:end_idx]
            print(snippet[:500] + "..." if len(snippet) > 500 else snippet)
            print()
            print("Looking for the specific instruction part:")
            if "I can answer questions related to Physical AI & Humanoid Robotics only" in snippet:
                print("✓ English instruction found in general chat system prompt")
            else:
                print("✗ English instruction NOT found in general chat system prompt")
        else:
            print("Could not locate the system prompt string")

print("\n" + "="*50)
print("Current system prompt in selection chat (around line 275):")
# Find the second occurrence
first_idx = content.find('You are a helpful assistant', content.find('You are a helpful assistant') + 1)
if first_idx != -1:
    quote_start = content.rfind('"content": f"', 0, first_idx)
    if quote_start != -1:
        # Find the end similarly
        end_idx = first_idx
        brace_count = 0
        i = quote_start

        while i < len(content):
            if content[i:i+12] == '"content": f"' and i == quote_start:
                i += 11
            elif content[i] == '{' and i > 0 and content[i-1] != '\\':
                brace_count += 1
            elif content[i] == '}' and i > 0 and content[i-1] != '\\':
                brace_count -= 1
            elif content[i] == '"' and brace_count == 0 and i > 0 and content[i-1] != '\\':
                j = i + 1
                while j < len(content) and content[j] in [' ', '\n', '\t']:
                    j += 1
                if content[j] in [',', '}', ']']:
                    end_idx = j
                    break
            i += 1

        snippet = content[quote_start:end_idx]
        print(snippet[:500] + "..." if len(snippet) > 500 else snippet)
        print()
        print("Looking for the specific instruction part:")
        if "I can answer questions related to Physical AI & Humanoid Robotics only" in snippet:
            print("✓ English instruction found in selection chat system prompt")
        else:
            print("✗ English instruction NOT found in selection chat system prompt")

print("\n" + "="*50)
print("Summary:")
english_msg = "I can answer questions related to Physical AI & Humanoid Robotics only."
hindi_msg = "Sorry, aapka sawal humare Humanoid Robotics book ke content se related nhi hai. Kripya book se related sawal poochiye."

if english_msg in content:
    print(f"✓ English message found in code: '{english_msg}'")
else:
    print(f"✗ English message NOT found in code: '{english_msg}'")

if hindi_msg in content:
    print(f"✗ Hindi message still in code: '{hindi_msg}'")
else:
    print(f"✓ Hindi message removed from code: '{hindi_msg}'")