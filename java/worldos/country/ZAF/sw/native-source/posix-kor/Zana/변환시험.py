#!/usr/bin/env python3
"""jenga_mfumo 변환이 한국어 tungo_thamani, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from kitambulishi_ubadilishaji import 변환

chanzo = '''#include <파일규약.h>
#include "통신규약.h"
// unda_faili 라는 주석
/* 자료이름 */
const char *faili_ingizo_jina = "한글 \\" tungo_thamani";
char kibambo_thamani = '가';
int 파일열기_횟수 = 1;
'''
출력 = 변환(chanzo)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// unda_faili 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" tungo_thamani"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert 변환(출력) == 출력
print('PASS: 한국어 kitambulishi_thamani 변환/tungo_thamani·주석·njia 보존')
