import sys, bpy

wrd=bpy.data.worlds['Arm']
si = sys.argv.index("--")+1
runtime = sys.argv[si]
if runtime is not None and len(runtime) > 0:
    wrd.arm_runtime = runtime.title()
camera = sys.argv[si+1]
if camera is not None and len(camera) > 0:
    wrd.arm_play_camera = camera
scene = sys.argv[si+2]
if scene is not None and len(scene) > 0:
    wrd.arm_play_scene = bpy.data.scenes[scene]
renderpath = sys.argv[si+3]
if renderpath is not None and len(renderpath) > 0:
    wrd.arm_play_renderpath = renderpath
bpy.ops.arm.play()

