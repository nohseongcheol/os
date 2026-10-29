#!/usr/bin/env python3
"""épít_Rendszer 변환이 magyar sztring_ÉRTÉK, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from azonosító_átalakítás import konvertál_ÉRTÉK

FORRÁS = '''#include <파일규약.h>
#include "통신규약.h"
// készít_Fájl 라는 주석
/* 자료이름 */
const char *Fájl_bejegyzés_név = "한글 \\" sztring_ÉRTÉK";
char karakter_ÉRTÉK = '가';
int 파일열기_횟수 = 1;
'''
Kimenet = konvertál_ÉRTÉK(FORRÁS)
assert '#include <파일규약.h>' in Kimenet
assert '#include "통신규약.h"' in Kimenet
assert '// készít_Fájl 라는 주석' in Kimenet
assert '/* 자료이름 */' in Kimenet
assert '"한글 \\" sztring_ÉRTÉK"' in Kimenet
assert "'가'" in Kimenet
assert '\\ud30c\\uc77c\\uc774\\ub984' in Kimenet
assert '파일열기_횟수' not in Kimenet
assert konvertál_ÉRTÉK(Kimenet) == Kimenet
print('PASS: magyar azonosító_ÉRTÉK konvertál_ÉRTÉK/sztring_ÉRTÉK·주석·ÚTVONAL 보존')
