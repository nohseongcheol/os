#!/usr/bin/env python3
"""빌드 변환이 한국어 문자열, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from 식별자변환 import 변환

Fonte = '''#include <파일규약.h>
#include "통신규약.h"
// 파일열기 라는 주석
/* 자료이름 */
const char *파일이름 = "한글 \\" 문자열";
char 글자 = '가';
int 파일열기_횟수 = 1;
'''
Exito = 변환(Fonte)
assert '#include <파일규약.h>' in Exito
assert '#include "통신규약.h"' in Exito
assert '// 파일열기 라는 주석' in Exito
assert '/* 자료이름 */' in Exito
assert '"한글 \\" 문자열"' in Exito
assert "'가'" in Exito
assert '\\ud30c\\uc77c\\uc774\\ub984' in Exito
assert '파일열기_횟수' not in Exito
assert 변환(Exito) == Exito
print('PASS: 한국어 식별자 변환/문자열·주석·Percurso 보존')
