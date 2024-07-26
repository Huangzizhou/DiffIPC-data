import torch
import polyfempy as pf

class StressNormLoss(torch.autograd.Function):

    @staticmethod
    # Input arguments "solution" and "vertices" are already cached in "solver"
    # They are only used in backward gradient propogation
    def forward(ctx, solver, solution, vertices, power=2, volume_selection=[]):
        ctx.solver = solver
        ctx.ushape = solution.shape
        ctx.vshape = vertices.shape
        args = {
            "state": 0,
            "type": "stress_norm",
            "volume_selection": volume_selection,
            "power": power,
            "weight": 1
        }
        ctx.obj = pf.create_objective("stress_norm", "shape", solver, args)
        ctx.x = vertices.detach().numpy().reshape((-1, 1))
        return torch.tensor(ctx.obj.value(ctx.x))

    @staticmethod
    @torch.autograd.function.once_differentiable
    def backward(ctx, grad_output):
        grad_u = torch.tensor(ctx.obj.derivative(ctx.solver, ctx.x, wrt="solution"))
        grad_x = torch.tensor(ctx.obj.derivative(ctx.solver, ctx.x, wrt="shape"))
        return None, (grad_u * grad_output).reshape(ctx.ushape), (grad_x * grad_output).reshape(ctx.vshape), None
