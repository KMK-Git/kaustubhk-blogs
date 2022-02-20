import React from "react"
import Box from '@mui/material/Box';
import { woodBackground } from "./styles";
import Header from "./header";
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import "@fontsource/roboto";


export default function SiteWrapper(props) {
  const theme = createTheme({
    typography: {
      allVariants: {
        fontFamily: 'Roboto'
      },
    },
  });
  return (
    <ThemeProvider theme={theme}>
      <React.Fragment>
        <CssBaseline />
        <Box component="div" sx={woodBackground}>
          <Header />
          {props.siteContent}
        </Box>
      </React.Fragment>
    </ThemeProvider>
  );
}
