#!/usr/bin/env python3
"""verzija_sistem 변환이 한국어 string_VALUE, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from identifikator_konverzija import CONVERT_VALUE

IZVOR = '''#include <파일규약.h>
#include "통신규약.h"
// kreirati_fajl 라는 주석
/* 자료이름 */
const char *fajl_unos_naziv = "한글 \\" string_VALUE";
char znak_VALUE = '가';
int 파일열기_횟수 = 1;
'''
Ispis = CONVERT_VALUE(IZVOR)
assert '#include <파일규약.h>' in Ispis
assert '#include "통신규약.h"' in Ispis
assert '// kreirati_fajl 라는 주석' in Ispis
assert '/* 자료이름 */' in Ispis
assert '"한글 \\" string_VALUE"' in Ispis
assert "'가'" in Ispis
assert '\\ud30c\\uc77c\\uc774\\ub984' in Ispis
assert '파일열기_횟수' not in Ispis
assert CONVERT_VALUE(Ispis) == Ispis
print('PASS: 한국어 identifikator_VALUE CONVERT_VALUE/string_VALUE·주석·Putanja 보존')
