# static-site-generator

A static site generator that I created so that I had a way of easily publishing a webpage based on my markdown notes. Behind the scenes, the generator is just a few Python scripts using Pandoc to convert the notes to HTML and do some extra stuff in-between.

Some notable stuff that I added:

- Custom `pandoc` filter for formatting spaced-repetition prompts
- Custom `pandoc` filter for formatting links
- A script that checks for broken links in my notes
- A script that generates backlinks for all of my notes
- A script that generates an 'index' file if one isn't present
- Custom CSS for all of the above

## Requirements

- Linux
  - `rsync`
  - `python` 3.8+
  - `pandoc` 2.8+

I haven't tested MacOS or Windows and this static site generator probably won't work on those OSes.

## Usage

Modify the variables at the top of the Makefile and then once you're sure that everything is in the right place, just run:

```bash
make
```

from this git repo and your Markdown files will be turned into a static site.
