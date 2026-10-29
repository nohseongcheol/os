#!/usr/bin/env python3
"""sanali_qarasaujaq 변환이 한국어 qimiaq_atuutilik, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from 식별자변환 import 변환

pivviujuq = '''#include <파일규약.h>
#include "통신규약.h"
// matuirli_ini 라는 주석
/* 자료이름 */
const char *ini_Iliniku_atiq = "한글 \\" qimiaq_atuutilik";
char immikkuuqtuq_atuutilik = '가';
int 파일열기_횟수 = 1;
'''
출력 = 변환(pivviujuq)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// matuirli_ini 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" qimiaq_atuutilik"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert 변환(출력) == 출력
print('PASS: 한국어 식별자 변환/qimiaq_atuutilik·주석·aqqut 보존')
