#!/usr/bin/python

import argparse
import glob
import os
import pathlib
import subprocess
import sys

script_dir = os.path.dirname(sys.argv[0])+'/blender'

armsdk_path = os.getenv('ARMSDK')
if armsdk_path == None:
    print("armsdk not found, set ARMSDK environment variable")
    sys.exit(1)

def get_main_blend_file(blend=None):
    if blend is None:
        dir = os.getcwd()
        dirname = os.path.basename(dir)
        blend = f"{dir}/{dirname}.blend"
        if not os.path.exists(blend):
            raise "blend file not found"
        return blend
    if not os.path.exists(blend):
        raise "blend file not found"
    return blend

def execute_blender(args):
    cmd = ["blender", "--background"]
    cmd.extend(args)
    print(" ".join(cmd))
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode == 0:
        print(p.stdout.decode("utf-8"))
    else:
        print(p.stderr.decode("utf-8"))
    sys.exit(p.returncode)

def execute_blender_script(script:str, blend=None, args=None):
    cmd = []
    if blend is not None:
        cmd.append(blend)
    cmd.extend(["--python", f"{script_dir}/{script}.py"])
    if args is not None:
        cmd.extend(args)
    execute_blender(cmd)

def execute_blender_expr(expr:str, blend:str=None):
    cmd = []
    if blend is not None:
        cmd.append(blend)
    cmd.extend(["--python-expr", "'"+expr+"'"])
    execute_blender(cmd)

def build(args):
    blend = get_main_blend_file(args.blend)
    execute_blender_script("build", blend)

def publish(args):
    blend = get_main_blend_file(args.blend)
    execute_blender_expr("bpy.ops.arm.publish_project()", blend)

def clean(args):
    blend = get_main_blend_file(args.blend)
    execute_blender_expr("bpy.ops.arm.clean_project()", blend)

def play(args):
    blend = get_main_blend_file(args.blend)
    execute_blender_expr("bpy.ops.arm.play()", blend)

def sdk(args):
    print(args)
    execute_blender_script('sdk')

argparser_main = argparse.ArgumentParser(prog='armory',description='Work seamlessly with Armory from the command line')
#argparser_main.add_argument('command', choices=['build','public','clean'])

subparsers = argparser_main.add_subparsers(help='sub-command help')

parser_build = subparsers.add_parser('build', help='build project')
parser_build.add_argument('--blend', help='path to main blend file')
parser_build.add_argument('--exporter', help='exporter to use')
parser_build.set_defaults(func=build)

parser_publish = subparsers.add_parser('publish', help='publish project')
parser_publish.add_argument('--blend', help='path to main blend file')
parser_publish.add_argument('--exporter', help='exporter to use')
parser_publish.set_defaults(func=publish)

parser_clean = subparsers.add_parser('clean', help='clean project')
parser_clean.add_argument('--blend', help='path to main blend file')
parser_clean.set_defaults(func=clean)

# parser_play = subparsers.add_parser('play', help='run project')
# parser_play.add_argument('--blend', help='path to main blend file')
# parser_play.add_argument('--runtime', default='Krom', help='runtime to use')
# parser_play.add_argument('--camera', default='Scene', help='viewport camera')
# parser_play.add_argument('--renderpath', help='Default render path')
# parser_play.set_defaults(func=play)

parser_sdk = subparsers.add_parser('sdk', help='manage armsdk')
#parser_sdk.add_argument('path', help='path to armsdk')
parser_sdk.set_defaults(func=sdk)

argparser_main.add_argument('--verbose',dest='verbose',action='store_true', help='print verbose outpout')

args = argparser_main.parse_args()
args.func(args)

