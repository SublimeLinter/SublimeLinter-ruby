#
# linter.py
# Linter for SublimeLinter, a code checking framework for Sublime Text
#
# Written by Aparajita Fishman
# Copyright (c) 2015-2025 The SublimeLinter Community
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
        'selector': 'source.ruby - text.html'
    }

    cmd = 'ruby -wc'
    regex = r"""
        (?xm)
        ^(?:(?P<exe>.*:\s)?)?                # optional "C:/ruby...:" prefix
        (?P<filename>.+?):(?P<line>\d+):     # file and line
        (?:\s?(?:(?P<error>.*?error)s?|(?P<warning>warning))) # "syntax error" or warning
        [,:]?\s(?P<message>[^\n]+)           # headline message
        (?:\n                                # optional multiline block
            (?:
              (?:\s*\d+\s*\|[^\n]*\n)*       # optional leading context lines
              >\s*(?P<culprit_line>\d+)\s*\|[^\n]*\n # culprit line
              \s*\|\s(?P<col>.*?)\^\s        # caret line with message
              (?P<culprit_message>[^\n]*)    # rest of caret line (error text)
            )?
        )?
    """
    on_stderr = None

    def split_match(self, match):
        """
        Return the error as matched by the regex.

        We override this for a better error message.
        """

        error = super().split_match(match)
        if culprit_message := error.get("culprit_message", None):
            error["message"] = culprit_message
        error["near"] = self.search_token(error.message)
        if error.error:
            error["error"] = error.error.replace(" ", "-")

        return error

    def search_token(self, message):
        """Search text token to be highlighted."""

        # First search for variable name enclosed in quotes
        m = re.search(r"(?<=`).*(?=')", message)

        # Then search for variable name following a dash
        if m is None:
            m = re.search(r'(?<= - )\S+', message)

        # Then search for mismatched indentation
        if m is None:
            m = re.search(r"(?<=mismatched indentations at ')end", message)

        # Then search for equal operator in conditional
        if m is None:
            m = re.search(r'(?<=found )=(?= in conditional)', message)

        # Then search for use of operator in void context
        if m is None:
            m = re.search(r'\S+(?= in void context)', message)

        # Then search for END in method
        if m is None:
            m = re.search(r'END(?= in method)', message)

        return m.group(0) if m else None
