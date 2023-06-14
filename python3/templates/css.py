"""
/*
The MIT License (MIT)

Copyright (c) 2023 Otavio Pontes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Based on:
 - https://github.com/mrmrs/fluidity
 - https://github.com/markdowncss/retro.git

*/

/* Responsiveness */
img,
canvas,
iframe,
video,
svg,
select,
textarea {
  max-width: 100%;
}

html,
body {
  min-height: 100%;
}

/* End Responsiviness */

/* Style */

pre,
code {
  font-family: Menlo, "Courier New", monospace;
  padding: .5rem;
  line-height: 1.25;
  overflow-x: scroll;
  background-color: #222;
}

blockquote {
  border-left: 3px solid #01ff70;
  padding-left: 1rem;
}

a,
a:visited {
  color: #01ff70;
}

a:hover,
a:focus,
a:active {
  color: #cb0000;
}

.no-decoration {
  text-decoration: none;
}

body {
  font-family: "Source Code Pro";
  line-height: 1.25;
  background-color: #000;
  margin: 3rem auto 3rem;
  max-width: 52rem;
  color: #ccc;
  padding: .25rem;
  font-size: 16px;
}

img{
  margin: 0.5rem 0 0.5rem 0;
}

p {
  font-size: 1rem;
  margin-bottom: 1.3rem;
}

h1,
h2,
h3,
h4,
h5,
h6 {
  margin-top: 0;
  margin: 1.414rem 0 .5rem;
  font-weight: inherit;
}

h1 {
  margin-top: 0;
  font-size: 3.1rem;
}

h2 {
  font-size: 2.5rem;
}

h3 {
  font-size: 2rem;
}

h4 {
  font-size: 1.56rem;
}

h5 {
  font-size: 1.25rem;
}

h6 {
  font-size: 1rem;
}

small {
  font-size: .75em;
}

/* Media Print */
@media print {
  *,
  *:before,
  *:after {
    background: transparent !important;
    color: #000 !important;
    box-shadow: none !important;
    text-shadow: none !important;
  }

  a,
  a:visited {
    text-decoration: underline;
  }

  a[href]:after {
    content: " (" attr(href) ")";
  }

  abbr[title]:after {
    content: " (" attr(title) ")";
  }

  a[href^="#"]:after,
  a[href^="javascript:"]:after {
    content: "";
  }

  pre,
  blockquote {
    border: 1px solid #999;
    page-break-inside: avoid;
  }

  thead {
    display: table-header-group;
  }

  tr,
  img {
    page-break-inside: avoid;
  }

  img {
    max-width: 100% !important;
  }

  p,
  h2,
  h3 {
    orphans: 3;
    widows: 3;
  }

  h2,
  h3 {
    page-break-after: avoid;
  }

}
/* End Media Print */
"""
