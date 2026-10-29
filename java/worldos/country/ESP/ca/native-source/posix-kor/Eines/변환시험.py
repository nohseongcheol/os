#!/usr/bin/env python3
"""generar_sistema 변환이 Català cadena_VALOR, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from identificador_conversió import CONVERT_VALOR

FONT = '''#include <파일규약.h>
#include "통신규약.h"
// crear_arxiu 라는 주석
/* 자료이름 */
const char *arxiu_introducció_nom = "한글 \\" cadena_VALOR";
char caràcter_VALOR = '가';
int 파일열기_횟수 = 1;
'''
Sortida = CONVERT_VALOR(FONT)
assert '#include <파일규약.h>' in Sortida
assert '#include "통신규약.h"' in Sortida
assert '// crear_arxiu 라는 주석' in Sortida
assert '/* 자료이름 */' in Sortida
assert '"한글 \\" cadena_VALOR"' in Sortida
assert "'가'" in Sortida
assert '\\ud30c\\uc77c\\uc774\\ub984' in Sortida
assert '파일열기_횟수' not in Sortida
assert CONVERT_VALOR(Sortida) == Sortida
print('PASS: Català identificador_VALOR CONVERT_VALOR/cadena_VALOR·주석·Camí 보존')
