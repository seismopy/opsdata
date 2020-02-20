"""
Script which runs before generating project.
"""
import re
from pathlib import Path

from cookiecutter.main import cookiecutter

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


def _get_base_name(name):
    """Get a base name, all lower case with spaces."""
    return re.sub('[^a-zA-Z0-9\n]', ' ', name).lower().strip()


def get_snake_name(name):
    """ Convert the name to snake_case. """
    base = _get_base_name(name)
    return base.replace(' ', '_')


def get_camel_name(name):
    """ Convert name to CamelCase."""
    base = _get_base_name(name)
    return base.title().replace(' ', '')


extra_content = dict(
    class_name=get_camel_name(dataset_name),
    module_name=get_snake_name(dataset_name),
)

base_path = Path(__file__).absolute().parent.parent
breakpoint()
cookiecutter('gh:seismopy/opsdata', extra_context=extra_content)




if __name__ == "__main__":
    # first test base names
    assert _get_base_name(' Dude-Anch bill') == 'dude anch bill'
