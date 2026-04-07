import sys
import os

import numpy as np

sys.path.append(os.path.dirname(__file__))

from manimlib import *
from vector3D import Vector3D


class Utils(ThreeDScene):
    @staticmethod
    def func(x: float, y: float) -> float:
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
        axes.plane = None
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
            # plane.shift(0.01 * IN)
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

    def get_Dot3D(self, coordinates, axes: ThreeDAxes, color=RED, opacity: float = 1, radius=0.04):
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

    def get_tan_curve(self, axes, p, t_vec, f=func, width=13, t_range=(-2, 2, 0.1)) -> ParametricCurve:
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

        x, y, _ = p
        tx, ty, _ = t_vec
        curve = ParametricCurve(lambda t: axes.c2p(x + t * tx, y + t * ty, f(x + t * tx, y + t * ty)), t_range,
                                z_index=-1)
        curve.set_stroke(width=width, opacity=1, color=WHITE)
        return curve


class test(Scene):

    FONT_SIZE = 30

    def construct(self):



        steps = [
            r"f(x_0+h) - f(x_0) - \langle\nabla f(x_0),h\rangle = \frac12 h^TH_fh + o(|h|^2)",
            r"e(h) = \frac12 h^TH_fh + o(|h|^2)",
            r"e(h) = \frac12 h^T \begin{pmatrix}\partial_{xx}f &\partial_{xy}f\\ \partial_{yx}f &\partial_{yy}f\end{pmatrix} h + o(|h|^2)",
            r"e(h) = \frac12 \begin{pmatrix}h^1,h^2\end{pmatrix} \begin{pmatrix}\partial_{xx}f &\partial_{xy}f\\ \partial_{yx}f &\partial_{yy}f\end{pmatrix} \begin{pmatrix}h^1\\ h^2\end{pmatrix} + o(|h|^2)",
            r"e(h) = (h^1)^2 \frac12\partial_{xx}f + h^1h^2\partial_{xy}f +  (h^2)^2 \frac12\partial_{yy}f + o(|h|^2)",
        ]

        text = [Tex(steps[i], font_size=self.FONT_SIZE+15).to_edge(UP, buff=LARGE_BUFF).shift(DOWN*1.5*i) for i in range( len(steps))]
        idx = [index_labels(tex) for tex in text]


        self.add( *text, *idx)

