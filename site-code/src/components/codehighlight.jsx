import React from 'react';
import { Highlight, Prism } from 'prism-react-renderer';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';

(typeof global !== 'undefined' ? global : window).Prism = Prism;
require('prismjs/components/prism-hcl');
require('prismjs/components/prism-bash');

export default function CodeHighlight({ theme, code, language }) {
  const Pre = styled.pre`
    text-align: left;
    margin: 1em 0;
    padding: 0.5em;
    overflow: scroll;
    `;

  const Line = styled.div`
    display: table-row;
    `;

  const LineNo = styled.span`
    display: table-cell;
    text-align: right;
    padding-right: 1em;
    user-select: none;
    opacity: 0.5;
    `;

  const LineContent = styled.span`
    display: table-cell;
    `;
  return (
    // eslint-disable-next-line react/jsx-props-no-spreading
    <Highlight theme={theme} code={code} language={language}>
      {({
        className, style, tokens, getLineProps, getTokenProps,
      }) => (
        <Pre className={className} style={style}>
          {tokens.map((line, i) => (
            // eslint-disable-next-line react/jsx-props-no-spreading,react/no-array-index-key
            <Line key={i} {...getLineProps({ line, key: i })}>
              <LineNo>{i + 1}</LineNo>
              <LineContent>
                {line.map((token, key) => (
                  // eslint-disable-next-line react/jsx-props-no-spreading,react/no-array-index-key
                  <span key={key} {...getTokenProps({ token, key })} />
                ))}
              </LineContent>
            </Line>
          ))}
        </Pre>
      )}
    </Highlight>
  );
}

CodeHighlight.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  theme: PropTypes.object.isRequired,
  code: PropTypes.string.isRequired,
  language: PropTypes.string.isRequired,
};
