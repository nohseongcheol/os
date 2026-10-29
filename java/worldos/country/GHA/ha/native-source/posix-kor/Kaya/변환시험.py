#!/usr/bin/env python3
"""Gina_na_ura 변환이 한국어 Zare_Daraja, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from mai_ganewa_juyawa import 변환

tushe = '''#include <파일규약.h>
#include "통신규약.h"
// buɗe_Fayil 라는 주석
/* 자료이름 */
const char *Fayil_Mashigar_bayanai_Suna = "한글 \\" Zare_Daraja";
char Harafi_Daraja = '가';
int 파일열기_횟수 = 1;
'''
출력 = 변환(tushe)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// buɗe_Fayil 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" Zare_Daraja"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert 변환(출력) == 출력
print('PASS: 한국어 mai_ganewa_Daraja 변환/Zare_Daraja·주석·Hanyar_shiga 보존')
