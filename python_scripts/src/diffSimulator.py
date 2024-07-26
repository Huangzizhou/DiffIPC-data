import torch
import polyfempy as pf

# Differentiable simulator that computes shape derivatives
class Simulate(torch.autograd.Function):

    @staticmethod
    def forward(ctx, solver, vertices):
        # Update solver setup
        solver.mesh().set_vertices(vertices)
        # Enable caching intermediate variables in the simulation, which will be used for solve_adjoint
        solver.set_cache_level(pf.CacheLevel.Derivatives)
        # Run simulation
        solver.solve()
        # Collect transient simulation solutions
        sol = torch.tensor(solver.get_solutions())
        # Cache solver for backward gradient propagation
        ctx.solver = solver
        return sol

    @staticmethod
    @torch.autograd.function.once_differentiable
    def backward(ctx, grad_output):
        # solve_adjoint only needs to be called once per solver, independent of number of types of optimization variables
        ctx.solver.solve_adjoint(grad_output)
        # Compute shape derivatives
        return None, torch.tensor(pf.shape_derivative(ctx.solver))
    