#!/usr/bin/env python3
"""añadirFinalEntradaElemento Python 패키지 없이 español Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def númeroElementosPuntoCódigo(valorContenidoValor, biblioteca, directorioClase):
    resultado = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(biblioteca), str(directorioClase)]), 'ComandoTexto', valorContenidoValor],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(resultado.stdout.strip())


if __name__ == '__main__':
    analizarArgumentos = argparse.ArgumentParser(description=__doc__)
    analizarArgumentos.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/JavaEspañol.jar'))
    analizarArgumentos.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    analizarArgumentos.add_argument('--text', default='한글 😀')
    argumentos = analizarArgumentos.parse_args()
    print('Python → español.Java.Caracteres.númeroElementosPuntoCódigo:',
          númeroElementosPuntoCódigo(argumentos.text, argumentos.jar, argumentos.classes))
