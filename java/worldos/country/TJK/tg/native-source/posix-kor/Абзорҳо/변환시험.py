#!/usr/bin/env python3
"""сохт_система 변환이 한국어 сатр_қимат_6ca8363c, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from 식별자변환 import 변환

манбаъ = '''#include <파일규약.h>
#include "통신규약.h"
// кушодан_файл 라는 주석
/* 자료이름 */
const char *файл_ворида_ном = "한글 \\" сатр_қимат_6ca8363c";
char аломат_қимат_068c2631 = '가';
int 파일열기_횟수 = 1;
'''
출력 = 변환(манбаъ)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// кушодан_файл 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" сатр_қимат_6ca8363c"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert 변환(출력) == 출력
print('PASS: 한국어 идентификатор_қимат 변환/сатр_қимат_6ca8363c·주석·масир 보존')
