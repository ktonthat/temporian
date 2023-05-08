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

"""Moving count operator class and public API function definition."""

from typing import Optional

from temporian.core import operator_lib
from temporian.core.data.dtype import DType
from temporian.core.data.duration import Duration
from temporian.core.data.node import Node
from temporian.core.data.feature import Feature
from temporian.core.operators.window.base import BaseWindowOperator


class MovingMaxOperator(BaseWindowOperator):
    @classmethod
    @property
    def operator_def_key(cls) -> str:
        return "MOVING_MAX"

    def get_feature_dtype(self, feature: Feature) -> DType:
        return feature.dtype


operator_lib.register_operator(MovingMaxOperator)


def moving_max(
    input: Node,
    window_length: Duration,
    sampling: Optional[Node] = None,
) -> Node:
    """Computes the maximum in a sliding window over the event.

    For each t in sampling, and for each feature independently, returns at time
    t the max of non-nan values for the feature in the window
    [t - window_length, t].

    If `sampling` is provided samples the moving window's value at each
    timestamp in `sampling`, else samples it at each timestamp in `event`.

    If the window does not contain any values (e.g., all the values are missing,
    or the window does not contain any sampling), outputs missing values.

    Args:
        event: Event for which to count the number of values in each feature.
        window_length: Sliding window's length.
        sampling: Timestamps to sample the sliding window's value at. If not
            provided, timestamps in `event` are used.

    Returns:
        Event containing the max of each feature in `event`.
    """
    return MovingMaxOperator(
        input=input,
        window_length=window_length,
        sampling=sampling,
    ).outputs["output"]