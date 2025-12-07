import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './styles.module.css'; // Ensure this points to the correct CSS module

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

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Home | ${siteConfig.title}`} // Updated title for clarity
      description="Learn about Physical AI and Humanoid Robotics with our comprehensive guide."> {/* Updated description */}
      <HomepageHeader />
      <main>
        {/* <HomepageFeatures /> This component might be removed or updated based on further instructions */}
      </main>
    </Layout>
  );
}
