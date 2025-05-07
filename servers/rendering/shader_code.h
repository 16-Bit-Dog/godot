#ifndef SHADER_CODE_H
#define SHADER_CODE_H

#include "core/string/ustring.h"
#include "servers/rendering/shader_language_type.h"

struct SlangASTData
{

};

struct ShaderCode {

private:
	String code = {}; // code as string
	SlangASTData ast = {}; // ONLY Slang --> AST of code
	const ShaderLanguageType &language_type;

public:

	ShaderCode(ShaderLanguageType &p_type) :
			language_type(p_type)
	{
	}
	ShaderCode(const ShaderLanguageType &p_type) :
			language_type(p_type) {
	}

	bool is_empty() {
		return code.is_empty();
	}

	ShaderLanguageType getType() {
		return language_type;
	}

	String& getCode() {
		return code;
	}

	SlangASTData& getAST() {
		return ast;
	}

	void reset() {
		code = String();
		ast = SlangASTData();
	}
};

#endif
