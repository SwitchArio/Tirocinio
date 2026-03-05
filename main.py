
from manimlib import *

class Utils(ThreeDScene):
    def func(self, x, y):
        return np.exp(-x ** 2 - y ** 2)

    def get_function_graph(
            self,
            axes,
            func,
            color=interpolate_color(BLUE_E, BLACK, 0.6),
            opacity=1.0,
            shading=(0.2, 0.2, 0.4),
            resolution=(101, 101), # manim default
    ) -> ParametricSurface:
        graph = axes.get_graph(func, resolution=resolution)
        graph.set_color(color)
        graph.set_opacity(opacity)
        graph.set_shading(*shading)
        return graph

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

        graph = self.get_function_graph(axes, lambda x,y: np.sin(x**2 + y**2), opacity=0.7)
        # self.play(ShowCreation(graph))

        mesh = SurfaceMesh(graph, resolution=(30, 30), stroke_color=GREY_C)
        mesh.set_stroke(WHITE, 0.5, opacity=0.25)
        mesh.set_flat_stroke(False)

        self.play(ShowCreation(graph))
        self.play(ShowCreation(mesh))

        # self.play( ReplacementTransform(graph, mesh), run_time=2 )

        # self.embed()


