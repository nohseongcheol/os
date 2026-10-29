#!/usr/bin/env python3
"""eraiki_sistema 변환이 Euskara kate_balio, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from identifikatzaile_bihurketa import BIHURTU_balio

ITURBURUA = '''#include <파일규약.h>
#include "통신규약.h"
// ireki_fitxategi 라는 주석
/* 자료이름 */
const char *fitxategi_sarrera_izen = "한글 \\" kate_balio";
char karaktere_balio = '가';
int 파일열기_횟수 = 1;
'''
Irteera = BIHURTU_balio(ITURBURUA)
assert '#include <파일규약.h>' in Irteera
assert '#include "통신규약.h"' in Irteera
assert '// ireki_fitxategi 라는 주석' in Irteera
assert '/* 자료이름 */' in Irteera
assert '"한글 \\" kate_balio"' in Irteera
assert "'가'" in Irteera
assert '\\ud30c\\uc77c\\uc774\\ub984' in Irteera
assert '파일열기_횟수' not in Irteera
assert BIHURTU_balio(Irteera) == Irteera
print('PASS: Euskara identifikatzaile_balio BIHURTU_balio/kate_balio·주석·Bide_izena 보존')
