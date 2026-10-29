#!/usr/bin/env python3
"""yakha_inkqubo 변환이 isiXhosa uluhlu_lweekharektha_ixabiso, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from isalathisi_uguqulo import 변환

UMTHOMBO = '''#include <파일규약.h>
#include "통신규약.h"
// vula_ifayile 라는 주석
/* 자료이름 */
const char *ifayile_ufako_nkcukacha_igama = "한글 \\" uluhlu_lweekharektha_ixabiso";
char ikharakhtha_ixabiso = '가';
int 파일열기_횟수 = 1;
'''
출력 = 변환(UMTHOMBO)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// vula_ifayile 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" uluhlu_lweekharektha_ixabiso"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert 변환(출력) == 출력
print('PASS: isiXhosa isalathisi_ixabiso 변환/uluhlu_lweekharektha_ixabiso·주석·INDLELA 보존')
