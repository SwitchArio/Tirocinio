
from manimlib import *

class Utils(ThreeDScene):
    def func(self, x, y):
        return np.exp(-x ** 2 - y ** 2)

    def get_axes(
            self,
            x_range=(-3, 3),
            y_range=(-3, 3),
            z_range=(0, 1.5, 0.5),
            width=8,
            height=8,
            depth=3,
            center=0.5 * IN,
            include_plane=False
    ):
        axes = ThreeDAxes(
            x_range, y_range, z_range,
            width=width, height=height, depth=depth
        )
        axes.set_stroke(GREY_C)
        if include_plane:
            plane = NumberPlane(
                x_range, y_range,
                width=width, height=height,
                background_line_style=dict(
                    stroke_color=GREY_C,
                    stroke_width=1,
                ),
            )
            plane.faded_lines.set_stroke(opacity=0.5)
            plane.shift(0.01 * IN)
            axes.plane = plane
            axes.add(plane)

        x, y, z = axis_labels = VGroup(*map(Tex, "xyz"))
        axis_labels.use_winding_fill(False)
        x.next_to(axes.x_axis, RIGHT)
        y.next_to(axes.y_axis, UP)
        z.rotate(90 * DEGREES, RIGHT)
        z.next_to(axes.z_axis, OUT)
        axes.labels = axis_labels
        axes.add(axis_labels)

        axes.shift(center - axes.c2p(0, 0, 0)) # centra il piano in center
        axes.set_flat_stroke(False)
        return axes

class prova(Utils):
    def construct(self):
        # axes = self.get_axes(include_plane=True)
        axes = ThreeDAxes(
            (-3, 3), (-3, 3), (0, 1.5, 0.5),
            width=8, height=8, depth=3
        )
        self.play(ShowCreation(axes))

        # self.camera.frame.get_orientation()
        self.play(self.camera.frame.animate.set_euler_angles(phi=70*DEGREES, theta=-30*DEGREES))

        # self.embed()


