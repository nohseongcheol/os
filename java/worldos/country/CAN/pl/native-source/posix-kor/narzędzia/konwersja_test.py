#!/usr/bin/env python3
"""BLD_System 변환이 polski ciąg_WARTOŚĆ, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from identyfikator_konwersja import KONWERTUJ_WARTOŚĆ

plik_źródłowy = '''#include <Plik_ABI.h>
#include "sieć_ABI.h"
// otwarty_Plik 라는 주석
/* 자료이름 */
const char *Plik_wpis_nazwa = "한글 \\" ciąg_WARTOŚĆ";
char znak_WARTOŚĆ = '가';
int 파일열기_횟수 = 1;
'''
pozycja_wyjścia = KONWERTUJ_WARTOŚĆ(plik_źródłowy)
assert '#include <Plik_ABI.h>' in pozycja_wyjścia
assert '#include "sieć_ABI.h"' in pozycja_wyjścia
assert '// otwarty_Plik 라는 주석' in pozycja_wyjścia
assert '/* 자료이름 */' in pozycja_wyjścia
assert '"한글 \\" ciąg_WARTOŚĆ"' in pozycja_wyjścia
assert "'가'" in pozycja_wyjścia
assert '\\ud30c\\uc77c\\uc774\\ub984' in pozycja_wyjścia
assert '파일열기_횟수' not in pozycja_wyjścia
assert KONWERTUJ_WARTOŚĆ(pozycja_wyjścia) == pozycja_wyjścia
print('PASS: polski identyfikator_WARTOŚĆ KONWERTUJ_WARTOŚĆ/ciąg_WARTOŚĆ·주석·ścieżka_2 보존')
