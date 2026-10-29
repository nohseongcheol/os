#!/usr/bin/env python3
"""međuverzija_sustav 변환이 hrvatski niz_VALUE, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from identifikator_pretvorba import CONVERT_VALUE

IZVOR = '''#include <파일규약.h>
#include "통신규약.h"
// otvoreno_Datoteka 라는 주석
/* 자료이름 */
const char *Datoteka_unos_naziv = "한글 \\" niz_VALUE";
char znak_VALUE = '가';
int 파일열기_횟수 = 1;
'''
Izlaz = CONVERT_VALUE(IZVOR)
assert '#include <파일규약.h>' in Izlaz
assert '#include "통신규약.h"' in Izlaz
assert '// otvoreno_Datoteka 라는 주석' in Izlaz
assert '/* 자료이름 */' in Izlaz
assert '"한글 \\" niz_VALUE"' in Izlaz
assert "'가'" in Izlaz
assert '\\ud30c\\uc77c\\uc774\\ub984' in Izlaz
assert '파일열기_횟수' not in Izlaz
assert CONVERT_VALUE(Izlaz) == Izlaz
print('PASS: hrvatski identifikator_VALUE CONVERT_VALUE/niz_VALUE·주석·PUTANJA 보존')
