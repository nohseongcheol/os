#!/usr/bin/env python3
"""दाळचे_प्रणाली 변환이 한국어 स्ट्रिंग_मोल, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from वळखुपी_रूपांतर import CONVERT_मोल

स्त्रोत = '''#include <파일규약.h>
#include "통신규약.h"
// उगडचें_फायल 라는 주석
/* 자료이름 */
const char *फायल_प्रवेश_नांव = "한글 \\" स्ट्रिंग_मोल";
char वर्ण_मोल = '가';
int 파일열기_횟수 = 1;
'''
출력 = CONVERT_मोल(स्त्रोत)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// उगडचें_फायल 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" स्ट्रिंग_मोल"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert CONVERT_मोल(출력) == 출력
print('PASS: 한국어 वळखुपी_मोल CONVERT_मोल/स्ट्रिंग_मोल·주석·पाथ 보존')
