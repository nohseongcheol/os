#!/usr/bin/env python3
"""گڏ_ڪريو_سسٽم 변환이 한국어 اسٽرنگ_قدر, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from سڃاڻپ_ڪندڙ_تبديلي import 변환

ماخذ = '''#include <파일규약.h>
#include "통신규약.h"
// ٺاھيو_فائل 라는 주석
/* 자료이름 */
const char *فائل_داخلا_نالو = "한글 \\" اسٽرنگ_قدر";
char ڪريڪٽر_قدر = '가';
int 파일열기_횟수 = 1;
'''
출력 = 변환(ماخذ)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// ٺاھيو_فائل 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" اسٽرنگ_قدر"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert 변환(출력) == 출력
print('PASS: 한국어 سڃاڻپ_ڪندڙ_قدر 변환/اسٽرنگ_قدر·주석·راههه 보존')
