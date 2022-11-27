import sys
import bpy

wrd = bpy.data.worlds['Arm']
i = 0
for exporter in wrd.arm_exporterlist:
    str = f"{i} {exporter.name}"
    str += f" target={exporter.arm_project_target}"
    str += f" rp={exporter.arm_project_rp}"
    str += f" scene={exporter.arm_project_scene.name}"
    if i == wrd.arm_exporterlist_index:
        str += " *"
    print(str,file=sys.stderr)
    i+=1

