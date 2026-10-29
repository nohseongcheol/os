#!/usr/bin/env python3
"""zostava_systém 변환이 Slovenský reťazec_VALUE, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from identifikátor_konverzia import CONVERT_VALUE

ZDROJ = '''#include <파일규약.h>
#include "통신규약.h"
// otvoriť_Súbor 라는 주석
/* 자료이름 */
const char *Súbor_položka_názov = "한글 \\" reťazec_VALUE";
char znak_VALUE = '가';
int 파일열기_횟수 = 1;
'''
Výstup = CONVERT_VALUE(ZDROJ)
assert '#include <파일규약.h>' in Výstup
assert '#include "통신규약.h"' in Výstup
assert '// otvoriť_Súbor 라는 주석' in Výstup
assert '/* 자료이름 */' in Výstup
assert '"한글 \\" reťazec_VALUE"' in Výstup
assert "'가'" in Výstup
assert '\\ud30c\\uc77c\\uc774\\ub984' in Výstup
assert '파일열기_횟수' not in Výstup
assert CONVERT_VALUE(Výstup) == Výstup
print('PASS: Slovenský identifikátor_VALUE CONVERT_VALUE/reťazec_VALUE·주석·Cesta 보존')
