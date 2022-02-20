import React from "react"
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import { cardHeaderStyle } from "./styles";
import { Link } from "gatsby"


export default function Header() {
    return (
        <Grid
            container
            spacing={{ xs: 3 }}
            align="center"
        >
            <Grid key="offset" item xs={12} sm={3} />
            <Grid key="homepage" item xs={12} sm={3} align="center">
            <a href="https://kaustubhk.com" target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'none' }}>
                <Card elevation={8} sx={cardHeaderStyle}>
                    <CardContent>
                        <Typography variant="h5" component="div">
                            My Homepage
                        </Typography>
                    </CardContent>
                </Card>
                </a>
            </Grid>
            <Grid key="blogs" item xs={12} sm={3} align="center">
            <Link to="/" style={{ textDecoration: 'none' }}>
                <Card elevation={8} sx={cardHeaderStyle}>
                    <CardContent>
                        <Typography variant="h5" component="div" sx={{"padding": "16px", "paddingBottom": "11px"}}>
                            All Blogs
                        </Typography>
                    </CardContent>
                </Card>
                </Link>
            </Grid>
        </Grid>
    );
}