#!/usr/bin/env python3
"""smíð_kerfi 변환이 Íslenska strengur_VALUE, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from auðkenni_umskráning import CONVERT_VALUE

Uppruni = '''#include <파일규약.h>
#include "통신규약.h"
// opið_skrá 라는 주석
/* 자료이름 */
const char *skrá_færsla_heiti = "한글 \\" strengur_VALUE";
char stafur_VALUE = '가';
int 파일열기_횟수 = 1;
'''
úttak = CONVERT_VALUE(Uppruni)
assert '#include <파일규약.h>' in úttak
assert '#include "통신규약.h"' in úttak
assert '// opið_skrá 라는 주석' in úttak
assert '/* 자료이름 */' in úttak
assert '"한글 \\" strengur_VALUE"' in úttak
assert "'가'" in úttak
assert '\\ud30c\\uc77c\\uc774\\ub984' in úttak
assert '파일열기_횟수' not in úttak
assert CONVERT_VALUE(úttak) == úttak
print('PASS: Íslenska auðkenni_VALUE CONVERT_VALUE/strengur_VALUE·주석·SLÓÐ 보존')
