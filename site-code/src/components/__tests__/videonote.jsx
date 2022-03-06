import React from 'react';
import renderer from 'react-test-renderer';
import VideoNote from '../videonote';

const { act } = renderer;

describe('VideoNote', () => {
  it('renders correctly', async () => {
    let tree;
    act(() => {
      tree = renderer
        .create(<VideoNote
          text="You took a wrong turn"
          video="https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ"
          cardColors="#fff740"
          darkCardColors="#b3aa00"
        />);
    });
    expect(tree.toJSON()).toMatchSnapshot();
  });
});
