import argparse
import json
from argparse import Namespace
from datetime import datetime
from logging import Logger

import util
import generate_backlinks_files
import generate_index_file
import pandocify


DATE_TIME_FORMAT = '%Y-%m-%dT%H%M%S'


def persist_json(json_struct: dict, location: str) -> None:
    logger.info('dumping new state file to disk')
    util.create_folder(location=location)
    with open(util.path(location, 'state.json'), 'w') as f:
        json.dump(
            json_struct,
            f,
            indent=2,
            sort_keys=True)


def read_existing_json_state_file(location: str) -> dict:
    if util.validate_file_exists(util.path(location, 'state.json')):
        logger.info('reading existing json state file')
        with open(util.path(location, 'state.json'), 'r') as f:
            data: str = f.read()
            return json.loads(data)
    else:
        logger.info('no existing state file found, creating a new one')
        return {}


def setup_json_state_file(location: str) -> None:
    state_file: dict = read_existing_json_state_file(location=location)
    logger.info('persisting current script runtime to state file')
    state_file['runtime'] = datetime.now().strftime(DATE_TIME_FORMAT)

    persist_json(state_file, location)

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

    setup_json_state_file(location=args.temp)

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