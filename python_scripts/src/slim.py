import numpy as np
import igl

def mesh_quality(V, F):
    e0 = np.linalg.norm(V[F[:, 1]] - V[F[:, 0]], axis=1)
    e1 = np.linalg.norm(V[F[:, 2]] - V[F[:, 0]], axis=1)
    e2 = np.linalg.norm(V[F[:, 1]] - V[F[:, 2]], axis=1)
    out = np.hstack((e0[:, None], e1[:, None], e2[:, None]))
    return np.max(np.max(out, axis=1) / np.min(out, axis=1))

def smooth_internal_nodes(V, T, boundary_nodes, mapped_boundary_points, tolerance=1e-7, max_iter=50):
    Vinit = V.copy()
    dim = V.shape[1]
    if dim == 2:
        V = np.hstack((V, np.zeros((V.shape[0], 1), dtype=float)))
    slim = igl.SLIM(V, T, Vinit, boundary_nodes, mapped_boundary_points, 2, 1e5)
    err = 1
    niters = 0
    while err > tolerance and niters < max_iter:
        slim.solve(4)
        niters += 4
        err = np.linalg.norm(slim.vertices()[boundary_nodes, :] - mapped_boundary_points) / len(boundary_nodes)
    
    V[:, :dim] = slim.vertices()
    V[boundary_nodes, :dim] = mapped_boundary_points
    return V[:, :dim]
