import argparse
from bs4 import BeautifulSoup
from typing import Dict, Union, List
import sys
from pathvalidate import ValidationError, validate_filename
import os


HELP_HTML_FNAME = ("input html file name i.e. '--html_fname index.html'")

HELP_CSS_FNAME = ("output css file name i.e. '--css_fname overlays'")

HELP_SRC_PATH = (
    "input file path i.e. --src_path C:/users/src/")

HELP_DEST_PATH = (
    "output file path i.e. --dest_path C:/users/dest/")

HELP_ONLY = (
    "borderize these items only i.e. --only .class_name #id_name element_name"
)

HELP_EXCLUDE_ELEMENTS = ("exclude html elements, classes and/or "
                         "ids from having a color border i.e. "
                         "--exclude element_name .class_name #id_name")

HELP_ONLY_CONTAINERS = ("excludes any non-containers such as text")

ARG_PARSER_DESC = ("A script that takes in an html file and outputs a "
                   "css file that styles elements with contrasting "
                   "border lines. Useful for visualizing the space "
                   "html items take up without having to tediously apply a "
                   "border line color to each individual element/id/class.")


def get_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=ARG_PARSER_DESC)
    parser._action_groups.pop()
    required_args = parser.add_argument_group('required arguments')
    optional_args = parser.add_argument_group('optional arguments')
    required_args.add_argument('html_fname', metavar='filename.html',
                               type=str, help=HELP_HTML_FNAME, required=True)
    optional_args.add_argument('-css', '--css_fname', type=str,
                               required=False, help=HELP_CSS_FNAME)
    optional_args.add_argument('-src', '--src_path', type=str, required=False,
                               help=HELP_SRC_PATH)
    optional_args.add_argument('dest', '--dest_path', type=str, required=False,
                               help=HELP_DEST_PATH)
    # TODO: implement these optional features?
    # optional_args.add_argument('-o', '--only', action='extend', nargs="+",
    #                            type=str, required=False, help=HELP_ONLY)
    # optional_args.add_argument('-e', '--exclude', action="extend", nargs="+",
    #                            type=str, required=False,
    #                            help=HELP_EXCLUDE_ELEMENTS)
    optional_args.add_argument('-oc', '--only_containers', action="store_true",
                               type=bool, required=False,
                               help=HELP_ONLY_CONTAINERS, default=True)

    return vars(parser.parse_args())


def verify_file_name(name: str, expected_extension: str) -> str:
    if not name.endswith(f".{expected_extension}"):
        # extension excluded
        name = name + f".{expected_extension}"
    try:
        validate_filename(name)
    except ValidationError as e:
        print("{}\n".format(e), file=sys.stderr)
    return name


def validate_dirs_and_fps(dirs: List[str], file_paths: List[str]) -> None:
    for dir in dirs:
        if not os.path.isdir(dir):
            raise FileNotFoundError(f"The directory {dir} does not exist")
    for fp in file_paths:
        if not os.path.isfile(fp):
            raise FileNotFoundError(f"{fp} doesn't exist")


def setup_settings(args: Dict[str, str]) -> Dict[str, str]:
    settings: Dict[str, Union[str, bool]] = {}
    html_fname = verify_file_name(
        args.get("html_fname", "index.html"), "html")
    css_fname = verify_file_name(
        args.get("css_fname", "borders.css"), "css")
    src_dir = args.get("src_path", os.getcwd())
    dest_dir = args.get("dest_path", os.getcwd())
    directories = [src_dir, dest_dir]
    validate_dirs_and_fps(directories, [src_dir + html_fname])
    settings["input_fp"] = src_dir + html_fname
    settings["output_fp"] = dest_dir + css_fname
    # TODO: requires further implementation as above
    settings["only"] = args.get("only", None)
    settings["exclude"] = args.get("exclude", None)
    # -------------------------------------------------------
    settings["only_containers"] = args.get("only_containers", False)

    return settings


def get_html_items(filepath: str, only_containers: bool, encoding="utf-8") -> List[str]:
    with open(filepath, encoding=encoding, mode="+") as f:
        soup = BeautifulSoup(f, "html.parser")
        print(soup)
    return []


def main() -> None:
    args: Dict[str, str] = get_args()
    settings: Dict[str, Union[str, bool]] = setup_settings(args)
    # html_border_items: List[str] = get_html_items(
    #     settings["input_fp"], settings["only_containers"])


if __name__ == "__main__":
    main()
