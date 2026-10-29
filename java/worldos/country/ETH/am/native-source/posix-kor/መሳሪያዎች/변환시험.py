#!/usr/bin/env python3
"""ግንብ_ስርዓት 변환이 አማርኛ ኅብረቁምፊ_እሴት, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from መለያ_ንግግር import 변환

ምንጭ = '''#include <파일규약.h>
#include "통신규약.h"
// ክፈት_ፋይል 라는 주석
/* 자료이름 */
const char *ፋይል_ምዝግብ_ስም = "한글 \\" ኅብረቁምፊ_እሴት";
char ቁምፊ_እሴት = '가';
int 파일열기_횟수 = 1;
'''
ውጤት = 변환(ምንጭ)
assert '#include <파일규약.h>' in ውጤት
assert '#include "통신규약.h"' in ውጤት
assert '// ክፈት_ፋይል 라는 주석' in ውጤት
assert '/* 자료이름 */' in ውጤት
assert '"한글 \\" ኅብረቁምፊ_እሴት"' in ውጤት
assert "'가'" in ውጤት
assert '\\ud30c\\uc77c\\uc774\\ub984' in ውጤት
assert '파일열기_횟수' not in ውጤት
assert 변환(ውጤት) == ውጤት
print('PASS: አማርኛ መለያ_እሴት_5b7b8b77 변환/ኅብረቁምፊ_እሴት·주석·መተላለፊያ 보존')
