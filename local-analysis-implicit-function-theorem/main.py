from manimlib import *
from manim_slides.slide import Slide, ThreeDSlide



class CommonToAll:

    FONT_SIZE = 30

    def get_sentence(self, texts: list[str] | str, fix=True, arrange=RIGHT, buff=SMALL_BUFF) -> Group[TexText] | TexText:

        texts = [texts] if isinstance(texts, str) else texts  # check and adjusts depening on how many strings
        texts_mobj = [TexText(text, font_size=self.FONT_SIZE) for text in texts]

        if len(texts_mobj) > 1:
            frase = Group(*texts_mobj)
            frase.arrange(arrange, buff=buff)
        else:
            frase = texts_mobj[0]
        if fix: frase.fix_in_frame()

        return frase

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

class BaseAxisSurfaceScene(CommonToAll, ThreeDSlide):

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

    def to_fixed_coord(self, point = ORIGIN, camera_center = ORIGIN, camera_scaling = 1.):
        # doesn't condisider rotations
        return (point-camera_center)*(1/camera_scaling)

    def construct(self):
        frame = self.camera.frame

        camera_scaling = 1.3
        total_scaling = camera_scaling
        frame.set_euler_angles(phi=65 * DEGREES, theta=30 * DEGREES).shift(UP).scale(camera_scaling)
        axes = self.get_axes()

        xc, yc = paraboloid_center = (2, 1)
        a, b, c = (0.5, 2, 1)
        f = lambda x, y: a * (x - xc) ** 2 + b * (y - yc) ** 2

        paraboloid = self.get_function_graph(axes, f, opacity=0.35)
        paraboloid_mesh = SurfaceMesh(paraboloid, stroke_opacity=0.5)
        surface = Group(paraboloid_mesh, paraboloid)

        plane = self.get_function_graph(axes, lambda x, y: c, opacity=0.35, resolution=(10, 10))
        curve = self.get_ellissoid_curve(axes, paraboloid_center, a, b, c)

        texts = ["$F(x,y)$", "$F(x,y)=c$", "$F(x,y)-c=0$", "$G(x,y)=0$"]
        eq_problem = TextSequence(texts)
        eq_problem.target.to_corner(UR, buff=LARGE_BUFF).shift(LEFT)

        self.play(ShowCreation(axes))
        self.play(*map(ShowCreation, surface), eq_problem.next_and_play(), run_time=3)
        self.play(ShowCreation(plane), eq_problem.next_and_play(), run_time=2)

        self.next_slide()
        self.play(ShowCreation(curve), run_time=2)

        self.play(FadeOut(plane))
        shift_qty = ORIGIN - axes.c2p(0, 0, c)

        self.next_slide()
        self.play(surface.animate.shift(shift_qty), curve.animate.shift(shift_qty), eq_problem.next_and_play())
        self.play(eq_problem.next_and_play())

        self.next_slide() # Zoomming on ellipse

        camera_center = axes.c2p(xc, yc, 0)
        camera_scaling = 0.4
        total_scaling *= camera_scaling

        # camera_center = ORIGIN
        # camera_scaling = 0

        self.play(
            frame.animate.set_euler_angles(phi=0, theta=0).move_to(camera_center),
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
        self.play(ShowCreation(arc), ShowCreation(point), hypot_func.play(), curve.animate.set_stroke(opacity=0.2), run_time=3)
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

class CommonToDerivative(CommonToAll):
    X_COLOR = YELLOW
    F_COLOR = PINK
    FONT_SIZE = 35
    RR = r"\mathbb{R}"
    IO_DOTS_RADIUS = 0.016
    IO_DOTS_STROKE_WIDTH = 10
    IO_DOT_ANIM_LAG_RATIO = 0.05

    def get_axes(
            self,
            x_range=(-3, 3), y_range=(-3, 3),
            width=5,
            color=GREY,
            center=ORIGIN,
            show_numbers=True,
    ) -> Axes:
        axes = Axes(x_range=x_range, y_range=y_range).set_stroke(width=width, color=color).shift(center-ORIGIN)

        x, y = axis_labels = VGroup(Tex("x", font_size=25), Tex("y", font_size=25))
        x.next_to(axes.x_axis, RIGHT)
        axes.x_axis.add(x)
        y.next_to(axes.y_axis, UP)
        axes.y_axis.add(y)
        axes.add(axis_labels)

        if show_numbers:
            axes.add_coordinate_labels(font_size=18, excluding=[])
            axes.coordinate_labels[0][x_range[1]].set_opacity(0)
            axes.coordinate_labels[1][y_range[1]].set_opacity(0)
        return axes


    def get_curve(self, axes, f, t_range=(-3, 3, 0.1)):
        return ParametricCurve(
            lambda t: (axes.c2p(t, f(t))), t_range=t_range
        ).set_stroke(width=8, color=BLUE, opacity=0.7)

class DerivativeMeaning(CommonToDerivative, Slide):
    def construct(self):
        frame = self.camera.frame

        axes = self.get_axes()
        self.add(axes)
        self.wait(1)

        # Plot a function
        def func(x):
            return x ** 3 + 3 * x ** 2 - x - 3
        curve = ParametricCurve(
            lambda t: (axes.c2p(t, func(t))), (-3.5, 3, 0.1)
        ).set_stroke(width=8, color=BLUE, opacity=0.7)

        DER_COLOR = GREEN
        t2c = {"$\Delta f$":self.F_COLOR, "$\Delta x$": self.X_COLOR, "$c$":DER_COLOR, "$f'(x)$": DER_COLOR}
        comment = TextSequence(
            [
                "Immaginiamo di avere una funzione",
                "Se ingrandiamo molto in un punto",
                r"$\Delta f$ e' quasi un multiplo\\ scalare di $\Delta x$",
                r"Avere derivata\\ significa proprio questo"
            ],
            font_size=self.FONT_SIZE,
            t2c = t2c
        )
        comment.next().to_corner(UR, buff=0.5)
        comment.target.move_to(comment.current_mob)
        f_of_x = Tex(r"f(x) = x^3 + 3x^2 - x - 3", font_size=35).set_color(BLUE).next_to(comment.current_mob, DOWN)

        self.play(comment.play())
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
            FadeOut(f_of_x), comment.next_and_play(),
            frame.animate(run_time=zoom_run_time).scale(0.008).move_to(points[chosen_point_index] + UP * 0.01),
            localAxes.animate(run_time=zoom_run_time).set_stroke(width=5)
        )

        # Show small changes in x and y
        braces_scaling = 0.011
        text_buff = 0.002
        text_FS = 0.5

        brace_x = Brace(Line(ORIGIN, RIGHT), DOWN).set_color(self.X_COLOR).scale(braces_scaling).align_to(localAxes.c2p(0, 0), UL)
        delta_x = Tex(r"\Delta x", font_size=text_FS).set_color(self.X_COLOR).next_to(brace_x, DOWN, buff=text_buff)

        comment.next()
        self.play(GrowFromEdge(brace_x, UP), Write(delta_x), comment.play())

        brace_fx = Brace(Line(ORIGIN, UP * 2.8), RIGHT).set_color(self.F_COLOR).scale(braces_scaling).align_to(brace_x.get_corner(UR), DL)
        delta_fx = Tex(r"\Delta f(x)", font_size=text_FS).set_color(self.F_COLOR).next_to(brace_fx, RIGHT, buff=text_buff)
        self.play(GrowFromEdge(brace_fx, LEFT), Write(delta_fx))

        # Show that Delta f(x) = Delta x * c

        equation = TextSequence(
            [
                r"$\Delta f(x) \approx \Delta x \cdot {c}$",
                r"$\Delta f(x) \approx \Delta x \cdot {f'(x)}$"
            ],
            t2c={r"\Delta f(x)": self.F_COLOR, r"\Delta x": self.X_COLOR, "{c}": DER_COLOR, "{f'(x)}": DER_COLOR},
            font_size=48,
        )
        equation.next().to_corner(UL, buff=MED_SMALL_BUFF).shift(RIGHT * 0.3)
        equation.target.move_to(equation.current_mob)


        msg = TextSequence(["(localmente)"], font_size=48)
        msg.next().scale(0.85).next_to(equation.current_mob, DOWN)

        self.play( equation.play(), msg.play(), run_time=2.5 )

        self.wait(2)
        rect = SurroundingRectangle(equation.current_mob, buff=0.1, fill_opacity=0, stroke_width=300, stroke_color=TEAL).fix_in_frame()
        self.play(ShowCreation(rect, run_time=2))
        self.play(FadeOut(rect))
        self.wait(1)

        self.play(comment.next_and_play())
        self.wait(2)
        # der_f = Tex("{f'(x)}").next_to(equation.current_mob, RIGHT, buff=SMALL_BUFF)

        self.play(equation.next_and_play())
        self.wait(2)
        self.play(*map(FadeOut, [localAxes, brace_x, brace_fx, delta_x, delta_fx, curve, axes]))
        self.wait(0.5)
        self.play(comment.fade_out(), equation.fade_out(), msg.fade_out())

        frame.restore()

        return
        # Zoom back out to see the graph
        self.play(
            *map(FadeOut, [localAxes, brace_x, brace_fx, delta_x, delta_fx]),
            comment.fade_out(), frame.animate(run_time=zoom_run_time).restore()
        )

        self.wait(0.5)
        self.play(*map(FadeOut, [axes.get_y_axis(), curve]), axes.coordinate_labels[0][x_range[1]].animate.set_opacity(1))


        return
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

        input_space_group = Group(input_space, dots)
        input_space_group.generate_target()
        output_space = input_space.copy()
        f_of_x_label = Tex("f(x)").set_color(PINK)
        f_of_x_label.set_height(
            input_space[1].get_height() / f_of_x_label[1].get_height()
        ).match_y(
            output_space[1]
        ).align_to(
            output_space[1], LEFT
        )
        output_space[1].become(f_of_x_label)
        Group(input_space_group.target, output_space).arrange(RIGHT, buff=0.7).set_width(FRAME_WIDTH * 0.98)


        input_space_text = TexText("Input Space", font_size=60).next_to(input_space_group.target[0], DOWN, buff=0.5).set_color(YELLOW)
        output_space_text = TexText("Output Space", font_size=60).next_to(output_space, DOWN, buff=0.5).set_color(PINK)
        equation.clear_updaters()
        equation.generate_target()
        equation.target.set_x(0).to_edge(DOWN, buff=0.7)
        equation.target[-len(msg):].next_to(equation.target[:-len(msg)], RIGHT, buff=0.25)
        self.play(
            f_of_x.animate.match_x(output_space).set_color(WHITE).set_color_by_tex_to_color_map({"f": PINK, "x": YELLOW}),
            MoveToTarget(equation, run_time=2),
            AnimationGroup(
                MoveToTarget(input_space_group),
                FadeIn(output_space, shift=LEFT * 0.5),
                FadeIn(VGroup(input_space_text, output_space_text), shift=UP * 0.4), lag_ratio=0.5),
        )

