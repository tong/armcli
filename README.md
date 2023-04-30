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
usage: armory [-h] [--blender-stdout] [--blender-executeable BLENDER_EXECUTEABLE] [--blend BLEND] [--sdk ARMSDK] [--verbose]
              {build,publish,clean,play,exporters,renderpath,versioninfo,sdk} ...

positional arguments:
  {build,publish,clean,play,exporters,renderpath,versioninfo,sdk}
    build               build project
    publish             publish project
    clean               clean project
    play                play project
    exporters           manage exporters
    renderpath          manage renderpaths
    versioninfo         print version info
    sdk                 manage armsdk

options:
  -h, --help            show this help message and exit
  --blender-stdout      print blenders stdout
  --blender-executeable BLENDER_EXECUTEABLE
                        path to blender executeable
  --blend BLEND         path to main blend file
  --sdk ARMSDK          path to armsdk
  --verbose             print verbose outpout
```
