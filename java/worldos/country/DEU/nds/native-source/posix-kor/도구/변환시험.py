#!/usr/bin/env python3
"""빌드 변환이 한국어 문자열, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from 식별자변환 import 변환

Born = '''#include <파일규약.h>
#include "통신규약.h"
// 파일열기 라는 주석
/* 자료이름 */
const char *파일이름 = "한글 \\" 문자열";
char 글자 = '가';
int 파일열기_횟수 = 1;
'''
Utgaav = 변환(Born)
assert '#include <파일규약.h>' in Utgaav
assert '#include "통신규약.h"' in Utgaav
assert '// 파일열기 라는 주석' in Utgaav
assert '/* 자료이름 */' in Utgaav
assert '"한글 \\" 문자열"' in Utgaav
assert "'가'" in Utgaav
assert '\\ud30c\\uc77c\\uc774\\ub984' in Utgaav
assert '파일열기_횟수' not in Utgaav
assert 변환(Utgaav) == Utgaav
print('PASS: 한국어 식별자 변환/문자열·주석·PADD 보존')
