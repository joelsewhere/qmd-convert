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
    cli.add_argument('--extract-media', default=None)
    args = cli.parse_args()

    if (args.format == None) and ('.' not in args.output):
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
                

def qmd_json(filepath, transform_ojs=True, extract_media=Path.cwd()):
    rendered_json = sh.quarto('render', filepath, to='json', output='-', **{"extract-media": extract_media})
    read_pandoc = pandoc.read(rendered_json, format='json')
    if transform_ojs:
        format_ojs(read_pandoc)

    return read_pandoc

                    
def main():
    
    args = get_cli_arguments()
    input_ = Path(args.input).resolve()
    output = Path(args.output).resolve()
    if not args.extract_media:
        media = output.parent
    else:
        media = Path(args.extract_media).resolve()

    read_pandoc = qmd_json(filepath=input_, extract_media=media)

    pandoc.write(read_pandoc, file=output.as_posix(), format=args.format)

if __name__ == '__main__':
    main()


