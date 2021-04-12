## Instructions

```bash
# Clone this repository
$ git clone <https://github.com/mateusosmarin/tcc.git
$ cd tcc
```

## Linux

```bash

# Install the required dependencies
$ pip install -r requirements.txt

# Now run
$ python main.py
```

## Windows

For Windows, you must install MSYS2 <https://www.msys2.org>. Follow their instructions then install the needed packages.

```bash
# On MSYS shell
$ pacman -S --needed base-devel mingw-w64-x86_64-toolchain
$ pacman -S mingw-w64-x86_64-gtk3
$ pacman -S mingw-w64-x86_64-python-gobject
$ pacman -S mingw-w64-x86_64-python-numpy
$ pacman -S mingw-w64-x86_64-python-matplotlib
$ pacman -S mingw-w64-x86_64-python-scipy

# Run the program on MinGW-64 shell
$ python main.py
```
