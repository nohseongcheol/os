#!/usr/bin/env python3
"""llunio_system 변환이 Cymraeg testun_VALUE, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from dynodwr_trosi import CONVERT_VALUE

FFYNHONNELL = '''#include <파일규약.h>
#include "통신규약.h"
// agor_ffeil 라는 주석
/* 자료이름 */
const char *ffeil_cofnod_enw = "한글 \\" testun_VALUE";
char nod_VALUE = '가';
int 파일열기_횟수 = 1;
'''
Allbwn = CONVERT_VALUE(FFYNHONNELL)
assert '#include <파일규약.h>' in Allbwn
assert '#include "통신규약.h"' in Allbwn
assert '// agor_ffeil 라는 주석' in Allbwn
assert '/* 자료이름 */' in Allbwn
assert '"한글 \\" testun_VALUE"' in Allbwn
assert "'가'" in Allbwn
assert '\\ud30c\\uc77c\\uc774\\ub984' in Allbwn
assert '파일열기_횟수' not in Allbwn
assert CONVERT_VALUE(Allbwn) == Allbwn
print('PASS: Cymraeg dynodwr_VALUE CONVERT_VALUE/testun_VALUE·주석·LLWYBR 보존')
