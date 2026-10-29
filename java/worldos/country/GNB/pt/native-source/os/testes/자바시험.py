#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Executar_comando, falha_VALOR/recurso_VALOR limite_VALOR testes."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile
import time
from teste_Usenet import VM, posição


def Editar_VALOR(computador, Nome, Conteúdo_VALOR, Store_VALOR=True):
    iniciar = len(computador.LOG_linha)
    computador.직렬.sendall(('edit ' + Nome + '\n').encode())
    computador.estado_de_espera('...> ', iniciar)
    for linha_de_entrada in Conteúdo_VALOR.splitlines():
        assert len(linha_de_entrada) <= 128
        iniciar = len(computador.LOG_linha)
        computador.직렬.sendall((linha_de_entrada + '\n').encode())
        computador.estado_de_espera('...> ', iniciar)
    iniciar = len(computador.LOG_linha)
    computador.직렬.sendall(b'.save\n' if Store_VALOR else b'.cancel\n')
    resultado = computador.estado_de_espera('jkoros> ', iniciar)
    assert ('Saved:' if Store_VALOR else 'Cancelled; original preserved') in resultado, resultado


def Arquivo_email():
    resultado = subprocess.check_output(['nm', '-n', str(posição / 'build/kernel.elf')], universal_newlines=True)
    for linha_de_entrada in resultado.splitlines():
        if linha_de_entrada.endswith(' ram_files'):
            return int(linha_de_entrada.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def convidado_Arquivo(computador, slot_VALOR, Tamanho, caminho):
    # testes VM의 메모리에서 real_dados 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    Endereço = Arquivo_email() + slot_VALOR * 16384
    computador.monitor_VALOR.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(Endereço, Tamanho, caminho)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if caminho.exists() and caminho.stat().st_size == Tamanho:
            return caminho.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def execução_de_teste(Tipo_VALOR):
    computador = VM(posição / ('build/kernel.elf' if Tipo_VALOR == 'elf' else 'build/kernel.iso'), Tipo_VALOR, rede_VALOR=False)
    resultado = {}
    try:
        computador.comando('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        computador.comando('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        computador.comando('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        computador.comando('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        computador.comando('java Missing', ['cannot read class: -2', 'Exit: 1'])
        computador.comando('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        computador.comando('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Conteúdo_VALOR = '''public class Calc {
 public static int fact(int n) {
  if (n <= 1) { return 1; } else { return n * fact(n - 1); }
 }
 public static boolean check(int n) { return n == 7; }
 public static void main(String[] args) {
  int n = Integer.parseInt(args[0]);
  System.out.println(fact(n));
  int sum = 0;
  for (int i = 1; i <= n; i++) { sum = sum + i; }
  while (n > 0) { n--; }
  System.out.println(sum);
  System.out.println(n);
  System.out.println(check(7) && false || true);
  System.out.println(false && 1 / 0 == 0);
  System.out.println(true || 1 / 0 == 0);
  System.out.println(-2147483648 / -1);
  System.out.println(args[1]);
  System.out.println(args[1].length());
  System.out.println(args.length);
  String label = "sum=";
  label += sum;
  System.out.println(label);
  System.out.println(12 + "x" + false);
  System.out.println("logic=" + (true && check(7)));
  char letter = 'a';
  letter++;
  System.out.println(letter);
  System.out.println("letter=" + letter);
  int extra = 7;
  extra *= 3;
  extra -= 1;
  System.out.println(extra);
 }
}'''
        Editar_VALOR(computador, 'Calc.java', Conteúdo_VALOR)
        computador.comando('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        saídaTexto = computador.comando('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        resultado['guest_output'] = saídaTexto
        entrada_Lista_f07b3200 = computador.comando('ls', ['Calc.class'])
        Tamanho = int(re.search(r'Calc\.class\s+(\d+) bytes', entrada_Lista_f07b3200).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as Diretório_VALOR:
            caminho = Path(Diretório_VALOR) / 'Calc.class'
            dados = convidado_Arquivo(computador, 3, Tamanho, caminho)
            real_dados = subprocess.check_output(['java', '-Xverify:all', '-cp', Diretório_VALOR, 'Calc', '6', 'guest'], universal_newlines=True)
            assert real_dados.splitlines() == 기대, real_dados
            resultado['class_sha256'] = hashlib.sha256(dados).hexdigest()
            resultado['openjdk_output'] = real_dados
        # 실패한 Editar_VALOR/컴파일은 기존 class를 보존한다.
        Editar_VALOR(computador, 'Calc.java', 'not Java at all', Store_VALOR=False)
        computador.comando('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for inválido_RC in [
            'public class Calc { public static void main(String[] args) { int x = ; } }',
            'public class Calc { public static void main(String[] args) { int x = true; } }',
            'public class Calc { public static void main(String[] args) { int x = 2147483648; } }',
            'public class Calc { public static int f() { int x = 1; } }',
            'public class Calc { public static void main(String[] args) { Object x = new Object(); } }',
            'public class Other { public static void main(String[] args) {} }',
            'public class Calc { public static void main(String[] args) { int while = 3; } }',
            'public class Calc { public static void main(String[] args) { if (true) int x = 3; } }',
            'public class Calc { public static void main(String[] args) { int x = 010; } }',
        ]:
            Editar_VALOR(computador, 'Calc.java', inválido_RC)
            computador.comando('javac Calc.java', ['javac error:', 'Exit: 1'])
            computador.comando('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # sprint_VALOR 실행은 espaço_do_utilizador heap_VALOR/프레임을 매번 초기화한다.
        for número in range(12):
            computador.comando('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        computador.comando('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        computador.comando('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        Editar_VALOR(computador, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        computador.comando('javac Calc.java', ['Compiled:', 'Exit: 0'])
        computador.comando('java Calc', ['instruction limit', 'Exit: 1'])
        computador.comando('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        Editar_VALOR(computador, 'Bad.class', 'garbage')
        computador.comando('java Bad', ['JVM error:', 'Exit: 1'])
        computador.comando('rm Bad.class', ['Removed'])
        computador.comando('java Bad', ['cannot read class: -2'])
        # Editar_VALOR 입력의 넘친 부분을 잘라서 저장하지 않는다.
        iniciar = len(computador.LOG_linha)
        computador.직렬.sendall(b'edit Hello.java\n')
        computador.estado_de_espera('...> ', iniciar)
        iniciar = len(computador.LOG_linha)
        computador.직렬.sendall(b'x' * 129 + b'\n')
        computador.estado_de_espera('...> ', iniciar)
        computador.comando('.save', ['Too much input; original preserved'])
        computador.comando('javac Hello.java', ['Compiled:', 'Exit: 0'])
        Editar_VALOR(computador, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for número in range(3):
            Editar_VALOR(computador, 'f' + str(número), 'occupied')
        computador.comando('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        computador.comando('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in computador.LOG_linha.decode('utf-8', 'replace')
        resultado['serial'] = computador.LOG_linha.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(Tipo_VALOR))
        return resultado
    finally:
        computador.Fechar()


def 주코드(dados):
    """손상 시험용 main Code의 real_dados ficheiro 오프셋/길이만 읽는다."""
    cargo_VALOR = 8
    def 짧():
        nonlocal cargo_VALOR
        VALOR = struct.unpack_from('>H', dados, cargo_VALOR)[0]
        cargo_VALOR += 2
        return VALOR
    def leitura_inteiro_sem_sinal():
        nonlocal cargo_VALOR
        VALOR = struct.unpack_from('>I', dados, cargo_VALOR)[0]
        cargo_VALOR += 4
        return VALOR
    문자들 = {}
    for número in range(1, 짧()):
        Tipo_VALOR = dados[cargo_VALOR]
        cargo_VALOR += 1
        if Tipo_VALOR == 1:
            duração_VALOR = 짧()
            문자들[número] = dados[cargo_VALOR:cargo_VALOR + duração_VALOR]
            cargo_VALOR += duração_VALOR
        elif Tipo_VALOR in (7, 8): cargo_VALOR += 2
        elif Tipo_VALOR in (3, 9, 10, 12): cargo_VALOR += 4
        else: raise AssertionError(Tipo_VALOR)
    cargo_VALOR += 6
    item_CONT_NÚM = 짧()
    cargo_VALOR += item_CONT_NÚM * 2
    assert 짧() == 0
    for número in range(짧()):
        짧()
        Nome = 짧()
        짧()
        for número in range(짧()):
            valor_do_atributo = 짧()
            Tamanho = leitura_inteiro_sem_sinal()
            if 문자들[Nome] == b'main' and 문자들[valor_do_atributo] == b'Code':
                return cargo_VALOR + 8, struct.unpack_from('>I', dados, cargo_VALOR + 4)[0]
            cargo_VALOR += Tamanho
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        Diretório_VALOR = Path(임시)
        (Diretório_VALOR / 'build').mkdir()
        códigoFonte = Diretório_VALOR / 'Imported.java'
        códigoFonte.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(códigoFonte)], check=True)
        원본 = (Diretório_VALOR / 'Imported.class').read_bytes()
        valor_do_código, duração_VALOR = 주코드(원본)
        grade_VALOR = {}
        dados = bytearray(원본); dados[0] = 0; grade_VALOR['BadMagic'] = dados
        dados = bytearray(원본); dados[7] = 61; grade_VALOR['BadVer'] = dados
        dados = bytearray(원본); dados[8:10] = b'\xff\xff'; grade_VALOR['BadPool'] = dados
        dados = bytearray(원본); dados[valor_do_código:valor_do_código + duração_VALOR] = bytes(duração_VALOR)
        dados[valor_do_código:valor_do_código + 3] = b'\xa7\x00\x01'; dados[valor_do_código + duração_VALOR - 1] = 177; grade_VALOR['BadJump'] = dados
        dados = bytearray(원본); dados[valor_do_código:valor_do_código + duração_VALOR] = bytes(duração_VALOR)
        dados[valor_do_código] = 87; dados[valor_do_código + duração_VALOR - 1] = 177; grade_VALOR['BadStack'] = dados
        # Nome 검사를 통과시켜 real_dados Executar_comando 중의 operando_pilha 오류까지 검사한다.
        grade_VALOR['BadStack'] = grade_VALOR['BadStack'].replace(b'Imported', b'BadStack')
        entrada_VALOR_962f286b = ['Imported.class=' + str(Diretório_VALOR / 'Imported.class'), 'Imported.java=' + str(códigoFonte)]
        for Nome, dados in grade_VALOR.items():
            caminho = Diretório_VALOR / (Nome + '.class'); caminho.write_bytes(dados)
            entrada_VALOR_962f286b.append(Nome + '.class=' + str(caminho))
        Grupo_VALOR = Diretório_VALOR / 'build/java-files.bin'
        subprocess.run([sys.executable, str(posição / 'ferramentas/자바파일묶기.py'), '-o', str(Grupo_VALOR)] + entrada_VALOR_962f286b, check=True)
        subprocess.run(['as', '--32', '-o', str(Diretório_VALOR / 'user.o'), str(posição / 'arranque_da_máquina/espaço_do_utilizador.s')], cwd=str(Diretório_VALOR), check=True)
        kernel_VALOR = Diretório_VALOR / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(posição / 'arranque_da_máquina/disposição_de_ligação.ld'), '-o', str(kernel_VALOR),
                        str(posição / 'build/boot.o'), str(posição / 'build/java.o'), str(Diretório_VALOR / 'user.o'), str(posição / 'build/apps.o')], check=True)
        computador = VM(kernel_VALOR, rede_VALOR=False)
        try:
            computador.comando('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            computador.comando('cat Imported.java', ['int[] values = new int[3]'])
            for Nome, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                computador.comando('java ' + Nome, [문구, 'Exit: 1'])
                computador.comando('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return computador.LOG_linha.decode('utf-8', 'replace')
        finally:
            computador.Fechar()


if __name__ == '__main__':
    analisar_VALOR = argparse.ArgumentParser()
    analisar_VALOR.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    argumentos = analisar_VALOR.parse_args()
    resultado = {Tipo_VALOR: execução_de_teste(Tipo_VALOR) for Tipo_VALOR in (('elf', 'iso') if argumentos.boot == 'both' else (argumentos.boot,))}
    resultado['import'] = 적재시험()
    (posição / 'build/자바시험.json').write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n')
