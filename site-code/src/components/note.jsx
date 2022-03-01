import React, { useState, useEffect } from 'react';
import CardContent from '@mui/material/CardContent';
import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { Link } from 'gatsby';
import { GatsbyImage } from 'gatsby-plugin-image';
import PropTypes from 'prop-types';
import isDarkModeEnabled from '../utils/dark-mode';
import {
  cardRotate1, cardRotate2, cardRotate3, cardCommon,
} from './styles';

export default function Note({
  previewImage, title, summary, external, slug, cardColors, darkCardColors,
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
    setCardStyle({ backgroundColor: cardColor, ...cardRotate, ...cardCommon });
  };
  useEffect(calculateCardStyle, [cardColors, darkCardColors]);
  let image;
  if (previewImage) {
    image = (
      <CardMedia>
        <GatsbyImage image={previewImage.childImageSharp.gatsbyImageData} alt="CardImage" />
      </CardMedia>
    );
  } else {
    image = '';
  }
  const card = (
    <Card sx={cardStyle} elevation={8}>
      <CardContent>
        <Typography gutterBottom variant="h5" component="div">
          {title}
        </Typography>
      </CardContent>
      {image}
      <CardContent>
        <Typography
          variant="body2"
          dangerouslySetInnerHTML={{
            __html: summary,
          }}
        />
      </CardContent>
    </Card>
  );
  if (external) {
    return (
      <a href={slug} target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'none' }}>
        {card}
      </a>
    );
  }
  return (
    <Link to={slug} style={{ textDecoration: 'none' }}>
      {card}
    </Link>
  );
}

Note.propTypes = {
  title: PropTypes.string.isRequired,
  summary: PropTypes.string.isRequired,
  slug: PropTypes.string.isRequired,
  external: PropTypes.bool.isRequired,
  previewImage: PropTypes.exact({
    childImageSharp: PropTypes.exact({
      gatsbyImageData: PropTypes.any.isRequired,
    }).isRequired,
  }).isRequired,
  cardColors: PropTypes.string.isRequired,
  darkCardColors: PropTypes.string.isRequired,
};
