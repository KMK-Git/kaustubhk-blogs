module.exports = {
  siteMetadata: {
    title: `Kaustubh Khavnekar Blogs`,
    siteUrl: `https://blogs.kaustubhk.com`
  },
  plugins: ["gatsby-plugin-emotion", "gatsby-plugin-image", "gatsby-plugin-react-helmet", "gatsby-plugin-sitemap", {
    resolve: 'gatsby-plugin-manifest',
    options: {
      "name": "Kaustubh Khavnekar's blogs",
      "short_name": "KaustubhK Blogs",
      "start_url": "/",
      "background_color": "#c19a6b",
      "theme_color": "#c19a6b",
      "display": "standalone",
      "icon": "src/images/icon.png"
    }
  }, "gatsby-plugin-sharp", "gatsby-transformer-sharp", {
      resolve: 'gatsby-source-filesystem',
      options: {
        "name": "images",
        "path": "./src/images/"
      },
      __key: "images"
    }, {
      resolve: 'gatsby-source-filesystem',
      options: {
        "name": "articles",
        "path": "./src/articles/"
      },
      __key: "articles"
    },
    `gatsby-transformer-yaml`,
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        "name": "external_links",
        "path": "./src/external_links/"
      },
    }, `gatsby-remark-images`,
    {
      resolve: `gatsby-plugin-mdx`,
      options: {
        gatsbyRemarkPlugins: [
          {
            resolve: `gatsby-remark-images`,
            options: {
              maxWidth: 500,
            },
          },
        ],
      },
    }, `gatsby-plugin-offline`]
};
