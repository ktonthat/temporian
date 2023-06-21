# Copyright 2021 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Event/scalar arithmetic operators classes and public API definitions."""

from typing import Union

from temporian.core import operator_lib
from temporian.core.data.dtypes.dtype import DType
from temporian.core.data.node import Node
from temporian.core.operators.scalar.base import (
    BaseScalarOperator,
)

SCALAR = Union[float, int]


class AddScalarOperator(BaseScalarOperator):
    DEF_KEY = "ADDITION_SCALAR"


class SubtractScalarOperator(BaseScalarOperator):
    DEF_KEY = "SUBTRACTION_SCALAR"


class MultiplyScalarOperator(BaseScalarOperator):
    DEF_KEY = "MULTIPLICATION_SCALAR"


class FloorDivScalarOperator(BaseScalarOperator):
    DEF_KEY = "FLOORDIV_SCALAR"


class ModuloScalarOperator(BaseScalarOperator):
    DEF_KEY = "MODULO_SCALAR"


class PowerScalarOperator(BaseScalarOperator):
    DEF_KEY = "POWER_SCALAR"


class DivideScalarOperator(BaseScalarOperator):
    DEF_KEY = "DIVISION_SCALAR"

    def __init__(
        self,
        input: Node,
        value: Union[float, int],
        is_value_first: bool = False,
    ):
        super().__init__(input, value, is_value_first)

        for feat in input.schema.features:
            if feat.dtype in [DType.INT32, DType.INT64]:
                raise ValueError(
                    "Cannot use the divide operator on feature "
                    f"{feat.name} of type {feat.dtype}. Cast to a "
                    "floating point type or use floordiv operator (//)."
                )


def add_scalar(
    input: Node,
    value: Union[float, int],
) -> Node:
    """Adds a scalar value to a node.

    `value` is added to each item in each feature in `input`.

    Usage example:
        ```python
        >>> evset = tp.event_set(
        ...     timestamps=[1, 2, 3],
        ...     features={"f1": [0, 100, 200], "f2": [10, -10, 5]}
        ... )
        >>> a = evset.node()

        >>> # Equivalent
        >>> c = tp.add_scalar(a, 3)
        >>> c = a + 3
        >>> c.evaluate({a: evset})
        indexes: ...
                timestamps: [1. 2. 3.]
                'f1': [ 3 103 203]
                'f2': [13 -7 8]
        ...

        ```

    Args:
        input: Node to add a scalar to.
        value: Scalar value to add to the input.

    Returns:
        Addition of `input` and `value`.
    """
    return AddScalarOperator(
        input=input,
        value=value,
    ).outputs["output"]


def subtract_scalar(
    minuend: Union[Node, SCALAR],
    subtrahend: Union[Node, SCALAR],
) -> Node:
    """Subtracts a node and a scalar value.

    Each item in each feature in the node is subtracted with the scalar value.

    Either `minuend` or `subtrahend` should be a scalar value, but not both. If
    looking to subtract two nodes, use the `subtract` operator instead.

    Usage example:
        ```python
        >>> evset = tp.event_set(
        ...     timestamps=[1, 2, 3],
        ...     features={"f1": [0, 100, 200], "f2": [10, -10, 5]}
        ... )
        >>> a = evset.node()

        >>> # Equivalent
        >>> c = tp.subtract_scalar(a, 3)
        >>> c = a - 3
        >>> c.evaluate({a: evset})
        indexes: ...
                timestamps: [1. 2. 3.]
                'f1': [ -3  97 197]
                'f2': [ 7 -13   2]
        ...

        >>> # Equivalent
        >>> c = tp.subtract_scalar(3, a)
        >>> c = 3 - a
        >>> c.evaluate({a: evset})
        indexes: ...
                timestamps: [1. 2. 3.]
                'f1': [ 3  -97 -197]
                'f2': [-7 13  -2]
        ...

        ```

    Args:
        minuend: Node or scalar value being subtracted from.
        subtrahend: Node or scalar number being subtracted.

    Returns:
        Node with the difference between the minuend and subtrahend.
    """
    scalars_types = (float, int)

    if isinstance(minuend, Node) and isinstance(subtrahend, scalars_types):
        return SubtractScalarOperator(
            input=minuend,
            value=subtrahend,
            is_value_first=False,
        ).outputs["output"]

    if isinstance(minuend, scalars_types) and isinstance(subtrahend, Node):
        return SubtractScalarOperator(
            input=subtrahend,
            value=minuend,
            is_value_first=True,
        ).outputs["output"]

    raise ValueError(
        "Invalid input types for subtract_scalar. "
        "Expected (Node, SCALAR) or (SCALAR, Node), "
        f"got ({type(minuend)}, {type(subtrahend)})."
    )


