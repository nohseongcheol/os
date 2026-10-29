#!/usr/bin/env python3
"""верзија_систем 변환이 Македонски низа_VALUE_6ca8363c, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from идентификатор_конверзија import CONVERT_VALUE

ИЗВОР = '''#include <파일규약.h>
#include "통신규약.h"
// отвори_датотека 라는 주석
/* 자료이름 */
const char *датотека_внес_име = "한글 \\" низа_VALUE_6ca8363c";
char знак_VALUE = '가';
int 파일열기_횟수 = 1;
'''
출력 = CONVERT_VALUE(ИЗВОР)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// отвори_датотека 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" низа_VALUE_6ca8363c"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert CONVERT_VALUE(출력) == 출력
print('PASS: Македонски идентификатор_VALUE CONVERT_VALUE/низа_VALUE_6ca8363c·주석·ПАТЕКА 보존')
