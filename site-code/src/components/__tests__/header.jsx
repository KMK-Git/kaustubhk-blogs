import React from 'react';
import renderer from 'react-test-renderer';

import Header from '../header';

const { act } = renderer;

describe('Header', () => {
  it('renders correctly', async () => {
    let tree;
    act(() => {
      tree = renderer
        .create(<Header />);
    });
    expect(tree.toJSON()).toMatchSnapshot();
  });
});
