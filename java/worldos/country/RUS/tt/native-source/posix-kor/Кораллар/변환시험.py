#!/usr/bin/env python3
"""төзү_система 변환이 Татарча юл_VALUE_6ca8363c, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from күрсәткеч_үзгәртү import CONVERT_VALUE

чыганак = '''#include <파일규약.h>
#include "통신규약.h"
// ачу_файл 라는 주석
/* 자료이름 */
const char *файл_кертү_исем = "한글 \\" юл_VALUE_6ca8363c";
char символ_VALUE_068c2631 = '가';
int 파일열기_횟수 = 1;
'''
출력 = CONVERT_VALUE(чыганак)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// ачу_файл 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" юл_VALUE_6ca8363c"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert CONVERT_VALUE(출력) == 출력
print('PASS: Татарча күрсәткеч_VALUE CONVERT_VALUE/юл_VALUE_6ca8363c·주석·Yul 보존')
