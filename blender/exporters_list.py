import sys
import bpy

wrd = bpy.data.worlds['Arm']
i = 0
for exporter in wrd.arm_exporterlist:
    out = f"{i} {exporter.name}"
    out += f" target={exporter.arm_project_target}"
    out += f" rp={exporter.arm_project_rp}"
    out += f" scene={exporter.arm_project_scene.name}"
    if i == wrd.arm_exporterlist_index:
        out += " *"
    print(out,file=sys.stderr)
    i+=1
