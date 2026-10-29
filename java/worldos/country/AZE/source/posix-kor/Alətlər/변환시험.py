#!/usr/bin/env python3
"""qurmaq_sistem 변환이 한국어 sətir_VALUE, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from identifikator_çevirmə import CONVERT_VALUE

QAYNAQ = '''#include <파일규약.h>
#include "통신규약.h"
// açmaq_fayl 라는 주석
/* 자료이름 */
const char *fayl_daxiletmə_ad = "한글 \\" sətir_VALUE";
char simvol_VALUE_068c2631 = '가';
int 파일열기_횟수 = 1;
'''
출력 = CONVERT_VALUE(QAYNAQ)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// açmaq_fayl 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" sətir_VALUE"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert CONVERT_VALUE(출력) == 출력
print('PASS: 한국어 identifikator_VALUE CONVERT_VALUE/sətir_VALUE·주석·Cığır 보존')
