# Internship Project: Manim Mathematical Animations 🎓📽️

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![ManimGL](https://img.shields.io/badge/Manim-GL-grey)](https://github.com/3b1b/manim)

This repository contains the projects developed during my internship. The primary focus is on creating high-quality, 3D mathematical animations using [ManimGL](https://github.com/3b1b/manim) to visualize calculus and linear algebra concepts.

## 📂 Repository Structure

The repository is organized into distinct sub-projects, each focusing on a specific mathematical topic or animation scene.

    PrimoProgettoTirocinio/
    │
    ├── tangent-plane-to-hessian-eigenvalues/
    │   ├── main.py                # Core animation script for the Hessian scene
    │   └── vector3D.py            # Custom 3D vector and arrow classes
    │
    ├── other-project/    # Placeholder for future animations
    │   ├── main.py
    │   └── util-classes.py
    │
    └── .gitignore


---

## 🎬 Featured Projects

### 1. Tangent Plane to Hessian Eigenvalues
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
* **Math Computation:** `numpy`

---

## 🚀 Getting Started

To run these animations locally, you need to install ManimGL and its dependencies. 

For the complete installation instructions, please refer to the official PyPI page:
👉 [ManimGL on PyPI](https://pypi.org/project/manimgl/)

Once installed use the `manimgl` command line tool to render the scenes. 

---

## 👤 Author

**SwitchArio**
- GitHub: [@SwitchArio](https://github.com/SwitchArio)
