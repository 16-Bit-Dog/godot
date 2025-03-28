#!/usr/bin/env bash
scons.exe platform=windows vsproj=yes target=editor dev_build=yes slang=yes mesa_libs="./../godot-nir-static"
