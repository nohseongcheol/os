#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import màquina_virtual, Posició
from 자바시험 import Editar_VALOR, convidat_arxiu

def Executa_ordre():
    RESULTAT = {}
    FONT = (Posició.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        màquina = màquina_virtual(Posició / ('build/kernel.' + 종류), 종류, xarxa_VALOR=False)
        try:
            Editar_VALOR(màquina, 'FileDemo.java', FONT)
            màquina.Ordre('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for esprint_VALOR in range(2):
                Sortida = màquina.Ordre('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            introducció_Llista = màquina.Ordre('ls', ['java.txt  3 bytes'])
            Mida = int(re.search(r'FileDemo.class\s+(\d+) bytes', introducció_Llista)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                directori_VALOR = Path(임시)
                convidat_arxiu(màquina, 2, Mida, directori_VALOR / 'FileDemo.class')
                allotjar = subprocess.check_output(['java', '-Xverify:all', '-cp', str(directori_VALOR), 'FileDemo'], cwd=str(directori_VALOR), universal_newlines=True)
                assert allotjar == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', allotjar
                assert (directori_VALOR / 'java.txt').read_bytes() == b'A\xffB'
            Editar_VALOR(màquina, 'FileDemo.java', FONT.replace('output.write(65);', 'output.close(); output.write(65);'))
            màquina.Ordre('javac FileDemo.java', ['Exit: 0'])
            màquina.Ordre('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            Editar_VALOR(màquina, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            màquina.Ordre('javac FileDemo.java', ['Exit: 0'])
            màquina.Ordre('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            màquina.Ordre('run hello recovered', ['Exit: 0'])
            RESULTAT[종류] = màquina.LOG_fila.decode('utf-8', 'replace')
        finally:
            màquina.Tanca()
        print('PASS:', 종류, '게스트 Java Fitxer generar/이어쓰기/byte_VALOR/EOF/닫힘/error_VALOR/OpenJDK 교차 Executa_ordre', flush=True)
    (Posició / 'build/자바파일시험.json').write_text(json.dumps(RESULTAT, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Executa_ordre()
