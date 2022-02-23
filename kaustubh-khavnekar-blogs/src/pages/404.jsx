import React from 'react';
import VideoNote from '../components/videonote';
import SiteWrapper from '../components/sitewrapper';

export default function NotFound() {
  const videoNote = (
    <VideoNote
      text="You took a wrong turn"
      video="https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ"
      cardColors="#fff740,#7afcff,#ff7eb9"
      darkCardColors="#b3aa00,#00b0b3,#b30050"
    />
  );
  return (
    <SiteWrapper siteContent={videoNote} />
  );
}
