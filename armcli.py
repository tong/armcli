#!/usr/bin/python

""" Armory CLI """

import argparse
import os
import subprocess
import sys
from subprocess import PIPE, STDOUT


VERBOSE = False
PRINT_BLENDER_STDOUT = False
BLENDER_EXECUTEABLE = "blender"

armsdk_path = os.getenv("ARMSDK")
if armsdk_path is None:
    abort("armsdk not found, set ARMSDK environment variable")

if os.path.islink(sys.argv[0]):
    clidir = os.path.dirname(os.readlink(sys.argv[0]))
else:
    clidir = os.path.dirname(sys.argv[0])
script_dir = f"{clidir}/blender"
if not os.path.exists(script_dir) or not os.path.isdir(script_dir):
    print("armcli/blender/ not found", file=sys.stderr)
    sys.exit(1)


def abort(code=1, msg: str = None):
    if msg is not None:
        print(msg, file=sys.stderr)
    sys.exit(code)


def find_main_blend_file(blend: str = None):
    if blend is None:
        cwd = os.getcwd()
        blend = f"{cwd}/{os.path.basename(cwd)}.blend"
        if not os.path.exists(blend):
            if os.path.exists("main.blend"):
                return "main.blend"
            else:
                for e in os.scandir("."):
                    if e.name.endswith('.blend') and e.is_file():
                        return e.name
        return blend
    return blend


def execute_blender(params):
    cmd = [BLENDER_EXECUTEABLE, "--background"]
    cmd.extend(params)
    if VERBOSE:
        print(" ".join(cmd))
    if PRINT_BLENDER_STDOUT:
        proc = subprocess.Popen(cmd, stderr=PIPE)
    else:
        proc = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    while proc.poll() is None:
        out = proc.stderr.readline().decode("utf-8")
        if len(out) > 0:
            print(out, end="")
        err = proc.stderr.readline().decode("utf-8")
        if len(err) > 0:
            print(err, end="")
    sys.exit(proc.returncode)


def execute_blender_script(script: str, blend: str=None, params=None):
    cmd = []
    if blend is not None:
        if not os.path.exists(blend):
            abort(f'{blend} not found')
        cmd.append(blend)
    cmd.extend(["--python", f"{script_dir}/{script}.py"])
    if params is not None and len(params) > 0:
        cmd.append("--")
        cmd.extend(params)
    execute_blender(cmd)


def execute_blender_expr(expr: str, blend: str=None):
    cmd = []
    if blend is not None:
        cmd.append(blend)
    cmd.extend(["--python-expr", "'" + expr + "'"])
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
    execute_blender_script("clean", find_main_blend_file(_args.blend))


def cli_play(_args):
    #blend = find_main_blend_file(_args.blend)
    if _args.camera is None:
        _args.camera = ""
    if _args.scene is None:
        _args.scene = ""
    if _args.renderpath is None:
        _args.renderpath = ""
    params = [_args.runtime, _args.camera, _args.scene, _args.renderpath]
    execute_blender_script("play", find_main_blend_file(_args.blend), params)


def cli_exporters(_args):
    execute_blender_script(f"exporters_{_args.command}", find_main_blend_file(_args.blend))


def cli_renderpath(_args):
    execute_blender_script("renderpath_list", find_main_blend_file(_args.blend))


# def cli_renderpath_list(_args):
#     execute_blender_script("renderpath_list", find_main_blend_file(_args.blend))


def cli_traits(_args):
    blend = find_main_blend_file(_args.blend)
    execute_blender_script("traits", blend)


# def cli_compile(_args):
#     print(_args)
# if _args.build is not None:
#     build_dir = f"build_{_args.build}"
#     if not os.path.exists(build_dir):
#         abort(f"{build_dir} not found")
#     platforms = []
#     build_debug_dir = f"{build_dir}/debug"
#     if build_debug_dir:
#         for file in os.listdir(build_debug_dir):
#             if file.startswith("project-") and file.endswith(".hxml"):
#                 platform = file.split(".")[0][8:]
#                 path = f"{build_debug_dir}/{file}"
#                 print(platform)

# if os.path.isfile(path) and
# print(f)
# print(build_dir)
# subprocess.run([""])
# output_directories = []
# for d in os.listdir('.'):
#     if d.startswith('build_') and os.path.isdir(d):
#         output_directories.append(d)
# print(" ".join(output_directories))


