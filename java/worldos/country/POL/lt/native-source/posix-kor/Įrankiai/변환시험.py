#!/usr/bin/env python3
"""kompiliuoti_sistema 변환이 Lietuvių eilutė_VALUE, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from identifikatorius_konvertavimas import CONVERT_VALUE

ŠALTINIS = '''#include <파일규약.h>
#include "통신규약.h"
// kurti_Failas 라는 주석
/* 자료이름 */
const char *Failas_įrašas_pavadinimas = "한글 \\" eilutė_VALUE";
char simbolis_VALUE_068c2631 = '가';
int 파일열기_횟수 = 1;
'''
Išvestis = CONVERT_VALUE(ŠALTINIS)
assert '#include <파일규약.h>' in Išvestis
assert '#include "통신규약.h"' in Išvestis
assert '// kurti_Failas 라는 주석' in Išvestis
assert '/* 자료이름 */' in Išvestis
assert '"한글 \\" eilutė_VALUE"' in Išvestis
assert "'가'" in Išvestis
assert '\\ud30c\\uc77c\\uc774\\ub984' in Išvestis
assert '파일열기_횟수' not in Išvestis
assert CONVERT_VALUE(Išvestis) == Išvestis
print('PASS: Lietuvių identifikatorius_VALUE CONVERT_VALUE/eilutė_VALUE·주석·KELIAS 보존')
