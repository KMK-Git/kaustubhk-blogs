import React from 'react';
import Box from '@mui/material/Box';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import PropTypes from 'prop-types';
import { woodBackground } from './styles';
import Header from './header';
import '@fontsource/roboto';

export default function SiteWrapper({ siteContent }) {
  const theme = createTheme({
    typography: {
      allVariants: {
        fontFamily: 'Roboto',
      },
    },
  });
  return (
    <ThemeProvider theme={theme}>
      <>
        <CssBaseline />
        <Box component="div" sx={woodBackground}>
          <Header />
          {siteContent}
        </Box>
      </>
    </ThemeProvider>
  );
}

SiteWrapper.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  siteContent: PropTypes.any.isRequired,
};
