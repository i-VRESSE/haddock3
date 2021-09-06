#!/usr/bin/env python3
import argparse
import logging
import sys
from argparse import ArgumentTypeError
from functools import partial

from haddock.version import CURRENT_VERSION
from haddock.libs.libutil import file_exists, non_negative_int


# Command line interface parser
ap = argparse.ArgumentParser()

_arg_file_exist = partial(
    file_exists,
    exception=ArgumentTypeError,
    emsg="File {!r} does not exist or is not a file.")
ap.add_argument(
    "recipe",
    type=_arg_file_exist,
    help="The input recipe file path",
    )

_arg_pos_int = partial(
    non_negative_int,
    exception=ArgumentTypeError,
    emsg="Minimum value is 0, {!r} given.",
    )
ap.add_argument(
    "--restart",
    type=_arg_pos_int,
    default=0,
    help="Restart the recipe from this course",
    )

ap.add_argument(
    "--setup",
    help="Only setup the run, do not execute",
    action="store_true",
    dest='setup_only',
    )

_log_levels = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
ap.add_argument(
    "--log-level",
    default="INFO",
    choices=_log_levels,
    )

ap.add_argument(
    "-v",
    "--version",
    help="show version",
    action="version",
    version=f'{ap.prog} - {CURRENT_VERSION}',
    )


def load_args(ap):
    """Load argument parser args."""
    return ap.parse_args()


def cli(ap, main):
    """Command-line interface entry point."""
    cmd = load_args(ap)
    main(**vars(cmd))


def maincli():
    """Main client execution."""
    cli(ap, main)


def main(
        recipe,
        restart=0,
        setup_only=False,
        log_level="INFO",
        ):
    """
    Execute HADDOCK3 client logic.

    Parameters
    ----------
    recipe : str or pathlib.Path
        The path to the recipe (config file).

    restart : int
        At which step to restart haddock3 run.

    setup_only : bool
        Whether to setup the run without running it.

    log_level : str
        The logging level: INFO, DEBUG, ERROR, WARNING, CRITICAL.
    """
    # anti-pattern to speed up CLI initiation
    from haddock.workflow import WorkflowManager
    from haddock.gear.greetings import get_adieu, get_initial_greeting
    from haddock.gear.prepare_run import setup_run
    from haddock.error import HaddockError, ConfigurationError

    # Configuring logging
    logging.basicConfig(
        level=log_level,
        format="[%(asctime)s] %(name)s:L%(lineno)d %(levelname)s - %(message)s",
        )

    # Special case only using print instead of logging
    logging.info(get_initial_greeting())

    try:
        params, other_params = setup_run(recipe)

    except ConfigurationError as err:
        logging.error(err)
        sys.exit()

    if not setup_only:
        try:
            workflow = WorkflowManager(
                workflow_params=params,
                start=restart,
                **other_params,
                )

            # Main loop of execution
            workflow.run()

        except HaddockError as err:
            logging.error(err)

    # Finish
    logging.info(get_adieu())


if __name__ == "__main__":
    sys.exit(maincli())
