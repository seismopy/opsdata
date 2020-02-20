"""
Script which runs before generating project.
"""
import re
import sys

from cookiecutter.main import cookiecutter



MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"

dataset_name = "{{ cookiecutter.dataset_name }}"


def _camel2snake(name):
    """
    Convert CamelCase to snake_case.
    """
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
    return s2


def _snake2camel(name):
    """Convert snake_case to CamelCase."""
    out = (
        name
        .replace('_', ' ')
        .title()
        .replace(' ', '')
    )
    return out


class_name = ''  # TODO get class name
module_name = ''  # TODO get module name


# if not re.match(MODULE_REGEX, module_name):
#     print(
#         "ERROR: The project slug (%s) is not a valid Python module name. Please do not use a - and use _ instead"
#         % module_name
#     )
#     # Exit to cancel project
#     sys.exit(1)
