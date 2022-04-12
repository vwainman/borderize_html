from argparse import ArgumentParser
from bs4 import BeautifulSoup
from typing import Dict, Union, List, Set
from pathlib import Path
import os
import random

HELP_HTML_FNAME = (
    "Input html file name i.e. 'python borderize_html.py index.html'.")

HELP_CSS_FNAME = (
    "Output css file name i.e. '--css_fname overlays', defaults "
    "to borders.css.")

HELP_SRC_PATH = (
    "Input file directory/folder i.e. '--src_directory C:/users/src/'."
    " Defaults to current working directory.")

HELP_DEST_PATH = (
    "Output file directory/folder i.e. '--dest_directory C:/users/dest/'."
    " Defaults to current working directory.")

HELP_ONLY = (
    "Borderize these items only i.e. '--only"
    " .class_name #id_name element_name'."
)

HELP_EXCLUDE_TAGS = ("Exclude certain html elements, classes and/or "
                     "ids from having a color border i.e. "
                     "'--exclude element_name .class_name #id_name'.")

HELP_NO_ATTRIBUTES = (
    "Excludes any non-containers such as text. "
    " The default stylizes all html tags.")

ARG_PARSER_DESC = ("A script that takes in an html file and outputs a "
                   "css file that styles elements with contrasting "
                   "border lines. Useful for visualizing the space "
                   "html items take up without having to tediously apply a "
                   "border line color to each individual element/id/class.")

IGNORED_TAG_NAMES: set = {"title", "html", "meta", "script", "br", "hr",
                          "img", "link", "source", "style", "abbr", "address",
                          "audio", "base", "bdi", "bdo"}


def get_args() -> ArgumentParser:
    parser = ArgumentParser(description=ARG_PARSER_DESC)
    parser._action_groups.pop()
    required_args = parser.add_argument_group('required arguments')
    optional_args = parser.add_argument_group('optional arguments')
    required_args.add_argument('html_fname', metavar='filename.html',
                               type=str, help=HELP_HTML_FNAME)
    optional_args.add_argument('-css', '--css_fname', type=str,
                               help=HELP_CSS_FNAME,
                               default="borders.css")
    optional_args.add_argument('-src', '--src_directory', type=Path,
                               help=HELP_SRC_PATH, default=os.getcwd())
    optional_args.add_argument('-dest', '--dest_directory', type=Path,
                               help=HELP_DEST_PATH, default=os.getcwd())
    # TODO: implement these optional features?
    # optional_args.add_argument('-o', '--only', action='extend', nargs="+",
    #                            type=str, required=False, help=HELP_ONLY)
    # optional_args.add_argument('-e', '--exclude', action="extend", nargs="+",
    #                            type=str, required=False,
    #                            help=HELP_EXCLUDE_ELEMENTS)
    optional_args.add_argument('-na', '--no_attributes', action="store_true",
                               help=HELP_NO_ATTRIBUTES)

    return vars(parser.parse_args())


def validate_dirs_and_fps(dirs: List[Path], file_paths: List[str]) -> None:
    for dir in dirs:
        if not os.path.isdir(dir):
            raise FileNotFoundError(f"The directory {dir} does not exist")
    for fp in file_paths:
        if not os.path.isfile(fp):
            raise FileNotFoundError(f"{fp} doesn't exist")


def setup_settings(args: Dict[str, str]) -> Dict[str, str]:
    settings: Dict[str, Union[str, bool]] = {}
    html_fname = args["html_fname"]
    css_fname = args["css_fname"]
    src_dir = args["src_directory"]
    dest_dir = args["dest_directory"]
    # validate_dirs_and_fps(directories, [src_dir + Path(html_fname)])
    settings["html_fp"] = os.path.join(src_dir, html_fname)
    settings["css_fp"] = os.path.join(dest_dir, css_fname)
    # TODO: requires further implementation as above --------
    # settings["only"] = args.get("only", None)
    # settings["exclude"] = args.get("exclude", None)
    # -------------------------------------------------------
    settings["no_attributes"] = args["no_attributes"]

    return settings


def element_attributes(element: 'bs4.element.Tag') -> set:
    attributes = set()
    if element.has_attr("class"):
        for class_ in element["class"]:
            attributes.add("." + class_)
    if element.has_attr("id"):
        attributes.add("#" + element['id'])
    return attributes


def get_css_labels(filepath: str,
                   no_attributes: bool,
                   encoding="utf-8") -> Set[str]:
    """ Acquire all necessary css labels for styling by parsing
        the html page with beautiful soup."""

    with open(filepath, encoding=encoding, mode="r+") as f:
        soup = BeautifulSoup(f, "html.parser")
        elements = soup.find_all()
        css_labels = set()

        for element in elements:
            if element.name not in IGNORED_TAG_NAMES:
                css_labels.add(element.name)
                if not no_attributes:
                    css_labels.update(element_attributes(element))

    return css_labels


def create_css(css_names: Set[str]) -> Dict[str, str]:
    comp_colors_hex: list = ["#BB4430", "#000000", "#ff0000", "#ff7700",
                             "#00ff1e", "#0026ff", "#f700ff", "#ff0040",
                             "#c300ff", "#c300ff", "#fbff00", "#9d00ff"]
    CSS_BEFORE_COLOR: str = "{ border: 3px solid "
    CSS_AFTER_COLOR: str = ";}"
    css_borders: Dict[str, str] = {}

    for name in css_names:
        if len(comp_colors_hex) > 0:
            color_used = comp_colors_hex.pop()
        else:
            def r(): return random.randint(0, 255)
            color_used = '#%02X%02X%02X' % (r(), r(), r())
        css_borders[name] = CSS_BEFORE_COLOR + color_used + CSS_AFTER_COLOR

    return css_borders


def make_css_file(css_borders: Dict[str, str],
                  css_fp: Path, encoding="utf-8") -> None:
    with open(css_fp, mode="w", encoding=encoding) as f:
        for name, content in css_borders.items():
            f.write(name + " " + content + "\n")


def main() -> None:
    args: Dict[str, str] = get_args()
    settings: Dict[str, Union[str, bool]] = setup_settings(args)
    css_labels: Set[str] = get_css_labels(
        settings["html_fp"], settings["no_attributes"])
    css_borders: Dict[str, str] = create_css(css_labels)
    make_css_file(css_borders, settings["css_fp"])


if __name__ == "__main__":
    main()
