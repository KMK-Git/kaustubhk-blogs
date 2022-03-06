import React from 'react';
import renderer from 'react-test-renderer';
import SiteWrapper from '../sitewrapper';
import NoteList from '../notelist';

const { act } = renderer;
const mockCreateElement = React.createElement;

jest.mock('@gatsbyjs/reach-router', () => ({
  ...jest.requireActual('@gatsbyjs/reach-router'),
  useLocation: () => ({
    pathname: '/sampleroute',
  }),
}));

jest.mock('gatsby', () => ({
  __esModule: true,
  useStaticQuery: () => ({
    site: {
      siteMetadata: {
        title: 'Site Title',
        description: 'Site Description',
        siteUrl: 'Site Url',
        image: 'Site Image',
      },
    },
  }),
  graphql: () => ({
    mdx: {
      frontmatter: {
        title: 'Title',
        summary: 'Summary',
        slug: '/slug',
        previewImage: {
          childImageSharp: {
            original: { src: 'image.png', width: 200, height: 200 },
          },
        },
      },
      body: 'var _excluded = ["components"];\n\nfunction _extends() { _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; }; return _extends.apply(this, arguments); }\n\nfunction _objectWithoutProperties(source, excluded) { if (source == null) return {}; var target = _objectWithoutPropertiesLoose(source, excluded); var key, i; if (Object.getOwnPropertySymbols) { var sourceSymbolKeys = Object.getOwnPropertySymbols(source); for (i = 0; i < sourceSymbolKeys.length; i++) { key = sourceSymbolKeys[i]; if (excluded.indexOf(key) >= 0) continue; if (!Object.prototype.propertyIsEnumerable.call(source, key)) continue; target[key] = source[key]; } } return target; }\n\nfunction _objectWithoutPropertiesLoose(source, excluded) { if (source == null) return {}; var target = {}; var sourceKeys = Object.keys(source); var key, i; for (i = 0; i < sourceKeys.length; i++) { key = sourceKeys[i]; if (excluded.indexOf(key) >= 0) continue; target[key] = source[key]; } return target; }\n\n/* @jsxRuntime classic */\n\n/* @jsx mdx */\nvar _frontmatter = {\n  "slug": "/slug",\n  "date": "2022-02-20",\n  "title": "Testing",\n  "summary": "Summary",\n  "priority": 1,\n  "previewImage": "../images/medium/preview4.png",\n  "cardColors": "#fff740,#7afcff,#ff7eb9",\n  "darkCardColors": "#b3aa00,#00b0b3,#b30050"\n};\nvar layoutProps = {\n  _frontmatter: _frontmatter\n};\nvar MDXLayout = "wrapper";\nreturn function MDXContent(_ref) {\n  var components = _ref.components,\n      props = _objectWithoutProperties(_ref, _excluded);\n\n  return mdx(MDXLayout, _extends({}, layoutProps, props, {\n    components: components,\n    mdxType: "MDXLayout"\n  }), mdx("p", null, "Testing"));\n}\n;\nMDXContent.isMDXComponent = true;',
    },
    site: { siteMetadata: { siteUrl: 'http://localhost' } },
  }),
  Link: jest.fn().mockImplementation(
    // these props are invalid for an `a` tag
    ({
      activeClassName,
      activeStyle,
      getProps,
      innerRef,
      partiallyActive,
      ref,
      replace,
      to,
      ...rest
    }) => mockCreateElement('a', {
      ...rest,
      href: to,
    }),
  ),
}));

