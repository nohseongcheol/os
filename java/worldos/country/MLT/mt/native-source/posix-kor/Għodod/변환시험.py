#!/usr/bin/env python3
"""bena_sistema 변환이 Malti string_VALUE, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from identifikatur_qlib import CONVERT_VALUE

sors = '''#include <파일규약.h>
#include "통신규약.h"
// fetaħ_fajl 라는 주석
/* 자료이름 */
const char *fajl_entrata_isem = "한글 \\" string_VALUE";
char karattru_VALUE = '가';
int 파일열기_횟수 = 1;
'''
출력 = CONVERT_VALUE(sors)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// fetaħ_fajl 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" string_VALUE"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert CONVERT_VALUE(출력) == 출력
print('PASS: Malti identifikatur_VALUE CONVERT_VALUE/string_VALUE·주석·mogħdija 보존')
