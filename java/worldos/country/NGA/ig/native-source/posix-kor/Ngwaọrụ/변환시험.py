#!/usr/bin/env python3
"""wue_sistèm 변환이 한국어 ùsòròokwū_valuu, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from ihe_nkọwapụta_mgbanwe import 변환

ebensìbịa = '''#include <파일규약.h>
#include "통신규약.h"
// mepee_ọbọakwụkwọ 라는 주석
/* 자료이름 */
const char *ọbọakwụkwọ_ndebà_akara_ahà = "한글 \\" ùsòròokwū_valuu";
char mkpụrụedemede_valuu = '가';
int 파일열기_횟수 = 1;
'''
출력 = 변환(ebensìbịa)
assert '#include <파일규약.h>' in 출력
assert '#include "통신규약.h"' in 출력
assert '// mepee_ọbọakwụkwọ 라는 주석' in 출력
assert '/* 자료이름 */' in 출력
assert '"한글 \\" ùsòròokwū_valuu"' in 출력
assert "'가'" in 출력
assert '\\ud30c\\uc77c\\uc774\\ub984' in 출력
assert '파일열기_횟수' not in 출력
assert 변환(출력) == 출력
print('PASS: 한국어 ihe_nkọwapụta_valuu 변환/ùsòròokwū_valuu·주석·ụzọ_ozi 보존')
