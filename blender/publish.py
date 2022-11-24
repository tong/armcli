import sys
import bpy

wrd = bpy.data.worlds['Arm']
separator_index = -1
try:
    separator_index = sys.argv.index("--")
except:
    pass
if separator_index != -1:
    exporter_to_use = sys.argv[separator_index+1]
    exporter_index = wrd.arm_exporterlist.find(exporter_to_use)
    if exporter_index == -1:
        print(f"exporter [{exporter_to_use}] not found",file=sys.stderr)
        sys.exit(1)
    wrd.arm_exporterlist_index = exporter_index
bpy.ops.arm.publish_project()

