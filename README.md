# tex-to-txt

In order to run grammar and spell checking for latex files 
it is annoying that latex commands are in the source code and 
copying from a pdf is a pain.

Therefore this repository provides a small python script, that will 
convert a given `.tex` file into a `.txt` file by removing 
all latex specific commands etc.

This will then enable you to copy the whole content of the `.txt` file 
into a spell checker of your choice (e.g. word, online check etc.).

## Features:
- No extra dependencies (only python-out-of-the-box dependencies)
- Lightweight
- Not OS-dependant (runs on linux, macOS, windows)

## Extraction steps:
- Remove comments (line starting with `%`)
- Remove all figures, equatitions, tables etc. (As they can be very complex you have to check them manually)
- Remove citations
- Replace references with placeholder (`<Referenz entfernt>`)
- Remove latex commands (but keep the content):
    - ac and acs
    - enquote
    - chapter
    - section
    - subsection
- save the output as a `.txt` file


## How to run

Run from your commandline with:

```bash
python3 tex_to_txt.py <path-to-txt-file.tex> <desired-out-path-and-name.txt>
```