def multiply_scalar(
    input: Node,
    value: Union[float, int],
) -> Node:
    """Multiplies a node by a scalar value.

    Each item in each feature in `input` is multiplied by `value`.

    Usage example:
        ```python
        >>> evset = tp.event_set(
        ...     timestamps=[1, 2, 3],
        ...     features={"f1": [0, 100, 200], "f2": [10, -10, 5]}
        ... )
        >>> a = evset.node()

        >>> # Equivalent
        >>> c = tp.multiply_scalar(a, 2)
        >>> c = a * 2
        >>> c.evaluate({a: evset})
        indexes: ...
                timestamps: [1. 2. 3.]
                'f1': [ 0 200 400]
                'f2': [ 20 -20 10]
        ...

        ```

    Args:
        input: Node to multiply.
        value: Scalar value to multiply the input by.

    Returns:
        Integer division of `input` and `value`.
    """
    return MultiplyScalarOperator(
        input=input,
        value=value,
    ).outputs["output"]


def divide_scalar(
    numerator: Union[Node, SCALAR],
    denominator: Union[Node, SCALAR],
) -> Node:
    """Divides a node and a scalar value.

    Each item in each feature in the node is divided with the scalar value.

    Either `numerator` or `denominator` should be a scalar value, but not both.
    If looking to divide two nodes, use the `divide` operator instead.

    Usage example:
        ```python
        >>> evset = tp.event_set(
        ...     timestamps=[1, 2, 3],
        ...     features={"f1": [0., 100., 200.], "f2": [10., -10., 5.]}
        ... )
        >>> a = evset.node()

        >>> # Equivalent
        >>> c = tp.divide_scalar(a, 2)
        >>> c = a / 2
        >>> c.evaluate({a: evset})
        indexes: ...
                timestamps: [1. 2. 3.]
                'f1': [ 0. 50. 100.]
                'f2': [ 5. -5. 2.5]
        ...

        >>> # Equivalent
        >>> c = tp.divide_scalar(1000, a)
        >>> c = 1000 / a
        >>> c.evaluate({a: evset})
        indexes: ...
                timestamps: [1. 2. 3.]
                'f1': [inf 10. 5.]
                'f2': [ 100. -100. 200.]
        ...

        ```

    Args:
        numerator: Numerator node or value.
        denominator: Denominator node or value.

    Returns:
        Division of `numerator` and `denominator`.
    """
    scalars_types = (float, int)

    if isinstance(numerator, Node) and isinstance(denominator, scalars_types):
        return DivideScalarOperator(
            input=numerator,
            value=denominator,
            is_value_first=False,
        ).outputs["output"]

    if isinstance(numerator, scalars_types) and isinstance(denominator, Node):
        return DivideScalarOperator(
            input=denominator,
            value=numerator,
            is_value_first=True,
        ).outputs["output"]

    raise ValueError(
        "Invalid input types for divide_scalar. "
        "Expected (Node, SCALAR) or (SCALAR, Node), "
        f"got ({type(numerator)}, {type(denominator)})."
    )


def floordiv_scalar(
    numerator: Union[Node, SCALAR],
    denominator: Union[Node, SCALAR],
) -> Node:
    """Divides a node and a scalar and takes the result's floor.

    Each item in each feature in the node is divided with the scalar value.

    Either `numerator` or `denominator` should be a scalar value, but not both.
    If looking to floordiv two nodes, use the `floordiv` operator instead.

    Usage example:
        ```python
        >>> evset = tp.event_set(
        ...     timestamps=[1, 2, 3],
        ...     features={"f1": [1, 100, 200], "f2": [10., -10., 5.]}
        ... )
        >>> a = evset.node()

        >>> # Equivalent
        >>> c = tp.floordiv_scalar(a, 3)
        >>> c = a // 3
        >>> c.evaluate({a: evset})
        indexes: ...
                timestamps: [1. 2. 3.]
                'f1': [ 0 33 66]
                'f2': [ 3. -4. 1.]
        ...

        >>> # Equivalent
        >>> c = tp.floordiv_scalar(300, a)
        >>> c = 300 // a
        >>> c.evaluate({a: evset})
        indexes: ...
                timestamps: [1. 2. 3.]
                'f1': [300 3 1]
                'f2': [ 30. -30. 60.]
        ...

        ```

    Args:
        numerator: Numerator node or value.
        denominator: Denominator node or value.

    Returns:
        Integer division of `numerator` and `denominator`.
    """
    scalars_types = (float, int)

    if isinstance(numerator, Node) and isinstance(denominator, scalars_types):
        return FloorDivScalarOperator(
            input=numerator,
            value=denominator,
            is_value_first=False,
        ).outputs["output"]

    if isinstance(numerator, scalars_types) and isinstance(denominator, Node):
        return FloorDivScalarOperator(
            input=denominator,
            value=numerator,
            is_value_first=True,
        ).outputs["output"]

    raise ValueError(
        "Invalid input types for floordiv_scalar. "
        "Expected (Node, SCALAR) or (SCALAR, Node), "
        f"got ({type(numerator)}, {type(denominator)})."
    )


