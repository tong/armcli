import sys
import bpy

wrd = bpy.data.worlds['Arm']
i = 0
for rp in wrd.arm_rplist:
    out = f"{i} {rp.name}"
    print(out, file=sys.stderr)
    i+=1
