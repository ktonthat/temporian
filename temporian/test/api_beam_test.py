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
import os
from absl import flags
import temporian as tp

from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to
import apache_beam as beam
import temporian.beam as tp_beam
import tempfile


def test_data() -> str:
    return os.path.join(flags.FLAGS.test_srcdir, "temporian")


class TFPTest(absltest.TestCase):
    def test_base(self):
        tmp_dir = tempfile.gettempdir()
        input_path = os.path.join(tmp_dir, "input.csv")
        output_path = os.path.join(tmp_dir, "output.csv")

        # Create a dataset
        input_data = tp.event_set(
            timestamps=[1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
            features={
                "a": [2, 3, 4, 3, 2, 22, 23, 24, 23, 22],
                "b": ["x", "x", "x", "x", "x", "y", "y", "y", "y", "y"],
                "c": ["X", "Y", "Y", "X", "Z", "Z", "Z", "X", "Y", "X"],
                "d": [-1, -2, -3, -4, -5, -6, -7, -8, -9, -10],
                "e": [1, 1, 1, 2, 2, 1, 1, 1, 1, 1],
            },
            index_features=["b"],
        )
        tp.to_csv(input_data, path=input_path)

        # Define some computation
        input_node = input_data.node()
        # TODO: Do some computation.
        output_node = input_node

        # Execute computation in Beam and save the result in a csv file.
        with TestPipeline() as p:
            output = (
                p
                | tp_beam.read_csv(input_path, input_node.schema)
                # TODO: Do some computation.
                # | tp_beam.run(inputs=input_node, outputs=output_node)
                | tp_beam.write_csv(
                    output_path, output_node.schema, shard_name_template=""
                )
            )
            assert_that(output, equal_to([output_path]))

        with open(output_path, "r", encoding="utf-8") as f:
            print("Results:\n" + f.read(), flush=True)


if __name__ == "__main__":
    absltest.main()