import argparse
from argparse import Namespace
from logging import Logger

import util
import generate_backlinks_files
import generate_index_file
import pandocify


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Orchestrate static site generation including backlinks')
    parser.add_argument(
        '-n', '--notes',
        required=True,
        type=str,
        help='The absolute path of the folder that holds all of your notes. '
             'All of the notes that you want to generate the backlinks for '
             'should be in the top-level of this folder; the script will not '
             'recursively search for any markdown files that are in '
             'subfolders.')
    parser.add_argument(
        '-t', '--temp',
        required=True,
        type=str,
        help='The relative path of a folder where you want the backlinks '
             'files to be stored when they are generated.')
    parser.add_argument(
        '-o', '--html',
        required=True,
        type=str,
        help='The relative path to the folder where the output HTML files '
             'will go')
    args: Namespace = parser.parse_args()
    logger: Logger = util.get_logger(logger_name='ssg')

    generate_backlinks_files.generate_backlinks_files(
        notes_folder=args.notes,
        backlinks_folder=args.temp)
    generate_index_file.create_index_file(
        temp_folder=args.temp,
        notes_folder=args.notes)
    pandocify.do_pandoc_generation(
        notes_folder=args.notes,
        temp_folder=args.temp,
        html_folder=args.html)