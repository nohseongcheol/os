#!/usr/bin/env python3
"""akha_isistimu 변환이 Isi_Zulu uchunge_inani, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from isivezi_ukuguqula import 변환

umthombo = '''#include <파일규약.h>
#include "통신규약.h"
// vula_ifayela 라는 주석
/* 자료이름 */
const char *ifayela_okufakwayo_igama = "한글 \\" uchunge_inani";
char uhlamvusimo_inani = '가';
int 파일열기_횟수 = 1;
'''
출력 = 변환(umthombo)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// vula_ifayela 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" uchunge_inani"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert 변환(출력) == 출력
print('PASS: Isi_Zulu isivezi_inani 변환/uchunge_inani·주석·Indlela_2 보존')
