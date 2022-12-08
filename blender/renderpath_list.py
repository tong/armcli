import sys
import bpy

wrd = bpy.data.worlds['Arm']
for i, rp in enumerate(wrd.arm_rplist):
    out = f"{i} {rp.name}"
    print(out, file=sys.stderr)
