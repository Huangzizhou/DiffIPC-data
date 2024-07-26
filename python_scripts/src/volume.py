import torch
import polyfempy as pf

# Computes the mesh total volume
def VolumeLoss(vertices, faces):
    return 0.5 * torch.sum(
        vertices[faces[:, 0], 0] * vertices[faces[:, 1], 1] + \
        vertices[faces[:, 1], 0] * vertices[faces[:, 2], 1] + \
        vertices[faces[:, 2], 0] * vertices[faces[:, 0], 1] - \
        vertices[faces[:, 0], 0] * vertices[faces[:, 2], 1] - \
        vertices[faces[:, 2], 0] * vertices[faces[:, 1], 1] - \
        vertices[faces[:, 1], 0] * vertices[faces[:, 0], 1])

# Compute volume using C++ code
class VolumeLossCpp(torch.autograd.Function):

    @staticmethod
    # Input arguments "solution" and "vertices" are already cached in "solver"
    # They are only used in backward gradient propogation
    def forward(ctx, solver, vertices):
        ctx.solver = solver
        ctx.vshape = vertices.shape
        args = {
            "state": 0,
            "type": "volume",
            "volume_selection": [],
            "weight": 1
        }
        ctx.obj = pf.create_objective("volume", "shape", solver, args)
        ctx.x = vertices.detach().numpy().reshape((-1, 1))
        return torch.tensor(ctx.obj.value(ctx.x))

    @staticmethod
    @torch.autograd.function.once_differentiable
    def backward(ctx, grad_output):
        grad_x = torch.tensor(ctx.obj.derivative(ctx.solver, ctx.x, wrt="shape"))
        return None, (grad_x * grad_output).reshape(ctx.vshape), None
