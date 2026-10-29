#!/usr/bin/env python3
"""būvējums_sistēma 변환이 Latviešu virkne_VALUE, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from identifikators_pārvēršana import CONVERT_VALUE

AVOTS = '''#include <파일규약.h>
#include "통신규약.h"
// atvērt_Fails 라는 주석
/* 자료이름 */
const char *Fails_ievade_nosaukums = "한글 \\" virkne_VALUE";
char rakstzīme_VALUE = '가';
int 파일열기_횟수 = 1;
'''
Izvade = CONVERT_VALUE(AVOTS)
assert '#include <파일규약.h>' in Izvade
assert '#include "통신규약.h"' in Izvade
assert '// atvērt_Fails 라는 주석' in Izvade
assert '/* 자료이름 */' in Izvade
assert '"한글 \\" virkne_VALUE"' in Izvade
assert "'가'" in Izvade
assert '\\ud30c\\uc77c\\uc774\\ub984' in Izvade
assert '파일열기_횟수' not in Izvade
assert CONVERT_VALUE(Izvade) == Izvade
print('PASS: Latviešu identifikators_VALUE CONVERT_VALUE/virkne_VALUE·주석·CEĻŠ 보존')
