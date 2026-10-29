#!/usr/bin/env python3
"""Indietro_articolo Python 경로를 Java 미리 번역기에 연결한다. TRADUCI_fonte 구현은 자바도구/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from compilatore import errore_di_compilazione

azione_radice = Path(__file__).resolve().parent

class computer_CODICE_compilatore:
    def __init__(자신, 입력클래스들, esecuzione_target='kernel', heap_Conteggio_parole=262144):
        자신.percorso_elenco = [dati.percorso for dati in 입력클래스들]
        자신.esecuzione_target = esecuzione_target
        자신.heap_Conteggio_parole = heap_Conteggio_parole

    def generare(자신, punto_di_ingresso, 내보내기목록, 범용문자표기=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as 작업:
            KR_percorso = Path(작업)/'generated.c'
            comando = ['sh', str(azione_radice/'미리번역.sh'), '--entry', punto_di_ingresso,
                    '--profile', 자신.esecuzione_target, '--heap-words', str(자신.heap_Conteggio_parole), '-o', str(KR_percorso)]
            if 범용문자표기: comando.append('--ucn')
            for Assegna_VALORE in 내보내기목록: comando.extend(['--export', Assegna_VALORE])
            comando.extend(str(percorso) for percorso in 자신.percorso_elenco)
            risultato = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if risultato.returncode: raise errore_di_compilazione(risultato.stderr.decode('utf-8', 'replace'))
            return KR_percorso.read_text()

def avvia():
    raise SystemExit(subprocess.call(['sh', str(azione_radice/'미리번역.sh')] + sys.argv[1:]))

if __name__ == '__main__': avvia()
