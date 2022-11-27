import sys
import bpy

wrd = bpy.data.worlds['Arm']
i = 0
for rp in wrd.arm_rplist:
    str = f"{i} {rp.name}"
    i+=1

