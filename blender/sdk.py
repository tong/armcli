import os, sys
import bpy
print("preferences.sdk_path="+bpy.context.preferences.addons["armory"].preferences["sdk_path"], file=sys.stderr)
print("ARMSDK="+os.environ['ARMSDK'], file=sys.stderr)
