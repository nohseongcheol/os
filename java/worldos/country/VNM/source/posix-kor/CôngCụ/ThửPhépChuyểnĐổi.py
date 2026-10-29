#!/usr/bin/env python3
"""xâyDựngHệThống 변환이 tiếngViệt ChuỗiKýTự, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from PhépChuyểnĐổiĐịnhDanh import chuyểnĐổiGiáTrị

mãNguồn = '''#include <ABITệp.h>
#include "ABIMạng.h"
// mởTệp 라는 주석
/* 자료이름 */
const char *tênMụcTệp = "한글 \\" ChuỗiKýTự";
char giáTrịKýTự = 'toánHạngĐầuTiên';
int 파일열기_횟수 = 1;
'''
ĐầuRa = chuyểnĐổiGiáTrị(mãNguồn)
assert '#include <ABITệp.h>' in ĐầuRa
assert '#include "ABIMạng.h"' in ĐầuRa
assert '// mởTệp 라는 주석' in ĐầuRa
assert '/* 자료이름 */' in ĐầuRa
assert '"한글 \\" ChuỗiKýTự"' in ĐầuRa
assert "'toánHạngĐầuTiên'" in ĐầuRa
assert '\\ud30c\\uc77c\\uc774\\ub984' in ĐầuRa
assert '파일열기_횟수' not in ĐầuRa
assert chuyểnĐổiGiáTrị(ĐầuRa) == ĐầuRa
print('PASS: tiếngViệt giáTrịĐịnhDanh chuyểnĐổiGiáTrị/ChuỗiKýTự·주석·đườngDẫn 보존')
