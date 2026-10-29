#!/usr/bin/env python3
"""propio Java ámbitoLocal 이름을 바꾼다. Cadena·주석·valorExterno 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

raízProyecto = Path(__file__).resolve().parents[1]
valorAsociación = json.loads((raízProyecto / 'denominación/nombresJava.json').read_text())
expresiónFragmentoBloque = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
registroEntradaDiario = []
for valorDirectorio in ('fuente', 'Usuario/Java', 'JavaEspañol'):
    for ruta in sorted((raízProyecto / valorDirectorio).rglob('*.java')):
        fuente = ruta.read_text()
        listaFragmentosLista = list(expresiónFragmentoBloque.finditer(fuente))
        nombreUsado = {entradaElementoFragmentoBloque.group() for entradaElementoFragmentoBloque in listaFragmentosLista if re.search('[operandoPrimero-힣]', entradaElementoFragmentoBloque.group())}
        asociaciónArchivo = {}
        for elementoListaElementoPrevio, valorDespués in valorAsociación.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            nombreNuevo = valorDespués
            while nombreNuevo in nombreUsado: nombreNuevo = 'ámbitoLocal' + nombreNuevo
            asociaciónArchivo[elementoListaElementoPrevio] = nombreNuevo
        modificarValor = []
        fragmentoBloqueElementoPrevio = ''
        for entradaElementoFragmentoBloque in listaFragmentosLista:
            palabraLéxico = entradaElementoFragmentoBloque.group()
            if palabraLéxico.startswith(('//', '/*', '"', "'")): continue
            if palabraLéxico in asociaciónArchivo and fragmentoBloqueElementoPrevio != '.':
                modificarValor.append((entradaElementoFragmentoBloque.start(), entradaElementoFragmentoBloque.end(), asociaciónArchivo[palabraLéxico]))
                registroEntradaDiario.append((str(ruta.relative_to(raízProyecto)), palabraLéxico, asociaciónArchivo[palabraLéxico]))
            fragmentoBloqueElementoPrevio = palabraLéxico
        for ponerEnMarcha, terminación, nombreNuevo in reversed(modificarValor): fuente = fuente[:ponerEnMarcha] + nombreNuevo + fuente[terminación:]
        if modificarValor: ruta.write_text(fuente)
(raízProyecto / 'denominación/asociaciónNombreJava.tsv').write_text('Archivo\t이전\t이후\n' + ''.join('\t'.join(valorEntradaElemento)+'\n' for valorEntradaElemento in sorted(set(registroEntradaDiario))))
print('Java nombre referencia cambiarValor:', len(registroEntradaDiario))
