import React from "react"
import CardContent from '@mui/material/CardContent';
import Card from '@mui/material/Card';
import Typography from '@mui/material/Typography';
import { Link } from "gatsby"
import { cardColor1, cardColor2, cardColor3 } from "./styles";
import { cardRotate1, cardRotate2, cardRotate3 } from "./styles";
import { cardCommon } from "./styles";


export default class Note extends React.Component {

    render() {
        const cardColorList = [cardColor1, cardColor2, cardColor3];
        const cardColor = cardColorList[Math.floor(Math.random() * cardColorList.length)];
        const cardRotateList = [cardRotate1, cardRotate2, cardRotate3];
        const cardRotate = cardRotateList[Math.floor(Math.random() * cardColorList.length)];
        const cardStyle = { ...cardColor, ...cardRotate, ...cardCommon };
        const card =
            (
                <Card sx={cardStyle} elevation={8}>
                    <CardContent>
                        <Typography gutterBottom variant="h5" component="div">
                            {this.props.title}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" dangerouslySetInnerHTML={{
                            __html: this.props.summary,
                        }} />
                    </CardContent>
                </Card>
            );
        if (this.props.external) {
            return (
                <a href={this.props.slug} target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'none' }}>
                    {card}
                </a>
            )
        } else {
            return (
                <Link to={this.props.slug} style={{ textDecoration: 'none' }}>
                    {card}
                </Link>
            )
        }
    }
}
