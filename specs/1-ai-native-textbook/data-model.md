# Data Model: AI-Native Textbook

This document describes the data models for the AI-Native Textbook project.

## 1. User

The `User` model stores information about the users of the textbook.

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Primary key |
| `email` | String | User's email address |
| `hashed_password` | String | Hashed password |
| `created_at` | DateTime | Timestamp of when the user was created |
| `programming_level` | String | User's self-reported programming level (Beginner, Intermediate, Advanced) |
| `ai_knowledge_level` | String | User's self-reported AI knowledge level (Beginner, Intermediate, Advanced) |
| `hardware_availability`| String | User's hardware availability (Local Workstation, Cloud GPU) |

## 2. ChatLog

The `ChatLog` model stores information about the interactions with the RAG chatbot.

| Field | Type | Description |
|---|---|---|
| `id` | UUID | Primary key |
| `user_id` | UUID | Foreign key to the `User` model |
| `session_id` | String | A unique identifier for the chat session |
| `query` | String | The user's query |
| `response` | String | The chatbot's response |
| `cited_chapter` | String | The chapter cited in the response |
| `confidence_score` | Float | The chatbot's confidence score for the response |
| `created_at` | DateTime | Timestamp of when the log was created |
