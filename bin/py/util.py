import hashlib
import json
import logging
import os
import pathlib
import string
import sys
import unicodedata
from datetime import datetime
from subprocess import CompletedProcess, run
from typing import List


def get_logger(logger_name: str) -> logging.Logger:
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('%(name)s: %(levelname)s - %(message)s'))

    logger = logging.getLogger(name=logger_name)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger


def check_file_exists(path: str, error_on_validation_failure: bool = False) -> bool:
    if os.path.isfile(path):
        return True
    else:
        if error_on_validation_failure:
            raise FileNotFoundError(f'could not find \'{path}\'')
        else:
            return False


def sha256(file_name: str) -> str:
    with open(file_name, "rb") as f:
        raw_hash = hashlib.sha256(f.read())
        return raw_hash.hexdigest()


def persist_json(json_struct: dict, location: str) -> None:
    create_folder(location=location)
    with open(path(location, 'state.json'), 'w') as f:
        json.dump(
            json_struct,
            f,
            indent=2,
            sort_keys=True)


def read_existing_json_state_file(location: str) -> dict:
    if check_file_exists(path(location, 'state.json')):
        try:
            with open(path(location, 'state.json'), 'r') as f:
                data: str = f.read()
                return json.loads(data)
        except json.decoder.JSONDecodeError:
            return {}
    else:
        return {}


def last_n_chars(s: str, n: int) -> str:
    return s[-n::]


def is_md(file_name_with_extension: str) -> bool:
    return last_n_chars(file_name_with_extension, n=3) == '.md'


def first_line(file_path: str) -> str:
    with open(file_path, 'r') as f:
        return f.readline()


def note_title(file_path: str) -> str:
    return first_line(file_path) \
        .replace('# ', '') \
        .replace('\n', '')


def extract_todos(file_path: str) -> List[str]:
    tmp = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            if '::TODO' in line:
                line_clean = \
                    line.lstrip('- ')\
                        .replace('::', '')\
                        .replace('TODO', '')
                tmp.append(line_clean)
    return tmp


def change_file_extension(file_path: str, new_ext: str) -> str:
    fp: pathlib.Path = pathlib.Path(file_path)
    fp: pathlib.Path = fp.with_suffix('')
    fp: pathlib.Path = fp.with_suffix(new_ext)
    return str(fp)


def strip_file_extension(file_path: str) -> str:
    fp: pathlib.Path = pathlib.Path(file_path)
    fp: pathlib.Path = fp.with_suffix('')
    return str(fp)


def clean_filename(filename, chars_to_replace: str = ' ', replacement: str = '_'):
    whitelist = f'-_.() {string.ascii_letters}{string.digits}'
    file_name_max_size = 255

    # change the chars_to_replace into underscores
    for c in chars_to_replace:
        filename = filename.replace(c, replacement)

    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII',
                                                                      'ignore').decode()

    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)

    return cleaned_filename[:file_name_max_size]


def to_footnote_id(file_name) -> str:
    f: str = strip_file_extension(file_name)

    return clean_filename(f, chars_to_replace=' -').replace('_', '')


def create_folder(location: str) -> None:
    pathlib.Path(location).mkdir(parents=True, exist_ok=True)


def path(*args: str) -> str:
    return os.sep.join(args)


def do_run(cmd: List[str]) -> CompletedProcess:
    """
    you don't have to quote args that have spaces when you aren't using them
    in a shell; Python handles this for you.

    examples of using subprocess.run
        https://www.programcreek.com/python/example/94463/subprocess.run
    """
    return run(
        args=cmd,
        env={
            'PATH': os.environ['PATH']
        },
        check=True,
        capture_output=True,
        text=True
    )
