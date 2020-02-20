"""
Script which runs before generating project.
"""
import re
import sys

dataset_name = "{{ cookiecutter.dataset_name }}"

MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"

if not re.match(MODULE_REGEX, dataset_name):
    msg = (f"ERROR: The project slug {dataset_name} is not a valid Python "
           f"module name. Please do not use a - and use _ instead")
    print(msg)
    sys.exit(1)

#  TODO Pick this back up, need to find way to modify context in hook.
# def _camel2snake(name):
#     """
#     Convert CamelCase to snake_case.
#     """
#     s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
#     s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
#     return s2
#
#
# def _snake2camel(name):
#     """Convert snake_case to CamelCase."""
#     out = (
#         name
#             .replace('_', ' ')
#             .title()
#             .replace(' ', '')
#     )
#     return out
#
#
# def _get_base_name(name):
#     """Get a base name, all lower case with spaces."""
#     return re.sub('[^a-zA-Z0-9\n]', ' ', name).lower().strip()
#
#
# def get_snake_name(name):
#     """ Convert the name to snake_case. """
#     base = _get_base_name(name)
#     return base.replace(' ', '_')
#
#
# def get_camel_name(name):
#     """ Convert name to CamelCase."""
#     base = _get_base_name(name)
#     return base.title().replace(' ', '')
#
#
# extra_content = dict(
#     class_name=get_camel_name(dataset_name),
#     module_name=get_snake_name(dataset_name),
# )
#
# base_path = Path(__file__).absolute().parent.parent
# breakpoint()
# cookiecutter('gh:seismopy/opsdata', extra_context=extra_content)
#
#
#
#
# if __name__ == "__main__":
#     # first test base names
#     assert
#     assert _get_base_name(' Dude-Anch bill') == 'dude anch bill'
