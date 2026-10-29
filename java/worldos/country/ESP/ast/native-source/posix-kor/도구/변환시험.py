#!/usr/bin/env python3
"""빌드 변환이 한국어 문자열, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from 식별자변환 import 변환

FONTE = '''#include <파일규약.h>
#include "통신규약.h"
// 파일열기 라는 주석
/* 자료이름 */
const char *파일이름 = "한글 \\" 문자열";
char 글자 = '가';
int 파일열기_횟수 = 1;
'''
Salida = 변환(FONTE)
assert '#include <파일규약.h>' in Salida
assert '#include "통신규약.h"' in Salida
assert '// 파일열기 라는 주석' in Salida
assert '/* 자료이름 */' in Salida
assert '"한글 \\" 문자열"' in Salida
assert "'가'" in Salida
assert '\\ud30c\\uc77c\\uc774\\ub984' in Salida
assert '파일열기_횟수' not in Salida
assert 변환(Salida) == Salida
print('PASS: 한국어 식별자 변환/문자열·주석·Camín 보존')
