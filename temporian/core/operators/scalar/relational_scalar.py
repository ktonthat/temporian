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

"""Event/scalar relational operators classes and public API definitions."""

from typing import Union, List

from temporian.core import operator_lib
from temporian.core.data.dtype import DType
from temporian.core.data.node import Node
from temporian.core.data.schema import FeatureSchema
from temporian.core.operators.scalar.base import (
    BaseScalarOperator,
)


class RelationalScalarOperator(BaseScalarOperator):
    DEF_KEY = ""

    def output_feature_dtype(self, feature: FeatureSchema) -> DType:
        # override parent method to always return BOOLEAN features
        return DType.BOOLEAN

    @property
    def supported_value_dtypes(self) -> List[DType]:
        return [
            DType.FLOAT32,
            DType.FLOAT64,
            DType.INT32,
            DType.INT64,
            DType.BOOLEAN,
            DType.STRING,
        ]

    @classmethod
    def operator_def_key(cls) -> str:
        return cls.DEF_KEY


class EqualScalarOperator(RelationalScalarOperator):
    DEF_KEY = "EQUAL_SCALAR"


class NotEqualScalarOperator(RelationalScalarOperator):
    DEF_KEY = "NOT_EQUAL_SCALAR"


class GreaterEqualScalarOperator(RelationalScalarOperator):
    DEF_KEY = "GREATER_EQUAL_SCALAR"


class LessEqualScalarOperator(RelationalScalarOperator):
    DEF_KEY = "LESS_EQUAL_SCALAR"


class GreaterScalarOperator(RelationalScalarOperator):
    DEF_KEY = "GREATER_SCALAR"


class LessScalarOperator(RelationalScalarOperator):
    DEF_KEY = "LESS_SCALAR"


def equal_scalar(
    input: Node,
    value: Union[float, int, str, bool],
) -> Node:
    """Checks for equality between a node and a scalar element-wise.

    Each item in each feature in `input` is compared to `value`.
    Note that if both elements are NaNs, returns False.

    Usage example:
        ```python
        >>> evset = tp.event_set(
        ...     timestamps=[1, 2, 3],
        ...     features={"f1": [0, 100, 200], "f2": [-10, 100, 5]}
        ... )
        >>> a = evset.node()

        >>> # WARN: Don't use this for element-wise comparison
        >>> a == 100
        False

        >>> # Element-wise comparison
        >>> c = tp.equal_scalar(a, 100)
        >>> c.evaluate({a: evset})
        indexes: []
        features: [('f1', bool_), ('f2', bool_)]
        events:
            (3 events):
                timestamps: [1. 2. 3.]
                'f1': [False True False]
                'f2': [False True False]
        ...

        ```

    Args:
        input: Node to compare the value to.
        value: Scalar value to compare to the input.

    Returns:
        Node containing the result of the comparison.
    """
    return EqualScalarOperator(
        input=input,
        value=value,
    ).outputs["output"]


def not_equal_scalar(
    input: Node,
    value: Union[float, int, str, bool],
) -> Node:
    """Checks for differences between a node and a scalar element-wise.

    Each item in each feature in `input` is compared to `value`.
    Note that if both elements are NaNs, returns True.

    Usage example:
        ```python
        >>> evset = tp.event_set(
        ...     timestamps=[1, 2, 3],
        ...     features={"f1": [0, 100, 200], "f2": [-10, 100, 5]}
        ... )
        >>> a = evset.node()

        >>> # Equivalent
        >>> c = tp.not_equal_scalar(a, 100)
        >>> c = a != 100
        >>> c.evaluate({a: evset})
        indexes: []
        features: [('f1', bool_), ('f2', bool_)]
        events:
            (3 events):
                timestamps: [1. 2. 3.]
                'f1': [ True False True]
                'f2': [ True False True]
        ...

        ```

    Args:
        input: Node to compare the value to.
        value: Scalar value to compare to the input.

    Returns:
        Node containing the result of the comparison.
    """
    return NotEqualScalarOperator(
        input=input,
        value=value,
    ).outputs["output"]


