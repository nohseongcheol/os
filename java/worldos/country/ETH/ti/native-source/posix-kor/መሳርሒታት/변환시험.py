#!/usr/bin/env python3
"""ህነጽ_ስርዓት 변환이 ትግርኛ ሕብረ_ቁምፊ_ዋጋ, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from ፈላዪ_ቅየራ import 변환

ምንጪ = '''#include <파일규약.h>
#include "통신규약.h"
// ክፈት_ፋይል 라는 주석
/* 자료이름 */
const char *ፋይል_ምእታው_ሽም = "한글 \\" ሕብረ_ቁምፊ_ዋጋ";
char ፊደል_ዋጋ = '가';
int 파일열기_횟수 = 1;
'''
출력 = 변환(ምንጪ)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// ክፈት_ፋይል 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" ሕብረ_ቁምፊ_ዋጋ"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert 변환(출력) == 출력
print('PASS: ትግርኛ ፈላዪ_ዋጋ_5b7b8b77 변환/ሕብረ_ቁምፊ_ዋጋ·주석·መገዲ 보존')
