from manimlib import *
from manim_slides.slide import Slide, ThreeDSlide

class CommonToAll:

    FONT_SIZE = 30

    def wait(self, duration=1.0, **kwargs):
        self.play(Animation(Mobject(), run_time=duration), **kwargs)

class CommonToProblemDescription(CommonToAll):

    # some costants
    a, b, c = (0.5, 2, 1)
    xc, yc = (2, 1)
    alpha_start, alpha_end = (0, 0.25) # (0.05, 0.25)
    ARC_COLOR = PINK

    @staticmethod
    def get_f(a, b, xc, yc):
        return lambda x,y: a * (x - xc) ** 2 + b * (y - yc) ** 2

    @staticmethod
    def get_inverse_of_arc(a, b, c, xc, yc):
        return lambda y: xc + np.sqrt(c/a - b/a * (y - yc) ** 2)

    @staticmethod
    def get_ellissoid_curve(axes, center, a, b, c, color=YELLOW) -> ParametricCurve:
        xc, yc = center
        curve = ParametricCurve(
            lambda t: axes.c2p(xc + np.sqrt(c / a) * np.cos(t), yc + np.sqrt(c / b) * np.sin(t), c),
            (-PI, PI, 0.1))
        curve.set_stroke(width=5, opacity=1, color=color)
        return curve

    @staticmethod
    def get_ellipses_y(x, xc, yc, a, b, c):
        # Calcoliamo i quadrati dei "raggi" dell'ellisse
        rx_square = c / a
        ry_square = c / b

        # Calcoliamo il termine sotto la radice
        sqrt_term = 1 - ((x - xc) ** 2) / rx_square

        # Controllo: la x si trova effettivamente all'interno dell'ellisse?
        if sqrt_term < 0:
            raise ValueError(f"x={x} is outside ellipses domain.")

        # Calcoliamo la distanza dal centro lungo l'asse y
        offset_y = np.sqrt(ry_square) * np.sqrt(sqrt_term)

        # Restituiamo i due punti dell'ellisse per quella x (superiore e inferiore)
        upper_y = yc + offset_y
        lower_y = yc - offset_y

        return upper_y, lower_y


    @staticmethod
    def get_t_from_ellipsis_x(x, xc, a, c):
        """
        Calculates the parameter t for a given x coordinate on an ellipse.
        Returns two values of t (for the upper and lower halves).
        """
        # Calculate the horizontal semi-axis (radius)
        rx = np.sqrt(c / a)

        # Calculate the argument for the arccosine function
        # x = xc + rx * cos(t)  =>  cos(t) = (x - xc) / rx
        argument = (x - xc) / rx

        # Clip the value to stay within the valid domain [-1.0, 1.0]
        # This prevents math errors due to tiny floating-point inaccuracies
        argument = np.clip(argument, -1.0, 1.0)

        # Calculate t for the upper half of the ellipse (range: 0 to PI)
        t_upper = np.arccos(argument)

        # Calculate t for the lower half (range: -PI to 0)
        # Since cos(t) = cos(-t), we simply negate the upper value
        t_lower = -t_upper

        return t_upper, t_lower

    @staticmethod
    def to_fixed_coord(point = ORIGIN, camera_center = ORIGIN, camera_scaling = 1.):
        # doesn't condisider rotations
        return (point-camera_center)*(1/camera_scaling)

