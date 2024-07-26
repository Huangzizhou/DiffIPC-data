import torch
import polyfempy as pf

class BoundarySmooth(torch.autograd.Function):

    @staticmethod
    # Input arguments "solution" and "vertices" are already cached in "solver"
    # They are only used in backward gradient propogation
    def forward(ctx, solver, vertices, surface_selection=[], scale_invariant=False, power=2):
        ctx.solver = solver
        ctx.vshape = vertices.shape
        args = {
            "state": 0,
            "type": "boundary_smoothing",
            "surface_selection": surface_selection,
            "scale_invariant": scale_invariant,
            "power": power,
            "weight": 1
        }
        ctx.obj = pf.create_objective("boundary_smoothing", "shape", solver, args)
        ctx.x = vertices.detach().numpy().reshape((-1, 1))
        return torch.tensor(ctx.obj.value(ctx.x))

    @staticmethod
    @torch.autograd.function.once_differentiable
    def backward(ctx, grad_output):
        grad_x = torch.tensor(ctx.obj.derivative(ctx.solver, ctx.x, wrt="shape"))
        return None, (grad_x * grad_output).reshape(ctx.vshape), None
