#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Executa_ordre, error_VALOR/recurs_VALOR 경계 시험."""
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
from 사용자통신시험 import màquina_virtual, Posició


def Editar_VALOR(màquina, Nom, contingut_VALOR, Store_VALOR=True):
    Executa_2 = len(màquina.LOG_fila)
    màquina.직렬.sendall(('edit ' + Nom + '\n').encode())
    màquina.Espera_Estat('...> ', Executa_2)
    for línia in contingut_VALOR.splitlines():
        assert len(línia) <= 128
        Executa_2 = len(màquina.LOG_fila)
        màquina.직렬.sendall((línia + '\n').encode())
        màquina.Espera_Estat('...> ', Executa_2)
    Executa_2 = len(màquina.LOG_fila)
    màquina.직렬.sendall(b'.save\n' if Store_VALOR else b'.cancel\n')
    RESULTAT = màquina.Espera_Estat('jkoros> ', Executa_2)
    assert ('Saved:' if Store_VALOR else 'Cancelled; original preserved') in RESULTAT, RESULTAT


def arxiu_ADREÇA():
    RESULTAT = subprocess.check_output(['nm', '-n', str(Posició / 'build/kernel.elf')], universal_newlines=True)
    for línia in RESULTAT.splitlines():
        if línia.endswith(' ram_files'):
            return int(línia.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def convidat_arxiu(màquina, 슬롯, Mida, Camí):
    # 시험 VM의 메모리에서 real_dades 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    Adreça = arxiu_ADREÇA() + 슬롯 * 16384
    màquina.monitor_VALOR.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(Adreça, Mida, Camí)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if Camí.exists() and Camí.stat().st_size == Mida:
            return Camí.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    màquina = màquina_virtual(Posició / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, xarxa_VALOR=False)
    RESULTAT = {}
    try:
        màquina.Ordre('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        màquina.Ordre('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        màquina.Ordre('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        màquina.Ordre('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        màquina.Ordre('java Missing', ['cannot read class: -2', 'Exit: 1'])
        màquina.Ordre('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        màquina.Ordre('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        contingut_VALOR = '''public class Calc {
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
        Editar_VALOR(màquina, 'Calc.java', contingut_VALOR)
        màquina.Ordre('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Sortida = màquina.Ordre('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        RESULTAT['guest_output'] = Sortida
        introducció_Llista = màquina.Ordre('ls', ['Calc.class'])
        Mida = int(re.search(r'Calc\.class\s+(\d+) bytes', introducció_Llista).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as directori_VALOR:
            Camí = Path(directori_VALOR) / 'Calc.class'
            dades = convidat_arxiu(màquina, 3, Mida, Camí)
            real_dades = subprocess.check_output(['java', '-Xverify:all', '-cp', directori_VALOR, 'Calc', '6', 'guest'], universal_newlines=True)
            assert real_dades.splitlines() == 기대, real_dades
            RESULTAT['class_sha256'] = hashlib.sha256(dades).hexdigest()
            RESULTAT['openjdk_output'] = real_dades
        # 실패한 Editar_VALOR/컴파일은 기존 class를 보존한다.
        Editar_VALOR(màquina, 'Calc.java', 'not Java at all', Store_VALOR=False)
        màquina.Ordre('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for invàlid_mesura in [
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
            Editar_VALOR(màquina, 'Calc.java', invàlid_mesura)
            màquina.Ordre('javac Calc.java', ['javac error:', 'Exit: 1'])
            màquina.Ordre('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # esprint_VALOR 실행은 usuari 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            màquina.Ordre('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        màquina.Ordre('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        màquina.Ordre('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        Editar_VALOR(màquina, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        màquina.Ordre('javac Calc.java', ['Compiled:', 'Exit: 0'])
        màquina.Ordre('java Calc', ['instruction limit', 'Exit: 1'])
        màquina.Ordre('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        Editar_VALOR(màquina, 'Bad.class', 'garbage')
        màquina.Ordre('java Bad', ['JVM error:', 'Exit: 1'])
        màquina.Ordre('rm Bad.class', ['Removed'])
        màquina.Ordre('java Bad', ['cannot read class: -2'])
        # Editar_VALOR 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Executa_2 = len(màquina.LOG_fila)
        màquina.직렬.sendall(b'edit Hello.java\n')
        màquina.Espera_Estat('...> ', Executa_2)
        Executa_2 = len(màquina.LOG_fila)
        màquina.직렬.sendall(b'x' * 129 + b'\n')
        màquina.Espera_Estat('...> ', Executa_2)
        màquina.Ordre('.save', ['Too much input; original preserved'])
        màquina.Ordre('javac Hello.java', ['Compiled:', 'Exit: 0'])
        Editar_VALOR(màquina, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            Editar_VALOR(màquina, 'f' + str(수), 'occupied')
        màquina.Ordre('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        màquina.Ordre('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in màquina.LOG_fila.decode('utf-8', 'replace')
        RESULTAT['serial'] = màquina.LOG_fila.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return RESULTAT
    finally:
        màquina.Tanca()


def 주코드(dades):
    """손상 시험용 main Code의 real_dades Fitxer 오프셋/길이만 읽는다."""
    càrrec_VALOR = 8
    def 짧():
        nonlocal càrrec_VALOR
        VALOR = struct.unpack_from('>H', dades, càrrec_VALOR)[0]
        càrrec_VALOR += 2
        return VALOR
    def tancar_enter_sense_signe():
        nonlocal càrrec_VALOR
        VALOR = struct.unpack_from('>I', dades, càrrec_VALOR)[0]
        càrrec_VALOR += 4
        return VALOR
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = dades[càrrec_VALOR]
        càrrec_VALOR += 1
        if 종류 == 1:
            durada_VALOR = 짧()
            문자들[수] = dades[càrrec_VALOR:càrrec_VALOR + durada_VALOR]
            càrrec_VALOR += durada_VALOR
        elif 종류 in (7, 8): càrrec_VALOR += 2
        elif 종류 in (3, 9, 10, 12): càrrec_VALOR += 4
        else: raise AssertionError(종류)
    càrrec_VALOR += 6
    element_COMPT = 짧()
    càrrec_VALOR += element_COMPT * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Nom = 짧()
        짧()
        for 수 in range(짧()):
            valor_d_atribut = 짧()
            Mida = tancar_enter_sense_signe()
            if 문자들[Nom] == b'main' and 문자들[valor_d_atribut] == b'Code':
                return càrrec_VALOR + 8, struct.unpack_from('>I', dades, càrrec_VALOR + 4)[0]
            càrrec_VALOR += Mida
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        directori_VALOR = Path(임시)
        (directori_VALOR / 'build').mkdir()
        FONT = directori_VALOR / 'Imported.java'
        FONT.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(FONT)], check=True)
        원본 = (directori_VALOR / 'Imported.class').read_bytes()
        CODI_VALOR, durada_VALOR = 주코드(원본)
        변형 = {}
        dades = bytearray(원본); dades[0] = 0; 변형['BadMagic'] = dades
        dades = bytearray(원본); dades[7] = 61; 변형['BadVer'] = dades
        dades = bytearray(원본); dades[8:10] = b'\xff\xff'; 변형['BadPool'] = dades
        dades = bytearray(원본); dades[CODI_VALOR:CODI_VALOR + durada_VALOR] = bytes(durada_VALOR)
        dades[CODI_VALOR:CODI_VALOR + 3] = b'\xa7\x00\x01'; dades[CODI_VALOR + durada_VALOR - 1] = 177; 변형['BadJump'] = dades
        dades = bytearray(원본); dades[CODI_VALOR:CODI_VALOR + durada_VALOR] = bytes(durada_VALOR)
        dades[CODI_VALOR] = 87; dades[CODI_VALOR + durada_VALOR - 1] = 177; 변형['BadStack'] = dades
        # Nom 검사를 통과시켜 real_dades Executa_ordre 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        introducció_VALOR = ['Imported.class=' + str(directori_VALOR / 'Imported.class'), 'Imported.java=' + str(FONT)]
        for Nom, dades in 변형.items():
            Camí = directori_VALOR / (Nom + '.class'); Camí.write_bytes(dades)
            introducció_VALOR.append(Nom + '.class=' + str(Camí))
        Grup_VALOR = directori_VALOR / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Posició / 'Eines/자바파일묶기.py'), '-o', str(Grup_VALOR)] + introducció_VALOR, check=True)
        subprocess.run(['as', '--32', '-o', str(directori_VALOR / 'user.o'), str(Posició / '부팅/usuari.s')], cwd=str(directori_VALOR), check=True)
        nucli_VALOR = directori_VALOR / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Posició / '부팅/enllaç_disseny.ld'), '-o', str(nucli_VALOR),
                        str(Posició / 'build/boot.o'), str(Posició / 'build/java.o'), str(directori_VALOR / 'user.o'), str(Posició / 'build/apps.o')], check=True)
        màquina = màquina_virtual(nucli_VALOR, xarxa_VALOR=False)
        try:
            màquina.Ordre('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            màquina.Ordre('cat Imported.java', ['int[] values = new int[3]'])
            for Nom, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                màquina.Ordre('java ' + Nom, [문구, 'Exit: 1'])
                màquina.Ordre('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return màquina.LOG_fila.decode('utf-8', 'replace')
        finally:
            màquina.Tanca()


if __name__ == '__main__':
    analitzar_VALOR = argparse.ArgumentParser()
    analitzar_VALOR.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = analitzar_VALOR.parse_args()
    RESULTAT = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    RESULTAT['import'] = 적재시험()
    (Posició / 'build/자바시험.json').write_text(json.dumps(RESULTAT, ensure_ascii=False, indent=2) + '\n')
