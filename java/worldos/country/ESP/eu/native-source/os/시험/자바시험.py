#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 exekutatu_komando, hutsegite_balio/baliabide_balio 경계 시험."""
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
from 사용자통신시험 import makina_birtual, Posizioa


def edizio_balio(gailu, Izena, eduki_balio, Store_balio=True):
    Exekutatu_2 = len(gailu.LOG_marka)
    gailu.직렬.sendall(('edit ' + Izena + '\n').encode())
    gailu.itxaron_Egoera('...> ', Exekutatu_2)
    for Marra in eduki_balio.splitlines():
        assert len(Marra) <= 128
        Exekutatu_2 = len(gailu.LOG_marka)
        gailu.직렬.sendall((Marra + '\n').encode())
        gailu.itxaron_Egoera('...> ', Exekutatu_2)
    Exekutatu_2 = len(gailu.LOG_marka)
    gailu.직렬.sendall(b'.save\n' if Store_balio else b'.cancel\n')
    EMAITZA = gailu.itxaron_Egoera('jkoros> ', Exekutatu_2)
    assert ('Saved:' if Store_balio else 'Cancelled; original preserved') in EMAITZA, EMAITZA


def fitxategi_helbide():
    EMAITZA = subprocess.check_output(['nm', '-n', str(Posizioa / 'build/kernel.elf')], universal_newlines=True)
    for Marra in EMAITZA.splitlines():
        if Marra.endswith(' ram_files'):
            return int(Marra.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def gonbidatu_fitxategi(gailu, 슬롯, Tamaina, Bide_izena):
    # 시험 VM의 메모리에서 benetako_datuak 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    helbide = fitxategi_helbide() + 슬롯 * 16384
    gailu.monitore_balio.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(helbide, Tamaina, Bide_izena)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if Bide_izena.exists() and Bide_izena.stat().st_size == Tamaina:
            return Bide_izena.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    gailu = makina_birtual(Posizioa / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, sare_balio=False)
    EMAITZA = {}
    try:
        gailu.Komandoa('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        gailu.Komandoa('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        gailu.Komandoa('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        gailu.Komandoa('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        gailu.Komandoa('java Missing', ['cannot read class: -2', 'Exit: 1'])
        gailu.Komandoa('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        gailu.Komandoa('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        eduki_balio = '''public class Calc {
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
        edizio_balio(gailu, 'Calc.java', eduki_balio)
        gailu.Komandoa('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Irteera = gailu.Komandoa('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        EMAITZA['guest_output'] = Irteera
        sarrera_Zerrenda = gailu.Komandoa('ls', ['Calc.class'])
        Tamaina = int(re.search(r'Calc\.class\s+(\d+) bytes', sarrera_Zerrenda).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as direktorio_balio:
            Bide_izena = Path(direktorio_balio) / 'Calc.class'
            datuak = gonbidatu_fitxategi(gailu, 3, Tamaina, Bide_izena)
            benetako_datuak = subprocess.check_output(['java', '-Xverify:all', '-cp', direktorio_balio, 'Calc', '6', 'guest'], universal_newlines=True)
            assert benetako_datuak.splitlines() == 기대, benetako_datuak
            EMAITZA['class_sha256'] = hashlib.sha256(datuak).hexdigest()
            EMAITZA['openjdk_output'] = benetako_datuak
        # 실패한 edizio_balio/컴파일은 기존 class를 보존한다.
        edizio_balio(gailu, 'Calc.java', 'not Java at all', Store_balio=False)
        gailu.Komandoa('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for baliogabe_neurria in [
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
            edizio_balio(gailu, 'Calc.java', baliogabe_neurria)
            gailu.Komandoa('javac Calc.java', ['javac error:', 'Exit: 1'])
            gailu.Komandoa('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # iterazio_balio 실행은 erabiltzaile 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            gailu.Komandoa('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        gailu.Komandoa('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        gailu.Komandoa('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        edizio_balio(gailu, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        gailu.Komandoa('javac Calc.java', ['Compiled:', 'Exit: 0'])
        gailu.Komandoa('java Calc', ['instruction limit', 'Exit: 1'])
        gailu.Komandoa('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        edizio_balio(gailu, 'Bad.class', 'garbage')
        gailu.Komandoa('java Bad', ['JVM error:', 'Exit: 1'])
        gailu.Komandoa('rm Bad.class', ['Removed'])
        gailu.Komandoa('java Bad', ['cannot read class: -2'])
        # edizio_balio 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Exekutatu_2 = len(gailu.LOG_marka)
        gailu.직렬.sendall(b'edit Hello.java\n')
        gailu.itxaron_Egoera('...> ', Exekutatu_2)
        Exekutatu_2 = len(gailu.LOG_marka)
        gailu.직렬.sendall(b'x' * 129 + b'\n')
        gailu.itxaron_Egoera('...> ', Exekutatu_2)
        gailu.Komandoa('.save', ['Too much input; original preserved'])
        gailu.Komandoa('javac Hello.java', ['Compiled:', 'Exit: 0'])
        edizio_balio(gailu, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            edizio_balio(gailu, 'f' + str(수), 'occupied')
        gailu.Komandoa('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        gailu.Komandoa('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in gailu.LOG_marka.decode('utf-8', 'replace')
        EMAITZA['serial'] = gailu.LOG_marka.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return EMAITZA
    finally:
        gailu.Itxi()


def 주코드(datuak):
    """손상 시험용 main Code의 benetako_datuak Fitxategia 오프셋/길이만 읽는다."""
    kargu_balio = 8
    def 짧():
        nonlocal kargu_balio
        balio = struct.unpack_from('>H', datuak, kargu_balio)[0]
        kargu_balio += 2
        return balio
    def 정():
        nonlocal kargu_balio
        balio = struct.unpack_from('>I', datuak, kargu_balio)[0]
        kargu_balio += 4
        return balio
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = datuak[kargu_balio]
        kargu_balio += 1
        if 종류 == 1:
            luzera_balio = 짧()
            문자들[수] = datuak[kargu_balio:kargu_balio + luzera_balio]
            kargu_balio += luzera_balio
        elif 종류 in (7, 8): kargu_balio += 2
        elif 종류 in (3, 9, 10, 12): kargu_balio += 4
        else: raise AssertionError(종류)
    kargu_balio += 6
    elementu_ZENBATU = 짧()
    kargu_balio += elementu_ZENBATU * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Izena = 짧()
        짧()
        for 수 in range(짧()):
            atributu_balio = 짧()
            Tamaina = 정()
            if 문자들[Izena] == b'main' and 문자들[atributu_balio] == b'Code':
                return kargu_balio + 8, struct.unpack_from('>I', datuak, kargu_balio + 4)[0]
            kargu_balio += Tamaina
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        direktorio_balio = Path(임시)
        (direktorio_balio / 'build').mkdir()
        ITURBURUA = direktorio_balio / 'Imported.java'
        ITURBURUA.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ITURBURUA)], check=True)
        원본 = (direktorio_balio / 'Imported.class').read_bytes()
        KODE_balio, luzera_balio = 주코드(원본)
        변형 = {}
        datuak = bytearray(원본); datuak[0] = 0; 변형['BadMagic'] = datuak
        datuak = bytearray(원본); datuak[7] = 61; 변형['BadVer'] = datuak
        datuak = bytearray(원본); datuak[8:10] = b'\xff\xff'; 변형['BadPool'] = datuak
        datuak = bytearray(원본); datuak[KODE_balio:KODE_balio + luzera_balio] = bytes(luzera_balio)
        datuak[KODE_balio:KODE_balio + 3] = b'\xa7\x00\x01'; datuak[KODE_balio + luzera_balio - 1] = 177; 변형['BadJump'] = datuak
        datuak = bytearray(원본); datuak[KODE_balio:KODE_balio + luzera_balio] = bytes(luzera_balio)
        datuak[KODE_balio] = 87; datuak[KODE_balio + luzera_balio - 1] = 177; 변형['BadStack'] = datuak
        # Izena 검사를 통과시켜 benetako_datuak exekutatu_komando 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        sarrera_balio = ['Imported.class=' + str(direktorio_balio / 'Imported.class'), 'Imported.java=' + str(ITURBURUA)]
        for Izena, datuak in 변형.items():
            Bide_izena = direktorio_balio / (Izena + '.class'); Bide_izena.write_bytes(datuak)
            sarrera_balio.append(Izena + '.class=' + str(Bide_izena))
        talde_balio = direktorio_balio / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Posizioa / 'Tresnak/자바파일묶기.py'), '-o', str(talde_balio)] + sarrera_balio, check=True)
        subprocess.run(['as', '--32', '-o', str(direktorio_balio / 'user.o'), str(Posizioa / '부팅/erabiltzaile.s')], cwd=str(direktorio_balio), check=True)
        nukleo_balio = direktorio_balio / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Posizioa / '부팅/lotu_diseinu.ld'), '-o', str(nukleo_balio),
                        str(Posizioa / 'build/boot.o'), str(Posizioa / 'build/java.o'), str(direktorio_balio / 'user.o'), str(Posizioa / 'build/apps.o')], check=True)
        gailu = makina_birtual(nukleo_balio, sare_balio=False)
        try:
            gailu.Komandoa('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            gailu.Komandoa('cat Imported.java', ['int[] values = new int[3]'])
            for Izena, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                gailu.Komandoa('java ' + Izena, [문구, 'Exit: 1'])
                gailu.Komandoa('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return gailu.LOG_marka.decode('utf-8', 'replace')
        finally:
            gailu.Itxi()


if __name__ == '__main__':
    analizatu_balio = argparse.ArgumentParser()
    analizatu_balio.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    Argumentuak = analizatu_balio.parse_args()
    EMAITZA = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if Argumentuak.boot == 'both' else (Argumentuak.boot,))}
    EMAITZA['import'] = 적재시험()
    (Posizioa / 'build/자바시험.json').write_text(json.dumps(EMAITZA, ensure_ascii=False, indent=2) + '\n')
