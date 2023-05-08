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

"""Less scalar operator class and public API function definition."""

from typing import Union, List

from temporian.core import operator_lib
from temporian.core.data.dtype import DType
from temporian.core.data.node import Node
from temporian.core.data.feature import Feature
from temporian.core.operators.arithmetic_scalar.base import (
    BaseArithmeticScalarOperator,
)

# TODO: Rename operator to "lesser" or remove this todo. Note: Numpy uses
# greater / less for comparison operators.


class LessScalarOperator(BaseArithmeticScalarOperator):
    @classmethod
    @property
    def operator_def_key(cls) -> str:
        return "LESS_SCALAR"

    def output_feature_dtype(self, feature: Feature) -> DType:
        # override parent method to always return BOOLEAN features
        return DType.BOOLEAN

    @property
    def supported_value_dtypes(self) -> List[DType]:
        return [
            DType.FLOAT32,
            DType.FLOAT64,
            DType.INT32,
            DType.INT64,
        ]


operator_lib.register_operator(LessScalarOperator)


def less_scalar(
    input: Node,
    value: Union[float, int, str, bool],
) -> Node:
    """Computes event < value.

    Args:
        event: Event to compare the value to.
        value: Scalar value to compare to the event.

    Returns:
        Event containing the result of the computation.
    """
    return LessScalarOperator(
        input=input,
        value=value,
    ).outputs["output"]