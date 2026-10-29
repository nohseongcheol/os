#!/usr/bin/env python3
"""دروستکراو_سیستم 변환이 한국어 رست_نرخ, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from ناسێنەر_گۆڕین import 변환

ژێدەر = '''#include <파일규약.h>
#include "통신규약.h"
// کردنەوە_فایل 라는 주석
/* 자료이름 */
const char *فایل_تێنووسین_ناو = "한글 \\" رست_نرخ";
char نووسە_نرخ = '가';
int 파일열기_횟수 = 1;
'''
출력 = 변환(ژێدەر)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// کردنەوە_فایل 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" رست_نرخ"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert 변환(출력) == 출력
print('PASS: 한국어 ناسێنەر_نرخ 변환/رست_نرخ·주석·گوزەر 보존')