class Intro(CommonToProblemDescription, ThreeDSlide):

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

    def construct(self):
        frame = self.camera.frame

        camera_scaling = 1.3
        total_scaling = camera_scaling
        frame.set_euler_angles(phi=65 * DEGREES, theta=30 * DEGREES).shift(UP).scale(camera_scaling)
        axes = self.get_axes()

        xc, yc = paraboloid_center = (self.xc, self.yc)
        a, b, c = (self.a, self.b, self.c)
        f = self.get_f(a, b, xc, yc)

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

        self.play(surface.animate.shift(shift_qty), curve.animate.shift(shift_qty), eq_problem.next_and_play())
        self.play(eq_problem.next_and_play())

        self.next_slide() # Zoomming on ellipse

        camera_center = axes.c2p(xc, yc, 0)
        camera_scaling = 0.4
        total_scaling *= camera_scaling

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

        self.next_slide()

        # Creating Arc in the neighborhood of (x0,y0)
        ARC_COLOR = self.ARC_COLOR
        alpha_start, alpha_end = (self.alpha_start, self.alpha_end)
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
        self.wait(5)

        comment.next()[52:60].set_color(ARC_COLOR)
        self.play(comment.play())

        self.next_slide()
        comment.next()[21:29].set_color(ARC_COLOR)
        self.play(comment.play(matched_pairs=[(comment.last_mob[52:60], comment.current_mob[21:29])]))
        self.wait(2.5)
        self.play(comment.next_and_play())

        self.wait()
        self.play(*[FadeOut(mob) for mob in self.mobjects])

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
        self.wait(0.5)
        self.play(FadeIn(axes))


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
        self.play(Write(f_of_x, run_time=2), ShowCreation(curve, run_time=3))

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

        self.next_slide()
        self.wait(0.5)

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

        self.play(equation.next_and_play())
        self.wait(3.5)
        self.play(*map(FadeOut, [localAxes, brace_x, brace_fx, delta_x, delta_fx, curve, axes]))
        self.wait(0.5)
        self.play(comment.fade_out(), equation.fade_out(), msg.fade_out())

        frame.restore()

        return

class InvertibleDerivative(CommonToDerivative, Slide):
    def construct(self):
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
        self.next_slide()
        self.wait(0.5)

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
        self.wait(2.25)
        self.play(comment.next_and_play())

        # New Scene -- show that this doesn't work for null derivative
        g = lambda x: 1
        new_curve = self.get_curve(axes, g)
        dots_copy = dots.copy()
        y_min, y_max = (g(x_min), g(x_max))
        saved_position = new_curve.get_point_from_function(get_value_at_step(choosen_one_index, x_min, x_max))

        # shift x-dots to curve
        self.next_slide()
        self.wait(0.5)
        self.play(comment.fade_out(), FadeOut(choosen_dot))
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
        self.wait(2)
        self.play(comment.fade_out())

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
                r"In punti come questo le aree vengono collassate in rette o punti\\ ossia l'\textit{operatore} citato prima non e' invertibile",
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
        self.wait(0.5)
        self.play(comment.play())
        self.wait(2)
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

        self.next_slide()

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
        self.wait(4)
        self.play(comment.next_and_play())

        ### SHOW DET \NEQ 0 MEANING ###
        collapsing_square_label = TextSequence([r"Ad esempio, in questo quadratino\\ $\det J_f=0$"], font_size=40)
        collapsing_square_label.next().next_to(input_collapsing_square, UR)

        self.next_slide()
        # zoom on the collapsing square, make it fade in and write the label next to it
        self.wait(0.5)
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
        self.wait(7)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

class CommonToContractions(CommonToAll):

    def get_axes(
            self,
            x_range=(-3, 3), y_range=(-3, 3),
            width=5,
            color=GREY,
            center=ORIGIN,
            show_numbers=True,
    ) -> Axes:
        axes = Axes(x_range=x_range, y_range=y_range).set_stroke(width=width, color=color).shift(center - ORIGIN)

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

    def get_curve(self, axes, f, t_range=(-3, 3, 0.1), width = 8, color=BLUE):
        return ParametricCurve(
            lambda t: (axes.c2p(t, f(t))), t_range=t_range
        ).set_stroke(width=width, color=color, opacity=0.7)

