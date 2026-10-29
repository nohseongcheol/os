#!/usr/bin/env python3
"""nashr_tizim 변환이 한국어 satr_VALUE, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from identifikator_aylantirish import CONVERT_VALUE

manba = '''#include <파일규약.h>
#include "통신규약.h"
// ochmoq_fayl 라는 주석
/* 자료이름 */
const char *fayl_kiritish_nom = "한글 \\" satr_VALUE";
char belgi_VALUE = '가';
int 파일열기_횟수 = 1;
'''
출력 = CONVERT_VALUE(manba)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// ochmoq_fayl 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" satr_VALUE"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert CONVERT_VALUE(출력) == 출력
print('PASS: 한국어 identifikator_VALUE CONVERT_VALUE/satr_VALUE·주석·yo_l 보존')
