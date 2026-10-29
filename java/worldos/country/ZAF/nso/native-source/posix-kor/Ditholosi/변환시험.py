#!/usr/bin/env python3
"""aga_lenaneo 변환이 한국어 molokoloko_boleng, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from sešupi_Phetošetšo import 변환

mohlodi = '''#include <파일규약.h>
#include "통신규약.h"
// bula_faele 라는 주석
/* 자료이름 */
const char *faele_go_tsenya_tshedimošo_leina = "한글 \\" molokoloko_boleng";
char tlhaka_boleng = '가';
int 파일열기_횟수 = 1;
'''
출력 = 변환(mohlodi)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// bula_faele 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" molokoloko_boleng"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert 변환(출력) == 출력
print('PASS: 한국어 sešupi_boleng 변환/molokoloko_boleng·주석·Tsejana 보존')
