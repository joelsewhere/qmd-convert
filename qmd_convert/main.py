import sh
import shutil
import pandoc
from argparse import ArgumentParser
from pathlib import Path

code_dir = Path(__file__).resolve().parent
code_files = list(code_dir.iterdir())

def get_cli_arguments():
    cli = ArgumentParser()
    cli.add_argument('input')
    cli.add_argument('output')
    cli.add_argument('--format', default=None)
    cli.add_argument('--extract-media', default=Path.cwd())
    args = cli.parse_args()

    if not args.format and '.' not in args.output:
        raise ValueError(
            "The output path must have a .<file type> extension "
            "or --format=<file type> must be provided"
            )

    return args


def format_ojs(read_pandoc):
    """
    Iterate over every pandoc block and search for codeblocks
    that contain the string "{ojs}".

    When found convert to a RawBlock and place the contect of the block
    inside <script></script>
    """
    for block, path in pandoc.iter(read_pandoc, path=True):
        if isinstance(block, pandoc.types.CodeBlock):
            block_classes = block[0]
            for bc in block_classes:
                if isinstance(bc, list) and '{ojs}' in bc:
                    holder, index = path[-1]
                    holder[index] = pandoc.types.RawBlock(
                        pandoc.types.Format('html'),
                        '<script>' + block[-1] + '</script>'
                        )
                    
def clean_up():

    """
    Providing an `extract-media` argument to `quarto render`
    places the media in the correct location, but a copy of
    the media are still being added to the directory for this file

    This function removes any files in this directory 
    that were not provided with the install.
    """

    current_files = list(code_dir.iterdir())
    for file in current_files:
        if file not in code_files:
            if file.is_dir():
                shutil.rmtree(file.as_posix())
            else:
                file.unlink()
                    
def main():
    
    args = get_cli_arguments()
    input_ = Path(args.input).resolve()
    output = Path(args.output).resolve()
    media = Path(args.extract_media).resolve()


    rendered_json = sh.quarto('render', input_, to='json', output='-', **{"extract-media": media})
    read_pandoc = pandoc.read(rendered_json, format='json')
    format_ojs(read_pandoc)
    
    pandoc.write(read_pandoc, file=output.as_posix())

    clean_up()

if __name__ == '__main__':
    main()


