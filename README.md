# [Siggraph 2024] Differentiable solver for time-dependent deformation problems with contact
A repository of the data and script used in our work, ["Differentiable solver for time-dependent deformation problems with contact" [Huang et al. 2024]](https://dl.acm.org/doi/10.1145/3657648).

The scripts are input files for [PolyFEM](https://polyfem.github.io/). The simulation code is currently at [diffIPC](https://github.com/polyfem/polyfem/tree/diffIPC) branch.

# Citation
If you use this work/data. Please cite our paper:

```
@article{10.1145/3657648,
author = {Huang, Zizhou and Tozoni, Davi Colli and Gjoka, Arvi and Ferguson, Zachary and Schneider, Teseo and Panozzo, Daniele and Zorin, Denis},
title = {Differentiable solver for time-dependent deformation problems with contact},
year = {2024},
issue_date = {June 2024},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
volume = {43},
number = {3},
issn = {0730-0301},
url = {https://doi.org/10.1145/3657648},
doi = {10.1145/3657648},
abstract = {We introduce a general differentiable solver for time-dependent deformation problems with contact and friction. Our approach uses a finite element discretization with a high-order time integrator coupled with the recently proposed incremental potential contact method for handling contact and friction forces to solve ODE- and PDE-constrained optimization problems on scenes with complex geometry. It supports static and dynamic problems and differentiation with respect to all physical parameters involved in the physical problem description, which include shape, material parameters, friction parameters, and initial conditions. Our analytically derived adjoint formulation is efficient, with a small overhead (typically less than 10\% for nonlinear problems) over the forward simulation, and shares many similarities with the forward problem, allowing the reuse of large parts of existing forward simulator code.We implement our approach on top of the open-source PolyFEM library and demonstrate the applicability of our solver to shape design, initial condition optimization, and material estimation on both simulated results and physical validations.},
journal = {ACM Trans. Graph.},
month = {may},
articleno = {31},
numpages = {30},
keywords = {Differentiable simulation, finite element method, elastodynamics, frictional contact}
}
```
