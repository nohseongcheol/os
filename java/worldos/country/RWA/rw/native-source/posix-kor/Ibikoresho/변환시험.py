#!/usr/bin/env python3
"""gusohora_sisitemu 변환이 Ikinyarwanda igicenteruro_agaciro, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from indanga_ihindura import 변환

Inkomoko = '''#include <파일규약.h>
#include "통신규약.h"
// kurema_dosiye 라는 주석
/* 자료이름 */
const char *dosiye_icyinjizwa_izina = "한글 \\" igicenteruro_agaciro";
char inyuguti_agaciro = '가';
int 파일열기_횟수 = 1;
'''
출력 = 변환(Inkomoko)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// kurema_dosiye 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" igicenteruro_agaciro"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert 변환(출력) == 출력
print('PASS: Ikinyarwanda indanga_agaciro 변환/igicenteruro_agaciro·주석·Inzira 보존')
