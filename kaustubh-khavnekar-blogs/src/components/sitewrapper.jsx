import React from "react"
import Box from '@mui/material/Box';
import { woodBackground } from "./styles";
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import "@fontsource/roboto";


export default class SiteWrapper extends React.Component {
  render() {
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
            {this.props.siteContent}
          </Box>
        </React.Fragment>
      </ThemeProvider>
    )
  }
}
