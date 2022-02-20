import React from "react"
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Note from "./note"


export default class NoteList extends React.Component {


    render() {
        const renderedNotes = this.props.notes.map((note) =>
            <React.Fragment key={note.id} >
                <Grid key={note.id} item xs={12} sm={6} md={3} align="center">
                    <Note title={note.frontmatter.title} summary={note.frontmatter.summary} slug={note.frontmatter.slug} external={note.frontmatter.external}/>
                </Grid>
            </React.Fragment>
        );
        return (
            <Box sx={{ m: 2 }}>
                <Grid
                    container
                    spacing={{ xs: 3 }}
                    // direction="column"
                    align="center"
                >
                    {renderedNotes}
                </Grid>
            </Box>
        )
    }
}
