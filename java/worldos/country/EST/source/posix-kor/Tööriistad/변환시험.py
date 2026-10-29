#!/usr/bin/env python3
"""järk_süsteem 변환이 Eesti string_VALUE, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from identifikaator_teisendamine import CONVERT_VALUE

ALLIKAS = '''#include <파일규약.h>
#include "통신규약.h"
// avama_Fail 라는 주석
/* 자료이름 */
const char *Fail_kirje_nimetus = "한글 \\" string_VALUE";
char märk_VALUE = '가';
int 파일열기_횟수 = 1;
'''
Väljund = CONVERT_VALUE(ALLIKAS)
assert '#include <파일규약.h>' in Väljund
assert '#include "통신규약.h"' in Väljund
assert '// avama_Fail 라는 주석' in Väljund
assert '/* 자료이름 */' in Väljund
assert '"한글 \\" string_VALUE"' in Väljund
assert "'가'" in Väljund
assert '\\ud30c\\uc77c\\uc774\\ub984' in Väljund
assert '파일열기_횟수' not in Väljund
assert CONVERT_VALUE(Väljund) == Väljund
print('PASS: Eesti identifikaator_VALUE CONVERT_VALUE/string_VALUE·주석·RADA 보존')