const notes = [{
  previewImage: {
    childImageSharp: {
      gatsbyImageData: {
        layout: 'constrained',
        backgroundColor: '#080808',
        images: {
          fallback: {
            src: '/static/808f866ec80fb7744a46a37fd63265fe/45641/preview4.png',
            srcSet: '/static/808f866ec80fb7744a46a37fd63265fe/dcd12/preview4.png 85w,\n/static/808f866ec80fb7744a46a37fd63265fe/98502/preview4.png 170w,\n/static/808f866ec80fb7744a46a37fd63265fe/45641/preview4.png 340w',
            sizes: '(min-width: 340px) 340px, 100vw',
          },
          sources: [
            {
              srcSet: '/static/808f866ec80fb7744a46a37fd63265fe/a6e1b/preview4.webp 85w,\n/static/808f866ec80fb7744a46a37fd63265fe/20fe9/preview4.webp 170w,\n/static/808f866ec80fb7744a46a37fd63265fe/d0f2f/preview4.webp 340w',
              type: 'image/webp',
              sizes: '(min-width: 340px) 340px, 100vw',
            },
          ],
        },
        width: 340,
        height: 143,
      },
    },
  },
  title: 'Title',
  summary: 'Summary',
  external: false,
  slug: '/blog/test',
  cardColors: '#fff740',
  darkCardColors: '#b3aa00',
  priority: 1,
  date: '2022-01-02',
  id: 'id1',
}, {
  previewImage: {
    childImageSharp: {
      gatsbyImageData: {
        layout: 'constrained',
        backgroundColor: '#080808',
        images: {
          fallback: {
            src: '/static/808f866ec80fb7744a46a37fd63265fe/45641/preview4.png',
            srcSet: '/static/808f866ec80fb7744a46a37fd63265fe/dcd12/preview4.png 85w,\n/static/808f866ec80fb7744a46a37fd63265fe/98502/preview4.png 170w,\n/static/808f866ec80fb7744a46a37fd63265fe/45641/preview4.png 340w',
            sizes: '(min-width: 340px) 340px, 100vw',
          },
          sources: [
            {
              srcSet: '/static/808f866ec80fb7744a46a37fd63265fe/a6e1b/preview4.webp 85w,\n/static/808f866ec80fb7744a46a37fd63265fe/20fe9/preview4.webp 170w,\n/static/808f866ec80fb7744a46a37fd63265fe/d0f2f/preview4.webp 340w',
              type: 'image/webp',
              sizes: '(min-width: 340px) 340px, 100vw',
            },
          ],
        },
        width: 340,
        height: 143,
      },
    },
  },
  title: 'Title2',
  summary: 'Summary2',
  external: false,
  slug: '/blog/test2',
  cardColors: '#fff740',
  darkCardColors: '#b3aa00',
  priority: 1,
  date: '2022-01-01',
  id: 'id2',
}, {
  previewImage: {
    childImageSharp: {
      gatsbyImageData: {
        layout: 'constrained',
        backgroundColor: '#080808',
        images: {
          fallback: {
            src: '/static/808f866ec80fb7744a46a37fd63265fe/45641/preview4.png',
            srcSet: '/static/808f866ec80fb7744a46a37fd63265fe/dcd12/preview4.png 85w,\n/static/808f866ec80fb7744a46a37fd63265fe/98502/preview4.png 170w,\n/static/808f866ec80fb7744a46a37fd63265fe/45641/preview4.png 340w',
            sizes: '(min-width: 340px) 340px, 100vw',
          },
          sources: [
            {
              srcSet: '/static/808f866ec80fb7744a46a37fd63265fe/a6e1b/preview4.webp 85w,\n/static/808f866ec80fb7744a46a37fd63265fe/20fe9/preview4.webp 170w,\n/static/808f866ec80fb7744a46a37fd63265fe/d0f2f/preview4.webp 340w',
              type: 'image/webp',
              sizes: '(min-width: 340px) 340px, 100vw',
            },
          ],
        },
        width: 340,
        height: 143,
      },
    },
  },
  title: 'Title3',
  summary: 'Summary3',
  external: true,
  slug: '/blog/test3',
  cardColors: '#fff740',
  darkCardColors: '#b3aa00',
  priority: 1,
  date: '2022-01-02',
  id: 'id3',
}];

const renderedNotes = <NoteList notes={notes} />;

describe('SiteWrapper', () => {
  it('renders correctly', async () => {
    let tree;
    act(() => {
      tree = renderer
        .create(<SiteWrapper siteContent={renderedNotes} />);
    });
    expect(tree.toJSON()).toMatchSnapshot();
  });
});
