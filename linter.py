#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Aparajita Fishman
# Copyright (c) 2015-2016 The SublimeLinter Community
# Copyright (c) 2013-2014 Aparajita Fishman
#
# License: MIT
#

"""This module exports the Ruby plugin class."""

from SublimeLinter.lint import RubyLinter
import re


class Ruby(RubyLinter):
    """Provides an interface to ruby -wc."""

    defaults = {
        'selector': 'source.ruby'
    }

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

        match, line, col, error, warning, message, _ = super().split_match(match)
        near = self.search_token(message)

        return match, line, col, error, warning, message, near

    def search_token(self, message):
        """Search text token to be highlighted."""

        # First search for variable name enclosed in quotes
        m = re.search("(?<=`).*(?=')", message)

        # Then search for variable name following a dash
        if m is None:
            m = re.search('(?<= - )\S+', message)

        # Then search for mismatched indentation
        if m is None:
            m = re.search("(?<=mismatched indentations at ')end", message)

        # Then search for equal operator in conditional
        if m is None:
            m = re.search('(?<=found )=(?= in conditional)', message)

        # Then search for use of operator in void context
        if m is None:
            m = re.search('\S+(?= in void context)', message)

        # Then search for END in method
        if m is None:
            m = re.search('END(?= in method)', message)

        return m.group(0) if m else None
