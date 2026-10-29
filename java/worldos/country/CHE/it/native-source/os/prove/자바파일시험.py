#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from test_Usenet import VM, posizione
from 자바시험 import Modifica_VALORE, guest_File

def Esegui_comando():
    risultato = {}
    codiceSorgente = (posizione.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for Kind_VALORE in ('elf', 'iso'):
        computer = VM(posizione / ('build/kernel.' + Kind_VALORE), Kind_VALORE, rete_VALORE=False)
        try:
            Modifica_VALORE(computer, 'FileDemo.java', codiceSorgente)
            computer.comando('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for sprint_VALORE in range(2):
                uscitaTesto = computer.comando('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            voce_elenco = computer.comando('ls', ['java.txt  3 bytes'])
            Dimensione = int(re.search(r'FileDemo.class\s+(\d+) bytes', voce_elenco)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                elenco_VALORE = Path(임시)
                guest_File(computer, 2, Dimensione, elenco_VALORE / 'FileDemo.class')
                host = subprocess.check_output(['java', '-Xverify:all', '-cp', str(elenco_VALORE), 'FileDemo'], cwd=str(elenco_VALORE), universal_newlines=True)
                assert host == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', host
                assert (elenco_VALORE / 'java.txt').read_bytes() == b'A\xffB'
            Modifica_VALORE(computer, 'FileDemo.java', codiceSorgente.replace('output.write(65);', 'output.close(); output.write(65);'))
            computer.comando('javac FileDemo.java', ['Exit: 0'])
            computer.comando('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            Modifica_VALORE(computer, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            computer.comando('javac FileDemo.java', ['Exit: 0'])
            computer.comando('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            computer.comando('run hello recovered', ['Exit: 0'])
            risultato[Kind_VALORE] = computer.LOG_riga.decode('utf-8', 'replace')
        finally:
            computer.Chiudi()
        print('PASS:', Kind_VALORE, '게스트 Java file generare/이어쓰기/byte_VALORE/EOF/reparto_IT_chiusa/errore_VALORE/OpenJDK 교차 Esegui_comando', flush=True)
    (posizione / 'build/자바파일시험.json').write_text(json.dumps(risultato, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Esegui_comando()
