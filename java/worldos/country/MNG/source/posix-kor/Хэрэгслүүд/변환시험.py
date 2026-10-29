#!/usr/bin/env python3
"""хувилбар_систем 변환이 한국어 мөр_утга_6ca8363c, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from танигч_хөрвүүлэлт import 변환

ЭХ = '''#include <파일규약.h>
#include "통신규약.h"
// нээх_файл 라는 주석
/* 자료이름 */
const char *файл_оролт_нэр = "한글 \\" мөр_утга_6ca8363c";
char тэмдэгт_утга = '가';
int 파일열기_횟수 = 1;
'''
출력 = 변환(ЭХ)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// нээх_файл 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" мөр_утга_6ca8363c"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert 변환(출력) == 출력
print('PASS: 한국어 танигч_утга 변환/мөр_утга_6ca8363c·주석·ЗАМ 보존')
