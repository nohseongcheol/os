#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from teste_Usenet import VM, posição
from 자바시험 import Editar_VALOR, convidado_Arquivo

def Executar_comando():
    resultado = {}
    códigoFonte = (posição.parent / 'posix-kor/자바예제/FileDemo.java').read_text()
    for Tipo_VALOR in ('elf', 'iso'):
        computador = VM(posição / ('build/kernel.' + Tipo_VALOR), Tipo_VALOR, rede_VALOR=False)
        try:
            Editar_VALOR(computador, 'FileDemo.java', códigoFonte)
            computador.comando('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for sprint_VALOR in range(2):
                saídaTexto = computador.comando('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            entrada_Lista_f07b3200 = computador.comando('ls', ['java.txt  3 bytes'])
            Tamanho = int(re.search(r'FileDemo.class\s+(\d+) bytes', entrada_Lista_f07b3200)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 임시:
                Diretório_VALOR = Path(임시)
                convidado_Arquivo(computador, 2, Tamanho, Diretório_VALOR / 'FileDemo.class')
                host = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Diretório_VALOR), 'FileDemo'], cwd=str(Diretório_VALOR), universal_newlines=True)
                assert host == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', host
                assert (Diretório_VALOR / 'java.txt').read_bytes() == b'A\xffB'
            Editar_VALOR(computador, 'FileDemo.java', códigoFonte.replace('output.write(65);', 'output.close(); output.write(65);'))
            computador.comando('javac FileDemo.java', ['Exit: 0'])
            computador.comando('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            Editar_VALOR(computador, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            computador.comando('javac FileDemo.java', ['Exit: 0'])
            computador.comando('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            computador.comando('run hello recovered', ['Exit: 0'])
            resultado[Tipo_VALOR] = computador.LOG_linha.decode('utf-8', 'replace')
        finally:
            computador.Fechar()
        print('PASS:', Tipo_VALOR, '게스트 Java ficheiro gerar/이어쓰기/byte_VALOR/EOF/TI_fechado/falha_VALOR/OpenJDK 교차 Executar_comando', flush=True)
    (posição / 'build/자바파일시험.json').write_text(json.dumps(resultado, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Executar_comando()
