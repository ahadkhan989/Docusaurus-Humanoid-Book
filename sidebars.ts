import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  tutorialSidebar: [
    'foundations-of-physical-ai',
    {
      type: 'category',
      label: 'ROS 2 – Robotic Nervous System',
      items: [
        'ros2-core-concepts',
      ],
    },
    {
      type: 'category',
      label: 'Digital Twin – Gazebo & Unity',
      items: [
        'gazebo-simulation',
        'unity-visualization',
      ],
    },
    {
      type: 'category',
      label: 'AI Brain – NVIDIA Isaac',
      items: [
        'isaac-sim-fundamentals',
        'isaac-ros-perception',
      ],
    },
    {
      type: 'category',
      label: 'Vision-Language-Action Systems',
      items: [
        'voice-to-action',
        'llm-cognitive-planning',
        'multimodal-interaction',
      ],
    },
    {
      type: 'category',
      label: 'Capstone – Autonomous Humanoid',
      items: [
        'capstone-architecture',
        'capstone-implementation',
      ],
    },
  ],

  // But you can create a sidebar manually
  /*
  tutorialSidebar: [
    'intro',
    'hello',
    {
      type: 'category',
      label: 'Tutorial',
      items: ['tutorial-basics/create-a-document'],
    },
  ],
   */
};

export default sidebars;