def modulo_scalar(
    numerator: Union[Node, SCALAR],
    denominator: Union[Node, SCALAR],
) -> Node:
    """Remainder of the division of numerator by denominator.

    Either `numerator` or `denominator` should be a scalar value, but not both.
    For the operation between two nodes, use the `modulo` operator instead.

    Usage example:
        ```python
        >>> evset = tp.event_set(
        ...     timestamps=[1, 2, 3],
        ...     features={"f1": [1, 100, 200], "f2": [10., -10., 5.]}
        ... )
        >>> a = evset.node()

        >>> # Equivalent
        >>> c = tp.modulo_scalar(a, 3)
        >>> c = a % 3
        >>> c.evaluate({a: evset})
        indexes: ...
                timestamps: [1. 2. 3.]
                'f1': [1 1 2]
                'f2': [1. 2. 2.]
        ...

        >>> # Equivalent
        >>> c = tp.floordiv_scalar(300, a)
        >>> c = 300 % a
        >>> c.evaluate({a: evset})
        indexes: ...
                timestamps: [1. 2. 3.]
                'f1': [ 0 0 100]
                'f2': [ 0. -0. 0.]
        ...

        ```

    Args:
        numerator: Node or scalar to divide.
        denominator: Node or scalar to divide by.

    Returns:
        Remainder of the integer division.
    """
    scalar_types = (float, int)

    if isinstance(numerator, Node) and isinstance(denominator, scalar_types):
        return ModuloScalarOperator(
            input=numerator,
            value=denominator,
            is_value_first=False,
        ).outputs["output"]

    if isinstance(numerator, scalar_types) and isinstance(denominator, Node):
        return ModuloScalarOperator(
            input=denominator,
            value=numerator,
            is_value_first=True,
        ).outputs["output"]

    raise ValueError(
        "Invalid input types for modulo_scalar. "
        "Expected (Node, SCALAR) or (SCALAR, Node), "
        f"got ({type(numerator)}, {type(denominator)})."
    )


def power_scalar(
    base: Union[Node, SCALAR],
    exponent: Union[Node, SCALAR],
) -> Node:
    """Raise the base to the exponent (`base ** exponent`)

    Either `base` or `exponent` should be a scalar value, but not both.
    For the operation between two nodes, use the `power` operator instead.

    Usage example:
        ```python
        >>> evset = tp.event_set(
        ...     timestamps=[1, 2, 3],
        ...     features={"f1": [0, 2, 3], "f2": [1., 2., 3.]}
        ... )
        >>> a = evset.node()

        >>> # Equivalent
        >>> c = tp.power_scalar(a, 3)
        >>> c = a ** 3
        >>> c.evaluate({a: evset})
        indexes: ...
                timestamps: [1. 2. 3.]
                'f1': [ 0 8 27]
                'f2': [ 1. 8. 27.]
        ...

        >>> # Equivalent
        >>> c = tp.power_scalar(3, a)
        >>> c = 3 ** a
        >>> c.evaluate({a: evset})
        indexes: ...
                timestamps: [1. 2. 3.]
                'f1': [ 1 9 27]
                'f2': [ 3. 9. 27.]
        ...

        ```

    Args:
        base: Node or scalar to raise to the exponent
        exponent: Node or scalar for the exponent

    Returns:
        base values raised to the exponent
    """
    scalar_types = (float, int)

    if isinstance(base, Node) and isinstance(exponent, scalar_types):
        return PowerScalarOperator(
            input=base,
            value=exponent,
            is_value_first=False,
        ).outputs["output"]

    if isinstance(base, scalar_types) and isinstance(exponent, Node):
        return PowerScalarOperator(
            input=exponent,
            value=base,
            is_value_first=True,
        ).outputs["output"]

    raise ValueError(
        "Invalid input types for power_scalar. "
        "Expected (Node, SCALAR) or (SCALAR, Node), "
        f"got ({type(base)}, {type(exponent)})."
    )


operator_lib.register_operator(SubtractScalarOperator)
operator_lib.register_operator(AddScalarOperator)
operator_lib.register_operator(MultiplyScalarOperator)
operator_lib.register_operator(DivideScalarOperator)
operator_lib.register_operator(FloorDivScalarOperator)
operator_lib.register_operator(ModuloScalarOperator)
operator_lib.register_operator(PowerScalarOperator)
