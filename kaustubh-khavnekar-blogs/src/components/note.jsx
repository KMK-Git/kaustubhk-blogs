import React, { useState, useEffect } from "react"
import CardContent from '@mui/material/CardContent';
import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { Link } from "gatsby"
import { cardColor1, cardColor2, cardColor3 } from "./styles";
import { cardRotate1, cardRotate2, cardRotate3 } from "./styles";
import { cardCommon } from "./styles";
import { GatsbyImage } from "gatsby-plugin-image"


export default function Note(props) {
    const [cardStyle, setCardStyle] = useState({});

    const calculateCardStyle = () => {
        const cardColorList = [cardColor1, cardColor2, cardColor3];
        const cardColor = cardColorList[Math.floor(Math.random() * cardColorList.length)];
        const cardRotateList = [cardRotate1, cardRotate2, cardRotate3];
        const cardRotate = cardRotateList[Math.floor(Math.random() * cardColorList.length)];
        setCardStyle({ ...cardColor, ...cardRotate, ...cardCommon });
    };
    useEffect(calculateCardStyle, []);
    let image;
    if (props.previewImage) {
        image = <CardMedia>
            <GatsbyImage image={props.previewImage.childImageSharp.gatsbyImageData} alt="CardImage" />
        </CardMedia>;
    } else {
        image = "";
    }
    const card =
        (
            <Card sx={cardStyle} elevation={8}>
                <CardContent>
                    <Typography gutterBottom variant="h5" component="div">
                        {props.title}
                    </Typography>
                </CardContent>
                {image}
                <CardContent>
                    <Typography variant="body2" dangerouslySetInnerHTML={{
                        __html: props.summary,
                    }} />
                </CardContent>
            </Card>
        );
    if (props.external) {
        return (
            <a href={props.slug} target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'none' }}>
                {card}
            </a>
        );
    } else {
        return (
            <Link to={props.slug} style={{ textDecoration: 'none' }}>
                {card}
            </Link>
        );
    }
}
