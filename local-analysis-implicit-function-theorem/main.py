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

        xc, yc = paraboloid_center = (2, 1)
        a, b, c = (0.5, 2, 1)
        f = lambda x, y: a * (x - xc) ** 2 + b * (y - yc) ** 2

        paraboloid = self.get_function_graph(axes, f, opacity=0.35)
        paraboloid_mesh = SurfaceMesh(paraboloid, stroke_opacity=0.5)
        surface = Group(paraboloid_mesh, paraboloid)

        plane = self.get_function_graph(axes, lambda x, y: c, opacity=0.35, resolution=(10, 10))
        curve = self.get_ellissoid_curve(axes, paraboloid_center, a, b, c)

        texts = ["$F(x,y)$", "$F(x,y)=c$", "$F(x,y)-c=0$", "$G(x,y)=0$", r"$x\mapsto y(x)$ ?"]
        seq = TextSequence(texts)
        seq.target.to_corner(UR, buff=LARGE_BUFF)

        self.play(ShowCreation(axes))
        self.play(*map(ShowCreation, surface), seq.next_and_play(), run_time=3)
        self.play(ShowCreation(plane), seq.next_and_play(), run_time=2)

        self.next_slide()
        self.play(ShowCreation(curve), run_time=2)

        self.play(FadeOut(plane))
        shift_qty = ORIGIN - axes.c2p(0, 0, c)

        self.next_slide()
        self.play(surface.animate.shift(shift_qty), curve.animate.shift(shift_qty), seq.next_and_play())

        self.play(seq.next_and_play())

        self.next_slide()
        self.play(
            frame.animate.set_euler_angles(phi=0, theta=0).move_to(axes.c2p(xc, yc, 0)),
            FadeOut(surface), run_time=2
        )


        hypot_func = TextSequence([r"$x\mapsto y(x)$", "$\exists y(x)$ ? "])
        hypot_func.target.next_to(eq_problem.current_mob, DOWN)
        hypot_func.next().set_color(YELLOW)

        RR = "\mathbb{R}"
        comment = TextSequence(
            [
                "Questa non e' una funzione",
                r"Ma localmente?\\ In un intorno di $(x_0,y_0)$?",
                "Il teorema della funzione implicita risponde a questa domanda",
                fr"Sia $A\subset{RR}^2$ e $F:A\to{RR}^2$ di classe $C^1$, se $F(x_0,y_0)=0$ per $(x_0,y_0)\in A$ e se\\[4pt] "
                r"$\displaystyle\frac{\partial F}{\partial y}\neq 0$\\[4pt] allora $\exists ! y(x) $ tale che $F(x,y(x))=0$ in un intorno di $(x_0,y_0)$",
                r"Qual e' il significato di $\displaystyle\frac{\partial F}{\partial y}\neq 0$ ? ",
                "Per capirlo facciamo qualche passo indietro"
            ]
        )
        comment.target.next_to(hypot_func.target, 2*DOWN)
        self.play(hypot_func.play())
        self.play(comment.next_and_play(), frame.animate.scale(camera_scaling))

        self.next_slide() # Creating Arc in the neighborhood of (x0,y0)

        ARC_COLOR = PINK
        alpha_start, alpha_end = [0.05, 0.25]
        arc = curve.get_subcurve(alpha_start, alpha_end).set_color(ARC_COLOR).set_stroke(width=8)
        arc_middle = curve.point_from_proportion(0.5 * (alpha_end + alpha_start) - 0.01)
        point = Dot(arc_middle, radius=0.05).set_color(ARC_COLOR)
        self.play(eq_problem.fade_out(), comment.fade_out(), hypot_func.fade_out())
        hypot_func.next().set_color(ARC_COLOR).next_to(self.to_fixed_coord(point.get_center(), camera_center, total_scaling), UR)

        comment.next().set_color_by_tex("intorno di $(x_0,y_0)$", ARC_COLOR)
        self.play(curve.animate.set_color(GREY_A))
        self.play(comment.play())
        self.play(ShowCreation(arc), ShowCreation(point), hypot_func.play(), run_time=3)

        comment.target.move_to(ORIGIN).to_edge(UP, buff=LARGE_BUFF).shift(RIGHT * 0.5)
        comment.next()
        self.play(comment.play())

        comment.next()[52:60].set_color(ARC_COLOR)
        self.play(comment.play())

        self.next_slide()
        comment.next()[21:29].set_color(ARC_COLOR)
        self.play(comment.play(matched_pairs=[(comment.last_mob[52:60], comment.current_mob[21:29])]))
        self.wait()
        self.play(comment.next_and_play())
        # self.embed()

