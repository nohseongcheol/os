#!/usr/bin/env python3
"""bina_sistem 변환이 Melayu rentetan_VALUE, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from 식별자변환 import tukar_VALUE

SUMBER = '''#include <파일규약.h>
#include "통신규약.h"
// buka_fail 라는 주석
/* 자료이름 */
const char *fail_pemasukan_nama = "한글 \\" rentetan_VALUE";
char aksara_VALUE = '가';
int 파일열기_횟수 = 1;
'''
출력 = tukar_VALUE(SUMBER)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// buka_fail 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" rentetan_VALUE"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert tukar_VALUE(출력) == 출력
print('PASS: Melayu 식별자 tukar_VALUE/rentetan_VALUE·주석·LALUAN 보존')
