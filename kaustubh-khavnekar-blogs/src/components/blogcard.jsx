import React from 'react';
import CardContent from '@mui/material/CardContent';
import Card from '@mui/material/Card';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import { MDXProvider } from '@mdx-js/react';
import { MDXRenderer } from 'gatsby-plugin-mdx';
import PropTypes from 'prop-types';
import { cardBlogStyle } from './styles';
import CodeHighlight from './codehighlight';

const shortcodes = { CodeHighlight };

export default function BlogCard({ frontmatter, body }) {
  return (
    <Box sx={{ m: 5 }}>
      <Grid container>
        <Grid key="offset" item xs={1} md={2} />
        <Grid key="main" item xs={10} md={8}>
          <Card sx={cardBlogStyle} elevation={8}>
            <CardContent>
              <MDXProvider components={shortcodes}>
                {/* <MDXProvider> */}
                <MDXRenderer frontmatter={frontmatter}>{body}</MDXRenderer>
              </MDXProvider>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}

BlogCard.propTypes = {
  frontmatter: PropTypes.exact({
    title: PropTypes.string.isRequired,
  }).isRequired,
  body: PropTypes.string.isRequired,
};
