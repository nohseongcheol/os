#!/usr/bin/env python3
"""bouwen 변환이 Nederlands tekenreeks_WAARDE, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from id_omzetten import CONVERTEREN_WAARDE

broncode = '''#include <파일규약.h>
#include "통신규약.h"
// open_Bestand 라는 주석
/* 자료이름 */
const char *Bestand_invoer_naam = "한글 \\" tekenreeks_WAARDE";
char teken_WAARDE = '가';
int 파일열기_횟수 = 1;
'''
tekstuitvoer = CONVERTEREN_WAARDE(broncode)
assert '#include <파일규약.h>' in tekstuitvoer
assert '#include "통신규약.h"' in tekstuitvoer
assert '// open_Bestand 라는 주석' in tekstuitvoer
assert '/* 자료이름 */' in tekstuitvoer
assert '"한글 \\" tekenreeks_WAARDE"' in tekstuitvoer
assert "'가'" in tekstuitvoer
assert '\\ud30c\\uc77c\\uc774\\ub984' in tekstuitvoer
assert '파일열기_횟수' not in tekstuitvoer
assert CONVERTEREN_WAARDE(tekstuitvoer) == tekstuitvoer
print('PASS: Nederlands id_WAARDE CONVERTEREN_WAARDE/tekenreeks_WAARDE·주석·pad 보존')
