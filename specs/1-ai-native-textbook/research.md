# Research: AI-Native Textbook on Physical AI & Humanoid Robotics

This document outlines the key decisions that need to be made for the project, along with the options and trade-offs for each.

## 1. ROS Distribution

- **Decision**: ROS 2 Humble Hawksbill (LTS)
- **Rationale**: As an LTS release, Humble provides stability and long-term support, which is crucial for a textbook that needs to remain relevant and usable for students and educators over time. While newer versions might have more features, Humble is the most stable and widely used version, making it a safe choice for a learning platform.
- **Alternatives considered**: Iron Irwini (more recent, but not LTS).

## 2. Simulation Priority

- **Decision**: Gazebo-first
- **Rationale**: Gazebo is more accessible and has a lower barrier to entry than Isaac Sim. It does not require an NVIDIA RTX GPU, making it a more inclusive choice for students with varying hardware. While Isaac Sim offers higher fidelity and more advanced features, Gazebo is sufficient for the core learning objectives of the textbook.
- **Alternatives considered**: Isaac Sim-first (higher fidelity, but less accessible).

## 3. Cloud vs On-Prem Default

- **Decision**: Local workstation
- **Rationale**: A local workstation setup is more cost-effective and gives users more control over their environment. While a cloud GPU setup can be more powerful, it can also be expensive and complex to configure. The textbook will provide cloud alternatives for those who need them, but the default will be a local setup.
- **Alternatives considered**: Cloud GPU (more powerful, but more expensive and complex).

## 4. Capstone Complexity

- **Decision**: Full VLA + manipulation
- **Rationale**: A full VLA + manipulation capstone project will provide a more comprehensive and impressive demonstration of the skills learned in the textbook. While a simpler project might be easier to reproduce, a more complex project will better prepare students for industry-level robotics development and provide a more compelling demo.
- **Alternatives considered**: Navigation + Vision only (simpler, but less impressive).

## 5. Personalization Depth

- **Decision**: Explanations only
- **Rationale**: Limiting personalization to explanations will simplify the implementation and reduce the complexity of the project. While personalizing exercises and labs could provide more value, it would also require a more sophisticated content generation and management system. For the initial version of the textbook, personalizing explanations is a good starting point.
- **Alternatives considered**: Exercises + Labs as well (more complex, but more valuable).
