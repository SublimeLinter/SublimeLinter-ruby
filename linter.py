#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Aparajita Fishman
# Copyright (c) 2015 The SublimeLinter Community
#
# License: MIT
#

"""This module exports the Ruby plugin class."""

from SublimeLinter.lint import RubyLinter


class Ruby(RubyLinter):

    """Provides an interface to ruby -wc."""

    syntax = ('ruby', 'ruby on rails', 'rspec')
    cmd = 'ruby -wc'
    regex = (
        r'^(?P<file>.+?):(?P<line>\d+): (?:(?P<error>.*?error)|(?P<warning>warning))[,:] (?P<message>[^\r\n]+)\r?\n'
        r'(?:^[^\r\n]+\r?\n^(?P<col>.*?)\^)?'
    )
    multiline = True
    comment_re = r'\s*#'

    def split_match(self, match):
        """
        Return the components of the match.

        We override this because unrelated library files can throw errors,
        and we only want errors from the linted file.

        """

        if match:
            if match.group('file') != '-':
                match = None

        return super().split_match(match)
