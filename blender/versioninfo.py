import bpy
import sys
try:
    version = bpy.ops.arm_addon.print_version_info()
    print(version,file=sys.stderr)
except:
    pass
