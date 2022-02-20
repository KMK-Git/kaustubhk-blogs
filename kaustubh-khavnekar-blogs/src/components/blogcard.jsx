import React from "react"
import CardContent from '@mui/material/CardContent';
import Card from '@mui/material/Card';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import { cardBlogStyle } from "./styles";
import { MDXProvider } from "@mdx-js/react"
import { MDXRenderer } from "gatsby-plugin-mdx"
import CodeHighlight from "./codehighlight";

const shortcodes = { CodeHighlight };


export default function BlogCard(props) {
    return (
        <Box sx={{ m: 5 }}>
            <Grid container>
                <Grid key="offset" item xs={1} md={2} />
                <Grid key="main" item xs={10} md={8}>
                    <Card sx={cardBlogStyle} elevation={8}>
                        <CardContent>
                            <MDXProvider components={shortcodes}>
                            {/* <MDXProvider> */}
                                <MDXRenderer frontmatter={props.frontmatter}>{props.body}</MDXRenderer>
                            </MDXProvider>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        </Box>
    );
}
