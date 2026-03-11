import sys
import os

sys.path.append(os.path.dirname(__file__))

from manimlib import *
from vector3D import Vector3D


class Utils(ThreeDScene):
    @staticmethod
    def func(x : float, y : float) -> float:
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

    def get_Dot3D(self, coordinates, axes: ThreeDAxes, color=RED, opacity : float = 1, radius=0.04):
        x, y, z, *_ = coordinates
        s = Sphere(radius=radius)
        s.set_color(color)
        s.set_opacity(opacity)
        s.move_to(axes.c2p(x, y, z))
        return s

    def get_tan_plane(self, axes, xc, yc, z_index=0) -> ParametricSurface:
        dpx = self.der_par_x(self.func, xc, yc)
        dpy = self.der_par_y(self.func, xc, yc)

        p = ParametricSurface(
            lambda u, v: axes.c2p(u, v, self.func(xc, yc) + dpx * (u - xc) + dpy * (v - yc)),
            u_range=(xc - 1.4, xc + 1.4), v_range=(yc - 1.4, yc + 1.4),
            resolution=(8, 8),
            z_index=z_index
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

    def get_tan_curve(self, axes, p, t_vec, f=func, width=13, t_range=(-2,2, 0.1)) -> ParametricCurve:
        """Returns the tangent curve.

        Parameters
        ----------
        axes
            ThreeDAxes
        p
            (x,y,z) tuple, the point's surface the curve has to be tangent in
        t_vec
            the tangent vector in p
        f
            function defining the surface
        width
            stroke width
        t_range
            t range of the tangent curve

        Returns
        -------
        curve
            ParametricCurve

        """

        x,y,_ = p
        tx, ty, _ = t_vec
        curve = ParametricCurve(lambda t: axes.c2p(x+ t*tx, y + t*ty, f(x+ t*tx, y + t*ty)), t_range, z_index=-1)
        curve.set_stroke(width=width, opacity=1, color=WHITE)
        return curve


class MyScene(Utils):
    def construct(self):
        frame = self.camera.frame

        axes = self.get_axes(center=ORIGIN, include_plane=True)
        self.play(ShowCreation(axes))

        xp = ValueTracker(1)
        yp = ValueTracker(-0.5)
        point = self.get_Dot3D((xp.get_value(), yp.get_value(), self.func(xp.get_value(), yp.get_value())), axes)

        f_always(point.move_to, lambda: axes.c2p(
            xp.get_value(), yp.get_value(),
            self.func(xp.get_value(), yp.get_value())
        ))

        graph = self.get_function_graph(axes, self.func, opacity=0.5)
        graph_mesh = self.get_mesh(graph)

        sf = 1  # scaling factor

        norm_vec = self.get_vector3D( point.get_center(),
            point.get_center()
            - self.der_par_x(self.func, xp.get_value(), yp.get_value()) * RIGHT * sf
            - self.der_par_y(self.func, xp.get_value(), yp.get_value()) * UP * sf
            + OUT * sf
        )

        plane = self.get_tan_plane(axes, xp.get_value(), yp.get_value(), z_index=0)
        mesh_plane = self.get_mesh(plane)




        # SCENA 1
        self.play(ShowCreation(graph))
        self.play(ShowCreation(graph_mesh))
        self.play(ShowCreation(point))

        self.play(frame.animate.shift(UP*1.2).scale(1.2).set_euler_angles(theta=48*DEGREES, phi=64.5*DEGREES), run_time=3)

        self.play(ShowCreation(norm_vec))
        self.play(*map(ShowCreation, [mesh_plane, plane]))

        # adding updaters to norm_vec and plane
        def plane_updater(m):
            new_plane = self.get_tan_plane(axes, xp.get_value(), yp.get_value())
            m.uv_func = new_plane.uv_func
            m.become(new_plane)

        plane.add_updater(plane_updater)
        mesh_plane.add_updater(lambda m: m.become(self.get_mesh(plane)))
        f_always(norm_vec.become, lambda: self.get_vector3D(
            point.get_center(),
            point.get_center()
            - self.der_par_x(self.func, xp.get_value(), yp.get_value()) * RIGHT * sf
            - self.der_par_y(self.func, xp.get_value(), yp.get_value()) * UP * sf
            + OUT * sf
        ))

        # todo: fare un paio di movimenti prima
        self.play(frame.animate.move_to(point).scale(0.6).set_euler_angles(theta=50 * DEGREES, phi=85 * DEGREES),
                  xp.animate.set_value(0), yp.animate.set_value(-0.5), run_time=3)
        self.play(xp.animate.set_value(0.3), yp.animate.set_value(-0.1), run_time=3)
        self.play(xp.animate.set_value(0), yp.animate.set_value(0), run_time=3)
        self.play(frame.animate.set_euler_angles(theta=50 * DEGREES, phi=80.3 * DEGREES))

        # FINE SCENA 1

        # PREPARAZIONE SCENA 2


        vec = self.camera.get_location() - point.get_center() # vettore che congiunge camera e punto
        t_vec = normalize(np.cross(norm_vec.direction, vec)) # vettore tangente alla curva

        x, y = xp.get_value(), yp.get_value()
        dpx = self.der_par_x(self.func, x, y)
        dpy = self.der_par_y(self.func, x, y)
        g = lambda u, v: self.func(x, y) + dpx * (u - x) + dpy * (v - y)
        d_range = (-2, 2, 0.1)

        tan_curve = self.get_tan_curve(axes, (x, y, 1), t_vec, t_range=d_range, width=10)
        plane_curve = self.get_tan_curve(axes, (x, y, 0), t_vec, t_range=d_range, width=5, f=g)

        # p1, p2 sono i punti che si muovono rispettivamente sulla superficie e sul piano tangente
        p1 = self.get_Dot3D(ORIGIN, axes, radius=0.08, color=BLUE).move_to(point).set_z_index(-1)
        p2 = self.get_Dot3D(ORIGIN, axes, radius=0.08, color=BLUE).move_to(point).set_z_index(-1)

        alpha = ValueTracker(0)
        f_always(p2.move_to, lambda : plane_curve.t_func(alpha.get_value()))
        f_always(p1.move_to, lambda : tan_curve.t_func(alpha.get_value()))

        # linea congiungente p1,p2
        line = always_redraw(lambda: Line(p1.get_center(), p2.get_center(), color=BLUE, opacity=0.5).set_z_index(-1))
        deg = 180 * DEGREES - frame.get_euler_angles()[0] # theta = 50 DEGREES


        # INIZIO SCENA 2

        self.play(*map(ShowCreation, [tan_curve, plane_curve]), run_time=2)
        self.play(*map(FadeOut, [plane, mesh_plane]), *map(ShowCreation, [p1, p2]))
        self.play(alpha.animate.set_value(1.8), run_time=2)

        line.update()
        line.suspend_updating()
        self.play(FadeIn(line))
        line.resume_updating()

        font_size = 30
        brace = always_redraw(lambda: Brace3D(line, rotation=deg))

        text = always_redraw(lambda : Tex("e = ", font_size=font_size)
                             .next_to(brace, RIGHT)
                             .rotate(90 * DEGREES, axis=RIGHT)
                             .rotate(50 * DEGREES, about_point=brace.get_center()))

        number = always_redraw(lambda: DecimalNumber(line.get_length(), show_ellipsis=True, num_decimal_places=2, font_size=font_size)
                               .next_to(text, RIGHT)
                               .rotate(90 * DEGREES, axis=RIGHT)
                               .rotate(50 * DEGREES, about_point=text.get_center()))

        label = VGroup(text, number)
        self.play(FadeIn(brace, suspend_mobject_updating=True), Write(label, suspend_mobject_updating=True))

        self.play(alpha.animate.set_value(0.5), run_time=1.8)
        self.play(alpha.animate.set_value(1.2), run_time=1)

        to_remove = [brace, label, p1, p2, line, plane_curve, tan_curve, point]
        for i in to_remove: i.clear_updaters().set_z_index(2)
        # suspending updates before removal

        frame.save_state()

        self.play(*map(FadeOut, to_remove[0:2]))
        self.play(*[FadeOut(m, shift=IN) for m in to_remove[2:]],
                  *map(FadeIn, [plane, mesh_plane]),
                  frame.animate.set_euler_angles(theta=30 * DEGREES, phi=80 * DEGREES).scale(1.5).move_to(ORIGIN + OUT),
                  run_time=2
        )
        for i in to_remove: i.remove()
        # manually removing after fade out
        # todo: remove also xp, yp

        # SCENA : zoom out --> "anzi per tutti i punti del piano!"

        # coordinate dei punti
        points_coordinate = [
            (-0.92, 0.45), (0.33, -0.81), (0.87, 0.76), (-0.41, -0.38), (0.59, -0.95),
            (-0.73, 0.89), (0.44, 0.32), (-0.85, -0.67), (0.98, -0.42), (-0.36, 0.54)
        ]

        points_and_lines = []
        for coordinates in points_coordinate:
            x,y = coordinates
            op = 0.5
            p1 = self.get_Dot3D(axes.p2c(graph.uv_func(x, y)), axes, opacity=op, radius=0.08, color=BLUE)
            p2 = self.get_Dot3D(axes.p2c(plane.uv_func(x, y)), axes, opacity=op, radius=0.08, color=BLUE)
            line = Line(p1.get_center(), p2.get_center(), color=BLUE, stroke_opacity=op)
            points_and_lines.append(Group(p1, p2, line, opacity=op))

        for p in points_and_lines:
            self.play(FadeIn(p), run_time=0.2)

        #todo : check if suspend_mobject_updating=True is working
        self.play(*map(FadeOut, points_and_lines), FadeOut(norm_vec, suspend_mobject_updating=True))

        # SCENA : come possiamo calcolare e(h) analiticamente ?

        plane.suspend_updating(), mesh_plane.suspend_updating()
        self.play(
            frame.animate.set_euler_angles(theta=0 * DEGREES, phi=0 * DEGREES),
            FadeOut(plane), FadeOut(mesh_plane),
            *map(FadeOut, [graph, graph_mesh]), run_time=2
        )

        # todo : remeber to resume updaters

        # il piano è tangente in x_0

        x0 = self.get_Dot3D(ORIGIN, axes, radius=0.08, color=RED)
        x0_label = Tex("x_0", font_size=font_size).next_to(x0, UP+0.35*RIGHT).shift(OUT*0.1)
        y0 = x0.copy()

        line = DashedLine(x0.get_center(), y0.get_center() + UP+2*RIGHT, stroke_width=5, positive_space_ratio=0.6, color=RED)

        self.play(ShowCreation(x0), Write(x0_label))
        self.add(y0)
        self.play(y0.animate.shift(UP+2*RIGHT), ShowCreation(line), run_time=2)

        y0_label = Tex("y_0", font_size=font_size).next_to(y0, 0.5*UP+RIGHT).shift(OUT*0.1)
        self.play(Write(y0_label))

        new_y0_label = Tex("x_0 + h", font_size=font_size).next_to(y0, 0.5*(0.5*UP+RIGHT)).shift(OUT*0.1)
        direction = rotate_vector(line.get_vector(), PI/2, axis=IN) # to rotate it clock-wise
        brace = Brace(line, direction=direction)
        brace_label = Tex("h", font_size=font_size).next_to(brace.get_center(), direction)

        self.play(TransformMatchingTex(y0_label, new_y0_label), FadeIn(brace), Write(brace_label))


class Brace3D(Brace):
    """
    A 3D-oriented Brace object.

    This class extends the standard 2D Brace by projecting it onto a
    3D line segment and applying the necessary rotations to align it
    with the segment's spatial orientation.

    Parameters
    ----------
    line : Line
        The target Line object the brace will be associated with.
    rotation : float, optional
        The roll angle (in radians) around the line's own axis. Default is 0.
        To have the brace RIGHT to the line rotation = 180*DEGREES
    **kwargs
        Additional arguments passed to the Brace constructor (e.g., color, width).

    """
    def __init__(self, line, rotation=0, **kwargs):
        length = line.get_length()
        if length < 1e-9:
            # Initialize with a dummy line and scale to 0 to remain invisible
            super().__init__(Line(ORIGIN, RIGHT), direction=DOWN, **kwargs)
            self.scale(0)
            self.shift(line.get_start())
            return

        flatline = Line(ORIGIN, length*RIGHT)
        super().__init__(flatline, direction=DOWN, **kwargs) # np.array([0., -1., 0.])
        dline = line.get_end()-line.get_start()
        self.rotate(angle=rotation, about_point=flatline.get_start(),axis=RIGHT)
        # if np.linalg.norm(dline) > 0.0001:
        self.rotate(-np.asin(dline[2]/np.linalg.norm(dline)), about_point=flatline.get_start(), axis=UP)
        self.rotate(np.atan2(dline[1],dline[0]), about_point=flatline.get_start(), axis=OUT)
        self.shift(line.get_start()-flatline.get_start())
