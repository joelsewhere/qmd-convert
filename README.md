# qmd_convert

This project creates a cli tool for converting `.qmd` files to a different format without the additions quarto defaults to adding when running `quarto render`

There appears to be a way to drop most quarto add-on according to [this discussion](https://github.com/quarto-dev/quarto-cli/discussions/7987), but I'm finding the conversion process in this repository to be more straightforward mostly because it doesn't require adding a bunch of configuration variables mentioned to a `.qmd` file. 

### Conversion process
1. Use `quarto render` to execute the code of the qmd file, and convert the executed file to `json`. (At time of writing this, converting to json prevents quarto from adding any framework add-ons.)
1. Parse the json with `pandoc.read`
1. Iterate recursively over each pandoc block and transform codeblocks containing `"{ojs}"` to an html `<script>`
1. Convert the json to html using `pandoc.write`

## Depdendencies

The following software projects will need to be installed manually:

**Pandoc:** [Installation Guide](https://pandoc.org/installing.html)

**Quarto:** [Installation Guide](https://quarto.org/docs/get-started/)

## Install `qmd_convert`

```bash
python setup.py sdist && pip install dist/qmd_convert-1.tar.gz
```

## CLI - How to use

**Convert the file `./report.qmd` to `./report.html`**
```bash
nb_convert report.qmd report.html
```

**Place generated media files in a different location than the generated file**
```bash
nb_convert report.qmd report.html --extract-media=../../static/
```

**Convert to file without file-type extension:**
```bash
nb_convert report.qmd report --format=html
```

These examples convert to html, but you should be able to convert to any of the options lists [here](https://pandoc.org/MANUAL.html#general-options).

For each option, `nb_convert` requires the option be set as the file extension `<file name>.<file extension>` or that you provide the file type with the `--format` argument. 

## Python API - How to use

This project uses the python [pandoc](https://boisgera.github.io/pandoc/) package (which uses the pandoc software) for writing qmd files to another format.

The pipeline steps are:
1. Pass the filepath to `quarto render <file path> --to=json output=-`. The `output=-` tells pandoc to return the outputted json to stdout.
1. Apply transformations to the json
1. Use pandoc.write to write to the new format

If you want to apply your own transformations to step 2, you can do the following

```python
from qmd_convert import qmd_json

filepath = 'example.qmd'
converted_json = qmd_json(filepath)
```