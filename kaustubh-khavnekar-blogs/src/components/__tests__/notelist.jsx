import React from 'react';
import renderer from 'react-test-renderer';
import NoteList from '../notelist';

const { act } = renderer;

describe('NoteList', () => {
  it('renders correctly', () => {
    let tree;
    act(() => {
      tree = renderer
        .create(<NoteList notes={[{
          previewImage: {
            childImageSharp: {
              gatsbyImageData: {
                layout: 'constrained',
                backgroundColor: '#080808',
                images: {
                  fallback: {
                    src: '/static/808f866ec80fb7744a46a37fd63265fe/45641/preview4.png',
                    srcSet: '/static/808f866ec80fb7744a46a37fd63265fe/dcd12/preview4.png 85w,\n/static/808f866ec80fb7744a46a37fd63265fe/98502/preview4.png 170w,\n/static/808f866ec80fb7744a46a37fd63265fe/45641/preview4.png 340w',
                    sizes: '(min-width: 340px) 340px, 100vw',
                  },
                  sources: [
                    {
                      srcSet: '/static/808f866ec80fb7744a46a37fd63265fe/a6e1b/preview4.webp 85w,\n/static/808f866ec80fb7744a46a37fd63265fe/20fe9/preview4.webp 170w,\n/static/808f866ec80fb7744a46a37fd63265fe/d0f2f/preview4.webp 340w',
                      type: 'image/webp',
                      sizes: '(min-width: 340px) 340px, 100vw',
                    },
                  ],
                },
                width: 340,
                height: 143,
              },
            },
          },
          title: 'Title',
          summary: 'Summary',
          external: false,
          slug: '/blog/test',
          cardColors: '#fff740',
          darkCardColors: '#b3aa00',
          priority: 1,
          date: '2022-01-02',
          id: 'id1',
        }, {
          previewImage: {
            childImageSharp: {
              gatsbyImageData: {
                layout: 'constrained',
                backgroundColor: '#080808',
                images: {
                  fallback: {
                    src: '/static/808f866ec80fb7744a46a37fd63265fe/45641/preview4.png',
                    srcSet: '/static/808f866ec80fb7744a46a37fd63265fe/dcd12/preview4.png 85w,\n/static/808f866ec80fb7744a46a37fd63265fe/98502/preview4.png 170w,\n/static/808f866ec80fb7744a46a37fd63265fe/45641/preview4.png 340w',
                    sizes: '(min-width: 340px) 340px, 100vw',
                  },
                  sources: [
                    {
                      srcSet: '/static/808f866ec80fb7744a46a37fd63265fe/a6e1b/preview4.webp 85w,\n/static/808f866ec80fb7744a46a37fd63265fe/20fe9/preview4.webp 170w,\n/static/808f866ec80fb7744a46a37fd63265fe/d0f2f/preview4.webp 340w',
                      type: 'image/webp',
                      sizes: '(min-width: 340px) 340px, 100vw',
                    },
                  ],
                },
                width: 340,
                height: 143,
              },
            },
          },
          title: 'Title2',
          summary: 'Summary2',
          external: false,
          slug: '/blog/test2',
          cardColors: '#fff740',
          darkCardColors: '#b3aa00',
          priority: 1,
          date: '2022-01-01',
          id: 'id2',
        }, {
          previewImage: {
            childImageSharp: {
              gatsbyImageData: {
                layout: 'constrained',
                backgroundColor: '#080808',
                images: {
                  fallback: {
                    src: '/static/808f866ec80fb7744a46a37fd63265fe/45641/preview4.png',
                    srcSet: '/static/808f866ec80fb7744a46a37fd63265fe/dcd12/preview4.png 85w,\n/static/808f866ec80fb7744a46a37fd63265fe/98502/preview4.png 170w,\n/static/808f866ec80fb7744a46a37fd63265fe/45641/preview4.png 340w',
                    sizes: '(min-width: 340px) 340px, 100vw',
                  },
                  sources: [
                    {
                      srcSet: '/static/808f866ec80fb7744a46a37fd63265fe/a6e1b/preview4.webp 85w,\n/static/808f866ec80fb7744a46a37fd63265fe/20fe9/preview4.webp 170w,\n/static/808f866ec80fb7744a46a37fd63265fe/d0f2f/preview4.webp 340w',
                      type: 'image/webp',
                      sizes: '(min-width: 340px) 340px, 100vw',
                    },
                  ],
                },
                width: 340,
                height: 143,
              },
            },
          },
          title: 'Title3',
          summary: 'Summary3',
          external: true,
          slug: '/blog/test3',
          cardColors: '#fff740',
          darkCardColors: '#b3aa00',
          priority: 1,
          date: '2022-01-02',
          id: 'id3',
        }]}
        />);
    });
    expect(tree.toJSON()).toMatchSnapshot();
  });
});