class InvertibleDerivative(CommonToDerivative, Slide):
    def construct(self):
        frame = self.camera.frame
        axes = self.get_axes(y_range=(-4,4), center=DOWN)

        comment = TextSequence(
            [
                r"In \textit{dimensione} $1$ la derivata e' interpretabile come\\ la retta tangente alla funzione in un punto",
                r"Interpretiamo la derivata\\ come un \textit{operatore}",
                "Prende dei punti in input",
                r"E per ognuno di quelli,\\ genera un output",
                r"Per ogni $y$",
                r"Per ogni $y$ esiste una sola $x$",
                r"Ossia l'\textit{operatore} e' invertibile",
                r"Tuttavia se la derivata e' nulla",
                r"Tuttavia se la derivata e' nulla\\ l'operatore non e' invertibile",
                r"In \textit{dimensione} $1$, richiedere la derivata non nulla\\ significa richiedere che l'operatore derivata sia invertibile",
            ], font_size=self.FONT_SIZE,
            t2c={"input": self.X_COLOR, "$x$":self.X_COLOR, "output": self.F_COLOR, "$y$": self.F_COLOR}
        )

        f = lambda x: 1.5 * x
        curve = self.get_curve(axes, f)

        self.play(comment.next_and_play())
        self.wait(2)
        self.play(ShowCreation(curve))
        self.play(comment.fade_out())
        comment.next().to_corner(UL, LARGE_BUFF)
        self.play(comment.play())
        self.bring_to_back(axes)
        self.play(FadeIn(axes))

        n = 8
        get_value_at_step = lambda i, x_from, x_to : x_from + (i / (n - 1)) * (x_to - x_from)

        # Create dots on x-axis
        input_space = axes.get_x_axis()
        x_min, x_max = (0.5, 2.5)
        dots = VGroup(*[
            Dot(radius=self.IO_DOTS_RADIUS)
                      .move_to(input_space.n2p(get_value_at_step(i, x_min, x_max)))
                      .set_color(interpolate_color(YELLOW_B, YELLOW_E, i / n))
                      .set_stroke(width=self.IO_DOTS_STROKE_WIDTH)
            for i in range(n)
        ])

        comment.target.move_to(comment.current_mob)

        self.play(comment.next_and_play())

        # Show dots on x-axis
        show_dots_animation = AnimationGroup(*[FadeIn(dot, shift=DOWN) for dot in dots], lag_ratio=self.IO_DOT_ANIM_LAG_RATIO)
        self.play(input_space[1].animate.set_color(self.X_COLOR), show_dots_animation )

        output_space = axes.get_y_axis()


        y_min = f(x_min)
        y_max = f(x_max)
        choosen_one_index = int(n / 2)  # Epic
        saved_position = curve.get_point_from_function(get_value_at_step(choosen_one_index, x_min, x_max))

        # Create dots on y-axis
        y_dots = VGroup(*[
            Dot(radius=self.IO_DOTS_RADIUS)
                      .move_to(output_space.n2p(get_value_at_step(i, y_min, y_max)))
                      .set_color(interpolate_color(LIGHT_PINK, PINK, i / n))
                      .set_stroke(width=self.IO_DOTS_STROKE_WIDTH)
            for i in range(n)
        ])

        dots_copy = dots.copy() # copy of x-axis dot's to make the animation

        def get_shift_to_curve_anim(func, dots_list):
            shift_anims = [
                dots_list[i].animate.shift(
                    func.get_point_from_function(get_value_at_step(i, x_min, x_max)) - dots_list[i].get_center()
                ) for i in range(n)
            ]
            return AnimationGroup(*shift_anims)

        # Shift x-axis dots up to the function
        self.play(comment.next_and_play())
        self.play(get_shift_to_curve_anim(curve, dots_copy))

        # Shift x-axis dots from function to y-axis
        self.play(
            output_space[1].animate.set_color(self.F_COLOR),
            AnimationGroup(*[dots_copy[i].animate.become(y_dots[i]) for i in range(n) ], lag_ratio=self.IO_DOT_ANIM_LAG_RATIO),
        )

        y_dots = dots_copy
        choosen_dot = y_dots[choosen_one_index].copy() # copy the choosen one
        self.add(choosen_dot)

        # fade out all the dots except the choosen one
        self.play(FadeOut(dots), AnimationGroup(*[ FadeOut(y_dots[i]) for i in range(n)]), comment.fade_out())

        # move the choosen one back to the curve
        self.play(comment.next_and_play())
        self.play(choosen_dot.animate.move_to(saved_position))

        # show iniettivity
        self.play(choosen_dot.animate.become(dots[choosen_one_index]), comment.next_and_play())
        self.play(comment.next_and_play())
        self.play(comment.fade_out(), FadeOut(choosen_dot))

        # New Scene -- show that this doesn't work for null derivative
        g = lambda x: 1
        new_curve = self.get_curve(axes, g)
        dots_copy = dots.copy()
        y_min, y_max = (g(x_min), g(x_max))
        saved_position = new_curve.get_point_from_function(get_value_at_step(choosen_one_index, x_min, x_max))

        # shift x-dots to curve
        self.play(curve.animate.become(new_curve), comment.next_and_play())
        self.play(show_dots_animation)
        self.play(get_shift_to_curve_anim(new_curve, dots_copy))

        # shift them again to the choosen one (epic)
        choosen_dot = y_dots[choosen_one_index]
        choosen_dot.move_to(output_space.n2p(get_value_at_step(choosen_one_index, y_min, y_max)))
        self.play(AnimationGroup(*[dots_copy[i].animate.become(choosen_dot) for i in range(n)]))
        self.play(FadeOut(dots_copy), FadeIn(choosen_dot))

        # shift the choosen one to the curve
        self.play(choosen_dot.animate.move_to(saved_position))

        # question mark + no iniettivity
        question_mark = Text("?").set_color(interpolate_color(YELLOW_B,YELLOW_E, 0.5)).next_to(dots[4], UP)
        some_indexes = [1, 6, 4, 7, 2, 5]
        self.play(comment.next_and_play())
        self.play(Write(question_mark), AnimationGroup(*[choosen_dot.copy().animate.become(dots[i]) for i in some_indexes], lag_ratio=0.7))

        self.play(comment.fade_out(), *[FadeOut(mob) for mob in self.mobjects])
        comment.target.move_to(ORIGIN)
        self.play(comment.next_and_play())

