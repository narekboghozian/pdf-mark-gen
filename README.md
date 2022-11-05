# pdf-mark-gen
PDFMark generator to generate table of contents for PDFs.

## Usage

Create file:
``` bash
pdfmarkgen 'full/path/to/input/file'
```
File will be created in the same directory as the input file

Modify PDF:
``` bash
gs -o <output.pdf> -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress <input.pdf>  <pdfmark.file>
```


## Input file format

```txt
Title 1 of any length <page number>
  Sub title 1... <page number>
    Sub Sub title 1... <page number>
    Sub Sub title 2... <page number>
  Sub title 2... <page number>
offset <actual page in pdf> <page as is numbered>
Title 2 of any length <page number>
  Sub title 1... <page number>
  Sub title 2... <page number>
...
```
- First part of line until page number at end is the title
- Page number is the last number on the line
- Sub titles are indicated by tabs
- 'offset' command sets the pages order correctly so the table of contents can be copied directly, or to accomodate for missing pages

## Output file format

```txt
[ /Page N /Count M /Title (< title text >) /OUT pdfmark
[ /Page N /Count M /Title (< title text >) /OUT pdfmark
[ /Page N /Count M /Title (< title text >) /OUT pdfmark
...
```

## Example

['On Lisp' by Paul Graham](http://www.paulgraham.com/onlisp.html) does not have a table of contents as is:

<img width="996" alt="No bookmarks" src="https://user-images.githubusercontent.com/66885970/200142647-5e056cc1-7fa1-450d-b064-2a11b3ac6473.png">

Copying the table of contents into the input file [(ex/onlisp.txt)]()

<img width="468" alt="Copying table of contents" src="https://user-images.githubusercontent.com/66885970/200142660-b2f6f791-1795-42ef-9602-909ffb4b8b60.png">

After using the ghostscript command:

<img width="996" alt="Bookmarks!" src="https://user-images.githubusercontent.com/66885970/200142665-f0678c93-ae6d-4eb5-9887-73e3adbaf003.png">

## Requirements

- Python 3.x
- [Ghostscript](https://en.wikipedia.org/wiki/Ghostscript)
