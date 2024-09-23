import React from 'react';
import renderer from 'react-test-renderer';

import BlogCard from '../blogcard';

const { act } = renderer;

describe('BlogCard', () => {
  it('renders correctly', async () => {
    let tree;
    act(() => {
      tree = renderer
        .create(<BlogCard>Testing</BlogCard>);
    });
    expect(tree.toJSON()).toMatchSnapshot();
  });
});
