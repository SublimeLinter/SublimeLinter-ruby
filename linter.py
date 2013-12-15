#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Aparajita Fishman
# Copyright (c) 2013 Aparajita Fishman
#
# License: MIT
#

"""This module exports the Ruby plugin class."""

from SublimeLinter.lint import Linter, util


class Ruby(Linter):

    """Provides an interface to ruby -wc."""

    syntax = 'ruby'
    cmd = 'ruby -wc'
    regex = (
        r'^.+?:(?P<line>\d+):.+?, (?P<message>[^\r\n]+)\r?\n'
        r'(?:^[^\r\n]+\r?\n^(?P<col>.*?)\^)?'
    )
    multiline = True
    error_stream = util.STREAM_STDERR
    comment_re = r'\s*#'
