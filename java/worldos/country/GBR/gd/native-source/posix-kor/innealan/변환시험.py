#!/usr/bin/env python3
"""tog_siostam 변환이 한국어 sreang_VALUE, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from aithnichear_iompachadh import CONVERT_VALUE

tùs = '''#include <파일규약.h>
#include "통신규약.h"
// fosgail_faidhle 라는 주석
/* 자료이름 */
const char *faidhle_cur_a_steach_ainm = "한글 \\" sreang_VALUE";
char caractar_VALUE = '가';
int 파일열기_횟수 = 1;
'''
출력 = CONVERT_VALUE(tùs)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// fosgail_faidhle 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" sreang_VALUE"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert CONVERT_VALUE(출력) == 출력
print('PASS: 한국어 aithnichear_VALUE CONVERT_VALUE/sreang_VALUE·주석·Slighe 보존')
