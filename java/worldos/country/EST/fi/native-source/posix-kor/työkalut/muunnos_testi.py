#!/usr/bin/env python3
"""kääntää_Järjestelmä 변환이 suomi merkkijono_ARVO, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from tunniste_muunnos import MUUNNA_ARVO

lähdetiedosto = '''#include <파일규약.h>
#include "통신규약.h"
// avata_Tiedosto 라는 주석
/* 자료이름 */
const char *Tiedosto_merkintä_nimi = "한글 \\" merkkijono_ARVO";
char merkki_ARVO = '가';
int 파일열기_횟수 = 1;
'''
tulostuspaikka = MUUNNA_ARVO(lähdetiedosto)
assert '#include <파일규약.h>' in tulostuspaikka
assert '#include "통신규약.h"' in tulostuspaikka
assert '// avata_Tiedosto 라는 주석' in tulostuspaikka
assert '/* 자료이름 */' in tulostuspaikka
assert '"한글 \\" merkkijono_ARVO"' in tulostuspaikka
assert "'가'" in tulostuspaikka
assert '\\ud30c\\uc77c\\uc774\\ub984' in tulostuspaikka
assert '파일열기_횟수' not in tulostuspaikka
assert MUUNNA_ARVO(tulostuspaikka) == tulostuspaikka
print('PASS: suomi tunniste_ARVO MUUNNA_ARVO/merkkijono_ARVO·주석·polku_2 보존')
