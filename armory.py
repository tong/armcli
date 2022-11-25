#!/usr/bin/python

import argparse
import glob
import os
import pathlib
import subprocess
import sys
from subprocess import PIPE

if os.path.islink(sys.argv[0]):
    symlink = os.readlink(sys.argv[0])
    dir = os.path.dirname(symlink)
else:
    dir = os.path.dirname(sys.argv[0])
script_dir = f"{dir}/blender"

verbose = False

armsdk_path = os.getenv("ARMSDK")
if armsdk_path == None:
    print("armsdk not found, set ARMSDK environment variable")
    sys.exit(1)


def find_main_blend_file(blend=None):
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
    # if verbose:
    print(" ".join(cmd))
    p = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    while p.poll() is None:
        print(p.stdout.readline().decode("utf-8"), end="", file=sys.stdout)
        # print(p.stderr.readline().decode("utf-8"), end="", file=sys.stderr)
    sys.exit(p.returncode)


def execute_blender_script(script: str, blend=None, args=None):
    cmd = []
    if blend is not None:
        cmd.append(blend)
    cmd.extend(["--python", f"{script_dir}/{script}.py"])
    if args is not None and len(args) > 0:
        cmd.append("--")
        cmd.extend(args)
    execute_blender(cmd)


def execute_blender_expr(expr: str, blend: str = None):
    cmd = []
    if blend is not None:
        cmd.append(blend)
    cmd.extend(["--python-expr", "'" + expr + "'"])
    execute_blender(cmd)


def cli_build(args):
    blend = find_main_blend_file(args.blend)
    execute_blender_script("build", blend)


def cli_publish(args):
    blend = find_main_blend_file(args.blend)
    _args = []
    if args.exporter is not None:
        _args.append(args.exporter)
    execute_blender_script("publish", blend, _args)
    # execute_blender_expr("bpy.ops.arm.publish_project()", blend)


def cli_clean(args):
    blend = find_main_blend_file(args.blend)
    # execute_blender_expr("bpy.ops.arm.clean_project()", blend)
    execute_blender_script("clean", blend)


def cli_play(args):
    blend = find_main_blend_file(args.blend)
    execute_blender_expr("bpy.ops.arm.play()", blend)


def cli_traits(args):
    print(args)
    blend = find_main_blend_file(args.blend)
    execute_blender_script("traits", blend)


def cli_sdk(args):
    print(args)
    execute_blender_script("sdk")


argparser = argparse.ArgumentParser(prog="armory")
# argparser.add_argument('command', choices=['build','public','clean'])
argparser.add_argument(
    "--verbose", dest="verbose", action="store_true", help="print verbose outpout"
)

subparsers = argparser.add_subparsers()

parser_build = subparsers.add_parser("build", help="build project")
parser_build.add_argument("--blend", help="path to main blend file")
parser_build.add_argument("--exporter", help="exporter to use")
parser_build.set_defaults(func=cli_build)

parser_publish = subparsers.add_parser("publish", help="publish project")
parser_publish.add_argument("--blend", help="path to main blend file")
parser_publish.add_argument("--exporter", help="exporter to use")
parser_publish.set_defaults(func=cli_publish)

parser_clean = subparsers.add_parser("clean", help="clean project")
parser_clean.add_argument("--blend", help="path to main blend file")
parser_clean.set_defaults(func=cli_clean)

# parser_play = subparsers.add_parser('play', help='run project')
# parser_play.add_argument('--blend', help='path to main blend file')
# parser_play.add_argument('--runtime', default='Krom', help='runtime to use')
# parser_play.add_argument('--camera', default='Scene', help='viewport camera')
# parser_play.add_argument('--renderpath', help='Default render path')
# parser_play.set_defaults(func=play)

# parser_traits = subparsers.add_parser('traits', help='manage traits')
# parser_traits.add_argument('--blend', help='path to main blend file')
# parser_traits.set_defaults(func=traits)
# trait_subparsers = parser_traits.add_subparsers(help='sub-command help')
# parser_traits_list = trait_subparsers.add_parser('list')
# parser_traits_list.set_defaults(func=cli_traits)

parser_sdk = subparsers.add_parser("sdk", help="manage armsdk")
# parser_sdk.add_argument('path', help='path to armsdk')
parser_sdk.set_defaults(func=cli_sdk)

if len(sys.argv) == 1:
    argparser.print_help()
    sys.exit(1)

args = argparser.parse_args()
verbose = args.verbose
args.func(args)
