# [Armory3D](https://armory3d.org/) command line interface

## Install

Clone this repo:
```sh
git clone https://github.com/tong/armcli.git
```

Create a symlink somewhere in your PATH to `armcli/armory.py`:
```sh
ln -s <path-to-the-clone-of-this-repo>/armory.py $HOME/.local/bin/armory
```


## Usage
```sh
armory --help

usage: armory [-h] [--verbose] {build,publish,clean,sdk} ...

positional arguments:
  {build,publish,clean,sdk}
    build               build project
    publish             publish project
    clean               clean project
    sdk                 manage armsdk

options:
  -h, --help            show this help message and exit
  --verbose             print verbose outpout
```
