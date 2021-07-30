"""Utility helper module.

Basic helper utility methods.
"""


from typing import Tuple, TypeVar

# pylint: disable=invalid-name
T = TypeVar('T')
# pylint: enable=invalid-name


def unzip(zipped_list: Tuple[Tuple[T]]) -> Tuple[Tuple[T], ...]:
    """Unzips a list of values into pairwise list.

    [(a, b), (c, d), (e, f)] => ([a, c, e], [b, d, f])

    Args:
        zipped_list (Tuple[Tuple[T], ...]): list of values

    Returns:
        (Tuple[T, ...]): A pairwise list
    """
    return tuple(zip(*zipped_list))
