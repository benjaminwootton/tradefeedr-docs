import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docsSidebar: [
    'intro',
    {
      type: 'category',
      label: 'About The Tradefeedr UI',
      items: [
        'about-the-tradefeedr-ui/user-interface-tour',
        'about-the-tradefeedr-ui/data-warehouse',
      ],
    },
    {
      type: 'category',
      label: 'About The Tradefeedr API',
      items: [
        'about-the-tradefeedr-api/spot-trades',
        'about-the-tradefeedr-api/forward-trades',
      ],
    },
    'who-are-we',
    'some-page',
  ],
};

export default sidebars;
