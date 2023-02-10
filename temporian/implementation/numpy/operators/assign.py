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

"""Implementation for the Assign operator."""
from typing import Dict, List

import numpy as np
from temporian.implementation.numpy.data.event import NumpyEvent
from temporian.implementation.numpy.data.event import NumpyFeature
from temporian.implementation.numpy.data.sampling import NumpySampling


def _get_common_timestamps(
    sampling_1: NumpySampling, sampling_2: NumpySampling, index: tuple
) -> np.ndarray:
    """It returns a np.ndarray with same shape as sampling_1.data[index] with True
    values where sampling_1.data[index] == sampling_2.data[index], and False otherwise.

    Args:
        sampling_1 (NumpySampling): sampling of assignee event.
        sampling_2 (NumpySampling): sampling of assigned event.
        index (tuple): index to check.

    Returns:
        np.ndarray: boolean np.darray with same shape as sampling_1.data[index]

    """
    return np.isin(sampling_1.data[index], sampling_2.data[index])


def _convert_feature_to_new_sampling(
    feature: NumpyFeature,
    common_timestamps: List[bool],
    new_sampling: NumpySampling,
):
    """Convert feature to new sampling. It requires a boolean list with same length
    as the new sampling, where True values indicate that the feature has a value
    for that timestamp. And it needs the new sampling to assign to the new Feature object.


    Args:
        feature (NumpyFeature): feature to convert.
        common_timestamps (List[bool]): list of booleans indicating if sampling_2 has same timestamp in sampling_1
        new_sampling (NumpySampling): new sampling.

    Returns:
        NumpyFeature: feature with new sampling.

    """
    new_feature = NumpyFeature(
        name=feature.name,
        sampling=new_sampling,
        data=np.full(len(common_timestamps), np.nan),
    )

    # loop over common timestamps and if True, then add the common timestamp
    # to the new feature. As timestamps are in order, we can use the last_i
    # to know with which index of the feature we should take the data from.
    last_i = 0
    for i, is_common in enumerate(common_timestamps):
        if is_common:
            new_feature.data[i] = feature.data[last_i]
            last_i += 1

    return new_feature


class NumpyAssignOperator:
    def __call__(
        self, assignee_event: NumpyEvent, assigned_event: NumpyEvent
    ) -> Dict[str, NumpyEvent]:
        """Assign features to an event.

        Assignee and assigned must have same index names. Features cannot have more
        than one row for a single index + timestamp occurence. Output event will
        have same exact index and timestamps (sampling) as the assignee event.

        Assignment is done by matching the timestamps and index of the assignee and assigned.
        The assigned features will be appended to the assignee features in the matching
        indexes. If assignee event has more indexes values than assigned, the assigned features
        will be broadcasted to the assignee indexes with np.nan values according
        to the assignee sampling. If the assigned event has more timestamps in a matching
        index, then those values will not be included in the output event.


        Args:
            assignee_event (NumpyEvent): event to assign the feature to.
            assigned_event (NumpyEvent): features to assign to the event.

        Returns:
            NumpyEvent: a new event with the features assigned.

        Raises:
            ValueError: if assignee and assigned events have different indexes names.

        """
        # check both keys are the same
        if assignee_event.sampling.names != assigned_event.sampling.names:
            raise ValueError("Assign sequences must have the same index names.")

        output = NumpyEvent(
            data=assignee_event.data.copy(), sampling=assignee_event.sampling
        )

        for index in assignee_event.data.keys():
            # If index is in assigned append the features to the output event
            if index in assigned_event.data.keys():
                # get timestamps that are equal to sampling_1 & sampling_2
                common_timestamps = _get_common_timestamps(
                    sampling_1=assignee_event.sampling,
                    sampling_2=assigned_event.sampling,
                    index=index,
                )
                # loop over assigned features
                for assigned_feature in assigned_event.data[index]:
                    # convert feature to new sampling
                    assigned_feature_filtered = (
                        _convert_feature_to_new_sampling(
                            feature=assigned_feature,
                            common_timestamps=common_timestamps,
                            new_sampling=assignee_event.sampling,
                        )
                    )
                    output.data[index].append(assigned_feature_filtered)
            # If index is not in assigned, append the features of assigned with None values
            else:
                for feature_name in assigned_event.feature_names:
                    output.data[index].append(
                        NumpyFeature(
                            name=feature_name,
                            sampling=assignee_event.sampling,
                            # create a list of None values with the same length as assignee sampling
                            data=np.full(
                                len(assignee_event.sampling.data[index]), np.nan
                            ),
                        )
                    )

        # make assignment
        return {"event": output}
