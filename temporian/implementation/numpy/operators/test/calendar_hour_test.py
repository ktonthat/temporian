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

from absl.testing import absltest
import numpy as np
import pandas as pd

from temporian.core.operators.calendar.hour import (
    CalendarHourOperator,
)
from temporian.implementation.numpy.operators.calendar.hour import (
    CalendarHourNumpyImplementation,
)
from temporian.io.pandas import from_pandas
from temporian.implementation.numpy.data.io import event_set
from temporian.implementation.numpy.operators.test.test_util import (
    assertEqualEventSet,
)


class CalendarHourNumpyImplementationTest(absltest.TestCase):
    """Test numpy implementation of calendar_hour operator."""

    def test_basic(self) -> None:
        "Basic test with flat node."
        input_evset = from_pandas(
            pd.DataFrame(
                data=[
                    [pd.to_datetime("1970-01-01 00:00:00", utc=True)],
                    [pd.to_datetime("1970-01-01 01:00:00", utc=True)],
                    [pd.to_datetime("1970-01-01 01:59:59", utc=True)],
                    [pd.to_datetime("2023-06-06 12:00:00", utc=True)],
                    [pd.to_datetime("2023-06-06 23:59:59", utc=True)],
                ],
                columns=["timestamp"],
            ),
        )

        output_evset = event_set(
            timestamps=input_evset.get_arbitrary_index_data().timestamps,
            features={
                "calendar_hour": np.array([0, 1, 1, 12, 23]).astype(np.int32),
            },
            is_unix_timestamp=True,
        )

        operator = CalendarHourOperator(input_evset.node())
        impl = CalendarHourNumpyImplementation(operator)
        output = impl.call(sampling=input_evset)["output"]

        assertEqualEventSet(self, output, output_evset)
        self.assertTrue(
            output.get_arbitrary_index_data().features[0].dtype == np.int32
        )


if __name__ == "__main__":
    absltest.main()
