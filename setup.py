from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent

setup(
    name='mkdocs-exclude-unused-files',
    version='1.0.0',
    packages=['mkdocs_exclude_unused_files'],
    url='https://github.com/JonasDoesThings/mkdocs-exclude-unused-files',
    license='MIT',
    author='Jonas Lorenz <jonas@jonasdoesthings.com>',
    author_email='jonas@jonasdoesthings.com',
    description='A mkdocs plugin that excludes assets that are unused (orphaned) from being included in the final mkdocs output.',
    long_description=(this_directory / "README.md").read_text(),
    long_description_content_type='text/markdown',
    keywords=['mkdocs', 'mkdocs-plugin'],
    install_requires=['mkdocs', 'beautifulsoup4'],

    entry_points={
        'mkdocs.plugins': [
            'mkdocs_exclude_unused_files = mkdocs_exclude_unused_files.plugin:ExcludeUnusedFilesPlugin',
        ]
    },
)
