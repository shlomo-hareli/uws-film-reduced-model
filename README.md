# Tabulated Reduced-Order Model for Urea–Water-Solution (UWS) Film Decomposition in SCR-Relevant Flows

## Author Information

**Shlomo Hareli**  
Karlsruhe Institute of Technology (KIT)  
Institute of Technical Thermodynamics

**Manuscript Status:** Submitted to *Chemical Engineering Journal*

---

## Abstract

This repository presents a tabulated reduced-order model (ROM) for the deterministic simulation of coupled urea–water-solution (UWS) film heating, evaporation, and chemical decomposition in sele[...]

---

## 1. Scientific Objectives

This work addresses the computational challenge of simulating coupled thermochemical processes in SCR catalytic systems by developing a deterministic surrogate model capable of capturing:

- Film thermal evolution and heat transfer
- Phase change kinetics and evaporation dynamics
- Urea decomposition reaction pathways
- Intermediate species formation and transport
- Coupled heat and mass transfer phenomena

The primary objective is to achieve significant computational cost reduction relative to full detailed chemistry simulations while maintaining thermochemical fidelity within the intended parameter[...]

---

## 2. Mathematical Formulation

### 2.1 State Space Representation

The thermochemical state is parametrized as a function of four independent variables:

$$\Psi = \Psi(\phi, T_f, T_g, r)$$

where:
- $\phi$ = progress variable (0 to 1)
- $T_f$ = film temperature [K]
- $T_g$ = gas phase temperature [K]
- $r$ = film thickness [m]

### 2.2 Governing Evolution Equation

The system dynamics reduce to a single ordinary differential equation in the progress variable:

$$\frac{d\phi}{dt} = \dot{\phi}(\phi, T_f, T_g, r)$$

**Time integration (explicit scheme):**

$$\phi(t + \Delta t) = \phi(t) + \dot{\phi} \cdot \Delta t$$

All remaining thermochemical variables are reconstructed from the tabulated mapping $\Psi(\phi, T_f, T_g, r)$ without requiring on-the-fly chemistry integration.

---

## 3. State Vector Definition

The complete thermochemical state comprises 24 variables:

| Index | Variable | Description | Units |
|-------|----------|-------------|-------|
| 0 | $\phi$ | Progress variable | [−] |
| 1 | $\dot{\phi}$ | Progress variable source term | [s⁻¹] |
| 2 | $d_{eq}$ | Equivalent diameter | [m] |
| 3 | $m_d$ | Droplet/film mass | [kg] |
| 4 | $T$ | Temperature | [K] |
| 5 | $\rho$ | Density | [kg/m³] |
| 6 | $w_{H_2O}$ | Water mass fraction | [−] |
| 7 | $w_{Ur,s}$ | Solid urea mass fraction | [−] |
| 8 | $w_{Ur,l}$ | Liquid urea mass fraction | [−] |
| 9 | $w_{HNCO,l}$ | Isocyanic acid (liquid) mass fraction | [−] |
| 10 | $w_{Biu,l}$ | Biuret (liquid) mass fraction | [−] |
| 11 | $w_{Biu,s}$ | Biuret (solid) mass fraction | [−] |
| 12 | $w_{Triu}$ | Triuret mass fraction | [−] |
| 13 | $w_{Cya,s}$ | Cyanuric acid (solid) mass fraction | [−] |
| 14 | $w_{Amd,s}$ | Ammelide (solid) mass fraction | [−] |
| 15 | $\dot{e}_{H_2O}$ | Evaporation rate (H₂O) | [kg/s] |
| 16 | $\dot{e}_{NH_3}$ | Evaporation rate (NH₃) | [kg/s] |
| 17 | $\dot{e}_{Cya}$ | Evaporation rate (CYA) | [kg/s] |
| 18 | $\dot{e}_{Amd}$ | Evaporation rate (AMD) | [kg/s] |
| 19 | $\dot{e}_{Ur}$ | Evaporation rate (urea) | [kg/s] |
| 20 | $\dot{e}_{HNCO}$ | Evaporation rate (HNCO) | [kg/s] |
| 21 | $\dot{Q}$ | Heat flux | [W] |
| 22 | $t$ | Time | [s] |
| 23 | $\dot{m}$ | Mass loss rate | [kg/s] |

---

## 4. Parameter Space and Validity Domain

The ROM is tabulated over the following parameter ranges, representative of SCR-relevant thermal conditions:

| Parameter | Range |
|-----------|-------|
| Film temperature, $T_f$ | 400 – 650 K |
| Gas temperature, $T_g$ | 450 – 700 K |
| Film thickness, $r$ | $5 \times 10^{-5}$ – $1 \times 10^{-4}$ m |

