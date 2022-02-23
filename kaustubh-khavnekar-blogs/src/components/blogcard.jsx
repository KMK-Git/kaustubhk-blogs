import React from 'react';
import CardContent from '@mui/material/CardContent';
import Card from '@mui/material/Card';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import { MDXProvider } from '@mdx-js/react';
import { MDXRenderer } from 'gatsby-plugin-mdx';
import PropTypes from 'prop-types';
import { cardBlogStyle, darkCardBlogStyle } from './styles';
import isDarkModeEnabled from '../utils/dark-mode';
import CodeHighlight from './codehighlight';

const shortcodes = { CodeHighlight };

export default function BlogCard({ frontmatter, body }) {
  let cardStyle = cardBlogStyle;
  if (isDarkModeEnabled()) {
    cardStyle = darkCardBlogStyle;
  }
  return (
    <Box sx={{ m: 5 }}>
      <Grid container>
        <Grid key="offset" item xs={1} md={2} />
        <Grid key="main" item xs={10} md={8}>
          <Card sx={cardStyle} elevation={8}>
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
    summary: PropTypes.string.isRequired,
    slug: PropTypes.string.isRequired,
    previewImage: PropTypes.object.isRequired,
  }).isRequired,
  body: PropTypes.string.isRequired,
};
