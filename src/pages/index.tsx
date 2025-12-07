import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './styles.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className={clsx('hero__title', styles.heroTitle)}>
          Teaching Physical AI & Humanoid Robotics
        </Heading>
        <p className={clsx('hero__subtitle', styles.heroDescription)}>
          A comprehensive guide to integrating physical computing concepts with advanced humanoid robotics and machine learning principles.
        </p>
        <div className={styles.buttons}>
          <Link
            className={clsx('button button--primary button--lg', styles.callToActionButton)}
            to="/docs/foundations-of-physical-ai">
            Start Reading Now
          </Link>
          <Link
            className={clsx('button button--outline button--lg', styles.callToActionButtonOutline)}
            to="/docs"> {/* Corrected link here */}
            View Chapters
          </Link>
        </div>
      </div>
    </header>
  );
}

const moduleCards = [
    { 
      title: 'Foundations of Physical AI', 
      link: '/docs/0-foundations-of-physical-ai', 
      description: '🤖 Explore the fundamental concepts of Physical AI. Understand embodied intelligence and its unique challenges.',
    },
    { 
      title: 'Capstone Architecture', 
      link: '/docs/capstone-architecture', 
      description: '🏗️ Design robust architectures for your robotics projects. Learn to build scalable and efficient systems.',
    },
    { 
      title: 'Capstone Implementation', 
      link: '/docs/capstone-implementation', 
      description: '💻 Implement your capstone project from design to deployment. Bring your physical AI ideas to life.',
    },
    { 
      title: 'Gazebo Simulation', 
      link: '/docs/gazebo-simulation', 
      description: '🌍 Dive into Gazebo for realistic robot simulations. Test and refine your algorithms in a virtual environment.',
    },
    { 
      title: 'Isaac ROS Perception', 
      link: '/docs/isaac-ros-perception', 
      description: '👀 Master perception with Isaac ROS. Enable your robots to understand and interact with their surroundings.',
    },
    { 
      title: 'Isaac Sim Fundamentals', 
      link: '/docs/isaac-sim-fundamentals', 
      description: '🎮 Learn the basics of Isaac Sim for advanced robotics simulation. Build and control virtual robots with ease.',
    },
    { 
      title: 'LLM Cognitive Planning', 
      link: '/docs/llm-cognitive-planning', 
      description: '🧠 Integrate Large Language Models for cognitive planning. Empower robots with advanced decision-making capabilities.',
    },
    { 
      title: 'Multimodal Interaction', 
      link: '/docs/multimodal-interaction', 
      description: '🗣️ Explore multimodal interaction for natural human-robot communication. Create intuitive and responsive interfaces.',
    },
    { 
      title: 'ROS2 Core Concepts', 
      link: '/docs/ros2-core-concepts', 
      description: '⚙️ Grasp the core concepts of ROS2. Build a strong foundation for developing complex robotic applications.',
    },
    { 
      title: 'Unity Visualization', 
      link: '/docs/unity-visualization', 
      description: '🎨 Visualize your robotic systems in Unity. Create stunning 3D environments for simulation and presentation.',
    },
];

function ModuleCards() {
  return (
    <section className={styles.tutorialCards}>
      <div className="container">
        <Heading as="h2" className={clsx('text--center', styles.sectionTitle)}>
          Our Modules
        </Heading>
        <div className="row">
          {moduleCards.map((card, idx) => (
            <div key={idx} className="col col--6"> {/* Changed from col--4 to col--6 */}
              <div className={clsx('card', styles.tutorialCard)}>
                <div className="card__header">
                  <h3>{card.title}</h3>
                </div>
                <div className="card__body">
                  <p>
                    {card.description}
                  </p>
                </div>
                <div className="card__footer">
                  <Link
                    className={clsx('button button--primary button--block', styles.cardButton)}
                    to={card.link}>
                    Read More
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function OverviewSection() {
  return (
    <section className={styles.overviewSection}>
      <div className="container">
        <Heading as="h2" className={clsx('text--center', styles.sectionTitle)}>
          Overview
        </Heading>
        <div className="row">
          <div className="col col--8 col--offset-2">
            <p className={styles.overviewText}>
              This book provides a comprehensive journey into the world of Physical AI and Humanoid Robotics. Starting from the fundamental concepts that differentiate physical AI from traditional AI, we guide you through the core components of building intelligent, embodied systems. You will learn about perception, cognitive planning, and multimodal interaction, and gain hands-on experience with industry-standard tools like ROS2, Gazebo, and Isaac Sim.
            </p>
            <p className={styles.overviewText}>
              The curriculum is structured to build your skills progressively. Each module covers a specific domain, from basic simulations to advanced AI-driven behaviors. By the end of this book, you will have the knowledge to design, simulate, and implement complex robotics applications, culminating in a capstone project that integrates all the concepts you've learned.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Home | ${siteConfig.title}`}
      description="Learn about Physical AI and Humanoid Robotics with our comprehensive guide.">
      <HomepageHeader />
      <main>
        <ModuleCards />
        <OverviewSection />
      </main>
    </Layout>
  );
}