Extrapolation beyond these bounds is not recommended.

---

## 4.1 Table Resolution and Parameter Space (Film Model)

The film reduced-order model is constructed from a precomputed database of detailed simulations stored in tabulated form. The accuracy of the interpolation depends on the resolution of the parameter grids.

**Film temperature (wall temperature, adiabatic assumption):**
$$T_{\text{film}} = [400, 450, 500, 550, 600, 650] \text{ K}$$

**Ambient gas temperature:**
$$T_{\text{ambient}} = [450, 500, 550, 600, 650, 700] \text{ K}$$

**Film thickness:**
$$R_0 = [5.0 \times 10^{-5}, 1.0 \times 10^{-4}] \text{ m}$$

**Initial conditions:**
- Initial composition: 100% liquid urea

### Accuracy

The reduced model reproduces the detailed simulations with a typical deviation of **≤ 5%** for key observables including ammonia formation and solid residue evolution. Small deviations may appear in the timing of peak formation due to interpolation in coarse parameter directions (especially film thickness).

Accuracy can be improved by:
- Refining the temperature/thickness grids
- Increasing the resolution of the progress-variable discretization

---

## 5. Numerical Implementation

### 5.1 Interpolation Scheme

State reconstruction employs **trilinear interpolation** in the $(T_f, T_g, r)$ parameter space:

$$\Psi(\phi, T_f, T_g, r) = \sum_{i,j,k \in \{0,1\}} w_{ijk} \Psi_{ijk}(\phi)$$

where $w_{ijk}$ are trilinear basis functions and $\Psi_{ijk}$ denotes the precomputed table values at eight neighboring grid points.

### 5.2 Time Integration

The progress variable evolution is integrated using an explicit time-stepping scheme with the interpolated source term $\dot{\phi}(t)$.

### 5.3 Computational Efficiency

The ROM replaces stiff reactive transport equations with:
1. Tabulated data lookup
2. Trilinear interpolation
3. A single explicit ODE in $\phi$

This approach achieves substantial computational acceleration relative to detailed chemistry solvers while maintaining deterministic, reproducible behavior.

---

## 6. Model Assumptions and Limitations

The ROM operates under the following assumptions:

1. **Homogeneous film assumption:** One-dimensional composition and temperature profiles within the film
2. **No spatial gradients:** Uniform properties throughout the film thickness
3. **Valid parameter domain:** Predictive capability restricted to the tabulated range
4. **Droplet–film decoupling:** No inter-droplet or droplet–film interactions
5. **Interpolation closure:** All states outside explicit tabulation points are obtained through interpolation

---

## 7. Model Capabilities

The ROM captures the following physical phenomena:

- Fully coupled multiphase chemistry with tabulated closure
- Film evaporation kinetics and phase equilibrium
- Urea decomposition mechanisms and thermal sensitivity
- Residue formation (biuret, triuret, cyanuric acid, ammelide)
- Direct integration with CFD spray and film solvers
- Deterministic behavior without online chemistry integration

---

## 8. Computational Workflow

The reproducibility workflow proceeds as follows:

1. Load tabulated state data (`uws_film_table.pkl`)
2. Specify initial conditions: $T_f$, $T_g$, $r$, $\phi_0$
3. Perform trilinear interpolation to obtain initial state $\Psi_0$
4. Integrate progress variable evolution: $\phi(t + \Delta t) = \phi(t) + \dot{\phi} \Delta t$
5. Reconstruct full state vector from updated $\phi$ via tabulated mapping

---

## 9. Repository Contents

- **`reduced_model_film.py`** – Core ROM implementation and interpolation routines
- **`uws_film_table.pkl`** – Precomputed tabulated state data
- **`all_process_phi.py`** – Utility functions for data generation and analysis

---

## 10. Funding and Support

This work was supported by the **German Research Foundation (Deutsche Forschungsgemeinschaft, DFG)** under the **Collaborative Research Center SFB TRR 150** (Transregio 150), Task Project B07, Gr[...]

---

## 11. Publication

**Manuscript Title:**  
Tabulated Reduced-Order Model for Urea–Water-Solution (UWS) Film Decomposition in SCR-Relevant Flows

**Status:** Submitted to *Chemical Engineering Journal*

---

## 12. Contact

**Author:** Shlomo Hareli  
**Institution:** Karlsruhe Institute of Technology (KIT)  
**Department:** Institute of Technical Thermodynamics  

---

## References and Attribution

For inquiries regarding model validation, application guidance, or collaboration, please contact the author at the above institution.

