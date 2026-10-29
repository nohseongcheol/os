#!/usr/bin/env python3
"""tabax_kureel 변환이 한국어 araf_yu_bennoo_xëyma, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from raññeekaay_tuubal import 변환

Cosaan = '''#include <파일규약.h>
#include "통신규약.h"
// sos_bara_denc 라는 주석
/* 자료이름 */
const char *bara_denc_dugal_xabaar_tur = "한글 \\" araf_yu_bennoo_xëyma";
char Araf_xëyma = '가';
int 파일열기_횟수 = 1;
'''
출력 = 변환(Cosaan)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// sos_bara_denc 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" araf_yu_bennoo_xëyma"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert 변환(출력) == 출력
print('PASS: 한국어 raññeekaay_xëyma 변환/araf_yu_bennoo_xëyma·주석·Yoonu_jëmale 보존')
