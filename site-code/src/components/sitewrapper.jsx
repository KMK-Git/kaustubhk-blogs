import React, { useState, useEffect } from 'react';
import { useStaticQuery, graphql } from 'gatsby';
import Box from '@mui/material/Box';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import PropTypes from 'prop-types';
import { Global, css } from '@emotion/react';
import { Helmet } from 'react-helmet';
import { useLocation } from '@gatsbyjs/reach-router';
import { woodBackground, darkWoodBackgroundColor } from './styles';
import Header from './header';
import isDarkModeEnabled from '../utils/dark-mode';
import '@fontsource/roboto';

export default function SiteWrapper({ siteContent }) {
  const [backgroundStyle, setBackgroundStyle] = useState({});
  const calculateBackgroundStyle = () => {
    const style = {
      globalCss: `
    a {
      color: #c19a6b;
    }`,
      background: woodBackground,
    };
    if (isDarkModeEnabled()) {
      Object.assign(style.background, darkWoodBackgroundColor);
      style.globalCss = style.globalCss.concat(`
          img {
            filter: brightness(.8) contrast(1.2);
          }
      `);
    }
    setBackgroundStyle(style);
  };
  useEffect(calculateBackgroundStyle, []);
  const pageQuery = useStaticQuery(graphql`
  query metadataQuery {
    site {
      siteMetadata {
        title
        description
        siteUrl
        image
      }
    }
  }
`);
  const theme = createTheme({
    typography: {
      allVariants: {
        fontFamily: 'Roboto',
      },
    },
  });

  const { pathname } = useLocation();
  const seo = {
    image: `${pageQuery.site.siteMetadata.siteUrl}${pageQuery.site.siteMetadata.image}`,
    fullUrl: `${pageQuery.site.siteMetadata.siteUrl}${pathname}`,
    title: pageQuery.site.siteMetadata.title,
    description: pageQuery.site.siteMetadata.description,
  };
  return (
    <>
      <Helmet title={seo.title} htmlAttributes={{ lang: 'en' }}>
        <meta name="description" content={seo.description} />
        <meta name="image" content={seo.image} />
        <meta property="og:url" content={seo.fullUrl} />
        <meta property="og:title" content={seo.title} />
        <meta property="og:description" content={seo.description} />
        <meta property="og:image" content={seo.image} />
        <link
          rel="icon"
          type="image/png"
          sizes="32x32"
          href="/favicon-32x32.png"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="16x16"
          href="/favicon-16x16.png"
        />
        <link
          rel="apple-touch-icon"
          sizes="180x180"
          href="/apple-touch-icon.png"
        />
      </Helmet>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Box component="div" sx={backgroundStyle.background}>
          <Header />
          <Global styles={css(backgroundStyle.globalCss)} />
          {siteContent}
        </Box>
      </ThemeProvider>

    </>
  );
}

SiteWrapper.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  siteContent: PropTypes.any.isRequired,
};
