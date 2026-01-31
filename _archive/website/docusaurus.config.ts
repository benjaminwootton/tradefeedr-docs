import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Tradefeedr Documentation',
  tagline: 'Comprehensive documentation for Tradefeedr platform',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://docs.tradefeedr.com',
  baseUrl: '/',

  organizationName: 'tradefeedr',
  projectName: 'tradefeedr-docs',

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: '/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Tradefeedr',
      logo: {
        alt: 'Tradefeedr Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: 'Documentation',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Documentation',
          items: [
            {
              label: 'Getting Started',
              to: '/',
            },
            {
              label: 'UI Guide',
              to: '/about-the-tradefeedr-ui/user-interface-tour',
            },
            {
              label: 'API Reference',
              to: '/about-the-tradefeedr-api/spot-trades',
            },
          ],
        },
        {
          title: 'Company',
          items: [
            {
              label: 'Who Are We',
              to: '/who-are-we',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Tradefeedr. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
