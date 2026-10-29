#!/usr/bin/env python3
"""costruire 변환이 Italiano stringa_VALORE, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from identificatore_conversione import CONVERTI_VALORE

codiceSorgente = '''#include <File_ABI.h>
#include "rete_ABI.h"
// aperto_File 라는 주석
/* 자료이름 */
const char *File_voce_nome = "한글 \\" stringa_VALORE";
char carattere_VALORE = '가';
int 파일열기_횟수 = 1;
'''
uscitaTesto = CONVERTI_VALORE(codiceSorgente)
assert '#include <File_ABI.h>' in uscitaTesto
assert '#include "rete_ABI.h"' in uscitaTesto
assert '// aperto_File 라는 주석' in uscitaTesto
assert '/* 자료이름 */' in uscitaTesto
assert '"한글 \\" stringa_VALORE"' in uscitaTesto
assert "'가'" in uscitaTesto
assert '\\ud30c\\uc77c\\uc774\\ub984' in uscitaTesto
assert '파일열기_횟수' not in uscitaTesto
assert CONVERTI_VALORE(uscitaTesto) == uscitaTesto
print('PASS: Italiano identificatore_VALORE CONVERTI_VALORE/stringa_VALORE·주석·percorso 보존')
