#!/usr/bin/env python3
"""bou_stelsel 변환이 한국어 string_VALUE, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from waarde_konversasie import CONVERT_VALUE

Bron = '''#include <파일규약.h>
#include "통신규약.h"
// skep_lêer 라는 주석
/* 자료이름 */
const char *lêer_inskrywing_naam = "한글 \\" string_VALUE";
char karakter_VALUE = '가';
int 파일열기_횟수 = 1;
'''
Afvoer = CONVERT_VALUE(Bron)
assert '#include <파일규약.h>' in Afvoer
assert '#include "통신규약.h"' in Afvoer
assert '// skep_lêer 라는 주석' in Afvoer
assert '/* 자료이름 */' in Afvoer
assert '"한글 \\" string_VALUE"' in Afvoer
assert "'가'" in Afvoer
assert '\\ud30c\\uc77c\\uc774\\ub984' in Afvoer
assert '파일열기_횟수' not in Afvoer
assert CONVERT_VALUE(Afvoer) == Afvoer
print('PASS: 한국어 waarde_VALUE CONVERT_VALUE/string_VALUE·주석·Pad 보존')
