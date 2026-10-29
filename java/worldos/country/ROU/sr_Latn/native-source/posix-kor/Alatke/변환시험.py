#!/usr/bin/env python3
"""verzija_sistem 변환이 한국어 niska_VALUE, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from identifikator_konverzija import CONVERT_VALUE

izvor = '''#include <파일규약.h>
#include "통신규약.h"
// otvoren_Datoteka 라는 주석
/* 자료이름 */
const char *Datoteka_stavka_ime = "한글 \\" niska_VALUE";
char znak_VALUE = '가';
int 파일열기_횟수 = 1;
'''
출력 = CONVERT_VALUE(izvor)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// otvoren_Datoteka 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" niska_VALUE"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert CONVERT_VALUE(출력) == 출력
print('PASS: 한국어 identifikator_VALUE CONVERT_VALUE/niska_VALUE·주석·putanja 보존')
