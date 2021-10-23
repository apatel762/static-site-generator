import argparse
import os
from argparse import Namespace
from logging import Logger
from typing import Set

import util


def get_logger() -> Logger:
    return util.get_logger(logger_name='pandocify')


def do_pandoc_generation(notes_folder: str, temp_folder: str, html_folder: str) -> None:
    logger: Logger = get_logger()

    for folder in [notes_folder, temp_folder, html_folder]:
        logger.info('creating folder: \'%s\' if it doesn\'t exist already', folder)
        util.create_folder(folder)

    # only queue up files for pandoc generation if they (or the files that
    # point to them) have been modified recently, so that we don't have to
    # regenerate everything each time we make one change in one file.
    state_file: dict = util.read_existing_json_state_file(location=temp_folder)
    relevant_file_names: Set[str] = set()
    for file_name in os.listdir(notes_folder):
        if not util.is_md(file_name):
            continue
        key: str = util.strip_file_extension(file_name)
        if state_file['files'][key]['last_checked'] == state_file['runtime']:
            relevant_file_names.add(file_name)
            # ensure that we also refresh the backlinks for the files that are
            # referenced by this file (since the links go two ways)
            with open(util.path(notes_folder, file_name), 'r') as f:
                contents = f.read()
                # the results of re.findall() will look something like
                # [('Page B', 'pageB.md')]
                # where the link in markdown would've been [Page B](pageB.md)
                for _, link in util.md_links.findall(contents):
                    if util.is_md(link):
                        relevant_file_names.add(link)

    for file in relevant_file_names:
        # the path to the note is always gonna be in the notes_folder
        file_full_path: str = util.path(notes_folder, file)
        note_title = util.note_title(file_full_path)

        # the output HTML file should have the same name as the note but with
        # the .html suffix and it should be in the html folder
        file_html: str = util.path(html_folder, file)
        file_html: str = util.change_file_extension(file_html, '.html')

        # the backlinks file should have the same name as the note but with
        # the .md.backlinks suffix, and it should be in the temp folder
        file_backlinks: str = util.path(temp_folder, file + '.backlinks')

        logger.info('converting %s to html, title=%s', file, note_title)
        util.do_run(cmd=[
            'pandoc',
            file_full_path, file_backlinks,
            f'--defaults=pandoc.yaml',
            f'--id-prefix={util.to_footnote_id(file)}',
            f'--output={file_html}',
            f'--metadata=pagetitle:{note_title}'
        ])

    # if the index.md was generated in the temp folder, pandocify it
    index_file_name = 'index.md'
    generated_index_file = util.path(temp_folder, index_file_name)
    if util.check_file_exists(generated_index_file):
        output_file = util.path(
            html_folder, util.change_file_extension(index_file_name, '.html'))
        index_title = util.note_title(generated_index_file)
        logger.debug('converting %s to html, title=%s', generated_index_file, index_title)
        util.do_run(cmd=[
            'pandoc',
            generated_index_file,
            f'--defaults=pandoc.yaml',
            f'--id-prefix={util.to_footnote_id(index_file_name)}',
            f'--output={output_file}',
            f'--metadata=pagetitle:{index_title}'
        ])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert markdown notes to HTML')
    parser.add_argument(
        '-n', '--notes',
        required=True,
        type=str,
        help='The absolute path of your notes folder')
    parser.add_argument(
        '-t', '--temp',
        required=True,
        type=str,
        help='The relative path of the \'temp\' folder where the backlinks files are. '
             'These files should be generated before running this script.')
    parser.add_argument(
        '-o', '--html',
        required=True,
        type=str,
        help='The relative path to the folder where HTML files will go')
    args: Namespace = parser.parse_args()

    do_pandoc_generation(
        notes_folder=args.notes,
        temp_folder=args.temp,
        html_folder=args.html)
