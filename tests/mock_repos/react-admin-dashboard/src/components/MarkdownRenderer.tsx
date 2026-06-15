// src/components/MarkdownRenderer.tsx - FLAWED: XSS risk via dangerouslySetInnerHTML

import React from 'react';

interface MarkdownRendererProps {
  content: string;
}

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content }) => {
  // FLAW: Using dangerouslySetInnerHTML with user-controlled content = XSS risk (OWASP A03)
  // This renders raw HTML from user markdown without sanitization
  return (
    <div
      className="markdown-content"
      dangerouslySetInnerHTML={{ __html: content }}  // FLAW: No DOMPurify or sanitize step
    />
  );
};

// Correct approach would be:
// import DOMPurify from 'dompurify';
// <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(content) }} />
