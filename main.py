import sys
import os

sys.path.append(os.path.dirname(__file__))

from manimlib import *
from vector3D import Vector3D


class Utils(ThreeDScene):
    def func(self, x, y):
        # return 4 * np.exp(-(x ** 2 + y ** 2)) * np.sin(1 + 3 * x) * np.sin(y)
        return np.cos(x + y) / (1 + x ** 2)

    def der_par_x(self, f, x, y, h=0.0001):
        return (f(x + h, y) - f(x, y)) / h

    def der_par_y(self, f, x, y, h=0.0001):
        return (f(x, y + h) - f(x, y)) / h

    def get_function_graph(
            self,
            axes,
            func,
            color=interpolate_color(BLUE_E, BLACK, 0.6),
            opacity=1.0,
            shading=(0.1, 0.2, 0.4),
            resolution=(101, 101),  # manim default
            depth_test=True
    ) -> ParametricSurface:
        graph = axes.get_graph(func, resolution=resolution, depth_test=depth_test)
        graph.set_color(color)
        graph.set_opacity(opacity)
        graph.set_shading(*shading)

        return graph

    def get_vector3D(self, start, end, color=RED) -> Vector3D:
        return Vector3D(start=start, end=end, color=color)

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

        axes.shift(center - axes.c2p(0, 0, 0))  # centra il piano in center
        axes.set_flat_stroke(False)
        return axes

    def get_Dot3D(self, coordinates, axes: ThreeDAxes, color=RED, opacity=1, radius=0.04):
        x, y, z, *_ = coordinates
        s = Sphere(radius=radius)
        s.set_color(color)
        s.set_opacity(opacity)
        s.move_to(axes.c2p(x, y, z))
        return s

    def get_tan_plane(self, axes, xc, yc) -> ParametricSurface:
        dpx = self.der_par_x(self.func, xc, yc)
        dpy = self.der_par_y(self.func, xc, yc)

        p = ParametricSurface(
            lambda u, v: axes.c2p(u, v, self.func(xc, yc) + dpx * (u - xc) + dpy * (v - yc)),
            u_range=(xc - 1, xc + 1), v_range=(yc - 1, yc + 1),
            resolution=(8, 8),
        )
        p.set_color(RED_C)
        p.set_opacity(0.35)
        p.set_shading(0.2, 0.2, 0.4)

        return p

    def get_mesh(self, surf: ParametricSurface, color=WHITE, width=0.5, opacity=0.25) -> SurfaceMesh:
        mesh = SurfaceMesh(surf)
        mesh.set_stroke(color=color, width=width, opacity=opacity)
        mesh.set_flat_stroke(False)
        return mesh


class MyScene(Utils):
    def construct(self):
        frame = self.camera.frame

        axes = self.get_axes(center=ORIGIN)
        self.play(ShowCreation(axes))

        xp = ValueTracker(1)
        yp = ValueTracker(-0.5)
        point = self.get_Dot3D((xp.get_value(), yp.get_value(), self.func(xp.get_value(), yp.get_value())), axes)

        f_always(point.move_to, lambda: axes.c2p(
            xp.get_value(), yp.get_value(),
            self.func(xp.get_value(), yp.get_value())
        ))

        graph = self.get_function_graph(axes, self.func, opacity=0.1, depth_test=False)
        graph_mesh = self.get_mesh(graph)
        self.play(ShowCreation(graph))
        self.play(ShowCreation(graph_mesh))
        self.play(ShowCreation(point))

        self.play(
            frame.animate.set_euler_angles(theta=113.4 * DEGREES, phi=66.6 * DEGREES).move_to(point),
            run_time=3)
        self.play(frame.animate.scale(0.5))

        norm_vec = self.get_vector3D(
            point.get_center(),
            point.get_center()
            - self.der_par_x(self.func, xp.get_value(), yp.get_value()) * RIGHT
            - self.der_par_y(self.func, xp.get_value(), yp.get_value()) * UP
            + OUT
        )

        sf = 0.7  # scaling factor

        f_always(norm_vec.become, lambda: self.get_vector3D(
            point.get_center(),
            point.get_center()
            - self.der_par_x(self.func, xp.get_value(), yp.get_value()) * RIGHT * sf
            - self.der_par_y(self.func, xp.get_value(), yp.get_value()) * UP * sf
            + OUT * sf
        ))

        # dpx = self.der_par_x(self.func, xp.get_value(), yp.get_value())
        # px_vec = self.get_vector3D(point.get_center(), point.get_center() - dpx * RIGHT)
        # f_always(px_vec.become, lambda: self.get_vector3D(
        #      point.get_center(),
        #      point.get_center() - self.der_par_x(self.func, xp.get_value(), yp.get_value()) * RIGHT
        # ))

        # dpy = self.der_par_y(self.func, xp.get_value(), yp.get_value())
        # py_vec = self.get_vector3D(point.get_center(), point.get_center() - dpy * UP)
        # f_always(py_vec.become, lambda: self.get_vector3D(
        #     point.get_center(),
        #     point.get_center() - self.der_par_y(self.func, xp.get_value(), yp.get_value()) * UP
        # ))

        self.add(norm_vec)
        # self.add(px_vec, py_vec)

        self.play(xp.animate.set_value(1.5), yp.animate.set_value(1))
        self.play(xp.animate.set_value(-0.55), yp.animate.set_value(-0.3), run_time=3)
        self.play(xp.animate.set_value(1), yp.animate.set_value(-0.5), run_time=3)

        plane = self.get_tan_plane(axes, xp.get_value(), yp.get_value())
        self.play(ShowCreation(plane))

        # self.embed()
