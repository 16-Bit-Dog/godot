#ifndef SHADER_LANGUAGE_TYPE_H
#define SHADER_LANGUAGE_TYPE_H

#include "core/io/resource.h"

enum ShaderLanguageType {
	SHADER_LANGUAGE_TYPE_GDSHADER,
	SHADER_LANGUAGE_TYPE_SLANG,
	SHADER_LANGUAGE_TYPE_MAX
};

static const ShaderLanguageType ShaderLanguageType_slang = SHADER_LANGUAGE_TYPE_SLANG;

#endif
