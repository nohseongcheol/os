#!/usr/bin/env python3
"""compilar_sistema 변환이 Galego cadea_VALOR, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from 식별자변환 import CONVERTER_VALOR

FONTE = '''#include <파일규약.h>
#include "통신규약.h"
// abrir_Ficheiro 라는 주석
/* 자료이름 */
const char *Ficheiro_introdución_nome = "한글 \\" cadea_VALOR";
char carácter_VALOR = '가';
int 파일열기_횟수 = 1;
'''
Saída = CONVERTER_VALOR(FONTE)
assert '#include <파일규약.h>' in Saída
assert '#include "통신규약.h"' in Saída
assert '// abrir_Ficheiro 라는 주석' in Saída
assert '/* 자료이름 */' in Saída
assert '"한글 \\" cadea_VALOR"' in Saída
assert "'가'" in Saída
assert '\\ud30c\\uc77c\\uc774\\ub984' in Saída
assert '파일열기_횟수' not in Saída
assert CONVERTER_VALOR(Saída) == Saída
print('PASS: Galego 식별자 CONVERTER_VALOR/cadea_VALOR·주석·CAMIÑO 보존')
