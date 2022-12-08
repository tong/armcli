#!/usr/bin/python

""" armory cli """

import argparse
import os
import subprocess
import sys
from subprocess import PIPE

VERBOSE = False
PRINT_BLENDER_STDOUT = False

armsdk_path = os.getenv("ARMSDK")
if armsdk_path is None:
    print("armsdk not found, set ARMSDK environment variable")
    sys.exit(1)

if os.path.islink(sys.argv[0]):
    clidir = os.path.dirname(os.readlink(sys.argv[0]))
else:
    clidir = os.path.dirname(sys.argv[0])
script_dir = f"{clidir}/blender"
if not os.path.exists(script_dir) or not os.path.isdir(script_dir):
    print("armcli/blender/ not found", file=sys.stderr)
    sys.exit(1)


def find_main_blend_file(blend: str = None):
    if blend is None:
        cwd = os.getcwd()
        blend = f"{cwd}/{os.path.basename(dir)}.blend"
        if not os.path.exists(blend):
            print("main blend file not found", file=sys.stderr)
            sys.exit(1)
        return blend
    if not os.path.exists(blend):
        print('main blend file not found', file=sys.stderr)
        sys.exit(1)
    return blend


def execute_blender(params):
    cmd = ["blender", "--background"]
    cmd.extend(params)
    if VERBOSE:
        print(" ".join(cmd))
    if PRINT_BLENDER_STDOUT:
        proc = subprocess.Popen(cmd, stderr=PIPE)
    else:
        proc = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    while proc.poll() is None:
        print(proc.stderr.readline().decode("utf-8"), end="", file=sys.stdout)
    sys.exit(proc.returncode)


def execute_blender_script(script: str, blend: str = None, params=None):
    cmd = []
    if blend is not None:
        cmd.append(blend)
    cmd.extend(["--python", f"{script_dir}/{script}.py"])
    if params is not None and len(params) > 0:
        cmd.append("--")
        cmd.extend(params)
    execute_blender(cmd)


def execute_blender_expr(expr: str, blend: str = None):
    cmd = []
    if blend is not None:
        cmd.append(blend)
    cmd.extend(["--python-expr", f"'{expr}'"])
    execute_blender(cmd)


def cli_build(_args):
    execute_blender_script("build", find_main_blend_file(_args.blend))


def cli_publish(_args):
    blend = find_main_blend_file(_args.blend)
    params = []
    if _args.exporter is not None:
        params.append(_args.exporter)
    execute_blender_script("publish", blend, params)


def cli_clean(_args):
    blend = find_main_blend_file(_args.blend)
    execute_blender_script("clean", blend)


def cli_play(_args):
    blend = find_main_blend_file(_args.blend)
    if _args.camera is None:
        _args.camera = ""
    if _args.scene is None:
        _args.scene = ""
    if _args.renderpath is None:
        _args.renderpath = ""
    params = [_args.runtime, _args.camera, _args.scene, _args.renderpath]
    execute_blender_script("play", blend, params)


def cli_exporters(_args):
    blend = find_main_blend_file(_args.blend)
    execute_blender_script(f"exporters_{_args.command}", blend)


def cli_renderpath(_args):
    execute_blender_script("renderpath_list", find_main_blend_file(_args.blend))


def cli_traits(_args):
    blend = find_main_blend_file(_args.blend)
    execute_blender_script("traits", blend)


def cli_kha(_args):
    cmd = ["node", f"{armsdk_path}/Kha/make.js", "--shaderversion", "330"]
    proc = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    while proc.poll() is None:
        print(proc.stdout.readline().decode("utf-8"), end="", file=sys.stdout)
    sys.exit(proc.returncode)


def cli_sdk(_args):
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

parser_play = subparsers.add_parser("play", help="play project")
parser_play.add_argument("--blend", help="path to main blend file")
parser_play.add_argument(
    "--runtime", default="krom", choices=["krom", "browser"], help="runtime to use"
)
parser_play.add_argument("--camera", default="Scene", help="viewport camera")
parser_play.add_argument("--scene", help="scene to launch")
parser_play.add_argument("--renderpath", help="default render path")
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
VERBOSE = args.verbose
print_blender_stdout = args.print_blender_stdout
#print_script_call = args.print_script_call
args.func(args)
