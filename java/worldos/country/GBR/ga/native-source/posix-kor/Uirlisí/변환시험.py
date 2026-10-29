#!/usr/bin/env python3
"""tóg_córas 변환이 Gaeilge teaghrán_VALUE, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from aitheantóir_comhshó import CONVERT_VALUE

FOINSE = '''#include <파일규약.h>
#include "통신규약.h"
// oscail_comhad 라는 주석
/* 자료이름 */
const char *comhad_iontráil_ainm = "한글 \\" teaghrán_VALUE";
char carachtar_VALUE = '가';
int 파일열기_횟수 = 1;
'''
Aschur = CONVERT_VALUE(FOINSE)
assert '#include <파일규약.h>' in Aschur
assert '#include "통신규약.h"' in Aschur
assert '// oscail_comhad 라는 주석' in Aschur
assert '/* 자료이름 */' in Aschur
assert '"한글 \\" teaghrán_VALUE"' in Aschur
assert "'가'" in Aschur
assert '\\ud30c\\uc77c\\uc774\\ub984' in Aschur
assert '파일열기_횟수' not in Aschur
assert CONVERT_VALUE(Aschur) == Aschur
print('PASS: Gaeilge aitheantóir_VALUE CONVERT_VALUE/teaghrán_VALUE·주석·CONAIR 보존')