def greater_equal_scalar(
    input: Node,
    value: Union[float, int, str, bool],
) -> Node:
    """Check if the input node is greater or equal than a scalar element-wise.

    Each item in each feature in `input` is compared to `value`.
    Note that it will always return False on NaN elements.

    Usage example:
        ```python
        >>> evset = tp.event_set(
        ...     timestamps=[1, 2, 3],
        ...     features={"f1": [0, 100, 200], "f2": [-10, 100, 5]}
        ... )
        >>> a = evset.node()

        >>> # Equivalent
        >>> c = tp.greater_equal_scalar(a, 100)
        >>> c = a >= 100
        >>> c.evaluate({a: evset})
        indexes: []
        features: [('f1', bool_), ('f2', bool_)]
        events:
            (3 events):
                timestamps: [1. 2. 3.]
                'f1': [False True True]
                'f2': [False True False]
        ...

        ```

    Args:
        input: Node to compare the value to.
        value: Scalar value to compare to the input.

    Returns:
        Node containing the result of the comparison.
    """
    return GreaterEqualScalarOperator(
        input=input,
        value=value,
    ).outputs["output"]


def less_equal_scalar(
    input: Node,
    value: Union[float, int, str, bool],
) -> Node:
    """Check if the input node is less or equal than a scalar element-wise.

    Each item in each feature in `input` is compared to `value`.
    Note that it will always return False on NaN elements.

    Usage example:
        ```python
        >>> evset = tp.event_set(
        ...     timestamps=[1, 2, 3],
        ...     features={"f1": [0, 100, 200], "f2": [-10, 100, 5]}
        ... )
        >>> a = evset.node()

        >>> # Equivalent
        >>> c = tp.less_equal_scalar(a, 100)
        >>> c = a <= 100
        >>> c.evaluate({a: evset})
        indexes: []
        features: [('f1', bool_), ('f2', bool_)]
        events:
            (3 events):
                timestamps: [1. 2. 3.]
                'f1': [ True True False]
                'f2': [ True True True]
        ...

        ```

    Args:
        input: Node to compare the value to.
        value: Scalar value to compare to the input.

    Returns:
        Node containing the result of the comparison.
    """
    return LessEqualScalarOperator(
        input=input,
        value=value,
    ).outputs["output"]


def greater_scalar(
    input: Node,
    value: Union[float, int, str, bool],
) -> Node:
    """Check if the input node is greater than a scalar element-wise.

    Each item in each feature in `input` is compared to `value`.
    Note that it will always return False on NaN elements.

    Usage example:
        ```python
        >>> evset = tp.event_set(
        ...     timestamps=[1, 2, 3],
        ...     features={"f1": [0, 100, 200], "f2": [-10, 100, 5]}
        ... )
        >>> a = evset.node()

        >>> # Equivalent
        >>> c = tp.greater_scalar(a, 100)
        >>> c = a > 100
        >>> c.evaluate({a: evset})
        indexes: []
        features: [('f1', bool_), ('f2', bool_)]
        events:
            (3 events):
                timestamps: [1. 2. 3.]
                'f1': [False False True]
                'f2': [False False False]
        ...

        ```

    Args:
        input: Node to compare the value to.
        value: Scalar value to compare to the input.

    Returns:
        Node containing the result of the comparison.
    """
    return GreaterScalarOperator(
        input=input,
        value=value,
    ).outputs["output"]


def less_scalar(
    input: Node,
    value: Union[float, int, str, bool],
) -> Node:
    """Check if the input node is less than a scalar element-wise.

    Each item in each feature in `input` is compared to `value`.
    Note that it will always return False on NaN elements.

    Usage example:
        ```python
        >>> evset = tp.event_set(
        ...     timestamps=[1, 2, 3],
        ...     features={"f1": [0, 100, 200], "f2": [-10, 100, 5]}
        ... )
        >>> a = evset.node()

        >>> # Equivalent
        >>> c = tp.less_scalar(a, 100)
        >>> c = a < 100
        >>> c.evaluate({a: evset})
        indexes: []
        features: [('f1', bool_), ('f2', bool_)]
        events:
            (3 events):
                timestamps: [1. 2. 3.]
                'f1': [ True False False]
                'f2': [ True False True]
        ...

        ```

    Args:
        input: Node to compare the value to.
        value: Scalar value to compare to the input.

    Returns:
        Node containing the result of the comparison.
    """
    return LessScalarOperator(
        input=input,
        value=value,
    ).outputs["output"]


operator_lib.register_operator(EqualScalarOperator)
operator_lib.register_operator(NotEqualScalarOperator)
operator_lib.register_operator(GreaterEqualScalarOperator)
operator_lib.register_operator(LessEqualScalarOperator)
operator_lib.register_operator(GreaterScalarOperator)
operator_lib.register_operator(LessScalarOperator)
