import React from 'react';
import PropTypes from 'prop-types';

// https://mdawar.dev/blog/mdx-open-links-in-new-page
export default function MdxLink({ children, href }) {
  // Same page links
  const onPage = href.startsWith('#');

  return (
    // eslint-disable-next-line react/jsx-no-target-blank
    <a
      href={href}
      // Open the link in a new page
      target={onPage ? null : '_blank'}
      // Add noopener and noreferrer for security reasons
      rel={onPage ? null : 'noopener noreferrer'}
    >
      {children}
    </a>
  );
}

MdxLink.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  children: PropTypes.any.isRequired,
  href: PropTypes.string.isRequired,
};
