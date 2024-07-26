# %%
import numpy as np
import meshio
import igl
import os
import argparse

from sympy import false

# %%
def boundary_loop(f):
    V = np.zeros([np.amax(f) + 1, 2])
    TT, TTi = igl.triangle_triangle_adjacency(f)
    VF, NI = igl.vertex_triangle_adjacency(f, np.amax(f) + 1)
    unvisited = igl.is_border_vertex(V, f)

    unseen = set()
    for i in range(len(unvisited)):
        if (unvisited[i]):
            unseen.add(i)
    
    L = []
    while len(unseen) > 0:
        l = []
        
        start = unseen.pop()
        unvisited[start] = False
        l.append(start)

        done = False
        while not done:
            newBndEdge = False
            v = l[len(l)-1]
            for i in range(NI[v+1]-NI[v]):
                if newBndEdge:
                    break
                fid = VF[NI[v]+i]

                if np.amin(TT[fid]) < 0.0:
                    vLoc = -1
                    if f[fid][0] == v:
                        vLoc = 0
                    if f[fid][1] == v:
                        vLoc = 1
                    if f[fid][2] == v:
                        vLoc = 2

                    vNext = f[fid][(vLoc + 1) % f.shape[1]]

                    newBndEdge = False
                    if unvisited[vNext] and TT[fid][vLoc] < 0:
                        next = vNext
                        newBndEdge = True

            if newBndEdge:
                l.append(next)
                unseen.discard(next)
                unvisited[next] = False
            else:
                done = True

        L.append(l)
    
    return L

# %%
# input_path = 'before_remesh_iter40_mesh1.obj'
# output_path = 'out.msh'
# geo_path = "input.geo"
gmsh_exe = '/Applications/Gmsh.app/Contents/MacOS/gmsh'

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str)
parser.add_argument("output", type=str)
args = parser.parse_args()

input_path = args.input
output_path = args.output
geo_path = input_path + ".geo"

# %%
mesh = meshio.read(input_path)
v = mesh.points
f = mesh.cells[0].data
B = boundary_loop(f)

l = []
for b in B:
    for i in range(0, len(b)):
        l.append([b[i-1], b[i]])

# %%
mask = np.zeros(len(v), dtype=int)

for p in B:
    for x in p:
        mask[x] = 1

map = np.zeros(len(v), dtype=int)
idx = 0
for i in range(len(map)):
    if mask[i] == 0:
        map[i] = -1
    else:
        map[i] = idx
        idx += 1

for edge in range(len(l)):
    l[edge][0] = map[l[edge][0]]
    l[edge][1] = map[l[edge][1]]

l = np.array(l) + 1

new_v = []
for i in range(len(v)):
    if mask[i] == 1:
        new_v.append(v[i])

new_v = np.array(new_v)
v = new_v

# %%
# added = [0]
# lnew = [l[0]]
# cur_p = lnew[0][1]
# cur_line = lnew[0]
# while len(lnew) < len(l):
#     for i in range(len(l)):
#         line = l[i]
#         if cur_p in line and i not in added:
#             lnew.append(line)
#             # print(str(line[0])+","+str(line[1])+" added!", flush=True)
#             if line[0] == cur_p:
#                 cur_p = line[1]
#             else:
#                 cur_p = line[0]
#             added.append(i)
#             break

# %%
with open(geo_path,'w') as f:
    for i in range(v.shape[0]):
        p = v[i]
        f.write("Point("+str(i+1)+") = {"+repr(p[0])+","+repr(p[1])+","+repr(p[2])+",1.0};\n")
    
    for j in range(l.shape[0]):
        f.write("Line("+str(j+1)+") = {"+str(l[j][0])+","+str(l[j][1])+"};\n")
        
    f.write("Curve Loop(1) = {")
    for j in range(l.shape[0]):
        f.write(str(j+1))
        if j < l.shape[0] - 1:
            f.write(",")
        else:
            f.write("};\n")
            
    f.write("Plane Surface(1)={1};\n")
    f.write("Mesh 2;\n")

# %%
os.system(gmsh_exe+" "+geo_path+" -o "+output_path+" -format msh22 -save")
