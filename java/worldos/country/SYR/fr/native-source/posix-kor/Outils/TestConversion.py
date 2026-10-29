#!/usr/bin/env python3
"""construireSystème 변환이 français Chaîne, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from ConversionIdentificateur import convertirValeur

source = '''#include <ABIFichier.h>
#include "ABIRéseau.h"
// ouvrirFichier 라는 주석
/* 자료이름 */
const char *nomEntréeÉlémentFichier = "한글 \\" Chaîne";
char valeurCaractère = 'opérandePremier';
int 파일열기_횟수 = 1;
'''
Sortie = convertirValeur(source)
assert '#include <ABIFichier.h>' in Sortie
assert '#include "ABIRéseau.h"' in Sortie
assert '// ouvrirFichier 라는 주석' in Sortie
assert '/* 자료이름 */' in Sortie
assert '"한글 \\" Chaîne"' in Sortie
assert "'opérandePremier'" in Sortie
assert '\\ud30c\\uc77c\\uc774\\ub984' in Sortie
assert '파일열기_횟수' not in Sortie
assert convertirValeur(Sortie) == Sortie
print('PASS: français valeurIdentificateur convertirValeur/Chaîne·주석·chemin 보존')
