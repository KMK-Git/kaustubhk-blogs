import React from 'react';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import PropTypes from 'prop-types';
import Note from './note';

export default function NoteList({ notes }) {
  const renderedNotes = notes.map((note) => (
    <React.Fragment key={note.id}>
      <Grid key={note.id} item xs={12} sm={6} md={3} align="center">
        <Note
          title={note.title}
          summary={note.summary}
          slug={note.slug}
          external={note.external}
          previewImage={note.previewImage}
          cardColors={note.cardColors}
          darkCardColors={note.darkCardColors}
        />
      </Grid>
    </React.Fragment>
  ));
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

NoteList.propTypes = {
  notes: PropTypes.arrayOf(PropTypes.exact({
    title: PropTypes.string.isRequired,
    summary: PropTypes.string.isRequired,
    slug: PropTypes.string.isRequired,
    external: PropTypes.bool.isRequired,
    previewImage: PropTypes.object.isRequired,
    date: PropTypes.string.isRequired,
    priority: PropTypes.number.isRequired,
    cardColors: PropTypes.string.isRequired,
    darkCardColors: PropTypes.string.isRequired,
    id: PropTypes.string.isRequired,
  }).isRequired).isRequired,
};
