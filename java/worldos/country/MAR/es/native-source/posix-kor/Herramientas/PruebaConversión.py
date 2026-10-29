#!/usr/bin/env python3
"""construirSistema 변환이 español Cadena, 주석, 헤더 경로를 바꾸지 않는지 검사한다."""
from ConversiónIdentificador import convertirValor

fuente = '''#include <ABIArchivo.h>
#include "ABIRed.h"
// abrirArchivo 라는 주석
/* 자료이름 */
const char *nombreEntradaElementoArchivo = "한글 \\" Cadena";
char valorCarácter = 'operandoPrimero';
int 파일열기_횟수 = 1;
'''
Salida = convertirValor(fuente)
assert '#include <ABIArchivo.h>' in Salida
assert '#include "ABIRed.h"' in Salida
assert '// abrirArchivo 라는 주석' in Salida
assert '/* 자료이름 */' in Salida
assert '"한글 \\" Cadena"' in Salida
assert "'operandoPrimero'" in Salida
assert '\\ud30c\\uc77c\\uc774\\ub984' in Salida
assert '파일열기_횟수' not in Salida
assert convertirValor(Salida) == Salida
print('PASS: español valorIdentificador convertirValor/Cadena·주석·ruta 보존')