class WhatsAContraction(CommonToContractions, CommonToProblemDescription, Slide):
    speed_factor = 1

    def play(self, *args, **kwargs):
        # Applica il moltiplicatore solo se run_time non è forzato manualmente
        if 'run_time' not in kwargs:
            kwargs['run_time'] = 1.0 * self.speed_factor
        else:
            kwargs['run_time'] *= self.speed_factor
        super().play(*args, **kwargs)

    def construct(self):
        frame = self.camera.frame
        comment = TextSequence(
            [
                r"Ora che abbiamo capito la natura di $\displaystyle\frac{\partial f}{\partial y}\neq 0$",
                r"Ora che abbiamo capito la natura di $\displaystyle\frac{\partial f}{\partial y}\neq 0$\\"
                "cerchiamo di capire perche' e' fondamentale",
                "Per farlo torniamo al nostro problema iniziale,",
                r"per riuscire a costruire $y(x)$",
                r"per riuscire a costruire $y(x)$\\ dobbiamo trovare un modo per associare ad una $y$",
                r"per riuscire a costruire $y(x)$\\ dobbiamo trovare un modo per associare ad una $y$ una sola $x$",
                "Prendiamo $y$ abbastanza vicina ad $y_0$",
                "Ed iniziamo provando un punto abbastanza vicino a $x_0$",
                "Probabilmente avro' commesso un certo errore",
                r"avro' \textit{mancato il bersaglio} $y$ di un $ \Delta y $",
                r"allora per capire di quanto \textit{aggiustare la mira}",
                r"allora per capire di quanto \textit{aggiustare la mira} sfrutto la derivata",
                r"posso farlo poiche' l'operatore derivata",
                r"posso farlo poiche' l'operatore derivata\\ e' invertibile in quel punto",
                "...poi itero il procedimento",
                r"La convergenza del metodo e' garantita\\ solo per $y$ sufficientemente vicini",
                r"Se provo ad invertire un punto troppo lontano",
                r"I punti cadono al di fuori del domino dopo poche iterazioni",
                r"La necessita' che $y$ sia abbastanza vicina serve a garantire\\ che la funzione usata per iterare i punti sull'asse delle $x$\\ sia una \textit{contrazione}, e che quindi converga",
            ],
            font_size=35
        )
        axes = self.get_axes(show_numbers=False)

        xc, yc = paraboloid_center = (self.xc, self.yc)
        a, b, c = (self.a, self.b, self.c)
        f = self.get_f(a, b, xc, yc)
        nabla_f = lambda x, y: ((f(x+0.001, y)-f(x, y))/0.001, (f(x, y+0.001)-f(x, y))/0.001)
        curve = self.get_ellissoid_curve(axes, paraboloid_center, a, b, c, WHITE)
        alpha_start, alpha_end = (self.alpha_start, self.alpha_end)

        arc = curve.get_subcurve(alpha_start, alpha_end).set_color(self.ARC_COLOR).set_stroke(width=3)

        middle_alpha = 0.5 * (alpha_end + alpha_start) - 0.01
        arc_middle = curve.point_from_proportion(middle_alpha)

        ZOOMED_RADIUS = 0.015
        point = Dot(arc_middle, radius=ZOOMED_RADIUS).set_color(self.ARC_COLOR)
        curve.set_stroke(opacity=0.15) # shadowing the main curve

        self.wait(0.5)
        self.play(comment.next_and_play(), run_time=2)
        self.wait(2)
        self.play(comment.next_and_play(), run_time=2)
        self.wait(2)
        self.play(comment.fade_out())
        self.play(ShowCreation(axes))
        self.play(ShowCreation(curve), ShowCreation(arc))

        x0,y0 = axes.p2c(arc_middle) # x0 = 1.095
        px0, py0 = nabla_f(x0,y0) # -px0/py0 = - 0.416

        scaling = 0.2
        total_scaling = scaling
        comment.next().to_edge(UP, buff=MED_LARGE_BUFF).shift(2*RIGHT)
        comment.set_target()
        self.play(frame.animate.move_to(arc_middle).scale(scaling), FadeIn(point), FadeOut(curve))
        self.play(comment.play(), point.animate.set_color(WHITE), arc.animate.set_color(WHITE), )
        self.wait(2)

        ### SETTING UP BEFORE ITERATING
        TO_FIND_COLOR = RED_E
        RHO_COLOR = BLUE
        F_COLOR = PINK
        X_COLOR = YELLOW
        dash_len = 0.02
        line_opacity = 0.5

        # getting x0,y0 point, dot, label and dashed_line
        x0_point = axes.c2p(x0, 0)
        y0_point = axes.c2p(0, y0)

        x_axis_dot = Dot(x0_point, radius=ZOOMED_RADIUS)
        y_axis_dot = Dot(y0_point, radius=ZOOMED_RADIUS)

        x0_label, y0_label = [Tex(text, font_size=30).scale(total_scaling) for text in ["x_0", "y_0"]]
        x0_label.next_to(x0_point, DOWN*total_scaling), y0_label.next_to(y0_point, LEFT*total_scaling)

        x0_dashed_line = DashedLine(arc_middle, x0_point, dash_length=dash_len, stroke_opacity=line_opacity)
        y0_dashed_line = DashedLine(arc_middle, y0_point, dash_length=dash_len, stroke_opacity=line_opacity)

        # animating x0,y0 dot, line and label creation
        self.play(comment.fade_out())
        self.play(
            AnimationGroup(ShowCreation(x0_dashed_line), FadeIn(x_axis_dot), lag_ratio=0.5),
            AnimationGroup(ShowCreation(y0_dashed_line), FadeIn(y_axis_dot), comment.next_and_play(), lag_ratio=0.5),
        )
        self.wait(5)
        self.play(Write(x0_label), Write(y0_label), comment.next_and_play())
        self.wait(5)
        self.play(comment.next_and_play())
        self.wait(8)

        # getting the target y of the algorithm (point, dot, label and x,y values)
        target_y_point = curve.get_point_from_function(self.get_t_from_ellipsis_x(0.85, self.xc, self.a, self.c)[1])
        target_y_dot = Dot(target_y_point, radius=ZOOMED_RADIUS, fill_color=TO_FIND_COLOR)
        target_y_label = Tex("y", font_size=30).scale(total_scaling).set_color(TO_FIND_COLOR).next_to(target_y_dot, (DOWN*0.1+LEFT*0.3)*2*total_scaling)
        x_target, y_target, *_ = axes.p2c(target_y_point)

        self.play(comment.fade_out())
        self.play(comment.next_and_play())
        self.wait()
        self.play(FadeIn(target_y_dot), Write(target_y_label))
        self.wait(2)

        # calculating rangent
        range_delta = 0.4
        f_tan = lambda t: -px0/py0 * (t-x0) + y0 # tangent equation
        f_tan_inverse = lambda y: - (y - y0) * py0/px0 +x0 # the tangent's inverse function
        t_from_proportion = lambda x: (x - x0)/(2*range_delta) + 0.5 # proportion for x in (x0-\delta, x0+\delta)
        tangent = self.get_curve(axes, f_tan, width = 3, color=WHITE, t_range=(x0-range_delta, x0+range_delta, 0.1)).set_stroke(opacity=line_opacity)
        tangent.save_state()

        rho = ValueTracker(-0.4)
        guess = x0 + rho.get_value()
        guess_point = axes.c2p(guess, 0)

        # that's the line with rho length from x0 to the current guess
        rho_line = always_redraw(lambda: Line(x0_point, axes.c2p(x0 + rho.get_value()), color=RHO_COLOR))

        # creating guess dot and guess label
        guess_dot = Dot(guess_point, radius=ZOOMED_RADIUS, fill_color=RHO_COLOR)
        guess_dot.add_updater(lambda m: m.move_to(rho_line.get_end()))

        guess_label = Tex(r"x_1 = x_0+\rho", font_size=30).scale(total_scaling).set_color(RHO_COLOR).next_to(guess_dot, DOWN * total_scaling)
        guess_label.add_updater(lambda m: m.next_to(guess_dot, DOWN * total_scaling))

        self.play(comment.fade_out())
        comment.next().set_color_by_tex("punto", RHO_COLOR)
        self.play(comment.play())
        self.wait()
        self.play(FadeIn(guess_dot), ShowCreation(rho_line), Write(guess_label))

        iterations = 10
        scaling = 1
        frame.save_state()
        for i in range(1, iterations):
            if i == 2:
                scaling = 0.7
                total_scaling *= scaling
                # ZOOMED_RADIUS *= scaling
                self.wait()
                self.play(comment.fade_out())
                self.play(frame.animate.scale(scaling))

                self.speed_factor = 0.5
            if i == 3:
                self.speed_factor = 0.15

            guess = x0 + rho.get_value()
            guess_point = axes.c2p(guess, 0)

            # calulating y1 (getting dot, dashed line and label)
            new_y_point = curve.get_point_from_function(self.get_t_from_ellipsis_x(guess, self.xc, self.a, self.c)[1])
            new_y_dot = Dot(new_y_point, radius=ZOOMED_RADIUS, fill_color=RHO_COLOR).set_z_index(1)
            new_y_vertical_line = DashedLine(guess_point, new_y_point, color=RHO_COLOR, dash_length=dash_len, stroke_opacity=line_opacity)
            new_y_label = Tex(f"y_{i}", font_size=30).scale(total_scaling/scaling).set_color(RHO_COLOR).next_to(new_y_point, UP*1.5*total_scaling)

            # calculating dy as dy = y1 - y0 (getting line, brace and label)
            y_diff = new_y_point[1] - y_target # if > 0 we have to add correction, if < 0 we have to subtract correction

            orientation = LEFT if y_diff > 0 else RIGHT
            sign = 1 if y_diff > 0 else -1

            dy_line_end = axes.c2p(new_y_point[0], y_target)
            dy_line = Line(new_y_point, dy_line_end, color=F_COLOR)
            if y_diff < 0: dy_line = Line(dy_line_end, new_y_point, color=F_COLOR)

            to_play = FadeIn(dy_line)
            if i == 1 :
                brace_y = Brace(dy_line, orientation, buff=0.02, font_size=30)
                brace_y.set_color(F_COLOR).stretch(total_scaling, dim=0, about_edge=-orientation)
                brace_y_label = Tex(r"\Delta y", font_size=30)
                brace_y_label.scale(total_scaling).set_color(F_COLOR).next_to(brace_y, orientation*0.5*total_scaling)
                to_play = AnimationGroup(FadeIn(dy_line), Write(brace_y), Write(brace_y_label))

                self.play(comment.fade_out())
                comment.next().set_color_by_tex("errore", F_COLOR)
                self.play(comment.play())
                self.wait(3)


            # show: the new y_i corresponding to the guess -- then --> the error dy
            self.play(
                FadeIn(new_y_dot), ShowCreation(new_y_vertical_line, suspend_mobject_updating=True),
                Write(new_y_label),
            )
            if i == 1:
                self.wait()
                self.play(comment.fade_out())
                comment.next()[28:].set_color(F_COLOR)
                self.play(comment.play(), run_time=2)
                self.wait(2)
                self.play(to_play)
                self.play(comment.fade_out())
                comment.next()[23:33].set_color(X_COLOR)
                self.play(comment.play(), run_time=2)
                self.wait(1.5)
                comment.next()[23:33].set_color(X_COLOR)
                self.play(comment.play())

            ### we use tangent (first derivative) to approximate dx, here is the animation
            # we show the tangent, and move it where is easier (less messy) too see, to the same height of dy_line center
            self.bring_to_back(tangent)
            tangent.restore()
            self.play(ShowCreation(tangent))
            self.play(tangent.animate.match_y(dy_line).shift(2*RIGHT*total_scaling),)

            # dy_line -> temp_line -> dx_line
            # calculating where the dy_line edges will have to move when transforming dy_line -> temp_line
            intersection_point_1st = tangent.point_from_proportion(t_from_proportion(f_tan_inverse(y0 + dy_line.get_length()/2)))
            intersection_point_2nd = tangent.point_from_proportion(t_from_proportion(f_tan_inverse(y0 - dy_line.get_length()/2)))

            # calculating how much the dy_line will have to shift to meet tangent
            shift_to_right = intersection_point_1st - dy_line.get_start()

            # calculating final line and final line endpoint
            dx_line_endpoint = axes.c2p(intersection_point_2nd[0], intersection_point_1st[1])
            dx_line = Line(intersection_point_1st, dx_line_endpoint, color=X_COLOR)
            temp_dashed_line2 = DashedLine(intersection_point_2nd, dx_line_endpoint,  dash_length=dash_len, stroke_opacity=line_opacity, color=X_COLOR)

            # shift dy_line animation
            to_play = dy_line.animate.move_to(intersection_point_1st, aligned_edge=UP)
            if i == 1 :
                to_play = AnimationGroup(
                    dy_line.animate.move_to(intersection_point_1st, aligned_edge=UP),
                    AnimationGroup(brace_y.animate.shift(shift_to_right), brace_y_label.animate.shift(shift_to_right)),
                    lag_ratio=0.4
                )
            self.play(to_play)


            # setting up transform animation, we use a temporary variable/line and use dashed line to emphasize
            temp_line = Line(intersection_point_1st, intersection_point_2nd, color=F_COLOR)
            temp_dashed_line = DashedLine(dy_line.get_end(), intersection_point_2nd, dash_length=dash_len, stroke_opacity=line_opacity, color=F_COLOR)

            # actual animation: dy_line_copy -> temp_line
            dy_line_copy = dy_line.copy()
            self.play(AnimationGroup(dy_line_copy.animate.become(temp_line), ShowCreation(temp_dashed_line), lag_ratio=0.1))
            temp_line = dy_line_copy

            # temp_line -> dx_line
            self.play(AnimationGroup(temp_line.animate.become(dx_line), ShowCreation(temp_dashed_line2), lag_ratio=0.1))
            dx_line = temp_line

            # Creating + Animating brace and label for dx_line
            brace_x = Brace(dx_line, UP, buff=0.02, font_size=30).set_color(X_COLOR).stretch(total_scaling, dim=1, about_edge=DOWN)
            brace_x_label = Tex(r"\Delta x", font_size=30).scale(total_scaling/scaling).set_color(X_COLOR).next_to(brace_x, UP*0.5*total_scaling)

            if i == 1: self.play(ReplacementTransform(brace_y_label, brace_x_label), ReplacementTransform(brace_y, brace_x))
            else: self.play(Write(brace_x_label), Write(brace_x))
            self.play(*map(FadeOut, [temp_dashed_line, temp_dashed_line2, dy_line, tangent, brace_x]))

            # explaining why i can do that the first time
            if i == 1:
                self.play(comment.fade_out())
                self.play(comment.next_and_play())
                self.wait()
                self.play(comment.next_and_play())
                self.next_slide()
                self.wait(0.5)

            # moving dx_line to x-axis to show correction
            delta_x = Group(dx_line, brace_x_label)
            corner_to_align = dx_line.get_start() if y_diff > 0 else dx_line.get_end()
            self.play(delta_x.animate.shift(guess_point-corner_to_align).arrange(UP * total_scaling, center=False))

            # some things just for smoothing the last iteration
            to_play = rho.animate.increment_value(sign * dx_line.get_length())
            new_text = f"x_{i+1}"
            new_color = RHO_COLOR
            if i == iterations - 1:
                self.speed_factor = 1
                new_text = "x"
                new_color = TO_FIND_COLOR
                final_line = DashedLine(guess_point, target_y_point, color=TO_FIND_COLOR, dash_length=dash_len, stroke_opacity=line_opacity)
                to_play = AnimationGroup(
                    rho.animate.increment_value(sign * dx_line.get_length()),
                    guess_dot.animate.set_color(TO_FIND_COLOR),
                    ShowCreation(final_line),
                    FadeOut(rho_line),
                    run_time=2
                )

            # setting up new iteration
            new_label = Tex(new_text, font_size=30)
            new_label.scale(total_scaling/scaling).set_color(new_color).next_to(guess_dot, DOWN*total_scaling)
            if  i < iterations - 1:
                new_label.add_updater( lambda m: m.next_to(guess_dot, DOWN*total_scaling) )

            self.play(
                ReplacementTransform(guess_label, new_label),
                to_play,
                *map(FadeOut,[new_y_dot, new_y_label, new_y_vertical_line, delta_x])
            )

            guess_label = new_label

            if i == 1: self.play(comment.next_and_play())

        self.play(frame.animate.restore())

        self.play(*map(FadeOut, [
            x0_dashed_line, y0_dashed_line,
            x0_label, y0_label,
            x_axis_dot, y_axis_dot,

        ]))

        self.play(comment.next_and_play(), run_time=2)
        self.wait(4)
        self.play(comment.fade_out())


        dfdx = -px0/py0
        input_space = axes.get_x_axis()
        get_value_at_step = lambda i, x_from, x_to: x_from + (i / (n - 1)) * (x_to - x_from)
        n = 10
        delta = 0.3

        new_x = x0 - 0.3525
        new_target_y_point = curve.get_point_from_function(self.get_t_from_ellipsis_x(new_x, self.xc, self.a, self.c)[1])
        x_target, y_target = axes.p2c(new_target_y_point)[:2]

        self.play(comment.next_and_play(), run_time=2)
        self.play(
            target_y_label.animate.move_to(new_target_y_point).shift((DOWN * 0.1 + LEFT * 0.3) * 2 * total_scaling),
            target_y_dot.animate.move_to(new_target_y_point), *map(FadeOut, [guess_label, guess_dot, final_line])
        )


        x_min, x_max = (x0-delta, x0+delta)
        dots = VGroup(*[
            Dot(
                input_space.n2p(get_value_at_step(i, x_min, x_max)),
                radius=ZOOMED_RADIUS,
                fill_color=interpolate_color(WHITE, YELLOW, i / n)
            )
            for i in range(n)
        ])

        show_dots_animation = AnimationGroup(*[FadeIn(dot, shift=DOWN) for dot in dots], lag_ratio=0.05)
        self.wait()
        self.play(input_space[1].animate.set_color(X_COLOR), show_dots_animation)
        self.play(comment.fade_out())
        domain_left_bound = 0.5857
        still_in_domain = [k for k in range(n)]
        domain_line = DashedLine(axes.c2p(domain_left_bound, -0.5), axes.c2p(domain_left_bound, 10), dash_length=dash_len, stroke_opacity=line_opacity, stroke_color=RED_E)
        self.play(ShowCreation(domain_line))

        for dot in dots: dot.generate_target()

        def update_target(dot):
            current_p = dot.get_center()

            curr_x, curr_y = axes.p2c(current_p)[:2]

            val_y_on_curve = axes.p2c(curve.get_point_from_function(
                self.get_t_from_ellipsis_x(curr_x, self.xc, self.a, self.c)[1]
            ))[1]

            new_x_coord = curr_x + (y_target - val_y_on_curve) / dfdx
            dot.target.move_to(axes.c2p(new_x_coord, 0))

            if new_x_coord < domain_left_bound: return False
            return True

        self.play(comment.next_and_play(), run_time=2)
        for i in range(10):
            survived = [k for k in still_in_domain if update_target(dots[k])]
            if not still_in_domain: break
            self.play(AnimationGroup(*[MoveToTarget(dots[k]) for k in still_in_domain]))
            still_in_domain = survived

        self.next_slide()
        self.wait(0.5)

        self.play(*map(FadeOut, [
            target_y_dot, target_y_label, axes, arc, point, domain_line, dots,
        ]), comment.fade_out())

        frame.scale(1/total_scaling)

        comment.target.move_to(ORIGIN)
        self.play(comment.next_and_play(), run_time=3)


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

    def set_target(self):
        if self.current_mob is None: return
        self.target.move_to(self.current_mob.get_center())

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

    def fade_and_write(self, **kwargs):
        return AnimationGroup(self.fade_out(), self.next_and_play(**kwargs), lag_ratio=1)

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


""" TO RUN THE CODE AS PRESENTATION
manimgl main.py Intro DerivativeMeaning InvertibleDerivative InvertibilityGeneralization WhatsAContraction -w --hd
manim-slides convert Intro DerivativeMeaning InvertibleDerivative InvertibilityGeneralization WhatsAContraction Slides.html --open
"""
