#!/usr/bin/env python3
"""generare_sistem 변환이 Română șir_VALUE, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from identificator_conversie import CONVERT_VALUE

SURSĂ = '''#include <파일규약.h>
#include "통신규약.h"
// crea_Fișier 라는 주석
/* 자료이름 */
const char *Fișier_intrare_nume = "한글 \\" șir_VALUE";
char caracter_VALUE = '가';
int 파일열기_횟수 = 1;
'''
Rezultat = CONVERT_VALUE(SURSĂ)
assert '#include <파일규약.h>' in Rezultat
assert '#include "통신규약.h"' in Rezultat
assert '// crea_Fișier 라는 주석' in Rezultat
assert '/* 자료이름 */' in Rezultat
assert '"한글 \\" șir_VALUE"' in Rezultat
assert "'가'" in Rezultat
assert '\\ud30c\\uc77c\\uc774\\ub984' in Rezultat
assert '파일열기_횟수' not in Rezultat
assert CONVERT_VALUE(Rezultat) == Rezultat
print('PASS: Română identificator_VALUE CONVERT_VALUE/șir_VALUE·주석·Cale 보존')
