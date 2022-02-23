const isDarkModeEnabled = () => {
  if (typeof window === 'undefined') {
    return false; // Light mode if checking for dark mode is not supported.
  }
  const darkQuery = window.matchMedia('(prefers-color-scheme: dark)');
  if (darkQuery.media === 'not all') {
    return false; // Light mode if checking for dark mode is not supported.
  }
  return darkQuery.matches;
};

export default isDarkModeEnabled;
