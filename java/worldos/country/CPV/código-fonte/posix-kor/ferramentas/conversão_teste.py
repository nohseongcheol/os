#!/usr/bin/env python3
"""construir 변환이 Português cadeia_VALOR, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from identificador_conversão import CONVERTER_VALOR

códigoFonte = '''#include <Arquivo_ABI.h>
#include "rede_ABI.h"
// abrir_Arquivo 라는 주석
/* 자료이름 */
const char *Arquivo_entrada_nome = "한글 \\" cadeia_VALOR";
char caractere_VALOR = '가';
int 파일열기_횟수 = 1;
'''
saídaTexto = CONVERTER_VALOR(códigoFonte)
assert '#include <Arquivo_ABI.h>' in saídaTexto
assert '#include "rede_ABI.h"' in saídaTexto
assert '// abrir_Arquivo 라는 주석' in saídaTexto
assert '/* 자료이름 */' in saídaTexto
assert '"한글 \\" cadeia_VALOR"' in saídaTexto
assert "'가'" in saídaTexto
assert '\\ud30c\\uc77c\\uc774\\ub984' in saídaTexto
assert '파일열기_횟수' not in saídaTexto
assert CONVERTER_VALOR(saídaTexto) == saídaTexto
print('PASS: Português identificador_VALOR CONVERTER_VALOR/cadeia_VALOR·주석·caminho 보존')
