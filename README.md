# Internship: Manim Mathematical Animations 🎓

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![ManimGL](https://img.shields.io/badge/Manim-GL-grey)](https://github.com/3b1b/manim)
[![ManimSlides](https://img.shields.io/badge/Manim-Slides-Grey)](https://github.com/jeertmans/manim-slides)

This repository contains the projects developed during my internship. The primary focus is on creating high-quality, 3D mathematical animations using [ManimGL](https://github.com/3b1b/manim) to visualize calculus and linear algebra concepts.

## 📂 Repository Structure

The repository is organized into distinct sub-projects, each focusing on a specific mathematical topic or animation scene.

    Tirocinio/
    │
    ├── local-analysis-implicit-function-theorem/
    │   └── main.py                # Core animation script for the scene
    │  
    ├── tangent-plane-to-hessian-eigenvalues/
    │   ├── main.py                # Core animation script for the scene
    │   └── vector3D.py            # Custom 3D vector and arrow classes
    │
    └── .gitignore


---

## Featured Projects

### 1. Implicit Function Theorem (Dini)
**Folder:** `local-analysis-implicit-function-theorem/`

This project provides a geometric and intuitive walkthrough of the Implicit Function Theorem (Dini's Theorem), specifically designed for second-year Mathematical Analysis students. It bridges the gap between the theorem's formal hypotheses and their underlying geometric meaning. 

**Key Visualizations:**
* **Introduction to the problem:** Visualizes the equation $F(x, y) = c$ as the intersection of a 3D surface (e.g., a paraboloid) with a plane, identifying the conditions under which a curve can be locally treated as a function. Introduces the formal statement of the theorem
* **Partial Derivatives & Injectivity:** Illustrates why the condition $\frac{\partial F}{\partial y} \neq 0$ is required. The animation shows how a vanishing derivative leads to a loss of local injectivity, preventing the existence of a unique function $y = f(x)$.

![loss of local injectivity](./local-analysis-implicit-function-theorem/media/example.gif)


* **Jacobian Determinant & Grid Deformation:** Generalizes the concept to $\mathbb{R}^n$ by showing the Jacobian as a measure of space deformation. A grid animation demonstrates how a zero determinant "collapses" dimensions, making the local inversion of the map impossible.
* **Contraction Mapping & Newton’s Method:** Animates the constructive part of the theorem. It shows how the iterative Newton process converges to a fixed point and highlights how the choice of the neighborhood (delta/epsilon) is critical for the stability of the solution.

**Custom Utilities (inside `main.py`):**
**TextSequence Class:** A custom manager for $\LaTeX$ objects that automates the state-handling of text transitions. It encapsulates TransformMatchingTex logic to handle smooth symbol-by-symbol morphing between complex mathematical formulas without manual object tracking.

### 2. Tangent Plane to Hessian Eigenvalues
**Folder:** `tangent-plane-to-hessian-eigenvalues/`

This project visualizes the geometric intuition behind the second-order Taylor expansion for a multivariable function $f: \mathbb{R}^2 \to \mathbb{R}$. 

**Key Visualizations:**
* **Tangent Plane Approximation:** Shows a 3D surface $z = f(x, y)$ and how a tangent plane approximates the function at a given point $P$.
* **Error Surface $e(h)$:** Animates the difference between the function and the tangent plane, isolating the quadratic error term.
* **The Hessian Matrix ($H_f$):** Explains the transition from the Taylor formula to the quadratic form: $e(h) = \frac{1}{2} h^T H_f h + o(|h|^2)$.
* **Eigenvalues & Quadrics:** Demonstrates how diagonalizing the Hessian reveals the eigenvalues ($\lambda_1, \lambda_2$). The animation dynamically shows how the signs of these eigenvalues dictate the shape of the local error surface (e.g., an upward paraboloid, a downward paraboloid, or a saddle point).

**Custom Utilities (`vector3D.py`):**
Includes a custom `Vector3D` class implementing 3D arrows objects using cylindrical bodies and conical tips.

---

## 🛠️ Technologies & Libraries

* **Language:** Python
* **Animation Engine:** [ManimGL (`manimlib`)]([https://github.com/3b1b/manim](https://github.com/3b1b/manim)) - The version of Manim used by 3Blue1Brown.
* **Animation Utils:** [ManimSlides (`manim-slides`)]([https://github.com/jeertmans/manim-slides](https://github.com/jeertmans/manim-slides))

---

## 🚀 Getting Started

To run these animations locally, you need to install ManimGL, ManimSlides and its dependencies. 

For the complete installation instructions, please refer to the official PyPI page:
* [ManimGL on PyPI](https://pypi.org/project/manimgl/)
* [ManimSlides Installation](https://manim-slides.eertmans.be/latest/installation.html)

Once installed use the `manimgl` and `manim-slides` command line tool to render the scenes. 

---

## 👤 Author

**SwitchArio**
- GitHub: [@SwitchArio](https://github.com/SwitchArio)
