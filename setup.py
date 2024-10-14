from pathlib import Path
from setuptools import setup, find_packages


root = Path(__file__).resolve().parent
requirements = (root / 'qmd_convert' / 'requirements.txt').read_text().split('\n')

name = u'qmd_convert'
version = '1'
description = "Convert .qmd files to another format without quarto's framework additions"
setup_args = dict(
    name=name,
    version=version,
    description=description,
    author='Jo-L Collins',
    author_email='joelsewhere@gmail.com',
    license='MIT',
    url='http://github.com/joelsewhere/qmd_convert',
    packages=find_packages(),
    package_data={'': ['requirements.txt']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['qmd_convert=qmd_convert.main:main']
    },
    install_requires=requirements
)

if __name__ == "__main__":
    setup(**setup_args)