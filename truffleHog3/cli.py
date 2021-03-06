#!/usr/bin/env python3
"""truffleHog3 scanner cli."""

import argparse
import git
import os
import re
import shutil
import sys

from distutils import dir_util
from signal import signal, SIGINT
from tempfile import TemporaryDirectory
from urllib import parse

from truffleHog3 import core


def run(**kwargs):
    graceful_keyboard_interrupt()
    args = get_cmdline_args()
    args.__dict__.update(**kwargs)
    core.config.update(**args.__dict__)
    issues = []

    workdir = args.workdir
    if args.workdir is None:
        workdir = TemporaryDirectory()
    else:
        os.makedirs(workdir, exist_ok=True)

    if args.no_history:
        source = args.source.split("://")[-1]
        if os.path.isdir(source):
            dir_util.copy_tree(source, workdir, preserve_symlinks=True)
        else:
            shutil.copy2(source, workdir)
    else:
        try:
            if os.path.exists(os.path.join(workdir, '.git')):
                repo = git.Repo.init(workdir)
                repo.git.reset('--hard')
                repo.remotes.origin.pull()
            else:
                git.Repo.clone_from(args.source, workdir)
        except git.exc.GitError:  # pragma: no cover
            error = "Failed to clone repository: {}".format(args.source)
            raise RuntimeError(error)

        issues = core.search_history(workdir)

    issues += core.search_current(workdir)

    core.log(issues, output=args.output, json_output=args.json_output)
    return bool(issues)


def graceful_keyboard_interrupt():
    def exit_on_keyboard_interrupt():  # pragma: no cover
        sys.stdout.write("\rKeyboard interrupt. Exiting\n")
        sys.exit(0)

    signal(SIGINT, lambda signal, frame: exit_on_keyboard_interrupt())


class HelpFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings:
            metavar, = self._metavar_formatter(action, action.dest)(1)
            return metavar
        else:
            return ", ".join(action.option_strings)


def check_source(source):
    if not parse.urlparse(source).scheme:
        source = "file://{}".format(os.path.abspath(source))
    return source


def get_cmdline_args():
    parser = argparse.ArgumentParser(
        description="Find secrets in your codebase.",
        usage="trufflehog3 [options] source",
        formatter_class=HelpFormatter
    )
    parser.add_argument(
        "source", help="URL or local path for secret searching",
        type=check_source
    )
    parser.add_argument(
        "-r", "--rules", help="ignore default regexes and source from json",
        dest="rules", type=core.load
    )
    parser.add_argument(
        "-o", "--output", help="write report to file",
        dest="output", type=argparse.FileType("w")
    )
    parser.add_argument(
        "-b", "--branch", help="name of the branch to be scanned",
        dest="branch"
    )
    parser.add_argument(
        "-m", "--max-depth", help="max commit depth for searching",
        dest="max_depth", type=int
    )
    parser.add_argument(
        "-s", "--since-commit", help="scan starting from a given commit hash",
        dest="since_commit"
    )
    parser.add_argument(
        "-w", "--workdir", help="directory to cache files for future runs",
        dest="workdir"
    )
    parser.add_argument(
        "--json", help="output in JSON",
        dest="json_output", action="store_true"
    )
    parser.add_argument(
        "--exclude", help="exclude paths from scan",
        dest="exclude", type=re.compile, nargs="*"
    )
    parser.add_argument(
        "--no-regex", help="disable high signal regex checks",
        dest="no_regex", action="store_true"
    )
    parser.add_argument(
        "--no-entropy", help="disable entropy checks",
        dest="no_entropy", action="store_true"
    )
    parser.add_argument(
        "--no-history", help="disable commit history check",
        dest="no_history", action="store_true"
    )
    parser.set_defaults(**core.config.as_dict)
    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(run())  # pragma: no cover
