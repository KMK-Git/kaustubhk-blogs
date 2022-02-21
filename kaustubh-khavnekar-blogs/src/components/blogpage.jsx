import React from 'react';
import { graphql } from 'gatsby';
import PropTypes from 'prop-types';
import BlogCard from './blogcard';
import SiteWrapper from './sitewrapper';

export default function BlogPage({ data: { mdx: { frontmatter, body } } }) {
  const blogCard = <BlogCard frontmatter={frontmatter} body={body} />;
  return (
    <SiteWrapper siteContent={blogCard} />
  );
}
export const pageQuery = graphql`
  query BlogPostQuery($id: String) {
    mdx(id: { eq: $id }) {
      id
      body
      frontmatter {
        title
      }
    }
  }
`;

BlogPage.propTypes = {
  data: PropTypes.exact({
    mdx: PropTypes.exact({
      frontmatter: PropTypes.exact({
        title: PropTypes.string.isRequired,
      }).isRequired,
      body: PropTypes.string.isRequired,
    }).isRequired,
  }).isRequired,
};
