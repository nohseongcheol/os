#!/usr/bin/env python3
"""àtòpọ̀_ètò 변환이 한국어 fọ́nrán_iye, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from Àfidámọ̀_ìbánisọ̀rọ̀ import 변환

orísun = '''#include <파일규약.h>
#include "통신규약.h"
// ṣí_fáìlì 라는 주석
/* 자료이름 */
const char *fáìlì_ìgbéwọlé_orúkọ = "한글 \\" fọ́nrán_iye";
char ẹyọ_ọ̀rọ̀_iye = '가';
int 파일열기_횟수 = 1;
'''
출력 = 변환(orísun)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// ṣí_fáìlì 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" fọ́nrán_iye"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert 변환(출력) == 출력
print('PASS: 한국어 Àfidámọ̀_iye 변환/fọ́nrán_iye·주석·ọ̀nà 보존')
