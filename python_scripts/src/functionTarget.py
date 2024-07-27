import torch
import polyfempy as pf

class FunctionTargetLoss(torch.autograd.Function):

    @staticmethod
    # Input arguments "solution" and "param" are already cached in "solver"
    # They are only used in backward gradient propogation
    def forward(ctx, solver, solution, param, target_function, target_function_gradient, surface_selection=[]):
        ctx.solver = solver
        ctx.ushape = solution.shape
        args = {
            "state": 0,
            "type": "function-target",
            "surface_selection": surface_selection,
            "target_function": target_function,
            "target_function_gradient": target_function_gradient,
            "weight": 1
        }
        ctx.obj = pf.create_objective("function-target", "shape", solver, args)
        ctx.x = param.detach().numpy().reshape(-1)
        return torch.tensor(ctx.obj.value(ctx.x))

    @staticmethod
    @torch.autograd.function.once_differentiable
    def backward(ctx, grad_output):
        grad_u = torch.tensor(ctx.obj.derivative(ctx.solver, ctx.x, wrt="solution"))
        return None, (grad_u * grad_output).reshape(ctx.ushape), None, None, None, None
