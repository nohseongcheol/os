#!/usr/bin/env python3
"""graditev_sistem 변환이 slovenščina niz_VALUE, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from identifikator_sprememba_naročnine import CONVERT_VALUE

VIR = '''#include <파일규약.h>
#include "통신규약.h"
// odprto_Datoteka 라는 주석
/* 자료이름 */
const char *Datoteka_vnos_ime = "한글 \\" niz_VALUE";
char znak_VALUE = '가';
int 파일열기_횟수 = 1;
'''
Izpis = CONVERT_VALUE(VIR)
assert '#include <파일규약.h>' in Izpis
assert '#include "통신규약.h"' in Izpis
assert '// odprto_Datoteka 라는 주석' in Izpis
assert '/* 자료이름 */' in Izpis
assert '"한글 \\" niz_VALUE"' in Izpis
assert "'가'" in Izpis
assert '\\ud30c\\uc77c\\uc774\\ub984' in Izpis
assert '파일열기_횟수' not in Izpis
assert CONVERT_VALUE(Izpis) == Izpis
print('PASS: slovenščina identifikator_VALUE CONVERT_VALUE/niz_VALUE·주석·POT 보존')
