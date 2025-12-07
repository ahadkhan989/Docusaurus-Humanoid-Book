# Quickstart: AI-Native Textbook

This document provides a quick overview of how to set up the development environment for the AI-Native Textbook project.

## Prerequisites

- Ubuntu 22.04 LTS
- Python 3.10
- Node.js 18 or later
- Yarn

## Frontend (Docusaurus)

1.  Navigate to the `docusaurus` directory:
    ```bash
    cd docusaurus
    ```
2.  Install the dependencies:
    ```bash
    yarn install
    ```
3.  Start the development server:
    ```bash
    yarn start
    ```

## Backend (FastAPI)

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment:
    ```bash
    python3 -m venv venv
    ```
3.  Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```
4.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5.  Start the development server:
    ```bash
    uvicorn src.api.main:app --reload
    ```
