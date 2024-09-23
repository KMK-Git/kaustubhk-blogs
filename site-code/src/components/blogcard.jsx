import React, { useState, useEffect } from 'react';
import CardContent from '@mui/material/CardContent';
import Card from '@mui/material/Card';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import { MDXProvider } from '@mdx-js/react';
import PropTypes from 'prop-types';
import { cardBlogStyle, darkCardBlogStyle } from './styles';
import isDarkModeEnabled from '../utils/dark-mode';
import CodeHighlight from './codehighlight';
import MdxLink from './mdxlink';

const componentMappings = { CodeHighlight, a: MdxLink };

export default function BlogCard({ children }) {
  const [cardStyle, setCardStyle] = useState({});
  const calculateCardStyle = () => {
    let style = cardBlogStyle;
    if (isDarkModeEnabled()) {
      style = darkCardBlogStyle;
    } else {
      style = cardBlogStyle;
    }
    setCardStyle(style);
  };
  useEffect(calculateCardStyle, []);
  return (
    <Box sx={{ mt: 5 }}>
      <Grid container>
        <Grid key="offset" item xs={0} sm={1} md={2} />
        <Grid key="main" item xs={12} sm={10} md={8}>
          <Card sx={cardStyle} elevation={8}>
            <CardContent>
              <MDXProvider components={componentMappings}>
                {children}
              </MDXProvider>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>

  );
}

BlogCard.propTypes = {
  children: PropTypes.node.isRequired,
};
