#!/usr/bin/env python3
"""tafde_yuɓɓo 변환이 한국어 ɓoggol_njaru, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from 식별자변환 import 변환

sewnde = '''#include <파일규약.h>
#include "통신규약.h"
// udditde_fiilde 라는 주석
/* 자료이름 */
const char *fiilde_naatnugol_innde = "한글 \\" ɓoggol_njaru";
char alkulal_njaru = '가';
int 파일열기_횟수 = 1;
'''
출력 = 변환(sewnde)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// udditde_fiilde 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" ɓoggol_njaru"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert 변환(출력) == 출력
print('PASS: 한국어 식별자 변환/ɓoggol_njaru·주석·laawol 보존')
