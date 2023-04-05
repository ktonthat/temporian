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

import numpy as np

from temporian.implementation.numpy import implementation_lib
from temporian.core.operators.window.moving_sum import (
    MovingSumOperator,
)
from temporian.implementation.numpy.operators.window.base import (
    BaseWindowNumpyImplementation,
)


class MovingSumNumpyImplementation(BaseWindowNumpyImplementation):
    """Numpy implementation of the moving sum operator."""

    def __init__(self, operator: MovingSumOperator) -> None:
        super().__init__(operator)

    def _apply_operation(self, values: np.array) -> np.array:
        """
        Calculates the sum of the values in each row of the input array.

        The input array should have a shape (n, m), where 'n' is the length of
        the feature and 'm' is the size of the window. Each row represents a
        window of data points, with 'nan' values used for padding when the
        window size is  smaller than the number of data points in the time
        series. The function  computes the sum for each row (window) by ignoring
        the 'nan' values.

        Args:
            values: A 2D NumPy array with shape (n, m) where each row represents
                a  window of data points. 'n' is the length of the feature, and
                'm' is the size of the window. The array can contain 'nan'
                values as padding.

        Returns:
            np.array: A 1D NumPy array with shape (n,) containing the sum for
                    each row (window) in the input array.

        """
        # compute the sum for each row ignoring the np.nan values
        result = np.nansum(values, axis=1)
        # check which rows are all np.nan
        all_nan_rows = np.isnan(values).all(axis=1)
        # set the result for those rows to np.nan
        result[all_nan_rows] = np.nan
        return result


implementation_lib.register_operator_implementation(
    MovingSumOperator, MovingSumNumpyImplementation
)