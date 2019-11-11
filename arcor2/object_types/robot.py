import abc
from typing import Set

from arcor2.object_types.generic import Generic
from arcor2.data.common import Pose
from arcor2.data.object_type import MeshFocusAction


class Robot(Generic, metaclass=abc.ABCMeta):
    """
    Abstract class representing robot and its basic capabilities (motion)
    """

    @abc.abstractmethod
    def get_end_effectors_ids(self) -> Set[str]:
        pass

    @abc.abstractmethod
    def get_end_effector_pose(self, end_effector: str) -> Pose:
        pass

    def focus(self, mfa: MeshFocusAction) -> Pose:
        raise NotImplementedError()
