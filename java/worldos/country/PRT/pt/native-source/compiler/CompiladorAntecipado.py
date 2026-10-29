#!/usr/bin/env python3
"""Anterior_item Python 경로를 Java 미리 번역기에 연결한다. mover_fonte 구현은 FerramentasJava/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from compilador import erro_de_compilação

ação_raiz = Path(__file__).resolve().parent

class computador_CÓDIGO_compilador:
    def __init__(자신, 입력클래스들, execução_alvo='kernel', heap_Contagem_de_Palavras=262144):
        자신.caminho_Lista = [dados.caminho for dados in 입력클래스들]
        자신.execução_alvo = execução_alvo
        자신.heap_Contagem_de_Palavras = heap_Contagem_de_Palavras

    def gerar(자신, ponto_de_entrada, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            RC_caminho = Path(작업)/'generated.c'
            comando = ['sh', str(ação_raiz/'미리번역.sh'), '--entry', ponto_de_entrada,
                    '--profile', 자신.execução_alvo, '--heap-words', str(자신.heap_Contagem_de_Palavras), '-o', str(RC_caminho)]
            if 범용문자표기: comando.append('--ucn')
            for ceder_VALOR in 내보내기목록: comando.extend(['--export', ceder_VALOR])
            comando.extend(str(caminho) for caminho in 자신.caminho_Lista)
            resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if resultado.returncode: raise erro_de_compilação(resultado.stderr.decode('utf-8', 'replace'))
            return RC_caminho.read_text()

def iniciar():
    raise SystemExit(subprocess.call(['sh', str(ação_raiz/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': iniciar()
