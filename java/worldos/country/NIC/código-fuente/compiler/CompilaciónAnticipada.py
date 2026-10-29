#!/usr/bin/env python3
"""elementoListaElementoPrevio Python 경로를 Java 미리 번역기에 연결한다. traducirFuente 구현은 HerramientaJava/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from Compilador import ErrorCompilación

raízProyecto = Path(__file__).resolve().parent

class CompiladorCódigoMáquina:
    def __init__(valorPropio, clasesEntrada, objetivoEjecución='kernel', númeroElementosPalabraMontículo=262144):
        valorPropio.listaRuta = [Datos.ruta for Datos in clasesEntrada]
        valorPropio.objetivoEjecución = objetivoEjecución
        valorPropio.númeroElementosPalabraMontículo = númeroElementosPalabraMontículo

    def generar(valorPropio, puntoEntradaElemento, entradasExportar, notaciónCarácterUniversal=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as Tarea:
            rutaResultado = Path(Tarea)/'generated.c'
            comando = ['sh', str(raízProyecto/'tiempoDeAnticipado.sh'), '--entry', puntoEntradaElemento,
                    '--profile', valorPropio.objetivoEjecución, '--heap-words', str(valorPropio.númeroElementosPalabraMontículo), '-o', str(rutaResultado)]
            if notaciónCarácterUniversal: comando.append('--ucn')
            for valorAsignar in entradasExportar: comando.extend(['--export', valorAsignar])
            comando.extend(str(ruta) for ruta in valorPropio.listaRuta)
            resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if resultado.returncode: raise ErrorCompilación(resultado.stderr.decode('utf-8', 'replace'))
            return rutaResultado.read_text()

def ponerEnMarcha():
    raise SystemExit(subprocess.call(['sh', str(raízProyecto/'tiempoDeAnticipado.sh')] + sys.argv[1:]))

if __name__ == '__main__': ponerEnMarcha()
