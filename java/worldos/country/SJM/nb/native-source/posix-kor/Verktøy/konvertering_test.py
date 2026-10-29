#!/usr/bin/env python3
"""bygg_System 변환이 norsk streng_VERDI, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from identifikator_konvertering import KONVERTER_VERDI

KILDE = '''#include <파일규약.h>
#include "통신규약.h"
// åpen_Fil 라는 주석
/* 자료이름 */
const char *Fil_oppføring_navn = "한글 \\" streng_VERDI";
char tegn_VERDI = '가';
int 파일열기_횟수 = 1;
'''
Utgang = KONVERTER_VERDI(KILDE)
assert '#include <파일규약.h>' in Utgang
assert '#include "통신규약.h"' in Utgang
assert '// åpen_Fil 라는 주석' in Utgang
assert '/* 자료이름 */' in Utgang
assert '"한글 \\" streng_VERDI"' in Utgang
assert "'가'" in Utgang
assert '\\ud30c\\uc77c\\uc774\\ub984' in Utgang
assert '파일열기_횟수' not in Utgang
assert KONVERTER_VERDI(Utgang) == Utgang
print('PASS: norsk identifikator_VERDI KONVERTER_VERDI/streng_VERDI·주석·Sti 보존')
