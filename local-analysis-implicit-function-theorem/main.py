from manimlib import *
from manim_slides.slide import Slide, ThreeDSlide

class CommonToAll(ThreeDSlide):
    FONT_SIZE = 30

class BaseAxisSurfaceScene(CommonToAll):

    def get_axes(
            self,
            x_range=(-3, 5),
            y_range=(-3, 5),
            z_range=(0, 1.5, 0.5),
            width=8,
            height=8,
            depth=3,
            center=ORIGIN,
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

    def get_ellissoid_curve(self, axes, center, a, b, c) -> ParametricCurve:
        xc, yc = center
        curve = ParametricCurve(
            lambda t: axes.c2p(xc + np.sqrt(c / a) * np.cos(t), yc + np.sqrt(c / b) * np.sin(t), c),
            (-PI, PI, 0.1))
        curve.set_stroke(width=5, opacity=1, color=YELLOW)
        return curve

class Intro(BaseAxisSurfaceScene):

    def construct(self):
        frame = self.camera.frame
        frame.set_euler_angles(phi=65 * DEGREES, theta=30 * DEGREES).shift(UP).scale(1.3)
        axes = self.get_axes()

        xc, yc = paraboloid_center = (2,1)
        a, b, c = (0.5,2, 1)
        f = lambda x,y : a * (x - xc) ** 2 + b * (y - yc) ** 2

        paraboloid = self.get_function_graph(axes, f, opacity=0.35)
        paraboloid_mesh = SurfaceMesh(paraboloid, stroke_opacity=0.5)
        surface = Group(paraboloid_mesh, paraboloid)

        plane = self.get_function_graph(axes, lambda x,y: c, opacity=0.35, resolution=(10,10))
        curve = self.get_ellissoid_curve(axes, paraboloid_center, a, b, c)

        texts = ["$F(x,y)$", "$F(x,y)=c$", "$F(x,y)-c=0$", "$G(x,y)=0$", "$x\mapsto y(x)$ ?"]
        on_screen = self.get_sentence(texts[0]).to_corner(UR, buff=LARGE_BUFF)
        next_one = self.get_sentence(texts[1]).to_corner(UR, buff=LARGE_BUFF)

        self.play(ShowCreation(axes))
        self.play(*map(ShowCreation, surface), Write(on_screen), run_time=3)
        self.play(ShowCreation(plane), TransformMatchingTex(on_screen, next_one), run_time=2)
        on_screen = next_one
        next_one = self.get_sentence(texts[2]).to_corner(UR, buff=LARGE_BUFF)


        self.next_slide()
        self.play(ShowCreation(curve), run_time=2)

        self.play(FadeOut(plane))
        shift_qty = ORIGIN - axes.c2p(0, 0, c)

        self.next_slide()
        self.play(surface.animate.shift(shift_qty), curve.animate.shift(shift_qty), TransformMatchingTex(on_screen, next_one))
        on_screen = next_one
        next_one = self.get_sentence(texts[3]).to_corner(UR, buff=LARGE_BUFF).next_to(on_screen, DOWN)

        self.play(TransformMatchingTex(on_screen, next_one))
        on_screen = next_one
        next_one = self.get_sentence(texts[3]).to_corner(UR, buff=LARGE_BUFF).next_to(on_screen, DOWN)
        # fare una classe che mi permetta di gestire tutte le scritte scena per scena, e posso fare next, next_next, last, last_last, fade personalizzati

        self.next_slide()
        self.play(
            frame.animate.set_euler_angles(phi=0, theta=0).move_to(axes.c2p(xc, yc, 0)),
            FadeOut(surface), run_time=2
        )

    def get_sentence(self, texts : list[str] | str, fix=True, arrange = RIGHT, buff=SMALL_BUFF) -> Group[TexText] | TexText:

        texts = [texts] if isinstance(texts, str) else texts # check and adjusts depening on how many strings
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

# manim-slides convert Intro slides.html --open
# manim-slides convert Intro slides.html -cwidth=1920 -cheight=1080 --open
# manim-slides convert Intro slides.html -cwidth=1920 -cheight=1080 -cmargin=0 -cmin_scale=1 -cmax_scale=1 --open
# manimgl main.py Intro -w --hd

# manim-slides Intro
# manim-slides render --GL main.py Intro



















