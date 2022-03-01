const path = require('path');
// Get paths of Gatsby's required rules, which as of writing is located at:
// https://github.com/gatsbyjs/gatsby/tree/fbfe3f63dec23d279a27b54b4057dd611dce74bb/packages/
// gatsby/src/utils/eslint-rules
const gatsbyRequiredRules = path.join(
  process.cwd(),
  'node_modules',
  'gatsby',
  'dist',
  'utils',
  'eslint-rules',
);

const siteGlobalMetadata = {
  siteUrl: 'https://blogs.kaustubhk.com',
  title: 'Kaustubh Khavnekar Blogs',
  description: 'A personal website for Kaustubh Khavnekar. The website is hosted using various AWS Services with a frontend made using React and Gatsby.',
  image: '/static/icon.png',
};

module.exports = {
  siteMetadata: siteGlobalMetadata,
  plugins: [{
    resolve: 'gatsby-plugin-robots-txt',
    options: {
      policy: [{ userAgent: '*', allow: '/' }],
    },
  }, {
    resolve: 'gatsby-plugin-sitemap',
    options: {
      query: `
      {
        allSitePage {
          nodes {
            path
          }
        }
        allMdx {
          nodes {
            frontmatter {
              lastModified(formatString: "YYYY-MM-DD")
              slug
            }
          }
        }
      }      
    `,
      resolveSiteUrl: () => siteGlobalMetadata.siteUrl,
      resolvePages: ({
        allSitePage: { nodes: allPages },
        allMdx: { nodes: allArticles },
      }) => {
        let maxLastModified = null;
        /* eslint-disable no-param-reassign */
        const siteMap = allArticles.reduce((prevMap, node) => {
          const { slug, lastModified } = node.frontmatter;
          prevMap[slug] = node.frontmatter;
          if (maxLastModified === null || new Date(maxLastModified) < new Date(lastModified)) {
            maxLastModified = lastModified;
          }
          return prevMap;
        }, {});
        /* eslint-enable no-param-reassign */
        siteMap['/'] = { slug: '/', lastModified: maxLastModified };
        return allPages.map((page) => ({ ...page, ...siteMap[page.path] }));
      },
      serialize: ({ slug, lastModified }) => ({
        url: slug,
        lastmod: lastModified,
      }),
    },
  }, 'gatsby-plugin-emotion', 'gatsby-plugin-image', 'gatsby-plugin-react-helmet', {
    resolve: 'gatsby-plugin-manifest',
    options: {
      name: "Kaustubh Khavnekar's blogs",
      short_name: 'KaustubhK Blogs',
      start_url: '/',
      background_color: '#c19a6b',
      theme_color: '#c19a6b',
      display: 'standalone',
      icon: 'src/images/icon.png',
    },
  }, 'gatsby-plugin-sharp', 'gatsby-transformer-sharp', {
    resolve: 'gatsby-source-filesystem',
    options: {
      name: 'images',
      path: './src/images/',
    },
    __key: 'images',
  }, {
    resolve: 'gatsby-source-filesystem',
    options: {
      name: 'articles',
      path: './src/articles/',
    },
    __key: 'articles',
  },
  'gatsby-transformer-yaml',
  {
    resolve: 'gatsby-source-filesystem',
    options: {
      name: 'external_links',
      path: './src/external_links/',
    },
  }, 'gatsby-remark-images',
  {
    resolve: 'gatsby-plugin-mdx',
    options: {
      gatsbyRemarkPlugins: [
        {
          resolve: 'gatsby-remark-images',
          options: {
            maxWidth: 500,
          },
        },
      ],
    },
  }, 'gatsby-plugin-offline', {
    resolve: 'gatsby-plugin-eslint',
    options: {
      // Gatsby required rules directory
      rulePaths: [gatsbyRequiredRules],
      // Default settings that may be ommitted or customized
      stages: ['develop'],
      extensions: ['js', 'jsx', 'ts', 'tsx'],
      exclude: ['node_modules', 'bower_components', '.cache', 'public'],
      // Any additional eslint-webpack-plugin options below
      // ...
    },
  }],
};
