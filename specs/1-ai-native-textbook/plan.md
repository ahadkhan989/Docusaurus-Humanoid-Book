# Implementation Plan: AI-Native Textbook on Physical AI & Humanoid Robotics

**Branch**: `1-ai-native-textbook` | **Date**: 2025-12-06 | **Spec**: [../spec.md]
**Input**: Feature specification from `specs/1-ai-native-textbook/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This project will create a complete AI-native, hands-on, industry-aligned textbook and learning platform. It will enable students to go from zero knowledge to building a simulated conversational humanoid robot with Physical AI principles. The textbook will be delivered as a Docusaurus static site with an embedded RAG chatbot.

## Technical Context

**Language/Version**: Python 3.10 (on Ubuntu 22.04)
**Primary Dependencies**: Docusaurus, FastAPI, Qdrant, Neon, OpenAI SDK
**Storage**: Neon Serverless PostgreSQL, Qdrant Cloud
**Testing**: Pytest, Playwright (for E2E)
**Target Platform**: Web (Docusaurus), Backend (Linux server)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: Site loads in <3s, Chatbot responses in <5s
**Constraints**: Must work on Ubuntu 22.04, free-tier friendly
**Scale/Scope**: 12-15 chapters, 20+ labs, 1 capstone

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [ ] **I. Technical Accuracy**: All technical claims are verifiable and code is tested.
- [ ] **II. Clarity and Accessibility**: Content is simple, clear, and accessible to beginners.
- [ ] **III. Practical, Hands-on Learning**: Includes objectives, exercises, and assessments.
- [ ] **IV. Simulation-First Approach**: Prioritizes simulation; ROS 2 targets Ubuntu 22.04.
- [ ] **V. Ethical and Safe Application**: Includes safety warnings; no military applications.
- [ ] **VI. AI-Native Experience**: Integrates the RAG chatbot and personalization.
- [ ] **VII. Open-Source and Collaborative**: The work is public and open-source.

## Project Structure

### Documentation (this feature)

```text
specs/1-ai-native-textbook/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application (frontend + backend)
backend/
├── src/
│   ├── api/
│   │   └── main.py
│   ├── core/
│   │   └── config.py
│   ├── services/
│   │   └── chatbot.py
│   └── models/
│       └── user.py
└── tests/

docusaurus/
├── docs/
│   ├── intro.md
│   └── ...
├── src/
│   ├── components/
│   └── pages/
└── docusaurus.config.js
```

**Structure Decision**: The project is a web application with a Docusaurus frontend and a FastAPI backend. The `docusaurus` directory will contain the textbook content and the frontend application. The `backend` directory will contain the FastAPI application for the RAG chatbot.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
