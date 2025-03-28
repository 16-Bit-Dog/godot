#!/usr/bin/env bash
scons platform=linuxbsd target=editor dev_build=yes slang=yes mesa_libs="../godot-nir-static" use_llvm=yes
