from typing import Any, Tuple

import numpy as np

from manimlib import *
from manimlib.constants import LEFT, RIGHT, WHITE
from manimlib.mobject.three_dimensions import Line3D, Cone
from manimlib.utils.space_ops import get_norm, normalize


class Vector3D(Line3D):
    """An arrow made out of a cylindrical line and a conical tip.

    Parameters
    ----------
    start
        The start position of the arrow.
    end
        The end position of the arrow.
    width
        The thickness of the arrow.
    height
        The height of the conical tip.
    radius
        The base radius of the conical tip.
    color
        The color of the arrow and of the conical tip.
    resolution
        The resolution of the arrow line.

    """

    def __init__(
            self,
            start=LEFT,
            end=RIGHT,
            width: float = 0.02,
            height: float = 0.20,
            radius: float = 0.06,
            color=WHITE,
            resolution: Tuple[int, int] = (15, 15),
            **kwargs: Any,
    ) -> None:

        self.start = np.array(start, dtype=float)
        self.end_point = np.array(end, dtype=float)

        self.direction = normalize(end - start)
        self.length = np.linalg.norm(end - start)

        if self.length == 0:
            raise ValueError("Vector3D requires start and end to be different points.")
        # if height >= self.length:
        #     height = self.length/2
        #     raise ValueError("Vector3D requires height < length.")

        line_end = self.end_point - self.direction * height

        super().__init__(
            start=start,
            end=line_end,
            width=width,
            color=color,
            resolution=resolution,
            **kwargs,
        )

        # axis is the cone axis
        self.cone = Cone(
            # direction=self.direction,
            axis=self.direction,
            radius=radius,
            height=height,
            color=color,
            **kwargs,
        )
        self.cone.shift( -self.direction * 0.4 + start + (line_end-start)) # + start
        # self.cone.move_to()
        self.add(self.cone)

    def get_end(self) -> np.ndarray:
        """Returns the tip of the arrow calculated as start + direction * total length."""
        return self.start + self.direction * self.length
