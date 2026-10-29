#!/usr/bin/env python3
"""hanga_pūnaha 변환이 Reo_Māori aho_uara, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from pūtāutu_tahuritanga import CONVERT_uara

pūtake = '''#include <파일규약.h>
#include "통신규약.h"
// tiwhikete_kōnae 라는 주석
/* 자료이름 */
const char *kōnae_tāurunga_ingoa = "한글 \\" aho_uara";
char pūāhua_uara = '가';
int 파일열기_횟수 = 1;
'''
출력 = CONVERT_uara(pūtake)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// tiwhikete_kōnae 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" aho_uara"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert CONVERT_uara(출력) == 출력
print('PASS: Reo_Māori pūtāutu_uara CONVERT_uara/aho_uara·주석·ara 보존')