def cli_versioninfo(_args):
    execute_blender_script("versioninfo")


def cli_sdk(_args):
    execute_blender_script("sdk")


def cli_kha(_args):
    cmd = ["node", f"{armsdk_path}/Kha/make.js", "--shaderversion", "330"]
    proc = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    while proc.poll() is None:
        print(proc.stdout.readline().decode("utf-8"), end="", file=sys.stdout)
    sys.exit(proc.returncode)


# def cli_launch(_args):
#     for path in os.listdir("."):
#         if path.startswith("build_") and os.path.isdir(path):
#             debug_dir = f"{path}/debug"
#             if os.path.exists(debug_dir) and os.path.isdir(debug_dir):
#                 krom_dir = f"{debug_dir}/krom"
#                 if os.path.exists(krom_dir):
#                     print(krom_dir)
# for d in os.listdir(d):
#    print(d)
# subprocess.run([''])

argparser = argparse.ArgumentParser(prog="armory")
argparser.add_argument(
    "--blender-stdout",
    dest="print_blender_stdout",
    action="store_true",
    help="print blenders stdout",
    default=False
)
argparser.add_argument("--blender-executeable", help="path to blender executeable")
argparser.add_argument("--blend", help="path to main blend file")
argparser.add_argument("--verbose", dest="verbose", action="store_true", help="print verbose outpout")

subparsers = argparser.add_subparsers()

parser_build = subparsers.add_parser("build", help="build project")
parser_build.add_argument("--blend", help="path to main blend file")
parser_build.add_argument("--exporter", help="exporter to use", type=ascii)
parser_build.set_defaults(func=cli_build)

parser_publish = subparsers.add_parser("publish", help="publish project")
parser_publish.add_argument("--blend", help="path to main blend file")
parser_publish.add_argument("--exporter", help="exporter to use")
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
#parser_exporters.add_argument("command", choices=["list"], default="list", help="list exporters")
parser_exporters.set_defaults(func=cli_exporters)
# exporters_subparsers = parser_exporters.add_subparsers()
# parser_exporters_list = exporters_subparsers.add_parser('list')
# parser_exporters_list.set_defaults(func=cli_exporters_list)
# parser_exporters_list = parser_exporters.add_subparsers()
# parser_exporters_list.add_argument("list")
# parser_exporters.add_argument("command", choices=["add","remove","list"])

parser_renderpath = subparsers.add_parser("renderpath", help="manage renderpaths")
parser_renderpath.add_argument("--blend", help="path to blend file")
# group_renderpath = parser_renderpath.add_mutually_exclusive_group()
parser_renderpath.add_argument(
    "action",
    choices=["list", "select", "add"],
    default="list",
    help="perform renderpath action",
)
# group_renderpath.add_argument('select', action='store_true')
parser_renderpath.set_defaults(func=cli_renderpath)

# parser_traits = subparsers.add_parser('traits', help='manage traits')
# parser_traits.add_argument('--blend', help='path to main blend file')
# parser_traits.set_defaults(func=traits)
# trait_subparsers = parser_traits.add_subparsers(help='sub-command help')
# parser_traits_list = trait_subparsers.add_parser('list')
# parser_traits_list.set_defaults(func=cli_traits)

# parser_compile = subparsers.add_parser("compile", help="compile project")
# parser_compile.add_argument("--build", help="build to compile")
# parser_compile.add_argument("--platform", help="platform to compile")
# parser_compile.set_defaults(func=cli_compile)

# parser_khamake = subparsers.add_parser("kha", help="execute khamake")
# parser_khamake.set_defaults(func=cli_kha)

# parser_launch = subparsers.add_parser("launch", help="launch application")
# parser_launch.set_defaults(func=cli_launch)

parser_test = subparsers.add_parser("versioninfo", help="print version info")
parser_test.set_defaults(func=cli_versioninfo)

parser_sdk = subparsers.add_parser("sdk", help="manage armsdk")
parser_sdk.set_defaults(func=cli_sdk)

if len(sys.argv) == 1:
    argparser.print_help()
    sys.exit(1)

args = argparser.parse_args()
VERBOSE = args.verbose
PRINT_BLENDER_STDOUT = args.print_blender_stdout
if args.blender_executeable != None:
    BLENDER_EXECUTEABLE = args.blender_executeable
args.func(args)

