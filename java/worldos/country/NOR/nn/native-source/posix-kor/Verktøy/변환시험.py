#!/usr/bin/env python3
"""bygg_system 변환이 한국어 streng_VALUE, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from identifikator_konvertering import CONVERT_VALUE

KJELDE = '''#include <파일규약.h>
#include "통신규약.h"
// opne_fil 라는 주석
/* 자료이름 */
const char *fil_oppføring_namn = "한글 \\" streng_VALUE";
char teikn_VALUE = '가';
int 파일열기_횟수 = 1;
'''
Utdata = CONVERT_VALUE(KJELDE)
assert '#include <파일규약.h>' in Utdata
assert '#include "통신규약.h"' in Utdata
assert '// opne_fil 라는 주석' in Utdata
assert '/* 자료이름 */' in Utdata
assert '"한글 \\" streng_VALUE"' in Utdata
assert "'가'" in Utdata
assert '\\ud30c\\uc77c\\uc774\\ub984' in Utdata
assert '파일열기_횟수' not in Utdata
assert CONVERT_VALUE(Utdata) == Utdata
print('PASS: 한국어 identifikator_VALUE CONVERT_VALUE/streng_VALUE·주석·STIGE 보존')
