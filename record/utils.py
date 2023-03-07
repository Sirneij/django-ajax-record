import os
import re
from pathlib import Path


class FilePermissionError(Exception):
    """The key file permissions are insecure."""
    pass


quote_match = re.compile(r'''[^"]*"(.+)"''').match
match_setting = re.compile(r'^(?P<name>[A-Z][A-Z_0-9]+)\s?=\s?(?P<value>.*)').match
aliases = {'true': True, 'on': True, 'false': False, 'off': False}


def load_env(path: Path):
    """
    >>>
    """
    if not path.exists():
        return

    path = path.resolve()

    content = path.read_text()

    for line in content.split('\n'):
        line = line.strip()

        if not line:
            continue

        if line.startswith('#'):
            continue
        match = match_setting(line)

        if not match:
            continue

        name, value = match.groups()
        quoted = quote_match(value)

        if quoted:
            # Convert 'a', "a" to a, a
            value = str(quoted.groups()[0])

        if name in aliases:
            value = aliases[name]

        # Replace placeholders like ${PATH}
        for match_replace in re.findall(r'(\${([\w\d\-_]+)})', value):
            replace, name = match_replace
            value = value.replace(replace, os.environ.get(name, ''))

        # Set environment value
        os.environ[name] = value