class InvertibilityGeneralization(CommonToDerivative, Slide):
    in_plane : Axes = None
    out_plane : Axes = None
    comment = None

    # choosing some constant
    transf_run_time = 4
    restoring_run_time = transf_run_time - 1

    def apply_f_to_grid_animation(
            self,
            moving_plane,
            input_choosen_square = None,
            output_choosen_square = None,
            reset_grid_position = True
    ):
        frame = self.camera.frame

        # saving starting position of camera and squares y-grid
        moving_plane.save_state()
        frame.save_state()

        self.play(FadeIn(moving_plane))

        # apply f to grid, in case handle the square
        if input_choosen_square is not None and output_choosen_square is not None:
            self.play(
                frame.animate.scale(0.5, about_point=input_choosen_square.get_center()),
                input_choosen_square.animate.set_stroke(width=5, color=BLUE, opacity=1),
                run_time=3
            )
            self.wait(2)

            # if you want to move only the square or all the grid
            self.play(
                frame.animate(run_time=self.restoring_run_time).restore(),
                MoveToTarget(moving_plane, run_time=self.transf_run_time)
            )
        else:
            self.play(MoveToTarget(moving_plane, run_time=self.transf_run_time))

        # back to the saved position of squares y-grid
        if reset_grid_position:
            self.play(FadeOut(moving_plane))
            moving_plane.restore()

        self.wait(2)


    def construct(self):
        frame = self.camera.frame
        comment  = self.comment = TextSequence(
            [
                r"Questo si generalizza ad esempio in \textit{dimensione} $2$ ",
                rf"Visualizziamo $f:{self.RR}^2\to{self.RR}^2$",
                "come prima essere differenziabile significa che localmente la funzione e' lineare ",
                r"Nei punti in cui in cui lo Jacobiano non e' invertibile si ha $\det J_f = 0$",
                r"e' l'analogo del caso 1 dimensionale",
                r"In punti come questo le aree vengono collassate in rette o punti",
                r"In punti come questo le aree vengono collassate in rette o punti\\ e' questo a non rendere invertibile l'\textit{operatore} di prima",
            ], font_size=self.FONT_SIZE,
        )
        comment.next()

        f_of_xy = Tex(
            "f(x,y)=(x, y - \sin(x+y))",
            font_size=self.FONT_SIZE,
            tex_to_color_map={"f": self.F_COLOR, "x": self.X_COLOR, "y": self.X_COLOR}
        ).next_to(comment.current_mob, DOWN)
        xyCopy = f_of_xy.get_part_by_tex("(x,y)").copy()

        # Introductory comment
        self.play(comment.play())
        self.play(comment.fade_out())
        self.play(comment.next_and_play())
        self.play(Write(f_of_xy))
        self.wait(0.5)

        # Create two planes
        xy_max = 4
        self.in_plane, self.out_plane = planes = VGroup(
            NumberPlane((-xy_max, xy_max), (-xy_max, xy_max)),
            NumberPlane((-xy_max, xy_max), (-xy_max, xy_max)),
        )
        planes.set_height(5).arrange(RIGHT, buff=2).set_stroke(GREY_D, 1)

        # Create the plane axis labels'
        axis_labels = list(range(-xy_max, xy_max + 1))
        self.in_plane.add_coordinate_labels( axis_labels, axis_labels, font_size=16 )
        self.out_plane.add_coordinate_labels( axis_labels, axis_labels, font_size=16 )

        # Get squares x-grid
        grid_resolution = 8 * xy_max
        squares = Square().get_grid(grid_resolution , grid_resolution , buff=0)
        squares.replace(self.in_plane)
        squares.set_stroke(WHITE, 1, 0.5)

        self.F_COLOR = WHITE

        # Show the input and output space, move the xy and f_of_xy labels
        self.play(
            AnimationGroup(
                AnimationGroup(
                    self.comment.fade_out(),
                    xyCopy.animate.scale(0.7).next_to(self.in_plane, UP),
                    f_of_xy.animate.scale(0.7).next_to(self.out_plane, UP)
                ),
                AnimationGroup(
                    FadeIn(self.in_plane, shift=UP),
                    FadeIn(self.out_plane, shift=UP),
                    run_time=1.5
                ),
                lag_ratio=0.4,
            )
        )

        f = lambda x, y: (x, y - np.sin(x+y))

        # Get squares y-grid
        moving_plane = squares.copy()
        moving_plane.insert_n_curves(3)  # it was 10
        moving_plane.generate_target()
        moving_plane.target.apply_function(lambda p: self.out_plane.c2p(*f(*self.in_plane.p2c(p))))
        moving_plane.target.set_color(self.F_COLOR)

        # Apply-f-to-grid Animation, 1st time
        self.apply_f_to_grid_animation(moving_plane)
        frame.save_state()

        ### CHOOSE A SQUARE - ZOOM - SHOW LOCAL LINEARITY ###
        comment.next().to_edge(DOWN)
        comment.target.move_to(comment.current_mob)
        self.play(comment.play())

        # choosing a square in the middle
        choosen_square_index = int(grid_resolution**2 / 2 + 12)
        input_choosen_square = moving_plane[choosen_square_index]
        choosen_square_target = moving_plane.target[choosen_square_index].set_stroke(width=5, color=BLUE, opacity=1)

        # saving a square for a following animation
        collapsing_square_index = choosen_square_index + 4
        input_collapsing_square = moving_plane[collapsing_square_index].copy()


        self.apply_f_to_grid_animation(moving_plane, input_choosen_square, choosen_square_target, reset_grid_position=False)

        ### ZOOM ON GRID ###

        # Zoom in on grid to show limiting behavior
        num_of_planes = 6
        zoom_center = choosen_square_target.get_center()
        initial_area = frame.get_width() * frame.get_height()
        zoomed_planes = []
        zoom_run_time = 8

        def func(p):
            return self.out_plane.c2p(*f(*self.in_plane.p2c(p)))

        # Creating planes to zoom in
        for i in range(1, num_of_planes):
            grid_width = self.in_plane.get_width() / (2**i)

            plane = Square().get_grid(grid_resolution, grid_resolution, buff=0)
            plane.set_width(grid_width)
            plane.insert_n_curves(3)
            plane.move_to(input_choosen_square.get_center())
            plane.set_stroke(width=2 / (2**i), color=self.F_COLOR)
            plane.apply_function(func)
            zoomed_planes.append(plane)


            # the (i+1)-grid has to appear only after the i-grid disappeared
            def update_opacity(m : Mobject, index=i):

                # the "appearing range" is when current_area is the interval (start_a, end_a)
                current_area = frame.get_width() * frame.get_height()
                start_a = initial_area / (4**index)
                end_a = initial_area / (4**(index + 1))

                # getting the proportion for current_area in (start_a, end_a)
                alpha = (current_area - start_a) / (end_a - start_a) if start_a != end_a else 1
                alpha = max(0, min(1, alpha)) # handles (-\infty, start_a) or (end_a, \infty) cases

                m.set_stroke(opacity=float(alpha))

            plane.add_updater(update_opacity)
            self.add(plane)

        # actual zoom animation
        self.play(
            FadeOut(input_choosen_square),
            frame.animate.scale( 2**-(num_of_planes + 1), about_point=zoom_center ),
            run_time=zoom_run_time
        )
        self.play(comment.fade_out())
        self.wait(3)

        # restore camera
        self.play(frame.animate.restore(), run_time=zoom_run_time/2)
        self.remove(*zoomed_planes)

        self.play(comment.next_and_play())
        self.wait()
        self.play(comment.next_and_play())

        ### SHOW DET \NEQ 0 MEANING ###
        collapsing_square_label = TextSequence([r"Ad esempio, in questo quadratino\\ $\det J_f=0$"], font_size=40)
        collapsing_square_label.next().next_to(input_collapsing_square, UR)

        # zoom on the collapsing square, make it fade in and write the label next to it
        self.play(
            collapsing_square_label.play(),
            frame.animate.scale(0.5, about_point=input_collapsing_square.get_center()),
            input_collapsing_square.animate.set_stroke(width=6, color=RED_D, opacity=1),
            run_time=3
        )
        self.play(comment.fade_out())
        comment.target.shift(2*LEFT) # Adjusting the text position for a better readability
        self.play(comment.next_and_play())

        # setting the target right before the movement
        input_collapsing_square.target = moving_plane.target[collapsing_square_index].set_stroke(width=6, color=RED_D, opacity=1)

        # the squares moves to target and the camera follows the square
        self.play(
            AnimationGroup(
                frame.animate.restore(),
                frame.animate
                     .move_to(input_collapsing_square.target.get_center())
                     .scale(0.5, about_point=input_collapsing_square.target.get_center()),
                run_time=self.restoring_run_time, lag_ratio=1
            ),
            MoveToTarget(input_collapsing_square, run_time=self.transf_run_time),
            collapsing_square_label.fade_out()
        )

        # camera zooms out back to original position
        self.play(frame.animate.restore(), comment.next_and_play())

