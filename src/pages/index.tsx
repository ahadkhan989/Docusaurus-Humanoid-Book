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
            to="/docs/intro">
            Start Reading Now
          </Link>
          <Link
            className={clsx('button button--outline button--lg', styles.callToActionButtonOutline)}
            to="/docs">
            View Chapters
          </Link>
        </div>
      </div>
    </header>
  );
}

const tutorialCards = [
  {
    title: 'Congratulations',
    link: '/docs/tutorial-basics/congratulations',
  },
  {
    title: 'Create a Blog Post',
    link: '/docs/tutorial-basics/create-a-blog-post',
  },
  {
    title: 'Create a Document',
    link: '/docs/tutorial-basics/create-a-document',
  },
  {
    title: 'Create a Page',
    link: '/docs/tutorial-basics/create-a-page',
  },
  {
    title: 'Deploy Your Site',
    link: '/docs/tutorial-basics/deploy-your-site',
  },
  {
    title: 'Markdown Features',
    link: '/docs/tutorial-basics/markdown-features',
  },
];

function TutorialCards() {
  return (
    <section className={styles.tutorialCards}>
      <div className="container">
        <Heading as="h2" className={clsx('text--center', styles.sectionTitle)}>
          Tutorial - Basics
        </Heading>
        <div className="row">
          {tutorialCards.map((card, idx) => (
            <div key={idx} className="col col--4">
              <div className={clsx('card', styles.tutorialCard)}>
                <div className="card__header">
                  <h3>{card.title}</h3>
                </div>
                <div className="card__body">
                  <p>
                    Learn more about {card.title}.
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

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Home | ${siteConfig.title}`}
      description="Learn about Physical AI and Humanoid Robotics with our comprehensive guide.">
      <HomepageHeader />
      <main>
        <TutorialCards />
      </main>
    </Layout>
  );
}
