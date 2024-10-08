import React from 'react';
import renderer from 'react-test-renderer';

import BlogPage from '../blogpage';

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
        date: '2022-01-01',
        lastModified: '2022-01-01',
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

describe('BlogPage', () => {
  it('renders correctly', async () => {
    let tree;
    act(() => {
      tree = renderer
        .create(
          <BlogPage
            data={{
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
                  date: '2022-01-01',
                  lastModified: '2022-01-01',
                },
                id: 'mock-id',
              },
              site: { siteMetadata: { siteUrl: 'http://localhost' } },
            }}
          >
            Testing
          </BlogPage>,
        );
    });
    expect(tree.toJSON()).toMatchSnapshot();
  });
});
