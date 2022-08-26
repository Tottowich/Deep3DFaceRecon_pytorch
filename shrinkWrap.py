import bpy
from mathutils import Matrix
context = bpy.context

from random import uniform # random 20x20 to test
x, y = uniform(-20, 20), uniform(-20, 20)
remove_foot = True

target_surface = context.object


bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
#make the origin the pottom of cube
cube = context.object
me = cube.data
me.transform(Matrix.Translation((0, 0, 1)))
cube.scale = (4, 1, 1)


bpy.ops.mesh.primitive_circle_add(
        location=(x, y, 0),
        fill_type='TRIFAN')
foot = context.object
sw = foot.modifiers.new(name="SW", type='SHRINKWRAP') 
sw.target = target_surface
sw.wrap_method = 'PROJECT'
sw.use_positive_direction = True
sw.use_negative_direction = True
sw.use_project_z = True

### set the relation to foot
cube.parent = foot
cube.parent_type = 'VERTEX_3'
n = len(foot.data.vertices)
cube.parent_vertices = range(1, n, n // 3)

if remove_foot:
    dg = context.evaluated_depsgraph_get()
    mw = cube.evaluated_get(dg).matrix_world.copy()
    bpy.data.objects.remove(foot)
    cube.matrix_world = mw
context.view_layer.objects.active = target_surface

### set the relation to foot
dg = context.evaluated_depsgraph_get()
me_inst = foot.evaluated_get(dg).to_mesh(depsgraph=dg)
v = me_inst.vertices[0]

cube.location = foot.matrix_world @ v.co.copy()
q = v.normal.to_track_quat()
cube.rotation_euler = q.to_euler()
if remove_foot:
    bpy.data.objects.remove(foot)
context.view_layer.objects.active = target_surface

# z_axis = Vector((0, 0, 1)
# if v.normal.angle(z_axis) > radians(45):
#     pass
#     # don't put it there