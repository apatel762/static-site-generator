import argparse
import os
from logging import Logger
from typing import Set

import util


def get_logger() -> Logger:
    return util.get_logger(logger_name='broken_link_checker')


def check_for_broken_links(notes_folder: str, cache_folder: str):
    logger: Logger = get_logger()

    # figure out which files have changed since the last time we ran the
    # static site generator, so that we only check if there are broken links
    # in those files
    state_file: dict = util.read_existing_json_state_file(location=cache_folder)
    files_to_check_as_they_may_not_exist: Set[str] = set()
    for file_name in os.listdir(notes_folder):
        if not util.is_md(file_name):
            continue
        key: str = util.strip_file_extension(file_name)
        if state_file['files'][key]['last_checked'] == state_file['runtime']:
            # add all of the markdown links in this file to the set of files
            # to check
            with open(util.path(notes_folder, file_name), 'r') as f:
                contents = f.read()
                # the results of re.findall() will look something like
                # [('Page B', 'pageB.md')]
                # where the link in markdown would've been [Page B](pageB.md)
                for _, link in util.md_links.findall(contents):
                    if util.is_md(link):
                        files_to_check_as_they_may_not_exist.add(link)

    to_report: Set[str] = set()
    for file_name in files_to_check_as_they_may_not_exist:
        try:
            with open(util.path(notes_folder, file_name), 'r') as f:
                pass
        except FileNotFoundError:
            to_report.add(file_name)

    if len(to_report) > 0:
        for missing_file in to_report:
            logger.error('missing file \'%s\' is referenced in a bad link', missing_file)

        # fail with an error, and do not continue with site generation
        raise Exception(f"{len(to_report)} broken links were found in your notes")

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
        help='The relative path of the cache folder, where temp files are '
             'stored')
    args: argparse.Namespace = parser.parse_args()

    check_for_broken_links(
        notes_folder=args.notes,
        cache_folder=args.temp)