class MyScene(Utils):

    FONT_SIZE = 30

    # noinspection PyTypeChecker
    def construct(self):
        frame = self.camera.frame

        axes = self.get_axes(center=ORIGIN, include_plane=False)

        self.play(ShowCreation(axes))

        xp = ValueTracker(1)
        yp = ValueTracker(-0.5)
        point = self.get_Dot3D(
            (xp.get_value(), yp.get_value(), self.func(xp.get_value(), yp.get_value())),
            axes, radius=0.08
        )

        f_always(point.move_to, lambda: axes.c2p(
            xp.get_value(), yp.get_value(),
            self.func(xp.get_value(), yp.get_value())
        ))

        graph = self.get_function_graph(axes, self.func, opacity=0.5)
        graph_mesh = self.get_mesh(graph)

        sf = 1  # scaling factor

        norm_vec = self.get_vector3D(point.get_center(),
                                     point.get_center()
                                     - self.der_par_x(self.func, xp.get_value(), yp.get_value()) * RIGHT * sf
                                     - self.der_par_y(self.func, xp.get_value(), yp.get_value()) * UP * sf
                                     + OUT * sf
                                     )

        plane = self.get_tan_plane(axes, xp.get_value(), yp.get_value())
        mesh_plane = self.get_mesh(plane)

        FS = self.FONT_SIZE  # font size
        R = "\mathbb{R}"

        t1 = rf"Consideriamo una funzione $f:{R}^2\to{R}$ di classe $C^2$."
        text1 = TexText(t1, font_size=FS).fix_in_frame().to_corner(UL)

        # SCENA 1 - Creazione piano punto e piano tangente
        self.play(ShowCreation(graph))
        self.play(ShowCreation(graph_mesh), frame.animate.scale(1.2), Write(text1), run_time=2)
        self.wait()

        target_text = TexText(rf"$f:{R}^2\to{R},\; f\in C^2$", font_size=FS + 10).fix_in_frame().to_corner(DR).shift(UP)
        t2 = "Se consideriamo un punto $P$ sulla superficie"
        text2 = TexText(t2, font_size=FS).fix_in_frame().to_corner(UL)
        to_remove = [text2, text1]
        self.play(ShowCreation(point), TransformMatchingTex(text1, target_text))

        self.play(frame.animate.shift(UP * 1.2).set_euler_angles(theta=48 * DEGREES, phi=64.5 * DEGREES), Write(text2),
                  run_time=3)
        frame.save_state()
        self.play(frame.animate.move_to(point.get_center()).scale(0.6))
        self.play(Indicate(point), run_time=2)
        self.play(frame.animate.restore())  #ShowCreation(norm_vec)

        t3 = f"Possiamo sempre approssimare $f$ vicino ad $P$ con il suo piano tangente"
        text3 = TexText(t3, font_size=FS).fix_in_frame().to_corner(UL)
        self.play(FadeOut(text2), Write(text3), lag_ratio=1)
        self.play(*map(ShowCreation, [mesh_plane, plane]))

        # Trash
        self.remove(*to_remove)

        # SCENA 1 - Movimento del piano

        to_remove = [target_text, text3]

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

        self.play(frame.animate.move_to(point).scale(0.6).set_euler_angles(theta=50 * DEGREES, phi=85 * DEGREES),
                  xp.animate.set_value(0), yp.animate.set_value(-0.5), run_time=3)

        self.play(xp.animate.set_value(0.3), yp.animate.set_value(-0.1),
                  *map(FadeOut, to_remove)
                  , run_time=3)
        self.play(xp.animate.set_value(0), yp.animate.set_value(0), run_time=3)

        t1 = r"\text{Parliamo di approssimazione perche' se proviamo a stimare $f$ commetteremo un certo errore } e."
        text1 = Tex(t1, font_size=FS).fix_in_frame().to_corner(UL)

        self.play(frame.animate.set_euler_angles(theta=50 * DEGREES, phi=80.3 * DEGREES), Write(text1))
        self.remove(*to_remove)  # text1_T, text3 liberati
        # FINE SCENA 1

        # PREPARAZIONE SCENA 2
        vec = self.camera.get_location() - point.get_center()  # vettore che congiunge camera e punto
        t_vec = normalize(np.cross(norm_vec.direction, vec))  # vettore tangente alla curva

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
        f_always(p2.move_to, lambda: plane_curve.t_func(alpha.get_value()))
        f_always(p1.move_to, lambda: tan_curve.t_func(alpha.get_value()))

        # linea congiungente p1,p2
        line = always_redraw(lambda: Line(p1.get_center(), p2.get_center(), color=BLUE, opacity=0.5).set_z_index(-1))
        deg = 180 * DEGREES - frame.get_euler_angles()[0]  # theta = 50 DEGREES

        # INIZIO SCENA 2

        # occupati: t1
        t2 = "Piu' ci allontaniamo da $P$ e maggiore sara' l'errore"
        text2 = TexText(t2, font_size=FS).fix_in_frame().next_to(text1, DOWN, aligned_edge=UL)

        self.play(*map(ShowCreation, [tan_curve, plane_curve]), lag_ratio=1, run_time=2)
        self.play(*map(FadeOut, [plane, mesh_plane]), *map(ShowCreation, [p1, p2]))
        self.play(alpha.animate.set_value(1.8), run_time=2)

        line.update()
        line.suspend_updating()
        self.play(FadeIn(line))
        line.resume_updating()

        FS = 30
        brace = always_redraw(lambda: Brace3D(line, rotation=deg))

        text = always_redraw(lambda: Tex("e = ", font_size=FS)
                             .next_to(brace, RIGHT)
                             .rotate(90 * DEGREES, axis=RIGHT)
                             .rotate(50 * DEGREES, about_point=brace.get_center()))

        number = always_redraw(
            lambda: DecimalNumber(line.get_length(), show_ellipsis=True, num_decimal_places=2, font_size=FS)
            .next_to(text, RIGHT)
            .rotate(90 * DEGREES, axis=RIGHT)
            .rotate(50 * DEGREES, about_point=text.get_center()))

        label = VGroup(text, number)
        self.play(FadeIn(brace, suspend_mobject_updating=True), Write(label, suspend_mobject_updating=True))
        self.play(Write(text2))
        self.play(alpha.animate.set_value(0.5), run_time=1.8)
        self.play(alpha.animate.set_value(1.2), run_time=1)

        to_remove = [brace, label, p1, p2, line, plane_curve, tan_curve, point, text1, text2]
        for i in to_remove: i.clear_updaters().set_z_index(2)
        # suspending updates before removal

        frame.save_state()

        self.play(*map(FadeOut, to_remove[0:2]))
        self.play(*[FadeOut(m) for m in to_remove[2:]],
                  *map(FadeIn, [plane, mesh_plane]),
                  frame.animate.set_euler_angles(theta=30 * DEGREES, phi=80 * DEGREES).scale(1.5).move_to(ORIGIN + OUT),
                  run_time=2
                  )
        self.remove(*to_remove, xp, yp)
        # manually removing after fade out

        # SCENA : zoom out --> "anzi per tutti i punti del piano!"

        # coordinate dei punti
        points_coordinate = [
            (-0.92, 0.45), (0.33, -0.81), (0.87, 0.76), (-0.41, -0.38), (0.59, -0.95),
            (-0.73, 0.89), (0.44, 0.32), (-0.85, -0.67), (0.98, -0.42), (-0.36, 0.54)
        ]

        points_and_lines = []
        for coordinates in points_coordinate:
            x, y = coordinates
            op = 0.5
            p1 = self.get_Dot3D(axes.p2c(graph.uv_func(x, y)), axes, opacity=op, radius=0.08, color=BLUE)
            p2 = self.get_Dot3D(axes.p2c(plane.uv_func(x, y)), axes, opacity=op, radius=0.08, color=BLUE)
            line = Line(p1.get_center(), p2.get_center(), color=BLUE, stroke_opacity=op)
            points_and_lines.append(Group(p1, p2, line, opacity=op))

        t1 = "L'errore e' valutabile per ogni punto del piano tangente."
        text1 = TexText(t1, font_size=FS).fix_in_frame().to_corner(UL)
        self.play(Write(text1))
        for p in points_and_lines:
            self.play(FadeIn(p), run_time=0.2)

        self.play(*map(FadeOut, points_and_lines))

        self.play(FadeOut(text1))  # remove text1 ?
        plane.clear_updaters(), mesh_plane.clear_updaters()

        mobj_to_fade = [axes, plane, mesh_plane, graph, graph_mesh]
        self.play(*map(FadeOut, mobj_to_fade))

        t1 = ["Dunque possiamo associare un certo", "errore"]
        t2 = "ad ogni punto in cui e' definito il piano tangente"

        text1, text2 = frase = Group(
            TexText(*t1, font_size=FS, t2c={"errore": RED}),
            TexText(t2, font_size=FS)
        ).fix_in_frame().arrange(RIGHT, buff=SMALL_BUFF)

        self.play(Write(text1), run_time=2)
        self.play(Write(text2), run_time=2)
        self.wait()

        t3 = "Ma come si traduce questo in termini matematici?"
        t4 = "E' possibile determinarne l'espressione analitica?"

        text3, text4 = frase2 = Group(
            TexText(t3, font_size=FS),
            TexText(t4, font_size=FS, t2c={"espressione analitica": BLUE})
        ).fix_in_frame().arrange(DOWN)

        self.play(FadeOut(frase))
        self.play(Write(text3), run_time=2)
        self.wait()
        self.play(Write(text4))
        self.wait(3)
        self.play(FadeOut(frase2))

        t1 = "Ricordiamo un momento la formula per il piano tangente ad una superficie $S$"
        t2 = "Nel nostro caso $S$ e' definita dal grafico di $f$"
        # t3 = rf"ossia $S=\{{(x^1,x^2,x^3)\in{R}^3:x^3=f(x^1,x^2)\}}$"
        t3 = rf"ossia $S:x^3=f(x^1,x^2)$"

        S_COLOR = GREEN
        X_COLOR = YELLOW

        text2, text3 = frase = Group(
            TexText(t2, font_size=FS, t2c={"$S$": S_COLOR}),
            TexText(t3, font_size=FS, t2c={"S": S_COLOR})
        ).fix_in_frame().arrange(RIGHT, buff=SMALL_BUFF)

        text1, _ = frase2 = Group(
            TexText(t1, font_size=FS, t2c={"superficie $S$": S_COLOR}),
            frase
        ).fix_in_frame().arrange(DOWN)

        # tar_t = rf"$S=\{{(x^1,x^2,x^3)\in{R}^3:x^3=f(x^1,x^2)\}}$"
        tar_t = rf"$S:x^3=f(x^1,x^2)$"
        target_text = TexText(tar_t, font_size=FS, t2c={"S": S_COLOR}).fix_in_frame().to_edge(UP)


        self.play(Write(text1), run_time=2)
        self.wait()
        self.play(Write(text2), run_time=2)
        self.wait(0.5)
        self.play(Write(text3), run_time=2)
        self.wait(4)
        self.play(TransformMatchingTex(text3.copy(), target_text), *map(FadeOut, [frase2]))
        self.wait(3)
        text4 = target_text

        t1 = rf"Allora, preso $x_0\in{R}^2$, il piano tangente ad $S$ in $P=(x_0, f(x_0))\in{R}^3$"
        t2 = ["e' la superficie definita al variare di $x$ come", r"$T:f(x_0)+\langle\nabla f(x_0),$", "$x$",
              r"$-x_0\rangle$"]

        text1, text2 = frase = Group(
            TexText(t1, font_size=FS, t2c={"$S$": S_COLOR}),
            TexText(*t2, font_size=FS, t2c={"$x$": X_COLOR})
        ).fix_in_frame().arrange(DOWN, buff=SMALL_BUFF)

        self.play(Write(text1), run_time=2)
        self.wait()
        self.play(Write(text2), run_time=2)
        self.wait(3)

        tar_t = [r"$T:f(x_0)+\langle\nabla f(x_0),$", r"$x-x_0\rangle$"]
        target_text = TexText(*tar_t, font_size=FS).fix_in_frame().to_corner(UL, buff=MED_LARGE_BUFF)

        self.play(FadeOut(frase), FadeOut(text4), TransformMatchingTex(text2.copy(), target_text))
        self.remove(text1, text2, text3, text4)
        self.play(*map(FadeIn, mobj_to_fade))

        # SCENA : come possiamo calcolare e(h) analiticamente ?

        self.play(
            *map(FadeOut, [plane, mesh_plane, graph, graph_mesh]),
            frame.animate.set_euler_angles(theta=0 * DEGREES, phi=0 * DEGREES).scale(0.7),
            run_time=2
        )

        # il piano e' tangente in x_0

        x0 = self.get_Dot3D(ORIGIN, axes, radius=0.08, color=RED)
        x0_label = Tex("x_0", font_size=FS).next_to(x0, UP + 0.35 * RIGHT).shift(OUT * 0.1)
        y0 = x0.copy()

        shift_dir = (DOWN + 2 * RIGHT)
        stroke_width = 5
        positive_space_ratio = 0.6

        line = DashedLine(
            x0.get_center(), y0.get_center() + shift_dir,
            stroke_width=stroke_width,
            positive_space_ratio=positive_space_ratio,
            color=RED
        )

        t1 = "Se mi sposto da $x_0$,"
        t2 = "in un punto $y_0$"
        t3 = rf"dove $y_0=x_0+h$ per qualche $h\in{R}^2$"
        text1, text2 = frase = Group(
            TexText(t1, font_size=FS), TexText(t2, font_size=FS)
        ).arrange(RIGHT, buff=SMALL_BUFF)
        text3, _ = frase2 = Group(
            TexText(t3, font_size=FS), frase
        ).fix_in_frame().arrange(UP, buff=SMALL_BUFF).to_edge(LEFT).shift(2 * UP)

        self.play(ShowCreation(x0), Write(x0_label), Write(text1))
        self.add(y0)
        self.play(y0.animate.shift(shift_dir), ShowCreation(line), Write(text2), run_time=2)

        y0_label = Tex("y_0", font_size=FS).next_to(y0, 0.5 * UP + RIGHT).shift(OUT * 0.1)
        self.play(Write(y0_label))

        new_y0_label = Tex("x_0 + h", font_size=FS).next_to(y0, 0.5 * (0.5 * UP + RIGHT)).shift(OUT * 0.1)
        direction = rotate_vector(line.get_vector(), PI / 2, axis=IN)  # to rotate it clock-wise
        brace = Brace(line, direction=direction).shift(OUT * 0.1)
        brace_label = Tex("h", font_size=FS).next_to(brace.get_center(), direction)

        self.wait()
        self.play(TransformMatchingTex(y0_label, new_y0_label), FadeIn(brace), Write(brace_label), Write(text3))
        self.wait()

        self.play(FadeOut(frase2))

        t1 = "Allora posso esprimere $e$ in funzione di $h$,"
        t2 = r"ossia $e(h)$ rappresenta l'errore se mi sposto di $h$ da $x_0$"
        text1, text2 = frase = Group(
            TexText(t1, font_size=FS),
            TexText(t2, font_size=FS)
        ).fix_in_frame().arrange(DOWN, buff=SMALL_BUFF).to_edge(LEFT).shift(2 * UP)

        self.play(Write(text1), run_time=2)
        self.wait(0.5)
        self.play(Write(text2), run_time=2)
        self.wait(2)

        mobj_to_fade = [x0, x0_label, new_y0_label, line, brace, brace_label, frase]
        self.play(*map(FadeOut, mobj_to_fade))
        self.remove(*mobj_to_fade, y0_label, frase2)

        text2, text3, text4 = formula = self.get_sentence(
            ["$e(h) = $","$f(x_0+h)$", r"$ - f(x_0) - \langle\nabla f(x_0),h\rangle $"]
        ).to_edge(LEFT).shift(2 * UP)

        self.play(frame.animate.restore(), *map(FadeIn, [graph, graph_mesh, plane, mesh_plane]), run_time=2)
        self.wait()

        x, y, *_ = axes.point_to_coords(y0.get_center())
        y0_plane = self.get_Dot3D(ORIGIN, axes, radius=0.08, color=BLUE).move_to(plane.uv_func(x, y))
        y0_plane_label = Tex("Q", font_size=FS, stroke_width=1).next_to(y0_plane.get_center())
        y0_plane_label.rotate(90 * DEGREES, axis=RIGHT).rotate(50 * DEGREES, about_point=y0_plane.get_center())
        y0_plane_label.set_z_index(-2)

        y0_graph = self.get_Dot3D(ORIGIN, axes, radius=0.08, color=GREEN).move_to(graph.uv_func(x, y))
        y0_graph_label = Tex("P", font_size=FS, stroke_width=1).next_to(y0_graph.get_center())
        y0_graph_label.rotate(90 * DEGREES, axis=RIGHT).rotate(50 * DEGREES, about_point=y0_graph.get_center())
        y0_graph_label.set_z_index(-2)

        line = DashedLine(
            y0.get_center(), y0_plane.get_center(),
            stroke_width=stroke_width,
            positive_space_ratio=positive_space_ratio,
            color=RED
        ).set_z_index(-1)

        # self.play(*map(ShowCreation, [y0_plane, y0_graph, line]))
        self.play(ShowCreation(line), Write(text2))

        self.play(ShowCreation(y0_graph), *map(Write, [y0_graph_label, text3]), run_time=2)
        self.play(*map(Indicate, [y0_graph_label, text3]), run_time=1.5)
        self.play(ShowCreation(y0_plane), *map(Write, [y0_plane_label, text4]), run_time=2)
        self.play(*map(Indicate, [y0_plane_label, text4]), run_time=1.5)

        mobj_to_fade = [text1, formula, target_text, y0_plane_label, y0_graph_label]
        self.play(*map(FadeOut, mobj_to_fade[2:]))
        self.remove(*mobj_to_fade)

        text1, text2 = frase = self.get_sentence(
            ["Per visualizzare il grafico di $e(h)$", "dobbiamo spostarci sul piano tangente"]
        ).to_corner(UL)

        frame.save_state()
        self.play(Write(text1), run_time=2)
        self.play(Write(text2), run_time=2)

        self.play(
            frame.animate
            .move_to(plane.get_center())
            .set_euler_angles(gamma=-180 * DEGREES, phi=95 * DEGREES, theta=90 * DEGREES)
            .scale(0.8),
            plane.animate.shift(OUT * 0.03),
            *map(FadeOut, [y0_plane, y0_graph, line, y0]),
            run_time=3
        )

        self.wait()
        self.play(FadeOut(frase))
        self.remove(frase)

        t1 = "Osservando la superficie dell'errore $e(h)$, non c'e' traccia di linearita'."
        t2 = "Questa e' quasi una parabola che emerge dal piano. "

        t3 = "Eppure, la definizione che abbiamo usato"
        t4 = "non sembra avere una natura quadratica."
        t5 = r"e(h) = f(x_0+h) - f(x_0) - \langle\nabla f(x_0),h\rangle"
        tar_t = [
            "e(h) = f(x_0+h) - f(x_0) - ",
            r"\partial f\over\partial x^1", "(x_0)", "h^1", "-",
            r"\partial f\over\partial x^2", "(x_0)", "h^2"
        ]

        text1, text2 = frase = Group(
            TexText(t1, font_size=FS),
            TexText(t2, font_size=FS)
        ).fix_in_frame().arrange(DOWN, aligned_edge=DL).to_edge(DOWN).shift(UP)

        text3, text4 = frase2 = Group(
            TexText(t3, font_size=FS),
            TexText(t4, font_size=FS)
        ).fix_in_frame().arrange(RIGHT, buff=SMALL_BUFF).to_edge(DOWN).shift(UP * 1.3)

        text5 = Tex(t5, font_size=FS).fix_in_frame().to_edge(DOWN, buff=SMALL_BUFF).shift(UP * 0.5)
        error_formula = Tex(*tar_t, font_size=FS).fix_in_frame().move_to(text5)

        self.wait()
        self.play(Write(text1), run_time=2)
        self.wait()
        self.play(Write(text2), run_time=2)
        self.wait(2.5)
        self.play(FadeOut(frase), run_time=2)
        self.play(Write(text3), run_time=2)
        self.play(Write(text4), run_time=2)
        self.wait(0.5)
        self.play(Write(text5), run_time=2)
        self.wait()
        self.play(TransformMatchingTex(text5, error_formula))
        self.wait(4.5)

        plane.clear_updaters()
        mobj_to_fade = [axes, graph, graph_mesh, plane, mesh_plane, frase2]
        self.play(*map(FadeOut, mobj_to_fade))

        HEISSIAN_COLOR = YELLOW
        LINEAR_TERM_COLOR = BLUE
        FX0_COLOR = GREEN_D
        FX0H_COLOR = GREEN_A

        t2c = {
            "f(x_0+h)": FX0H_COLOR,
            "f(x_0)": FX0_COLOR,
            r"\langle\nabla f(x_0),h\rangle": LINEAR_TERM_COLOR,
            r"\frac12 h^TH_fh": HEISSIAN_COLOR,
            r"\partial_{xx}f": HEISSIAN_COLOR,
            r"\partial_{xy}f": HEISSIAN_COLOR,
            r"\partial_{yx}f": HEISSIAN_COLOR,
            r"\partial_{yy}f": HEISSIAN_COLOR
        }

        t1 = "Da dove nasce questa curvatura?"
        t2 = "Dobbiamo guardare oltre il primo ordine"

        taylor_formula = [
            r"f(x_0+h)",
            r"f(x_0+h) = f(x_0) ",
            r"f(x_0+h) = f(x_0) + \langle\nabla f(x_0),h\rangle ",
            r"f(x_0+h) = f(x_0) + \langle\nabla f(x_0),h\rangle + \frac12 h^TH_fh",
            r"f(x_0+h) = f(x_0) + \langle\nabla f(x_0),h\rangle + \frac12 h^TH_fh + o(|h|^2)"
        ]

        text1, text2 = frase = Group(
            TexText(t1, font_size=FS),
            TexText(t2, font_size=FS)
        ).fix_in_frame().arrange(DOWN)

        text_formula = [Tex(t, font_size=FS, t2c=t2c).fix_in_frame().to_edge(UP, buff=LARGE_BUFF) for t in taylor_formula]

        self.play(Write(text1), run_time=2)
        self.wait(4)
        self.play(Write(text2), run_time=2)
        self.wait(2)
        self.play(FadeOut(frase))
        self.play(Write(text_formula[0]), run_time=2)
        for i in range(len(taylor_formula) - 1):
            self.play(TransformMatchingTex(text_formula[i], text_formula[i + 1]), run_time=1.5)

        self.play(error_formula.animate.next_to(text_formula[-1], UP))

        steps = [
            r"f(x_0+h) - f(x_0) - \langle\nabla f(x_0),h\rangle = \frac12 h^TH_fh + o(|h|^2)",
            r"e(h) = \frac12 h^TH_fh + o(|h|^2)",
            r"e(h) = \frac12 h^T \begin{pmatrix}\partial_{xx}f &\partial_{xy}f\\ \partial_{yx}f &\partial_{yy}f\end{pmatrix} h + o(|h|^2)",
            r"e(h) = \frac12 \begin{pmatrix}h^1,h^2\end{pmatrix} \begin{pmatrix}\partial_{xx}f &\partial_{xy}f\\ \partial_{yx}f &\partial_{yy}f\end{pmatrix} \begin{pmatrix}h^1\\ h^2\end{pmatrix} + o(|h|^2)",
            r"e(h) = (h^1)^2 \frac12\partial_{xx}f + h^1h^2\partial_{xy}f +  (h^2)^2 \frac12\partial_{yy}f + o(|h|^2)",
        ]

        # Data Structure: (start_source, end_source, start_target, end_target)
        # Using None to replicate open slice behaviour (e.g. [:24] becomes None, 24)
        raw_indices = [
            # Transition 0 -> 1 (steps[0] -> steps[1])
            [
                (None, 24, None, 4),
                (24, None, 4, None)
            ],
            # Transition 1 -> 2 (steps[1] -> steps[2])
            [
                (None, 10, None, 10),
                (10, 12, 10, 28),
                (12, None, 28, None),
            ],
            # Transition 2 -> 3
            [
                (8, 10, 8, 15),
                (10, 28, 15, 33),
                (28, 29, 33, 39),
                (29, None, 39, None),
            ],
            # Transition 3 -> 4
            [
                (None, 5, None, 5),
                (5, 8, 10, 13),
                (16, 20, 13, 17),
                (24, 28, 22, 26),
                (28, 32, 35, 39),
                (39, None, 39, None),
            ]
        ]

        tex_steps = [Tex(steps[i], font_size=FS, t2c=t2c).fix_in_frame() for i in range(len(steps))]
        tex_steps[0].next_to(text_formula[-1], DOWN)
        for i in range(1, len(steps)): tex_steps[i].next_to(tex_steps[i-1], DOWN)

        matched_pairs = [
            [
                (tex_steps[i][s_start:s_end], tex_steps[i+1][t_start:t_end])
                for s_start, s_end, t_start, t_end in transitions
            ]
            for i, transitions in enumerate(raw_indices)
        ]

        self.play(TransformMatchingTex(text_formula[-1].copy(), tex_steps[0]))
        self.wait(1)
        for i in range(1, len(steps)):
            self.play(TransformMatchingTex(tex_steps[i-1].copy(), tex_steps[i], matched_pairs=matched_pairs[i-1]))
        self.wait(3)

        self.play(*map(FadeOut, [text_formula[-1], *tex_steps[:-1], error_formula]))
        self.remove(frase, *text_formula, error_formula)

        abc_to_isolate = ["x^2", "a", "xy", "c", "y^2", "b"]
        step_to_isolate = ["(h^1)^2", r"\frac12\partial_{xx}f", "h^1h^2", r"\partial_{xy}f", "(h^2)^2", r"\frac12\partial_{yy}f"]

        abc_formula = Tex(
            "a x^2 + c xy + b y^2 ",
            isolate=abc_to_isolate,
            font_size=FS+10
        ).fix_in_frame()
        tex_steps[-2].set_color(WHITE)
        self.play(tex_steps[-1].animate.next_to(abc_formula, UP).set_color(WHITE))
        self.play(Write(abc_formula))
        for i in range(len(abc_to_isolate)):
            self.play(*map(Indicate, [
                abc_formula.get_part_by_tex(abc_to_isolate[i]),
                tex_steps[-1].get_part_by_tex(step_to_isolate[i])
            ]), run_time=2)

        self.play(FadeOut(abc_formula), tex_steps[-1].animate.to_edge(UP, buff=MED_LARGE_BUFF))
        self.remove(plane, mesh_plane, abc_formula)

        plane = NumberPlane(x_range=(-4, 4), y_range=(-4, 4),
                            background_line_style={"stroke_color": WHITE, "stroke_width": 1.25, "stroke_opacity": 0.4})
        x, y = axis_labels = VGroup(Tex("h^1"), Tex("h^2"))
        x.next_to(plane.axes, RIGHT)
        y.next_to(plane.axes, UP)
        plane.axis_labels = axis_labels
        plane.add(axis_labels)

        frame.set_euler_angles(gamma=0 * DEGREES, phi=80 * DEGREES).move_to(ORIGIN)

        df_dx = lambda x, y: self.der_par_x(self.func, x, y)
        df_dy = lambda x, y: self.der_par_y(self.func, x, y)

        # derivate parziali
        dxx = lambda x, y: self.der_par_x(df_dx, x, y)
        dxy = lambda x, y: self.der_par_y(df_dx, x, y)
        dyy = lambda x, y: self.der_par_y(df_dy, x, y)

        # heissiana
        Hf = lambda x, y: [[dxx(x, y), dxy(x, y)], [dxy(x, y), dyy(x, y)]]

        new_f = lambda u, v: -self.func(u, v) + self.func(0, 0) # f rovesciata
        paraboloid = lambda u, v: 0.5 * dxx(0, 0) * u**2 + dxy(0,0) * u * v + 0.5 * dyy(0, 0) * v**2


        graph = self.get_function_graph(axes, paraboloid, opacity=0.5, color=GREY_A, resolution=(50, 50)).set_z_index(-1)
        graph_mesh = self.get_mesh(graph).set_z_index(-1)

        f_graph = self.get_function_graph(axes, self.func, opacity=0.5)
        f_graph_mesh = self.get_mesh(f_graph).set_z_index(-1)

        shift_in = ORIGIN - axes.c2p(0,0,self.func(0, 0))

        # forse ste 2 righe son da togliere
        frame.rotate(180 * DEGREES).shift(IN).scale(1.4).set_euler_angles(phi=95 * DEGREES)
        f_graph.shift(shift_in), f_graph_mesh.shift(shift_in)

        self.play(*map(ShowCreation, [f_graph, f_graph_mesh]))

        self.play(
            frame.animate.rotate(90*DEGREES).scale(1.7).set_euler_angles(phi=0),
            FadeOut(tex_steps[-1]), run_time=4
        )
        self.play(ShowCreation(plane))
        self.play(frame.animate.set_euler_angles(phi=75*DEGREES).scale(0.7), run_time=5)
        self.play(*map(ShowCreation, [graph, graph_mesh]), Write(tex_steps[-1]),  run_time=2)

        tex_steps[-2].move_to(tex_steps[-1])
        self.play(TransformMatchingTex(tex_steps[-1], tex_steps[-2]),  run_time=2)
        self.play( *map(FadeOut, [f_graph, f_graph_mesh]) )

        opacity_value = 0.3
        diag_txt = r"e(h) = \frac12 \begin{pmatrix}h^1,h^2\end{pmatrix} P \begin{pmatrix}\lambda_1 &0\\ 0 &\lambda_2\end{pmatrix}P^T \begin{pmatrix}h^1\\ h^2\end{pmatrix} + o(|h|^2)"
        diag = Tex(diag_txt, font_size=FS).fix_in_frame().move_to(tex_steps[-2])
        diag.save_state()
        diag[:15].set_opacity(opacity_value)
        diag[26:].set_opacity(opacity_value)
        matched_pairs = [
            (tex_steps[-2][:15], diag[:15]),
            (tex_steps[-2][15:33], diag[15:26]),
            (tex_steps[-2][33:], diag[26:]),
        ]
        self.play(
            tex_steps[-2][:15].animate.set_opacity(opacity_value),
            tex_steps[-2][33:].animate.set_opacity(opacity_value),  run_time=2
        )


        frase1, frase2 = gruppo = self.get_comb_sentences([
                self.get_sentence(["Dunque possiamo diagonalizzarla,", r"$\lambda_1,\lambda_2$ sono i due autovalori"]),
                self.get_sentence(["Nell'esempio che state vedendo sono ", r"$\lambda_1=-2+\sqrt{2}$ e $\lambda_2=-2-\sqrt{2}$"]),
        ]).next_to(tex_steps[-2], DOWN)

        gruppo2 = self.get_comb_sentences([
            self.get_sentence(["Applicare il cambio di variabile $u=P^Th$", "equivale a considerare gli assi $u^1$, $u^2$ ruotati"]),
            self.get_sentence([r"in cui si ha la forma canonica di $e(\cdot)$"]),
        ]).to_edge(DOWN, buff=MED_SMALL_BUFF)

        canon_txt = r"e(h) = \frac12 u^T \begin{pmatrix}\lambda_1 &0\\ 0 &\lambda_2\end{pmatrix} u + o(|h|^2)"
        canon = Tex(canon_txt, font_size=FS).fix_in_frame().move_to(tex_steps[-2])

        u1 = Arrow(
            plane.get_origin(), plane.x_axis.get_end(),
            fill_color=RED, buff=0, stroke_width=1, stroke_color=RED
        ).set_z_index(-2).shift(OUT*0.01)
        u2 = Arrow(
            plane.get_origin(), plane.y_axis.get_end(),
            fill_color=RED, buff=0, stroke_width=1, stroke_color=RED
        ).set_z_index(-2).shift(OUT*0.01)
        u1_label = Tex("u^1", t2c={"u^1":RED}).next_to(u1.get_end(), UR)
        u2_label = Tex("u^2", t2c={"u^2":RED}).next_to(u2.get_end(), UR)

        always(u1_label.next_to, u1.get_end(), UR)
        always(u2_label.next_to, u2.get_end(), UR)

        lam1 = ValueTracker(-0.5858)
        lam2 = ValueTracker(-3.4142)
        theta = ValueTracker(5 * PI / 12)

        self.play(Write(frase1[0]))
        frame.save_state()
        self.play(TransformMatchingTex(tex_steps[-2],diag, matched_pairs=matched_pairs), Write(frase1[1]), run_time=2)
        self.wait(2)
        self.play(frame.animate.scale(1.8).set_euler_angles(phi=0*DEGREES), FadeOut(frase1))
        self.play(Write(gruppo2[0][0]))
        self.play(diag.animate.restore())
        self.play(
            TransformMatchingTex(
                diag, canon,
                matched_pairs=[
                    (diag[:8], canon[:8]),
                    (diag[8:16], canon[8:10]),
                    (diag[16:24], canon[10:18]),
                    (diag[24:27], canon[18:19]),
                    (diag[27:], canon[19:])
                ]
            ), run_time=2
        )
        self.play(*map(ShowCreation, [u1,u2]), *map(Write, [u1_label,u2_label]))
        self.play(
            Write(gruppo2[0][1]),
            u1.animate.rotate(-65 * DEGREES, about_point=plane.get_origin()),
            u2.animate.rotate(-65 * DEGREES, about_point=plane.get_origin()),
            run_time=5
        )
        self.play(Write(gruppo2[1]))
        self.wait(4)
        self.play(frame.animate.restore(), FadeOut(gruppo2), *map(FadeOut, [u1, u2, u1_label,u2_label]))

        self.play(Write(frase2[0]))
        self.play(Write(frase2[1]))

        frase = self.get_sentence([
            r"$\lambda_1=-2+\sqrt{2}$ e $\lambda_2=-2-\sqrt{2}$", "sono entrambi numeri negativi,",
            "per questo la parabola e' rivolta verso il basso"
        ]).to_corner(UL, buff=MED_SMALL_BUFF)

        target = self.get_sentence([r"$\lambda_1<0$ e $\lambda_2<0$", "sono entrambi numeri negativi,"]).to_corner(UL, buff=MED_SMALL_BUFF)

        self.play(*map(FadeOut, [frase2, canon]), TransformMatchingTex(frase2[1].copy(), frase[0]), run_time=2)
        self.play(Write(frase[1]))
        self.play(TransformMatchingTex(frase[0], target[0]), TransformMatchingTex(frase[1], target[1]))
        frase[2].next_to(target[1], RIGHT, buff=SMALL_BUFF)
        self.play(Write(frase[2]))

        get_e = lambda l1, l2, th: lambda u, v: 0.5 * (l1 * (u * np.cos(th) + v * np.sin(th))**2
                                                       + l2 * (-u * np.sin(th) + v * np.cos(th))**2)

        l1 = Group(
            Tex("\lambda_1=", font_size=FS),
            DecimalNumber(lam1.get_value(), font_size=FS, stroke_width=0.05, stroke_color=BLACK, show_ellipsis=True),
        ).fix_in_frame().arrange(RIGHT, buff=SMALL_BUFF).to_edge(UP).shift(RIGHT*5)
        l2 = Group(
            Tex("\lambda_2=", font_size=FS),
            DecimalNumber( lam2.get_value(), font_size=FS, stroke_width=0.05, stroke_color=BLACK, show_ellipsis=True)
        ).fix_in_frame().arrange(RIGHT, buff=SMALL_BUFF).next_to(l1, DOWN)

        self.play(
            FadeOut(frase[2]), FadeOut(target),
            TransformMatchingTex(target[0].copy(), l1[0]),
            TransformMatchingTex(target[0].copy(), l2[0])
        )

        self.play(Write(l1[1]), Write(l2[1]),)

        f_always(l1[1].set_value,lam1.get_value)
        f_always(l2[1].set_value,lam2.get_value)

        frase = self.get_sentence(["Invece per segni opposti si ha una sella"]).to_corner(UL, buff=MED_SMALL_BUFF)
        self.play(Write(frase))

        # graph.add_updater(lambda mob: mob.become(self.get_function_graph(axes, e, resolution=(28, 28), opacity=0.5, color=GREY_A)))
        # graph_mesh.add_updater(lambda mob: mob.become(self.get_mesh(graph)))

        new_lambda_values = [0.5, -3.4142]
        new_graph = self.get_function_graph(
            axes, get_e(new_lambda_values[0], new_lambda_values[1], theta.get_value()),
            resolution=(50, 50), opacity=0.5, color=GREY_A
        )
        self.play(
            lam1.animate.set_value(new_lambda_values[0]),
            graph.animate.become(new_graph),
            graph_mesh.animate.become(self.get_mesh(new_graph)),
            frame.animate.scale(1.5).set_euler_angles(phi=65*DEGREES),
            run_time=3
        )
        self.wait(2)

        new_lambda_values = [-3.4142, 0.5 ]
        new_graph = self.get_function_graph(
            axes, get_e(new_lambda_values[0], new_lambda_values[1], theta.get_value()),
            resolution=(50, 50), opacity=0.5, color=GREY_A
        )
        self.play(
            lam1.animate.set_value(new_lambda_values[0]),
            lam2.animate.set_value(new_lambda_values[1]),
            graph.animate.become(new_graph),
            graph_mesh.animate.become(self.get_mesh(new_graph)),
            run_time=3
        )

        self.play(FadeOut(frase))

        frase = self.get_sentence(["Se entrambi positivi", "la parabola e' rivolta verso l'alto"]).to_corner(DL, buff=MED_SMALL_BUFF)
        self.play(Write(frase[0]))

        new_lambda_values = [0.4312, 0.6174]
        new_graph = self.get_function_graph(
            axes, get_e(new_lambda_values[0], new_lambda_values[1], theta.get_value()),
            resolution=(50, 50), opacity=0.5, color=GREY_A
        )

        self.play(
            Write(frase[1]),
            frame.animate.set_euler_angles(phi=85 * DEGREES).shift(3*OUT).scale(0.8),
            lam1.animate.set_value(new_lambda_values[0]),
            lam2.animate.set_value(new_lambda_values[1]),
            graph.animate.become(new_graph),
            graph_mesh.animate.become(self.get_mesh(new_graph)),
            run_time=3
        )
        self.wait(8)

        # self.embed()

    def get_sentence(self, texts : list[str], fix=True, arrange = RIGHT, buff=SMALL_BUFF) -> Group[TexText]:
        texts_mobj = [TexText(text, font_size=self.FONT_SIZE) for text in texts]
        if len(texts_mobj) > 1:
            frase = Group(*texts_mobj)
            frase.arrange(arrange, buff=buff)
        else:
            frase = texts_mobj[0]
        if fix: frase.fix_in_frame()

        return frase

    def get_comb_sentences(self, sentences : list, fix=True, arrange=DOWN, buff=SMALL_BUFF) -> Group[TexText | Group[TexText]]:
        final_sentence = Group()

        for mob in sentences:
            if isinstance(mob, list):
                final_sentence.add(self.get_sentence(mob))
                continue

            final_sentence.add(mob)

        if fix: final_sentence.fix_in_frame()
        final_sentence.arrange(arrange, buff=buff)

        return final_sentence

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

        flatline = Line(ORIGIN, length * RIGHT)
        super().__init__(flatline, direction=DOWN, **kwargs)  # np.array([0., -1., 0.])
        dline = line.get_end() - line.get_start()
        self.rotate(angle=rotation, about_point=flatline.get_start(), axis=RIGHT)
        # if np.linalg.norm(dline) > 0.0001:
        self.rotate(-np.asin(dline[2] / np.linalg.norm(dline)), about_point=flatline.get_start(), axis=UP)
        self.rotate(np.atan2(dline[1], dline[0]), about_point=flatline.get_start(), axis=OUT)
        self.shift(line.get_start() - flatline.get_start())