class Derivative(CommonToAll, Slide):
    def construct(self):
        comment = TextSequence(["Immaginiamo di avere una funzione"])
        frame = self.camera.frame
        # Plot a function
        
        #  - get axes
        x_range = (-3, 3)
        y_range = (-3, 3)
        axes = Axes( x_range=x_range, y_range=y_range ).set_stroke(width=5, color=GREY)
        axes.axis_labels = VGroup(*map(Tex, ["x", "f(x)"]))
        axes.add(axes.axis_labels)
        axes.add_coordinate_labels(font_size=18, excluding=[])
        axes.coordinate_labels[0][x_range[1]].set_opacity(0)
        axes.coordinate_labels[1][y_range[1]].set_opacity(0)
        self.add(axes)
        
        self.wait(1)

        # - draw function
        def func(x):
            return x ** 3 + 3 * x ** 2 - x - 3
        curve = ParametricCurve(
            lambda t: (axes.c2p(t, func(t))), (-3.5, x_range[1], 0.1)
        ).set_stroke(width=8, color=BLUE, opacity=0.7)
        f_of_x = Tex(r"f(x) = x^3 + 3x^2 - x - 4", font_size=40).set_color(BLUE).to_corner(UR, buff=0.5)
        self.play(Write(f_of_x, run_time=2), ShowCreation(curve, run_time=4))
        self.wait(1)

        # Draw a set of local axes labeled dx and dy
        points = curve.get_points()
        chosen_point_index = 20
        localAxes = Axes( x_range=(-5, 5), y_range=(-5, 5) )
        localAxes.axis_labels = VGroup(*map(Tex, ["dx", "df(x)"]))
        localAxes.axis_labels.set_opacity(0)
        localAxes.set_stroke(width=3, color=GREY).scale(0.1).move_to(points[chosen_point_index])

        self.bring_to_back(localAxes) # modifies the z-index
        self.play(FadeIn(localAxes))

        # Zoom in on part of the graph
        frame.save_state()
        zoom_run_time = 5
        self.play(
            FadeOut(f_of_x),
            frame.animate(run_time=zoom_run_time).scale(0.008).move_to(points[chosen_point_index] + UP * 0.01),
            localAxes.animate(run_time=zoom_run_time).set_stroke(width=5)
        )

        # Show small changes in x and y
        braces_scaling = 0.011
        text_buff = 0.002
        text_FS = 0.5
        F_COLOR = PINK
        X_COLOR = YELLOW

        texts = [texts] if isinstance(texts, str) else texts  # check and adjusts depening on how many strings
        texts_mobj = [TexText(text, font_size=self.FONT_SIZE) for text in texts]

        if len(texts_mobj) > 1:
            frase = Group(*texts_mobj)
            frase.arrange(arrange, buff=buff)
        else:
            frase = texts_mobj[0]
        if fix: frase.fix_in_frame()

        # View the function as a transformation
        input_space = axes.get_x_axis()
        input_space[1].set_color(YELLOW)
        n = 250
        x_min = 0
        x_max = 3
        dots = VGroup(*[
            Dot(radius=0.001)
                      .move_to(input_space.n2p(x_min + (i / (n - 1)) * (x_max - x_min)))
                      .set_color(interpolate_color(YELLOW_E, YELLOW_A, i / n))
                      .set_stroke(width=10)
            for i in range(n)
        ])
        self.play(AnimationGroup(*[FadeIn(dot, shift=DOWN) for dot in dots], lag_ratio=0.003))

    def get_comb_sentences(self, sentences: list, fix=True, arrange=DOWN, buff=SMALL_BUFF) -> Group[TexText | Group[TexText]]:
        final_sentence = Group()

        for mob in sentences:
            if isinstance(mob, list):
                final_sentence.add(self.get_sentence(mob))
                continue

            final_sentence.add(mob)

        if fix: final_sentence.fix_in_frame()
        final_sentence.arrange(arrange, buff=buff)

        return final_sentence


class TextSequence:
    def __init__(self, texts, font_size=30, corner=UR, buff=LARGE_BUFF):
        self.texts = texts
        self.font_size = font_size
        self.corner = corner
        self.buff = buff

        self.index = 0
        self.saved = None
        self.last_mob = None
        self.current_mob = None

        self.target = VectorizedPoint(ORIGIN)

    def next(self):
        """Passa alla stringa successiva nella sequenza."""
        if self.index >= len(self.texts): return None

        # Genera e posiziona il nuovo testo
        new_text = TexText(self.texts[self.index], font_size=self.font_size)
        new_text.fix_in_frame()
        new_text.move_to(self.target)

        # Aggiorna lo stato
        self.last_mob = self.current_mob
        self.current_mob = new_text
        self.index += 1

        return self.current_mob

    def play(self, **kwargs):
        """plays current animation"""
        if self.last_mob is None:
            return Write(self.current_mob)
        else:
            return TransformMatchingTex(self.last_mob, self.current_mob, **kwargs)

    def next_and_play(self, **kwargs):
        self.next()
        return self.play(**kwargs)

    def save(self):
        self.saved = self.current_mob

    def restore(self, **kwargs):
        if self.saved is None: return None
        self.last_mob = self.current_mob
        self.current_mob = self.saved
        self.saved = None
        return TransformMatchingTex(self.last_mob, self.current_mob, **kwargs)

    def clear(self):
        """Fa svanire il testo attualmente a schermo."""
        if self.current_mob is not None:
            fade_animation = FadeOut(self.current_mob)
            self.current_mob = None
            return fade_animation
        return None

# manim-slides convert Intro slides.html --open
# manim-slides convert Intro slides.html -cwidth=1920 -cheight=1080 --open
# manim-slides convert Intro slides.html -cwidth=1920 -cheight=1080 -cmargin=0 -cmin_scale=1 -cmax_scale=1 --open
# manimgl main.py Intro -w --hd

# manim-slides Intro
# manim-slides render --GL main.py Intro
