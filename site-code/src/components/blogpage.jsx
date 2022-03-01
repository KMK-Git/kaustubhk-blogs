import React from 'react';
import { graphql } from 'gatsby';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import { useLocation } from '@gatsbyjs/reach-router';
import BlogCard from './blogcard';
import SiteWrapper from './sitewrapper';

export default function BlogPage({
  data: {
    mdx: { frontmatter, body },
    site: { siteMetadata: { siteUrl } },
  },
}) {
  const { pathname } = useLocation();
  const seo = {
    fullUrl: `${siteUrl}${pathname}`,
    previewImageSrc: `${siteUrl}${frontmatter.previewImage.childImageSharp.original.src}`,
    previewImageHeight: frontmatter.previewImage.childImageSharp.original.height,
    previewImageWidth: frontmatter.previewImage.childImageSharp.original.width,
  };
  const blogCard = (
    <>
      <Helmet title={frontmatter.title}>
        <meta name="description" content={frontmatter.summary} />
        <meta property="og:url" content={seo.fullUrl} />
        <meta property="og:title" content={frontmatter.title} />
        <meta property="og:description" content={frontmatter.summary} />
        <meta property="og:type" content="article" />
        <meta property="og:image" content={seo.previewImageSrc} />
        <meta property="og:image:width" content={seo.previewImageHeight} />
        <meta property="og:image:height" content={seo.previewImageWidth} />
      </Helmet>
      <BlogCard frontmatter={frontmatter} body={body} />
    </>
  );
  return (
    <SiteWrapper siteContent={blogCard} />
  );
}
export const pageQuery = graphql`
  query BlogPostQuery($id: String) {
    site {
      siteMetadata {
        siteUrl
      }
    }
    mdx(id: { eq: $id }) {
      id
      body
      frontmatter {
        slug
        title
        summary
        previewImage {
          childImageSharp {
            original {
              src
              height
              width
            }
          }
        }
      }
    }
  }
`;

BlogPage.propTypes = {
  data: PropTypes.exact({
    mdx: PropTypes.exact({
      frontmatter: PropTypes.exact({
        title: PropTypes.string.isRequired,
        summary: PropTypes.string.isRequired,
        slug: PropTypes.string.isRequired,
        previewImage: PropTypes.object.isRequired,
      }).isRequired,
      body: PropTypes.string.isRequired,
    }).isRequired,
    site: PropTypes.exact({
      siteMetadata: PropTypes.exact({
        siteUrl: PropTypes.string.isRequired,
      }).isRequired,
    }).isRequired,
  }).isRequired,
};