class Test(Scene):
    def construct(self):
        FS = 45
        RR = r"\mathbb{R}"
        t_source = r"\text{(at a small scale)}"

        t_target = r"$f(x,y)=(x+\sin(y),y+\sin(x))$"

        source_mob = TexText(t_source, font_size=FS)
        target_mob = TexText(t_target, font_size=FS)

        group = VGroup(source_mob, target_mob).arrange(DOWN, buff=1.5)

        self.add(group)
        source_labels = index_labels(source_mob).set_color(YELLOW).set_backstroke(BLACK, 5)
        target_labels = index_labels(target_mob).set_color(PINK).set_backstroke(BLACK, 5)

        self.add(source_labels)
        self.add(target_labels)

class TextSequence:
    """
        Manages a sequence of text animations, transitioning smoothly from one string to the next
        using `TransformMatchingTex`. It supports custom index mapping to prevent unpredictable
        behavior during complex formula transformations.

        Parameters
        ----------
        texts : list of str
            A list of LaTeX strings representing the sequence of steps to display.
        transitions : list of list of tuples, optional
            Custom index mappings to force specific substring matches during `TransformMatchingTex`.
            Each sub-list corresponds to a transition between two consecutive steps
            (e.g., `transitions[0]` manages `texts[0] -> texts[1]`).

            A mapping tuple can be formatted in two ways:
            - 1-to-1 mapping: `(source_index, target_index)`
            - Slice mapping: `(start_source, end_source, start_target, end_target)`
              (Use `None` to replicate open slice behavior, e.g., `[:5]` becomes `(None, 5)`).

        font_size : int, optional
            The font size of the text (default is 30).
        corner : np.ndarray, optional
            The corner of the screen where the text will be placed initially (default is UR).
        buff : float, optional
            The buffer distance from the screen edge (default is LARGE_BUFF).
        """

    def __init__(self, texts, font_size=30, transitions=None, t2c = None):
        self.texts = texts
        self.font_size = font_size
        self.transitions = transitions or []
        self.t2c = t2c or dict()

        self.index = 0
        self.saved = None
        self.last_mob = None
        self.current_mob = None

        self.target = VectorizedPoint(ORIGIN)


    def next(self):
        """Passa alla stringa successiva nella sequenza."""
        if self.index >= len(self.texts): return None

        # Genera e posiziona il nuovo testo
        new_text = TexText(self.texts[self.index], font_size=self.font_size, t2c=self.t2c)
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
            pairs = self.get_matched_pairs()
            if pairs is not None:
                kwargs['matched_pairs'] = pairs

            return TransformMatchingTex(self.last_mob, self.current_mob, **kwargs)

    def get_matched_pairs(self):
        """
        Parses the custom transitions for the current step.
        Automatically distinguishes between 1-to-1 exact index mapping (2-element tuples)
        and slice-based mapping (4-element tuples) to generate the target Mobject pairs.
        """

        # index = n --> nth element of list is the current element
        # this means that the transition n.0 occours when the index is 2
        trans_idx = self.index - 2

        if not self.transitions or trans_idx < 0 or trans_idx >= len(self.transitions):
            return None
        # the checks handle respectively the following cases
        #   1) there are no transitions / self.transitions is empty
        #   2) Index is 0 or 1, so there are still not enough elements to make a transition
        #   3) There are less customized transition than total transition

        step_transitions = self.transitions[trans_idx]
        if not step_transitions:
            return None

        # transition : last_mob -> current_mob
        pairs = []
        for match in step_transitions:
            # Shortcut: mappa 1 a 1 un singolo elemento (es: (5, 8))
            if len(match) == 2:
                s_idx, t_idx = match
                pairs.append((self.last_mob[s_idx], self.current_mob[t_idx]))

            # Formato classico per le slice: (start_source, end_source, start_target, end_target)
            elif len(match) == 4:
                s_start, s_end, t_start, t_end = match
                pairs.append((self.last_mob[s_start:s_end], self.current_mob[t_start:t_end]))

        return pairs

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

    def fade_out(self):
        """Fa svanire il testo attualmente a schermo."""
        if self.current_mob is None: return None

        fade_animation = FadeOut(self.current_mob)
        self.current_mob = None
        return fade_animation


# manim-slides convert Intro slides.html --open
# manim-slides convert Intro slides.html -cwidth=1920 -cheight=1080 --open
# manim-slides convert Intro slides.html -cwidth=1920 -cheight=1080 -cmargin=0 -cmin_scale=1 -cmax_scale=1 --open
# manimgl main.py Intro -w --hd

# manim-slides Intro
# manim-slides render --GL main.py Intro
