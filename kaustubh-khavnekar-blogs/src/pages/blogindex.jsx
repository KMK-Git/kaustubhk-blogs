import React from "react"
import { graphql } from "gatsby"
import NoteList from "../components/notelist"
import SiteWrapper from "../components/sitewrapper";

export default function Template({
  data, // this prop will be injected by the GraphQL query below.
}) {
  const notes = data.allMarkdownRemark.nodes;
  const renderedNotes = <NoteList notes={notes}></NoteList>;
  return (
    <SiteWrapper siteContent={renderedNotes}/>
  )
}

export const pageQuery = graphql`
  {
    allMarkdownRemark(sort: {fields: frontmatter___date, order: DESC}) {
      nodes {
        html
        frontmatter {
          date(formatString: "YYYY-MM-DD")
          slug
          title
          summary
          external
        }
        id
      }
    }
  }
`
