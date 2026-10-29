#!/usr/bin/env python3
"""düz_ulgam 변환이 한국어 setir_baha_6ca8363c, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from tanaýjy_öwürme import 변환

Çeşme = '''#include <파일규약.h>
#include "통신규약.h"
// aç_faýl 라는 주석
/* 자료이름 */
const char *faýl_girizmeklik_at = "한글 \\" setir_baha_6ca8363c";
char nyşan_baha_068c2631 = '가';
int 파일열기_횟수 = 1;
'''
출력 = 변환(Çeşme)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// aç_faýl 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" setir_baha_6ca8363c"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert 변환(출력) == 출력
print('PASS: 한국어 tanaýjy_baha 변환/setir_baha_6ca8363c·주석·Ýol 보존')
