#!/usr/bin/env python3
"""build_System 변환이 Dansk streng_VÆRDI, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from identifikator_konvertering import KONVERTER_VÆRDI

KILDE = '''#include <파일규약.h>
#include "통신규약.h"
// åben_fil 라는 주석
/* 자료이름 */
const char *fil_post_navn = "한글 \\" streng_VÆRDI";
char tegn_VÆRDI = '가';
int 파일열기_횟수 = 1;
'''
Udgang = KONVERTER_VÆRDI(KILDE)
assert '#include <파일규약.h>' in Udgang
assert '#include "통신규약.h"' in Udgang
assert '// åben_fil 라는 주석' in Udgang
assert '/* 자료이름 */' in Udgang
assert '"한글 \\" streng_VÆRDI"' in Udgang
assert "'가'" in Udgang
assert '\\ud30c\\uc77c\\uc774\\ub984' in Udgang
assert '파일열기_횟수' not in Udgang
assert KONVERTER_VÆRDI(Udgang) == Udgang
print('PASS: Dansk identifikator_VÆRDI KONVERTER_VÆRDI/streng_VÆRDI·주석·Sti 보존')
