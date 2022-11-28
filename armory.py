#!/usr/bin/python

import argparse
import glob
import os
import pathlib
import subprocess
import sys
from subprocess import PIPE

verbose = False
print_blender_stdout = True
print_script_call = True

armsdk_path = os.getenv("ARMSDK")
if armsdk_path == None:
    print("armsdk not found, set ARMSDK environment variable")
    sys.exit(1)

if os.path.islink(sys.argv[0]):
    dir = os.path.dirname(os.readlink(sys.argv[0]))
else:
    dir = os.path.dirname(sys.argv[0])
script_dir = f"{dir}/blender"
if not os.path.exists(script_dir) or not os.path.isdir(script_dir):
    raise "armcli/blender/ not found"


def find_main_blend_file(blend: str = None):
    if blend is None:
        dir = os.getcwd()
        blend = f"{dir}/{os.path.basename(dir)}.blend"
        if not os.path.exists(blend):
            print("main blend file not found", file=sys.stderr)
            sys.exit(1)
        return blend
    if not os.path.exists(blend):
        raise "blend file not found"
    return blend


def execute_blender(args):
    cmd = ["blender", "--background"]
    cmd.extend(args)
    if print_script_call:
        print(" ".join(cmd))
    if print_blender_stdout:
        p = subprocess.Popen(cmd, stderr=PIPE)
    else:
        p = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    while p.poll() is None:
        print(p.stderr.readline().decode("utf-8"), end="", file=sys.stdout)
    sys.exit(p.returncode)


def execute_blender_script(script: str, blend: str = None, args=None):
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


def cli_clean(args):
    blend = find_main_blend_file(args.blend)
    execute_blender_script("clean", blend)


def cli_play(args):
    blend = find_main_blend_file(args.blend)
    if args.camera is None: args.camera = ""
    if args.scene is None: args.scene = ""
    if args.renderpath is None: args.renderpath = ""
    params = [args.runtime,args.camera,args.scene,args.renderpath]
    execute_blender_script("play", blend, params)


def cli_exporters(args):
    blend = find_main_blend_file(args.blend)
    execute_blender_script(f"exporters_{args.command}", blend)


def cli_renderpath(args):
    execute_blender_script(f"renderpath_list", find_main_blend_file(args.blend))


def cli_traits(args):
    blend = find_main_blend_file(args.blend)
    execute_blender_script("traits", blend)


def cli_kha(args):
    cmd = ["node", f"{armsdk_path}/Kha/make.js", "--shaderversion", "330"]
    p = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    while p.poll() is None:
        print(p.stdout.readline().decode("utf-8"), end="", file=sys.stdout)
    sys.exit(p.returncode)


def cli_sdk(args):
    execute_blender_script("sdk")


argparser = argparse.ArgumentParser(prog="armory")
argparser.add_argument(
    "--print-script-call",
    dest="print_script_call",
    action="store_true",
    help="print the call to blender",
)
argparser.add_argument(
    "--print-blender-stdout",
    dest="print_blender_stdout",
    action="store_true",
    help="print blenders stdout",
)
argparser.add_argument(
    "--verbose", dest="verbose", action="store_true", help="print verbose outpout"
)

subparsers = argparser.add_subparsers()

parser_build = subparsers.add_parser("build", help="build project")
parser_build.add_argument("--blend", help="path to main blend file")
parser_build.add_argument("--exporter", help="exporter to use", type=ascii)
parser_build.set_defaults(func=cli_build)

parser_publish = subparsers.add_parser("publish", help="publish project")
parser_publish.add_argument("--blend", help="path to main blend file")
parser_publish.add_argument("--exporter", help="exporter to use", type=ascii)
parser_publish.set_defaults(func=cli_publish)

parser_clean = subparsers.add_parser("clean", help="clean project")
parser_clean.add_argument("--blend", help="path to main blend file")
parser_clean.set_defaults(func=cli_clean)

parser_play = subparsers.add_parser('play', help='play project')
parser_play.add_argument('--blend', help='path to main blend file')
parser_play.add_argument('--runtime', default='krom', choices=['krom','browser'], help='runtime to use')
parser_play.add_argument('--camera', default='Scene', help='viewport camera')
parser_play.add_argument('--scene', help='scene to launch')
parser_play.add_argument('--renderpath', help='default render path')
parser_play.set_defaults(func=cli_play)

parser_exporters = subparsers.add_parser("exporters", help="manage exporters")
parser_exporters.add_argument("--blend", help="path to main blend file")
parser_exporters.add_argument(
    "command", choices=["list"], default="list", help="path to main blend file"
)
parser_exporters.set_defaults(func=cli_exporters)
# exporters_subparsers = parser_exporters.add_subparsers()
# parser_exporters_list = exporters_subparsers.add_parser('list')
# parser_exporters_list.set_defaults(func=cli_exporters_list)
# parser_exporters_list = parser_exporters.add_subparsers()
# parser_exporters_list.add_argument("list")
# parser_exporters.add_argument("command", choices=["add","remove","list"])

parser_renderpath = subparsers.add_parser("renderpath", help="manage renderpaths")
parser_renderpath.add_argument("--blend", help="path to blend file")
parser_renderpath.set_defaults(func=cli_renderpath)
# parser_traits = subparsers.add_parser('traits', help='manage traits')
# parser_traits.add_argument('--blend', help='path to main blend file')
# parser_traits.set_defaults(func=traits)
# trait_subparsers = parser_traits.add_subparsers(help='sub-command help')
# parser_traits_list = trait_subparsers.add_parser('list')
# parser_traits_list.set_defaults(func=cli_traits)

parser_khamake = subparsers.add_parser("kha", help="execute khamake")
parser_khamake.set_defaults(func=cli_kha)

parser_sdk = subparsers.add_parser("sdk", help="manage armsdk")
# parser_sdk.add_argument('path', help='path to armsdk')
parser_sdk.set_defaults(func=cli_sdk)

if len(sys.argv) == 1:
    argparser.print_help()
    sys.exit(1)

args = argparser.parse_args()
verbose = args.verbose
print_blender_stdout = args.print_blender_stdout
print_script_call = args.print_script_call
args.func(args)
