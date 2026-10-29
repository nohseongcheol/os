#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 사용자통신시험 import máquina_virtual, Posición
from 자바시험 import editar_VALOR, convidado_Ficheiro

def executar_comando():
    RESULTANTE = {}
    FONTE = (Posición.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for 종류 in ('elf', 'iso'):
        máquina = máquina_virtual(Posición / ('build/kernel.' + 종류), 종류, Rede_VALOR=False)
        try:
            editar_VALOR(máquina, 'FileDemo.java', FONTE)
            máquina.Orde('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for sprint_VALOR in range(2):
                Saída = máquina.Orde('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            introdución_Lista = máquina.Orde('ls', ['java.txt  3 bytes'])
            Tamaño = int(re.search(r'FileDemo.class\s+(\d+) bytes', introdución_Lista)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                directorio_VALOR = Path(임시)
                convidado_Ficheiro(máquina, 2, Tamaño, directorio_VALOR / 'FileDemo.class')
                hospedar = subprocess.check_output(['java', '-Xverify:all', '-cp', str(directorio_VALOR), 'FileDemo'], cwd=str(directorio_VALOR), universal_newlines=True)
                assert hospedar == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', hospedar
                assert (directorio_VALOR / 'java.txt').read_bytes() == b'A\xffB'
            editar_VALOR(máquina, 'FileDemo.java', FONTE.replace('output.write(65);', 'output.close(); output.write(65);'))
            máquina.Orde('javac FileDemo.java', ['Exit: 0'])
            máquina.Orde('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            editar_VALOR(máquina, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            máquina.Orde('javac FileDemo.java', ['Exit: 0'])
            máquina.Orde('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            máquina.Orde('run hello recovered', ['Exit: 0'])
            RESULTANTE[종류] = máquina.LOG_fila.decode('utf-8', 'replace')
        finally:
            máquina.Pechar()
        print('PASS:', 종류, '게스트 Java Ficheiro xerar/이어쓰기/byte_VALOR/EOF/닫힘/erro_VALOR/OpenJDK 교차 executar_comando', flush=True)
    (Posición / 'build/자바파일시험.json').write_text(json.dumps(RESULTANTE, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    executar_comando()
