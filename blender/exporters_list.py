import sys
import bpy

wrd = bpy.data.worlds['Arm']
for i, exporter in enumerate(wrd.arm_exporterlist):
    out = f"{i} {exporter.name}"
    out += f" target={exporter.arm_project_target}"
    out += f" rp={exporter.arm_project_rp}"
    out += f" scene={exporter.arm_project_scene.name}"
    if i == wrd.arm_exporterlist_index:
        out += " *"
    print(out,file=sys.stderr)
