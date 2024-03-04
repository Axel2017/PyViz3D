import bpy
import math
import mathutils
import numpy as np
import subprocess
import json


C = bpy.context
D = bpy.data

import sys
argv = sys.argv
try:
    argv = argv[argv.index("--") + 1:]  # get all args after "--"
except ValueError:
   argv = []

def clear_scene():
  # Remove all meshes from the scene, keep the light and camera
  for o in C.scene.objects:
    print(o)
    if o.type == 'MESH':
        o.select_set(True)
    else:
        o.select_set(False)
  bpy.ops.object.delete()


def render(path, file_format='PNG', color_mode='RGBA'):
  """
  :path: the file path of the rendered image
  :file_format: {PNG, JPEG}
  """
  C.scene.render.image_settings.file_format=file_format
  C.scene.render.filepath = path

  # C.scene.view_settings.view_transform = 'Standard'
  # D.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
  # bpy.context.scene.world.use_nodes = False
  # bpy.context.scene.world.color = (1, 1, 1)
  # C.scene.render.alpha_mode = 'SKY'
  bpy.ops.render.render(use_viewport=True, write_still=True)


def save_blender_scene(path):
  bpy.ops.wm.save_as_mainfile(filepath=f'/Users/francis/Programming/PyViz3D/{path}')


def compute_object_center(object):
  local_bbox_center = 0.125 * sum((mathutils.Vector(b) for b in object.bound_box),
                                   mathutils.Vector())
  return object.matrix_world @ local_bbox_center


def look_at(camera,
            eye=mathutils.Vector((13.0, 13.0, 13.0)),
            at=mathutils.Vector((0.0, 0.0, 3.0)),
            up=mathutils.Vector((0.0, 0.0, 1.0))):
  d = (eye - at).normalized()
  r = up.cross(d).normalized()
  u = d.cross(r).normalized()
  camera.matrix_world = mathutils.Matrix(((r.x, u.x, d.x, eye.x),
                                          (r.y, u.y, d.y, eye.y),
                                          (r.z, u.z, d.z, eye.z),
                                          (0.0, 0.0, 0.0, 1.0)))


def create_video(input_dir, pattern, output_filepath):
  trans_to_white = "format=yuva444p,\
  geq=\
  'if(lte(alpha(X,Y),16),255,p(X,Y))':\
  'if(lte(alpha(X,Y),16),128,p(X,Y))':\
  'if(lte(alpha(X,Y),16),128,p(X,Y))'"

  # f = "color=white,format=rgb24[c];[c][0]scale2ref[c][i];[c][i]overlay=format=auto:shortest=1,setsar=1"
  # cmd = ["ffmpeg", "-i", pattern, '-filter_complex', f, '-y', output_filepath]
  # subprocess.run(cmd)

  import glob
  for fi in glob.glob(f'{input_dir}/output_*.png'):
    subprocess.run(["convert", "-flatten", fi, fi])
    # subprocess.run(["convert", fi, "-background", "white", "-alpha", "remove", "-flatten", "-alpha", "off", fi])
  # subprocess.run(["ffmpeg", "-i", pattern, '-y', output_filepath])
  subprocess.run(["ffmpeg", "-i", f'{input_dir}/{pattern}', "-vcodec", "libx264", "-vf", "format=yuv420p", "-y", output_filepath])
  # subprocess.run(["convert", "-delay", "1", "-loop", "0", "*.png", "myimage.gif"])


def init_scene(resolution_x=800, resolution_y=600):
  # render stuff
  C.scene.render.resolution_x = resolution_x
  C.scene.render.resolution_y = resolution_y
  D.scenes["Scene"].render.film_transparent = True
  C.scene.render.image_settings.color_mode = 'RGBA'
  C.scene.view_settings.look = 'AgX - Medium High Contrast'
  C.scene.view_settings.view_transform = 'Standard'
  C.scene.render.engine = 'CYCLES'
  C.scene.cycles.device = 'GPU'
  C.scene.cycles.preview_samples = 100
  C.scene.cycles.samples = 150
  C.scene.frame_end = 60
  # Add lights
  C.scene.objects['Light'].data.shadow_soft_size = 1.0
  C.scene.objects['Light'].data.cycles.cast_shadow = False
  bpy.ops.object.light_add(type='POINT', radius=1, align='WORLD', location=(-1, 1, 10), scale=(1, 1, 1))
  C.scene.objects['Point'].data.energy = 7000.0
  C.scene.objects['Point'].data.shadow_soft_size = 3


def create_mat(obj):
    mat = bpy.data.materials.new(name="test")
    mat.use_backface_culling = True
    obj.data.materials.append(mat)
    mat.use_nodes = True
    mat.node_tree.nodes.new(type="ShaderNodeVertexColor")
    mat.node_tree.nodes["Color Attribute"].layer_name = "Col"
    mat.node_tree.links.new(
      mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"],
      mat.node_tree.nodes["Color Attribute"].outputs["Color"])
    mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0  # specular

