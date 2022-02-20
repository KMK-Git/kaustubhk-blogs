import React from "react"
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Note from "./note"


export default function NoteList(props) {
    const renderedNotes = props.notes.map((note) =>
        <React.Fragment key={note.id} >
            <Grid key={note.id} item xs={12} sm={6} md={3} align="center">
                <Note title={note.title} summary={note.summary}
                    slug={note.slug} external={note.external} previewImage={note.previewImage} />
            </Grid>
        </React.Fragment>
    );
    return (
        <Box sx={{ m: 2 }}>
            <Grid
                container
                spacing={{ xs: 3 }}
                align="center"
            >
                {renderedNotes}
            </Grid>
        </Box>
    );
}
