#!/usr/bin/env python3
"""BLD_Systém 변환이 čeština řetězec_HODNOTA, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from identifikátor_převod import CONVERT_HODNOTA

zdrojový_soubor = '''#include <Soubor_ABI.h>
#include "síť_ABI.h"
// otevřít_Soubor 라는 주석
/* 자료이름 */
const char *Soubor_položka_název = "한글 \\" řetězec_HODNOTA";
char znak_HODNOTA = '가';
int 파일열기_횟수 = 1;
'''
výstupní_pozice = CONVERT_HODNOTA(zdrojový_soubor)
assert '#include <Soubor_ABI.h>' in výstupní_pozice
assert '#include "síť_ABI.h"' in výstupní_pozice
assert '// otevřít_Soubor 라는 주석' in výstupní_pozice
assert '/* 자료이름 */' in výstupní_pozice
assert '"한글 \\" řetězec_HODNOTA"' in výstupní_pozice
assert "'가'" in výstupní_pozice
assert '\\ud30c\\uc77c\\uc774\\ub984' in výstupní_pozice
assert '파일열기_횟수' not in výstupní_pozice
assert CONVERT_HODNOTA(výstupní_pozice) == výstupní_pozice
print('PASS: čeština identifikátor_HODNOTA CONVERT_HODNOTA/řetězec_HODNOTA·주석·cesta_2 보존')
