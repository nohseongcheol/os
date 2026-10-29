#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 executar_comando, erro_VALOR/Recurso_VALOR 경계 시험."""
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
from 사용자통신시험 import máquina_virtual, Posición


def editar_VALOR(máquina, Nome, Contido_VALOR, Store_VALOR=True):
    Executar_2 = len(máquina.LOG_fila)
    máquina.직렬.sendall(('edit ' + Nome + '\n').encode())
    máquina.agarda_Estado('...> ', Executar_2)
    for Liña in Contido_VALOR.splitlines():
        assert len(Liña) <= 128
        Executar_2 = len(máquina.LOG_fila)
        máquina.직렬.sendall((Liña + '\n').encode())
        máquina.agarda_Estado('...> ', Executar_2)
    Executar_2 = len(máquina.LOG_fila)
    máquina.직렬.sendall(b'.save\n' if Store_VALOR else b'.cancel\n')
    RESULTANTE = máquina.agarda_Estado('jkoros> ', Executar_2)
    assert ('Saved:' if Store_VALOR else 'Cancelled; original preserved') in RESULTANTE, RESULTANTE


def Ficheiro_ENDEREZO():
    RESULTANTE = subprocess.check_output(['nm', '-n', str(Posición / 'build/kernel.elf')], universal_newlines=True)
    for Liña in RESULTANTE.splitlines():
        if Liña.endswith(' ram_files'):
            return int(Liña.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def convidado_Ficheiro(máquina, 슬롯, Tamaño, CAMIÑO):
    # 시험 VM의 메모리에서 real_datos 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ENDEREZO = Ficheiro_ENDEREZO() + 슬롯 * 16384
    máquina.monitor_VALOR.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ENDEREZO, Tamaño, CAMIÑO)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if CAMIÑO.exists() and CAMIÑO.stat().st_size == Tamaño:
            return CAMIÑO.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    máquina = máquina_virtual(Posición / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Rede_VALOR=False)
    RESULTANTE = {}
    try:
        máquina.Orde('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        máquina.Orde('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        máquina.Orde('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        máquina.Orde('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        máquina.Orde('java Missing', ['cannot read class: -2', 'Exit: 1'])
        máquina.Orde('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        máquina.Orde('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Contido_VALOR = '''public class Calc {
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
        editar_VALOR(máquina, 'Calc.java', Contido_VALOR)
        máquina.Orde('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Saída = máquina.Orde('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        RESULTANTE['guest_output'] = Saída
        introdución_Lista = máquina.Orde('ls', ['Calc.class'])
        Tamaño = int(re.search(r'Calc\.class\s+(\d+) bytes', introdución_Lista).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as directorio_VALOR:
            CAMIÑO = Path(directorio_VALOR) / 'Calc.class'
            datos = convidado_Ficheiro(máquina, 3, Tamaño, CAMIÑO)
            real_datos = subprocess.check_output(['java', '-Xverify:all', '-cp', directorio_VALOR, 'Calc', '6', 'guest'], universal_newlines=True)
            assert real_datos.splitlines() == 기대, real_datos
            RESULTANTE['class_sha256'] = hashlib.sha256(datos).hexdigest()
            RESULTANTE['openjdk_output'] = real_datos
        # 실패한 editar_VALOR/컴파일은 기존 class를 보존한다.
        editar_VALOR(máquina, 'Calc.java', 'not Java at all', Store_VALOR=False)
        máquina.Orde('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for non_válido_medida in [
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
            editar_VALOR(máquina, 'Calc.java', non_válido_medida)
            máquina.Orde('javac Calc.java', ['javac error:', 'Exit: 1'])
            máquina.Orde('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # sprint_VALOR 실행은 usuario 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            máquina.Orde('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        máquina.Orde('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        máquina.Orde('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        editar_VALOR(máquina, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        máquina.Orde('javac Calc.java', ['Compiled:', 'Exit: 0'])
        máquina.Orde('java Calc', ['instruction limit', 'Exit: 1'])
        máquina.Orde('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        editar_VALOR(máquina, 'Bad.class', 'garbage')
        máquina.Orde('java Bad', ['JVM error:', 'Exit: 1'])
        máquina.Orde('rm Bad.class', ['Removed'])
        máquina.Orde('java Bad', ['cannot read class: -2'])
        # editar_VALOR 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Executar_2 = len(máquina.LOG_fila)
        máquina.직렬.sendall(b'edit Hello.java\n')
        máquina.agarda_Estado('...> ', Executar_2)
        Executar_2 = len(máquina.LOG_fila)
        máquina.직렬.sendall(b'x' * 129 + b'\n')
        máquina.agarda_Estado('...> ', Executar_2)
        máquina.Orde('.save', ['Too much input; original preserved'])
        máquina.Orde('javac Hello.java', ['Compiled:', 'Exit: 0'])
        editar_VALOR(máquina, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            editar_VALOR(máquina, 'f' + str(수), 'occupied')
        máquina.Orde('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        máquina.Orde('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in máquina.LOG_fila.decode('utf-8', 'replace')
        RESULTANTE['serial'] = máquina.LOG_fila.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return RESULTANTE
    finally:
        máquina.Pechar()


def 주코드(datos):
    """손상 시험용 main Code의 real_datos Ficheiro 오프셋/길이만 읽는다."""
    cargo_VALOR = 8
    def 짧():
        nonlocal cargo_VALOR
        VALOR = struct.unpack_from('>H', datos, cargo_VALOR)[0]
        cargo_VALOR += 2
        return VALOR
    def 정():
        nonlocal cargo_VALOR
        VALOR = struct.unpack_from('>I', datos, cargo_VALOR)[0]
        cargo_VALOR += 4
        return VALOR
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = datos[cargo_VALOR]
        cargo_VALOR += 1
        if 종류 == 1:
            duración_VALOR = 짧()
            문자들[수] = datos[cargo_VALOR:cargo_VALOR + duración_VALOR]
            cargo_VALOR += duración_VALOR
        elif 종류 in (7, 8): cargo_VALOR += 2
        elif 종류 in (3, 9, 10, 12): cargo_VALOR += 4
        else: raise AssertionError(종류)
    cargo_VALOR += 6
    elemento_CONTAR = 짧()
    cargo_VALOR += elemento_CONTAR * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Nome = 짧()
        짧()
        for 수 in range(짧()):
            atributo_VALOR = 짧()
            Tamaño = 정()
            if 문자들[Nome] == b'main' and 문자들[atributo_VALOR] == b'Code':
                return cargo_VALOR + 8, struct.unpack_from('>I', datos, cargo_VALOR + 4)[0]
            cargo_VALOR += Tamaño
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        directorio_VALOR = Path(임시)
        (directorio_VALOR / 'build').mkdir()
        FONTE = directorio_VALOR / 'Imported.java'
        FONTE.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(FONTE)], check=True)
        원본 = (directorio_VALOR / 'Imported.class').read_bytes()
        CÓDIGO_VALOR, duración_VALOR = 주코드(원본)
        변형 = {}
        datos = bytearray(원본); datos[0] = 0; 변형['BadMagic'] = datos
        datos = bytearray(원본); datos[7] = 61; 변형['BadVer'] = datos
        datos = bytearray(원본); datos[8:10] = b'\xff\xff'; 변형['BadPool'] = datos
        datos = bytearray(원본); datos[CÓDIGO_VALOR:CÓDIGO_VALOR + duración_VALOR] = bytes(duración_VALOR)
        datos[CÓDIGO_VALOR:CÓDIGO_VALOR + 3] = b'\xa7\x00\x01'; datos[CÓDIGO_VALOR + duración_VALOR - 1] = 177; 변형['BadJump'] = datos
        datos = bytearray(원본); datos[CÓDIGO_VALOR:CÓDIGO_VALOR + duración_VALOR] = bytes(duración_VALOR)
        datos[CÓDIGO_VALOR] = 87; datos[CÓDIGO_VALOR + duración_VALOR - 1] = 177; 변형['BadStack'] = datos
        # Nome 검사를 통과시켜 real_datos executar_comando 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        introdución_VALOR = ['Imported.class=' + str(directorio_VALOR / 'Imported.class'), 'Imported.java=' + str(FONTE)]
        for Nome, datos in 변형.items():
            CAMIÑO = directorio_VALOR / (Nome + '.class'); CAMIÑO.write_bytes(datos)
            introdución_VALOR.append(Nome + '.class=' + str(CAMIÑO))
        Grupo_VALOR = directorio_VALOR / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Posición / 'Ferramentas/자바파일묶기.py'), '-o', str(Grupo_VALOR)] + introdución_VALOR, check=True)
        subprocess.run(['as', '--32', '-o', str(directorio_VALOR / 'user.o'), str(Posición / '부팅/usuario.s')], cwd=str(directorio_VALOR), check=True)
        kernel_VALOR = directorio_VALOR / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Posición / '부팅/Ligar_deseño.ld'), '-o', str(kernel_VALOR),
                        str(Posición / 'build/boot.o'), str(Posición / 'build/java.o'), str(directorio_VALOR / 'user.o'), str(Posición / 'build/apps.o')], check=True)
        máquina = máquina_virtual(kernel_VALOR, Rede_VALOR=False)
        try:
            máquina.Orde('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            máquina.Orde('cat Imported.java', ['int[] values = new int[3]'])
            for Nome, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                máquina.Orde('java ' + Nome, [문구, 'Exit: 1'])
                máquina.Orde('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return máquina.LOG_fila.decode('utf-8', 'replace')
        finally:
            máquina.Pechar()


if __name__ == '__main__':
    analizar_VALOR = argparse.ArgumentParser()
    analizar_VALOR.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    Argumentos = analizar_VALOR.parse_args()
    RESULTANTE = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if Argumentos.boot == 'both' else (Argumentos.boot,))}
    RESULTANTE['import'] = 적재시험()
    (Posición / 'build/자바시험.json').write_text(json.dumps(RESULTANTE, ensure_ascii=False, indent=2) + '\n')
