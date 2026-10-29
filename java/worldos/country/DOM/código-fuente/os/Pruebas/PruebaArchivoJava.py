#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from pruebaRedUsuario import MáquinaVirtual, posición
from PruebaJava import valorEditar, archivoInvitado

def ejecutarComando():
    resultado = {}
    fuente = (posición.parent / 'posix-kor/EjemploJava/FileDemo.java').read_text()
    for valorClaseTipo in ('elf', 'iso'):
        máquina = MáquinaVirtual(posición / ('build/kernel.' + valorClaseTipo), valorClaseTipo, valorRed=False)
        try:
            valorEditar(máquina, 'FileDemo.java', fuente)
            máquina.comando('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for valorIteración in range(2):
                Salida = máquina.comando('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            listaEntradaElemento = máquina.comando('ls', ['java.txt  3 bytes'])
            tamaño = int(re.search(r'FileDemo.class\s+(\d+) bytes', listaEntradaElemento)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as valorTemporal:
                valorDirectorio = Path(valorTemporal)
                archivoInvitado(máquina, 2, tamaño, valorDirectorio / 'FileDemo.class')
                Anfitrión = subprocess.check_output(['java', '-Xverify:all', '-cp', str(valorDirectorio), 'FileDemo'], cwd=str(valorDirectorio), universal_newlines=True)
                assert Anfitrión == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', Anfitrión
                assert (valorDirectorio / 'java.txt').read_bytes() == b'A\xffB'
            valorEditar(máquina, 'FileDemo.java', fuente.replace('output.write(65);', 'output.close(); output.write(65);'))
            máquina.comando('javac FileDemo.java', ['Exit: 0'])
            máquina.comando('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            valorEditar(máquina, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            máquina.comando('javac FileDemo.java', ['Exit: 0'])
            máquina.comando('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            máquina.comando('run hello recovered', ['Exit: 0'])
            resultado[valorClaseTipo] = máquina.registroEntradaDiario.decode('utf-8', 'replace')
        finally:
            máquina.cerrar()
        print('PASS:', valorClaseTipo, '게스트 Java Archivo generar/añadirFinalContinuación/valorByte/EOF/esCerrado/valorFallo/OpenJDK 교차 ejecutarComando', flush=True)
    (posición / 'build/PruebaArchivoJava.json').write_text(json.dumps(resultado, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ejecutarComando()
