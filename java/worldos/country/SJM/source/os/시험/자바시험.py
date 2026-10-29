#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Utfør_kommando, feil_VERDI/ressurs_VERDI grense_VERDI 시험."""
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
from test_bruker_nettverk import VM, Posisjon


def Rediger_VERDI(maskin, Navn, Innhold_VERDI, Store_VERDI=True):
    Kjør_2 = len(maskin.LOG_POST)
    maskin.직렬.sendall(('edit ' + Navn + '\n').encode())
    maskin.ventende_tilstand('...> ', Kjør_2)
    for Linje in Innhold_VERDI.splitlines():
        assert len(Linje) <= 128
        Kjør_2 = len(maskin.LOG_POST)
        maskin.직렬.sendall((Linje + '\n').encode())
        maskin.ventende_tilstand('...> ', Kjør_2)
    Kjør_2 = len(maskin.LOG_POST)
    maskin.직렬.sendall(b'.save\n' if Store_VERDI else b'.cancel\n')
    KR = maskin.ventende_tilstand('jkoros> ', Kjør_2)
    assert ('Saved:' if Store_VERDI else 'Cancelled; original preserved') in KR, KR


def Fil_e_post():
    KR = subprocess.check_output(['nm', '-n', str(Posisjon / 'build/kernel.elf')], universal_newlines=True)
    for Linje in KR.splitlines():
        if Linje.endswith(' ram_files'):
            return int(Linje.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def gjest_Fil(maskin, åpning_VERDI, Størrelse, Sti):
    # 시험 VM의 메모리에서 faktisk_data 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    e_post = Fil_e_post() + åpning_VERDI * 16384
    maskin.skjerm_VERDI.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(e_post, Størrelse, Sti)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if Sti.exists() and Sti.stat().st_size == Størrelse:
            return Sti.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def test_kjøre(종류):
    maskin = VM(Posisjon / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, nettverk_VERDI=False)
    KR = {}
    try:
        maskin.Kommando('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        maskin.Kommando('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        maskin.Kommando('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        maskin.Kommando('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        maskin.Kommando('java Missing', ['cannot read class: -2', 'Exit: 1'])
        maskin.Kommando('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        maskin.Kommando('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Innhold_VERDI = '''public class Calc {
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
        Rediger_VERDI(maskin, 'Calc.java', Innhold_VERDI)
        maskin.Kommando('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Utgang = maskin.Kommando('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        KR['guest_output'] = Utgang
        oppføring_Liste = maskin.Kommando('ls', ['Calc.class'])
        Størrelse = int(re.search(r'Calc\.class\s+(\d+) bytes', oppføring_Liste).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as katalog_VERDI:
            Sti = Path(katalog_VERDI) / 'Calc.class'
            data = gjest_Fil(maskin, 3, Størrelse, Sti)
            faktisk_data = subprocess.check_output(['java', '-Xverify:all', '-cp', katalog_VERDI, 'Calc', '6', 'guest'], universal_newlines=True)
            assert faktisk_data.splitlines() == 기대, faktisk_data
            KR['class_sha256'] = hashlib.sha256(data).hexdigest()
            KR['openjdk_output'] = faktisk_data
        # 실패한 Rediger_VERDI/컴파일은 기존 class를 보존한다.
        Rediger_VERDI(maskin, 'Calc.java', 'not Java at all', Store_VERDI=False)
        maskin.Kommando('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for ugyldig_KR in [
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
            Rediger_VERDI(maskin, 'Calc.java', ugyldig_KR)
            maskin.Kommando('javac Calc.java', ['javac error:', 'Exit: 1'])
            maskin.Kommando('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # sprint_VERDI 실행은 bruker heap_VERDI/프레임을 매번 초기화한다.
        for nummer in range(12):
            maskin.Kommando('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        maskin.Kommando('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        maskin.Kommando('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        Rediger_VERDI(maskin, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        maskin.Kommando('javac Calc.java', ['Compiled:', 'Exit: 0'])
        maskin.Kommando('java Calc', ['instruction limit', 'Exit: 1'])
        maskin.Kommando('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        Rediger_VERDI(maskin, 'Bad.class', 'garbage')
        maskin.Kommando('java Bad', ['JVM error:', 'Exit: 1'])
        maskin.Kommando('rm Bad.class', ['Removed'])
        maskin.Kommando('java Bad', ['cannot read class: -2'])
        # Rediger_VERDI 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Kjør_2 = len(maskin.LOG_POST)
        maskin.직렬.sendall(b'edit Hello.java\n')
        maskin.ventende_tilstand('...> ', Kjør_2)
        Kjør_2 = len(maskin.LOG_POST)
        maskin.직렬.sendall(b'x' * 129 + b'\n')
        maskin.ventende_tilstand('...> ', Kjør_2)
        maskin.Kommando('.save', ['Too much input; original preserved'])
        maskin.Kommando('javac Hello.java', ['Compiled:', 'Exit: 0'])
        Rediger_VERDI(maskin, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for nummer in range(3):
            Rediger_VERDI(maskin, 'f' + str(nummer), 'occupied')
        maskin.Kommando('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        maskin.Kommando('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in maskin.LOG_POST.decode('utf-8', 'replace')
        KR['serial'] = maskin.LOG_POST.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return KR
    finally:
        maskin.Lukk()


def 주코드(data):
    """손상 시험용 main Code의 faktisk_data Fil 오프셋/길이만 읽는다."""
    plassere_VERDI = 8
    def 짧():
        nonlocal plassere_VERDI
        VERDI = struct.unpack_from('>H', data, plassere_VERDI)[0]
        plassere_VERDI += 2
        return VERDI
    def 정():
        nonlocal plassere_VERDI
        VERDI = struct.unpack_from('>I', data, plassere_VERDI)[0]
        plassere_VERDI += 4
        return VERDI
    문자들 = {}
    for nummer in range(1, 짧()):
        종류 = data[plassere_VERDI]
        plassere_VERDI += 1
        if 종류 == 1:
            lengde_VERDI = 짧()
            문자들[nummer] = data[plassere_VERDI:plassere_VERDI + lengde_VERDI]
            plassere_VERDI += lengde_VERDI
        elif 종류 in (7, 8): plassere_VERDI += 2
        elif 종류 in (3, 9, 10, 12): plassere_VERDI += 4
        else: raise AssertionError(종류)
    plassere_VERDI += 6
    vare_ANTALL = 짧()
    plassere_VERDI += vare_ANTALL * 2
    assert 짧() == 0
    for nummer in range(짧()):
        짧()
        Navn = 짧()
        짧()
        for nummer in range(짧()):
            attributtverdi = 짧()
            Størrelse = 정()
            if 문자들[Navn] == b'main' and 문자들[attributtverdi] == b'Code':
                return plassere_VERDI + 8, struct.unpack_from('>I', data, plassere_VERDI + 4)[0]
            plassere_VERDI += Størrelse
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        katalog_VERDI = Path(임시)
        (katalog_VERDI / 'build').mkdir()
        KILDE = katalog_VERDI / 'Imported.java'
        KILDE.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(KILDE)], check=True)
        원본 = (katalog_VERDI / 'Imported.class').read_bytes()
        KODE_VERDI, lengde_VERDI = 주코드(원본)
        variant_VERDI = {}
        data = bytearray(원본); data[0] = 0; variant_VERDI['BadMagic'] = data
        data = bytearray(원본); data[7] = 61; variant_VERDI['BadVer'] = data
        data = bytearray(원본); data[8:10] = b'\xff\xff'; variant_VERDI['BadPool'] = data
        data = bytearray(원본); data[KODE_VERDI:KODE_VERDI + lengde_VERDI] = bytes(lengde_VERDI)
        data[KODE_VERDI:KODE_VERDI + 3] = b'\xa7\x00\x01'; data[KODE_VERDI + lengde_VERDI - 1] = 177; variant_VERDI['BadJump'] = data
        data = bytearray(원본); data[KODE_VERDI:KODE_VERDI + lengde_VERDI] = bytes(lengde_VERDI)
        data[KODE_VERDI] = 87; data[KODE_VERDI + lengde_VERDI - 1] = 177; variant_VERDI['BadStack'] = data
        # Navn 검사를 통과시켜 faktisk_data Utfør_kommando 중의 operand_stakk 오류까지 검사한다.
        variant_VERDI['BadStack'] = variant_VERDI['BadStack'].replace(b'Imported', b'BadStack')
        oppføring_VERDI = ['Imported.class=' + str(katalog_VERDI / 'Imported.class'), 'Imported.java=' + str(KILDE)]
        for Navn, data in variant_VERDI.items():
            Sti = katalog_VERDI / (Navn + '.class'); Sti.write_bytes(data)
            oppføring_VERDI.append(Navn + '.class=' + str(Sti))
        gruppe_VERDI = katalog_VERDI / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Posisjon / 'Verktøy/자바파일묶기.py'), '-o', str(gruppe_VERDI)] + oppføring_VERDI, check=True)
        subprocess.run(['as', '--32', '-o', str(katalog_VERDI / 'user.o'), str(Posisjon / '부팅/bruker.s')], cwd=str(katalog_VERDI), check=True)
        kjerne_VERDI = katalog_VERDI / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Posisjon / '부팅/koble_Oppsett.ld'), '-o', str(kjerne_VERDI),
                        str(Posisjon / 'build/boot.o'), str(Posisjon / 'build/java.o'), str(katalog_VERDI / 'user.o'), str(Posisjon / 'build/apps.o')], check=True)
        maskin = VM(kjerne_VERDI, nettverk_VERDI=False)
        try:
            maskin.Kommando('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            maskin.Kommando('cat Imported.java', ['int[] values = new int[3]'])
            for Navn, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                maskin.Kommando('java ' + Navn, [문구, 'Exit: 1'])
                maskin.Kommando('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return maskin.LOG_POST.decode('utf-8', 'replace')
        finally:
            maskin.Lukk()


if __name__ == '__main__':
    dele_opp_VERDI = argparse.ArgumentParser()
    dele_opp_VERDI.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    Argumenter = dele_opp_VERDI.parse_args()
    KR = {종류: test_kjøre(종류) for 종류 in (('elf', 'iso') if Argumenter.boot == 'both' else (Argumenter.boot,))}
    KR['import'] = 적재시험()
    (Posisjon / 'build/자바시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2) + '\n')
