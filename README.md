# qmd_convert

This project creates a cli tool for converting `.qmd` files to a different format without the additions quarto defaults to adding when running `quarto render`

## Depdendencies

The following software projects will need to be installed manually:

**Pandoc:** [Installation Guide](https://pandoc.org/installing.html)
**Quarto:** [Installation Guide](https://quarto.org/docs/get-started/)

## Install `qmd_convert`

```bash
python setup.py sdist && pip install dist/qmd_convert-1.tar.gz
```

## How to use

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