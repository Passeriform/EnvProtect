"""Result type class for subscripting different result types."""

from __future__ import annotations
from typing import TypeVar, List, Optional, Generic, Union, Type

# pylint: disable=invalid-name
K = TypeVar('K')
E = TypeVar('E', bound=Exception)
# pylint: enable=invalid-name


class Result(Generic[K, E]):
    """Define result type and associated utility methods."""

    def __init__(self, ok: K, exception: Optional[List[E]]) -> None:
        """Initialize a result object.

        Args:
            ok: The ok element for result.
            exception: Exception collection for result.
        """
        self.ok = ok
        self.exception = exception

    def __getitem__(self, key: Union[int, str]) -> Union[K, Optional[List[E]]]:
        """Define __getitem__ method to access using `int` or `str`.

        Args:
            key: Accessor key for getting item.

        Returns:
            An element of Result.
        """
        if isinstance(key, int) and key in [0, 1]:
            return self.ok if key == 0 else self.exception

        if isinstance(key, str) and key in ["ok", "exception"]:
            q_attr: Union[K, Optional[List[E]]] = getattr(self, key)
            return q_attr

        raise LookupError("""
The indexing key used is either not a known one or of an unsupported type.
        """)

    def __setitem__(self, key: Union[int, str], value: Union[K, List[E]]) -> None:
        """Define __setitem__ method to set ok and exception.

        Args:
            key: Accessor key for getting item.
            value: Accessor value to be set to key field.
        """
        if isinstance(key, int) and key in [0, 1]:
            key = "ok" if key == 0 else "exception"

        if isinstance(key, str) and key in ["ok", "exception"]:
            setattr(self, key, value)
        else:
            raise LookupError("""
The indexing key used is either not a known one or of an unsupported type.
            """)

    def get_nested_str(self, root: Optional[Result[K, E]] = None, level: int = 0) -> str:
        """Format nested string representation.

        Args:
            root: Root result element to start getting nested tree from.
            level: Maintains level of tree explored. Used for prepending string representation.

        Returns:
            String representation for the result tree/subtree.
        """
        if root is None:
            root = self

        if not isinstance(root.ok, self.__class__):
            formatted_output: str = f"""
                [{type(root)}]
                | => {{root.meta}}
                | => {root.ok}
                \\-[{type(root.exception)}]
                  => {root.exception}
            """
            return "\n".join([f"""{"| " * level}{line}""" for line in formatted_output.split("\n")])

        formatted_output = f"""
            [{type(root)}]
            | => {{root.meta}}
            +-{self.get_nested_str(root=root.ok, level=level + 1)}
            \\-[{type(root.exception)}]
              => {root.exception}
            """

        return "\n".join([f"""{"| " * level}{line}""" for line in formatted_output.split("\n")])

    def __str__(self) -> str:
        r"""Serialize Result object into nested tree string representation.

        Returns:
            String represenation for result type. The example representation is as follows:
                [Result]
                \\-[{type(self)}]
                  | => {self.meta}
                  +-[{type(self.ok)}]
                  | | => {self.ok.meta}
                  | +-[{type(self.ok.ok)}]
                  | | | => {self.ok.ok.meta}
                  | | | => {self.ok.ok.ok}<only if its not a ResultType>
                  | | \\-[{type(self.ok.ok.exception)}]
                  | |   => {self.ok.ok.exception}
                  | \\-[{type(self.ok.exception)}]
                  |   => {self.ok.exception}
                  \\-[{type(self.exception)}]
                    => {self.exception}
        """
        header = "[Result]\n"
        return header + self.get_nested_str()


ResultType = Type[Result]
