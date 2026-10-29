#!/usr/bin/env python3
"""aga_tsamaiso 변환이 한국어 dikwalwa_Boleng, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from setlhaodi_phetolelo import 변환

Motswedi = '''#include <파일규약.h>
#include "통신규약.h"
// bula_faele 라는 주석
/* 자료이름 */
const char *faele_tsenyo_leina = "한글 \\" dikwalwa_Boleng";
char Letshwao_Boleng = '가';
int 파일열기_횟수 = 1;
'''
출력 = 변환(Motswedi)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// bula_faele 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" dikwalwa_Boleng"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert 변환(출력) == 출력
print('PASS: 한국어 setlhaodi_Boleng 변환/dikwalwa_Boleng·주석·tsela 보존')
