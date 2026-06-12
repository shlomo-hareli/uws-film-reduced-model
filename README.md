UWS Film Reduced Model (Tabulated Framework)

Tabulated Reduced-Order Model for Urea–Water-Solution (UWS) Film Decomposition in SCR-Relevant Flows

Manuscript status: Submitted to Chemical Engineering Journal

Author: Shlomo Hareli
Karlsruhe Institute of Technology (KIT)
Institute of Technical Thermodynamics

Project Overview

This repository provides a tabulated reduced-order model for the simulation of UWS film heating, evaporation, and chemical decomposition in Selective Catalytic Reduction (SCR) systems.

The model replaces expensive detailed multiphase reactive simulations with a deterministic surrogate model based on a progress-variable representation and precomputed high-fidelity simulation data.

It is designed for integration into Euler–Euler and Euler–Lagrange CFD frameworks.

Scientific Objective

The objective is to efficiently reproduce the following coupled processes:

Film heating and thermal evolution
Phase change and evaporation
Urea decomposition pathways
Intermediate species formation
Heat and mass transfer coupling

while significantly reducing computational cost compared to full detailed simulations.

Model Formulation

The thermochemical state is represented as:

Psi = Psi(phi, Tf, Tg, r)

where:

phi = progress variable
Tf = film temperature
Tg = gas temperature
r = film thickness

The system evolution is reduced to:

dphi/dt = phi_dot(phi, Tf, Tg, r)

Time integration:

phi(t + dt) = phi(t) + phi_dot * dt

All remaining thermochemical variables are reconstructed from phi using tabulated data.

State Vector (24 Variables)

0 phi progress variable
1 dphi_dt source term
2 d2eq equivalent diameter
3 md mass
4 temp temperature
5 rho density
6 w_h2o water mass fraction
7 w_ur_s solid urea
8 w_ur_l liquid urea
9 w_hnco_l isocyanic acid
10 w_biu_l biuret liquid
11 w_biu_s biuret solid
12 w_triu triuret
13 w_cya_s cyanuric acid
14 w_amd_s ammelide
15 e_h2o evaporation rate (H2O)
16 e_nh3 evaporation rate (NH3)
17 e_cya evaporation rate (CYA)
18 e_amd evaporation rate (AMD)
19 e_ur evaporation rate (urea)
20 e_hnco evaporation rate (HNCO)
21 qdot heat flux
22 t time
23 mdot mass loss rate

Parameter Space

Film temperature Tf: 400 – 650 K
Gas temperature Tg: 450 – 700 K
Film thickness r: 5e-5 – 1e-4 m

Numerical Method

Trilinear interpolation in (Tf, Tg, r) space using eight neighboring tabulated states
Reduction to a single progress variable phi
Explicit time integration using interpolated source term

Model Features

Fully tabulated reduced-order multiphase chemistry model
Captures evaporation, decomposition, and residue formation
Compatible with CFD spray and film solvers
Deterministic surrogate without on-the-fly chemistry integration
Efficient for large-scale simulations

Assumptions and Limitations

One-dimensional homogeneous film assumption
No spatial gradients inside the film
Valid only within tabulated parameter range
No droplet–film or film–film interaction
Interpolation-based closure assumption

Computational Efficiency

The model replaces stiff reactive transport equations with:

Table lookup and interpolation
One ODE in phi

Resulting in significant computational speed-up compared to detailed chemistry solvers.

Funding

German Research Foundation (DFG)
SFB TRR 150 (TP-B07), Project No. 237267381

Publication

Manuscript submitted to Chemical Engineering Journal

Title: Tabulated Reduced-Order Model for Urea–Water-Solution (UWS) Film Decomposition in SCR-Relevant Flows

Reproducibility

Load uws_film_table.pkl
Select Tf, Tg, r
Perform trilinear interpolation
Integrate phi evolution in time
Reconstruct full state vector

Repository Contents

reduced_model_film.py
uws_film_table.pkl
all_process_phi.py

Contact

Karlsruhe Institute of Technology (KIT)
Institute of Technical Thermodynamics
