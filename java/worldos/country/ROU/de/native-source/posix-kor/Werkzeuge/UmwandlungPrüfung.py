#!/usr/bin/env python3
"""systemErzeugenAbbild 변환이 Deutsch Zeichenkette, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from BezeichnerUmwandlung import wertUmwandeln

Quelltext = '''#include <DateiABI.h>
#include "NetzwerkABI.h"
// dateiÖffnen 라는 주석
/* 자료이름 */
const char *dateiEintragName = "한글 \\" Zeichenkette";
char zeichenWert = 'ersterOperand';
int 파일열기_횟수 = 1;
'''
Ausgabe = wertUmwandeln(Quelltext)
assert '#include <DateiABI.h>' in Ausgabe
assert '#include "NetzwerkABI.h"' in Ausgabe
assert '// dateiÖffnen 라는 주석' in Ausgabe
assert '/* 자료이름 */' in Ausgabe
assert '"한글 \\" Zeichenkette"' in Ausgabe
assert "'ersterOperand'" in Ausgabe
assert '\\ud30c\\uc77c\\uc774\\ub984' in Ausgabe
assert '파일열기_횟수' not in Ausgabe
assert wertUmwandeln(Ausgabe) == Ausgabe
print('PASS: Deutsch bezeichnerWert wertUmwandeln/Zeichenkette·주석·pfad 보존')
