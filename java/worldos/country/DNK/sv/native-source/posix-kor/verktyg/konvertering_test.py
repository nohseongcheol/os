#!/usr/bin/env python3
"""version_System 변환이 Svenska sträng_värde, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from identifierare_konvertering import KONVERTERA_värde

källfil = '''#include <파일규약.h>
#include "통신규약.h"
// skapa_fil 라는 주석
/* 자료이름 */
const char *fil_post_namn = "한글 \\" sträng_värde";
char tecken_värde = '가';
int 파일열기_횟수 = 1;
'''
utmatningsposition = KONVERTERA_värde(källfil)
assert '#include <파일규약.h>' in utmatningsposition
assert '#include "통신규약.h"' in utmatningsposition
assert '// skapa_fil 라는 주석' in utmatningsposition
assert '/* 자료이름 */' in utmatningsposition
assert '"한글 \\" sträng_värde"' in utmatningsposition
assert "'가'" in utmatningsposition
assert '\\ud30c\\uc77c\\uc774\\ub984' in utmatningsposition
assert '파일열기_횟수' not in utmatningsposition
assert KONVERTERA_värde(utmatningsposition) == utmatningsposition
print('PASS: Svenska identifierare_värde KONVERTERA_värde/sträng_värde·주석·sökväg_2 보존')
