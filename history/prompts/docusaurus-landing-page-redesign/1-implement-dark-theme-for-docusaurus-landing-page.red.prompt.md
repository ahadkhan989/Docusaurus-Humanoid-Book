---
id: 1
title: Implement Dark Theme for Docusaurus Landing Page
stage: red
date: 2025-12-07
surface: agent
model: gemini-1.5-pro-a2
feature: docusaurus-landing-page-redesign
branch: main
user: user
command: ".gemini\commands\sp.implement.md You are an expert Docusaurus developer. Your task is to update the Docusaurus landing page (Home Page) UI to a modern, dark-themed design. The design must be clean, responsive, and follow Docusaurus best practices to prevent errors.

**Goal:** Create a visually appealing Hero Section with a "Teaching Physical AI & Humanoid Robotics" title, a description, and prominent Call-to-Action (CTA) buttons.

**Color Theme:**
* **Background:** Dark/Black (e.g., #1A1A1A or similar dark grey).
* **Text/Primary:** Ash White/Light Grey (e.g., #F0F0F0).
* **Accent/Buttons:** Deep Blue (e.g., #3B82F6).

**Action 1: Update the Home Page Component (src/pages/index.js)**
1. Locate the Docusaurus Home Page component at `src/pages/index.js`.
2. Replace its current content with a new React Component.
3. The new component must import and use a local CSS module for styling (e.g., `styles.module.css`).
4. The Hero section must contain:
    * Main Title: **Teaching Physical AI & Humanoid Robotics**
    * Description: **A comprehensive guide to integrating physical computing concepts with advanced humanoid robotics and machine learning principles.**
    * Two CTA Buttons:
        * Button 1: **Start Reading Now** (Primary Blue, links to `/docs/intro`)
        * Button 2: **View Chapters** (Secondary/Outline, links to `/docs`)

**Action 2: Create/Update the CSS Module (src/pages/styles.module.css)**
1. Create a new file named **`src/pages/styles.module.css`** (or update an existing one if the user is using `src/pages/index.js` which is importing styles from here).
2. Add all necessary CSS rules to implement the dark theme and responsive layout for the Hero section.
3. Ensure the section is vertically centered and uses the specified color palette.

**Output:** Provide the **full content** for both `src/pages/index.js` and `src/pages/styles.module.css`. Ensure the CSS uses **CSS Modules convention** (e.g., `.heroSection`).
