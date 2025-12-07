# AI-Native Textbook on Physical AI & Humanoid Robotics Constitution

## Core Principles

### I. Technical Accuracy
All technical explanations must be verifiable from trusted sources. Code examples must be runnable, tested, and adhere to a high standard of quality.

### II. Clarity and Accessibility
Content must be written in simple language, avoiding unnecessary jargon to be accessible to beginners. Explanations should be step-by-step, with diagrams preferred over long theoretical passages.

### III. Practical, Hands-on Learning
Every chapter must include clear learning objectives, a concept explanation, a practical exercise, a summary, and an assessment or mini-project to ensure a hands-on learning experience.

### IV. Simulation-First Approach
Development and examples will prioritize simulation before moving to physical hardware. ROS 2 examples must target Ubuntu 22.04 LTS.

### V. Ethical and Safe Application
A strong emphasis is placed on the ethical and safe use of AI and robotics. All instructions involving physical robots must include clear safety warnings, and content will not cover military or weaponized use cases.

### VI. AI-Native Experience
The textbook will be an AI-native learning platform, featuring an embedded RAG chatbot for interactive learning, content personalization, and support.

### VII. Open-Source and Collaborative
The entire project must be public and open-source, encouraging community contributions and collaboration.

## Technical Stack and Standards

This section outlines the key technologies and standards that ensure consistency and quality across the project.

- **Book Framework:** Docusaurus
- **Content Generation:** Claude Code + Spec-Kit Plus
- **Chatbot:** OpenAI Agents / ChatKit SDK
- **Backend:** FastAPI
- **Database:** Neon Serverless PostgreSQL
- **Vector Store:** Qdrant Cloud (Free Tier)
- **Deployment:** GitHub Pages or Vercel

## Project Constraints and Success Criteria

This section defines the project's boundaries, constraints, and the criteria for success, ensuring alignment with the hackathon's requirements.

- **Content:** Must cover all 4 modules of the official hackathon course outline in sequence and include a complete Capstone Project.
- **Deployment:** The project must be deployable on low-budget setups using cloud alternatives and will be hosted on GitHub Pages or Vercel.
- **Success:** Is measured by the successful deployment of the book, the correct functioning of the RAG chatbot, and the reproducibility of the capstone demo.

## Governance

This Constitution is the guiding document for the project. All development, content creation, and contributions must align with these principles. Amendments to this constitution require team consensus and must be documented.

**Version**: 1.0.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06