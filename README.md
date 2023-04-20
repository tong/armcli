# [Armory3D](https://armory3d.org/) command line interface

## Install

Clone this repo:
```sh
git clone https://github.com/tong/armcli.git
```

Create a symlink somewhere in your PATH to `armcli/armory.py`:
```sh
ln -s <path-to-the-clone-of-this-repo>/armcli.py $HOME/.local/bin/armory
```


## Usage
```sh
armory --help

usage: armory [-h] [--print-script-call] [--print-blender-stdout] [--verbose] {build,publish,clean,play,exporters,renderpath,kha,sdk} ...

positional arguments:
  {build,publish,clean,play,exporters,renderpath,kha,sdk}
    build               build project
    publish             publish project
    clean               clean project
    play                play project
    exporters           manage exporters
    renderpath          manage renderpaths
    kha                 execute khamake
    sdk                 manage armsdk

options:
  -h, --help            show this help message and exit
  --print-script-call   print the call to blender
  --print-blender-stdout
                        print blenders stdout
  --verbose             print verbose outpout
```
