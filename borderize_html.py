import argparse

HELP_HTML_FNAME = ("input html file name i.e. '--html_fname index.html'")

HELP_CSS_FNAME = ("output css file name i.e. '--css_fname overlays'")

HELP_SRC_PATH = (
    "input file path i.e. --src_path C:/users/src/")

HELP_DEST_PATH = (
    "output file path i.e. --dest_path C:/users/dest/")

HELP_EXCLUDE_ELEMENTS = ("exclude html elements, classes and/or "
                         "ids from having a color border i.e. "
                         "[--exclude div .class_name #id_name]")

HELP_ONLY_CONTAINERS = ("excludes any non-containers such as text")

ARG_PARSER_DESC = ("A script that takes in an html file and outputs a "
                   "css file that styles elements with contrasting "
                   "border lines. Useful for visualizing web page "
                   "containers without having to tediously apply a "
                   "border line color to each individual element/id/class.")


def add_parser_args(parser) -> None:
    parser.add_argument('--html_fname', type=str,
                        required=True, help=HELP_HTML_FNAME)
    parser.add_argument('--css_fname', type=str,
                        required=False, help=HELP_CSS_FNAME)
    parser.add_argument('--exclude', action="extend", nargs="+",
                        type=str, required=False, help=HELP_EXCLUDE_ELEMENTS)
    parser.add_argument('--only_containers', action="store_true",
                        help=HELP_ONLY_CONTAINERS, default=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=ARG_PARSER_DESC)
    add_parser_args(parser)


if __name__ == "__main__":
    main()
