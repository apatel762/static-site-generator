import argparse
import os
from argparse import Namespace
from datetime import datetime
from logging import Logger

import util
import generate_backlinks_files
import generate_index_file
import pandocify


DATE_TIME_FORMAT = '%Y-%m-%dT%H%M%SZ'


def setup_json_state_file(location: str, notes_folder: str) -> None:
    """
    The main orchestrator of the state file mechanics. This method must be
    idempotent.

    Args:
        location (str): The relative or absolute location of the folder that
        contains the JSON state file
    """
    state_file: dict = util.read_existing_json_state_file(location=location)

    now: datetime = datetime.utcnow()
    now_str: str = now.strftime(DATE_TIME_FORMAT)

    # record current script runtime
    state_file['runtime'] = now_str

    # ensure that the files section of the state file exists
    if 'files' not in state_file:
        state_file['files'] = {}

    # ensure that file data is up to date
    for file_name_ in os.listdir(notes_folder):
        if not util.is_md(file_name_):
            continue

        file_path: str = util.path(notes_folder, file_name_)

        key: str = util.strip_file_extension(file_name_)

        # if it's a new file, populate the metadata
        if key not in state_file['files']:
            logger.info(f'adding new key in files: {key}')
            state_file['files'][key]: dict = {}
            state_file['files'][key]['sha256']: str = util.sha256(file_path)
            state_file['files'][key]['last_checked']: str = now_str

            # we are done processing this file, move to the next one
            continue

        # if the file was modified since we last checked it (which we know
        # has happened if the hash has changed) then update its info
        current_file_hash: str = util.sha256(file_path)
        if current_file_hash != state_file['files'][key]['sha256']:
            logger.info(f'updating changed key: {key}')
            state_file['files'][key]['sha256']: str = current_file_hash
            state_file['files'][key]['last_checked']: str = now_str

    # save the new state of the JSON file to disk so that we can use it
    # the next time the script is run
    util.persist_json(state_file, location)

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

    setup_json_state_file(location=args.temp, notes_folder=args.notes)

    # generate_backlinks_files.generate_backlinks_files(
    #     notes_folder=args.notes,
    #     backlinks_folder=args.temp)
    # generate_index_file.create_index_file(
    #     temp_folder=args.temp,
    #     notes_folder=args.notes)
    # pandocify.do_pandoc_generation(
    #     notes_folder=args.notes,
    #     temp_folder=args.temp,
    #     html_folder=args.html)