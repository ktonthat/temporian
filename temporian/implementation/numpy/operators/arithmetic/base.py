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
from typing import Dict
from abc import ABC, abstractmethod

from temporian.core.operators.arithmetic.base import BaseArithmeticOperator
from temporian.implementation.numpy.data.event import NumpyEvent
from temporian.implementation.numpy.data.feature import NumpyFeature
from temporian.implementation.numpy.operators.base import OperatorImplementation


class BaseArithmeticNumpyImplementation(OperatorImplementation, ABC):
    def __init__(self, operator: BaseArithmeticOperator) -> None:
        super().__init__(operator)

    @abstractmethod
    def _do_operation(
        self, event_1_feature: NumpyFeature, event_2_feature: NumpyFeature
    ) -> np.ndarray:
        """
        Perform the actual arithmetic operation corresponding to the subclass
        """

    def __call__(
        self, event_1: NumpyEvent, event_2: NumpyEvent
    ) -> Dict[str, NumpyEvent]:
        """Apply the corresponding arithmetic operation between two Events.

        Args:
            event_1: First Event.
            event_2: Second Event.

        Returns:
            Arithmetic of the two Events according to the operator.

        Raises:
            ValueError: If sampling of both events is not equal.
        """

        if event_1.sampling != event_2.sampling:
            raise ValueError("Sampling of both events must be equal.")

        if event_1.feature_count() != event_2.feature_count():
            raise ValueError(
                "Both events must have the same number of features."
            )

        output = NumpyEvent(data={}, sampling=event_1.sampling)

        for event_index, event_1_features in event_1.data.items():
            output.data[event_index] = []

            event_2_features = event_2.data[event_index]

            for i, event_1_feature in enumerate(event_1_features):
                event_2_feature = event_2_features[i]

                # check both features have the same dtype
                if event_1_feature.dtype != event_2_feature.dtype:
                    raise ValueError(
                        "Both features must have the same dtype."
                        f" event_1_feature: {event_1_feature} has dtype "
                        f"{event_1_feature.dtype}, event_2_feature: "
                        f"{event_2_feature} has dtype {event_2_feature.dtype}."
                    )

                result = self._do_operation(event_1_feature, event_2_feature)

                output.data[event_index].append(
                    NumpyFeature(
                        name=self._operator.output_feature_name(
                            event_1_feature, event_2_feature
                        ),
                        data=result,
                    )
                )

        return {"event": output}