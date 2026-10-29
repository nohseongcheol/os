#!/usr/bin/env python3
"""بلڈ_نظام 변환이 한국어 سٹرنگ_قدر, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from شناخت_کرنڑ_آلا_تبدیلی import 변환

ماخذ = '''#include <파일규약.h>
#include "통신규약.h"
// بنڑاؤ_فائل 라는 주석
/* 자료이름 */
const char *فائل_داخلہ_ناں = "한글 \\" سٹرنگ_قدر";
char کریکٹر_قدر = '가';
int 파일열기_횟수 = 1;
'''
출력 = 변환(ماخذ)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// بنڑاؤ_فائل 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" سٹرنگ_قدر"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert 변환(출력) == 출력
print('PASS: 한국어 شناخت_کرنڑ_آلا_قدر 변환/سٹرنگ_قدر·주석·راہ 보존')
