import sys
import bpy

wrd = bpy.data.worlds["Arm"]
if len(wrd.arm_exporterlist) == 0:
    print("Project has no exporters configured", file=sys.stderr)
    sys.exit(1)
SI = -1
try:
    SI = sys.argv.index("--")
except:
    pass
if SI != -1:
    exporter_to_use = sys.argv[SI + 1]
    exporter_index = wrd.arm_exporterlist.find(exporter_to_use)
    if exporter_index == -1:
        print(f"exporter [{exporter_to_use}] not found", file=sys.stderr)
        sys.exit(1)
    wrd.arm_exporterlist_index = exporter_index
bpy.ops.arm.publish_project()
exit(0)