def cylinder_between(x1, y1, z1, x2, y2, z2, r, c):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1    
    dist = math.sqrt(dx**2 + dy**2 + dz**2)
    bpy.ops.mesh.primitive_cylinder_add(
        radius = r, 
        depth = dist,
        location = (dx/2 + x1, dy/2 + y1, dz/2 + z1)   
    ) 
    phi = math.atan2(dy, dx) 
    theta = math.acos(dz/dist) 
    bpy.context.object.rotation_euler[1] = theta 
    bpy.context.object.rotation_euler[2] = phi 
    bpy.context.object.color = (c[0], c[1], c[2], 1.0)

    mat = bpy.data.materials.new("cylinder")
    mat.use_nodes = True
    # mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (c[0], c[1], c[2], 1.0)
    # mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0  # specular
    # principled = mat.node_tree.nodes['Principled BSDF']
    # principled.inputs['Base Color'].default_value = (c[0], c[1], c[2], 1.0)
    # principled.inputs[7].default_value = 0  # specular
    bpy.context.object.data.materials.append(mat)
    return bpy.context.object

def main():
    clear_scene()
    init_scene()

    path_json = f'nodes.json'
    with open(path_json) as f:
        nodes_dict = json.load(f)

    for name, properties in nodes_dict.items():
        print(name, properties)
        if properties['type'] == 'points':
           bpy.ops.wm.ply_import(filepath=name+'.ply')
           bpy.ops.object.shade_smooth()
           obj = bpy.data.objects[name]
           create_mat(obj)
        if properties['type'] == 'camera':
           eye = mathutils.Vector(properties['position'])
           at = mathutils.Vector(properties['look_at'])
           up = mathutils.Vector(properties['up'])
           look_at(C.scene.objects['Camera'], eye, at, up)
           C.scene.objects['Camera'].data.lens = properties['focal_length']
        if properties['type'] == 'cuboid':
           obj = bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD',
                                           location=mathutils.Vector(properties['position']),
                                           scale=mathutils.Vector(properties['size']))
        if properties['type'] == 'polyline':
            if len(properties['positions']) <= 1:
                continue
            for i in range(len(properties['positions']) - 1):
                x1 = properties['positions'][i][0]
                y1 = properties['positions'][i][1]
                z1 = properties['positions'][i][2]
                x2 = properties['positions'][i + 1][0]
                y2 = properties['positions'][i + 1][1]
                z2 = properties['positions'][i + 1][2]
                obj = cylinder_between(x1, y1, z1, x2, y2, z2, properties['edge_width'] * 2, properties['color'])
    if len(argv) > 0:
        render(argv[0])
    # loops = len(obj.data.loops)
    # verts = len(obj.data.vertices)
    # print(loops, verts, len(obj.data.vertex_colors['Col'].data))

    # Read vertex colors

    # name = 'PointClouds;1'  # Color
    # num_points = j[name]['num_points']
    # print(num_points)
    # binary_filename = j[name]['binary_filename']
    # path_pointcloud = f'{binary_filename}'
    # try:
    #     with open(path_pointcloud, 'rb') as f:
    #         data = f.read()
    # except:
    #     print(f'Could not read: {path_pointcloud}')
    #     points = data[:12 * num_points]
    #     normals = data[12 * num_points:24 * num_points]
    #     colors = data[24 * num_points:]

    # points = np.frombuffer(data[:12 * num_points], np.float32).reshape([-1, 3])
    # colors = np.frombuffer(data[24 * num_points:], np.uint8).reshape([-1, 3])

    # for i in range(num_points):
    #     bpy.ops.mesh.primitive_uv_sphere_add(segments=5,
    #                                         ring_count=5,
    #                                         radius=0.1,
    #                                         enter_editmode=False,
    #                                         location=points[i])

# try: 
#   for i, d in enumerate(obj.data.vertex_colors['Col'].data):
#     vertex_index = obj.data.loops[i].vertex_index
#      for j in [0, 1, 2]:
#       d.color[j] = float(colors[vertex_index * 3 + j]) / 255.0
# except:
# print(f'{name} not found: {path_pointcloud}')

# look into each loop's vertex ? (need to filter out double entries)
# visit = verts * [False]
# colors = {}

# for l in range(loops):
# v = obj.data.loops[l].vertex_index
# c = vcol.data[l].color
# if not visit[v]:
#         colors[v] = c
#         visit[v] = True

# sorted(colors)
# print("Vertex-Colors of Layer:", vcol.name)
# #print(colors)
# for v, c in colors.items():
#     print("Vertex {0} has Color {1}".format(v, (c[0], c[1], c[2])))

# bpy.ops.material.new()
# bpy.data.materials["Material.001"].use_backface_culling = True

# bpy.ops.object.mode_set(mode='VERTEX_PAINT')

#   create_mat(obj)
  
#   save_blender_scene(path=f'{name}.blend')
#   exit()
#   for i in range(0, 2):
#     a = i * 2 / 180.0 * math.pi
#     radius = 2.0
#     camera_position=mathutils.Vector(
#       (math.cos(a) * radius, math.sin(a) * radius, 1.0 ))
#     scene_center=compute_object_center(obj)
#     scene_center.z = -0.3
#     camera_position += scene_center
#     look_at(D.objects['Camera'],
#             eye=camera_position,
#             at=scene_center)
#     render(path=f'{prefix}/frames/output_{str(i).zfill(5)}', file_format='PNG')
#   create_video(f'{prefix}/frames', 'output_%05d.png', f"{prefix}/{scene_name}_{name}.mp4")


# if __name__ == "__main__":
#   main(scene_name="cnb_103",
#        layer_name="InstancesAll")  # Color, InstanceAll

# matg = bpy.data.materials.new("Green")
# matg.diffuse_color = (0,1,0,0.8)
# obj.active_material = matg
# obj.vertex_colors.new(name=vertex_colors_name)
# color_layer = mesh.vertex_colors[vertex_colors_name]
# print(len(obj.data.vertices))