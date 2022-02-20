import React from "react"
import { graphql } from "gatsby";
import BlogCard from "./blogcard";
import SiteWrapper from "./sitewrapper";


export default function BlogPage({ data: { mdx } }) {
    const blogCard = <BlogCard frontmatter={mdx.frontmatter} body={mdx.body} />
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
