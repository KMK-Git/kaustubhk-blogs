import React from 'react';
import { useStaticQuery, graphql } from 'gatsby';
import NoteList from '../components/notelist';
import SiteWrapper from '../components/sitewrapper';

export default function Template() {
  const pageQuery = useStaticQuery(graphql`
    {
      externalLinksQuery: externalLinksYaml(details: {}) {
        details {
          date
          previewImage {
            childImageSharp {
              gatsbyImageData(layout: CONSTRAINED, height: 170)
            }
          }
          priority
          slug
          summary
          title
          id
        }
      }
      blogsQuery: allMdx(sort: {fields: frontmatter___date, order: DESC}) {
        nodes {
          frontmatter {
            date(formatString: "YYYY-MM-DD")
            slug
            title
            summary
            priority
            previewImage {
              childImageSharp {
                gatsbyImageData(layout: CONSTRAINED, width: 250)
              }
            }
          }
          id
        }
      }
    }
  `);
  const externalLinks = pageQuery.externalLinksQuery.details.map((linkDetail) => (
    {
      ...linkDetail,
      external: true,
    }));
  const blogs = pageQuery.blogsQuery.nodes.map((blog) => ({
    slug: blog.frontmatter.slug,
    date: blog.frontmatter.date,
    title: blog.frontmatter.title,
    summary: blog.frontmatter.summary,
    priority: blog.frontmatter.priority,
    id: blog.id,
    previewImage: blog.frontmatter.previewImage,
    external: false,
  }));
  const notes = [...externalLinks, ...blogs];
  notes.sort((a, b) => {
    if (a.priority !== b.priority) {
      return a.priority - b.priority;
    }
    return new Date(b.date) - new Date(a.date);
  });
  const renderedNotes = <NoteList notes={notes} />;
  return (
    <SiteWrapper siteContent={renderedNotes} />
  );
}
