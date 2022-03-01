import React, { useState, useEffect } from 'react';
import CardContent from '@mui/material/CardContent';
import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import PropTypes from 'prop-types';
import isDarkModeEnabled from '../utils/dark-mode';
import {
  cardRotate1, cardRotate2, cardRotate3, videoCardCommon,
} from './styles';

export default function VideoNote({
  text, video, cardColors, darkCardColors,
}) {
  const [cardStyle, setCardStyle] = useState({});

  const calculateCardStyle = () => {
    let cardColorList;
    if (isDarkModeEnabled()) {
      cardColorList = darkCardColors.split(',');
    } else {
      cardColorList = cardColors.split(',');
    }
    const cardColor = cardColorList[Math.floor(Math.random() * cardColorList.length)];
    const cardRotateList = [cardRotate1, cardRotate2, cardRotate3];
    const cardRotate = cardRotateList[Math.floor(Math.random() * cardColorList.length)];
    setCardStyle({ backgroundColor: cardColor, ...cardRotate, ...videoCardCommon });
  };
  useEffect(calculateCardStyle, [cardColors, darkCardColors]);
  return (
    <Grid
      container
      spacing={{ xs: 3 }}
      align="center"
    >
      <Grid key="video" item xs={12} align="center">
        <Card sx={cardStyle} elevation={8}>
          <CardContent>
            <Typography gutterBottom variant="h5" component="div">
              {text}
            </Typography>
          </CardContent>
          <CardMedia>
            <iframe
              width="560"
              height="315"
              src={video}
              title="YouTube video player"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          </CardMedia>
        </Card>
      </Grid>
    </Grid>
  );
}

VideoNote.propTypes = {
  text: PropTypes.string.isRequired,
  video: PropTypes.string.isRequired,
  cardColors: PropTypes.string.isRequired,
  darkCardColors: PropTypes.string.isRequired,
};
// "https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ"
