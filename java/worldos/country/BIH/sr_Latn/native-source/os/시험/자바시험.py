#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Izvrši_komanda, otkazivanje_VALUE/resurs_VALUE 경계 시험."""
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
from 사용자통신시험 import VM, pozicija


def Uredi_VALUE(računar, ime, Sadržaj_VALUE, Store_VALUE=True):
    koristiti = len(računar.LOG_snimi)
    računar.직렬.sendall(('edit ' + ime + '\n').encode())
    računar.stanje_čekanja('...> ', koristiti)
    for red in Sadržaj_VALUE.splitlines():
        assert len(red) <= 128
        koristiti = len(računar.LOG_snimi)
        računar.직렬.sendall((red + '\n').encode())
        računar.stanje_čekanja('...> ', koristiti)
    koristiti = len(računar.LOG_snimi)
    računar.직렬.sendall(b'.save\n' if Store_VALUE else b'.cancel\n')
    KR = računar.stanje_čekanja('jkoros> ', koristiti)
    assert ('Saved:' if Store_VALUE else 'Cancelled; original preserved') in KR, KR


def Datoteka_adresa():
    KR = subprocess.check_output(['nm', '-n', str(pozicija / 'build/kernel.elf')], universal_newlines=True)
    for red in KR.splitlines():
        if red.endswith(' ram_files'):
            return int(red.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def gost_Datoteka(računar, 슬롯, promeniti_veličinu, putanja):
    # 시험 VM의 메모리에서 stvarni_podaci 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    adresa = Datoteka_adresa() + 슬롯 * 16384
    računar.monitor_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(adresa, promeniti_veličinu, putanja)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if putanja.exists() and putanja.stat().st_size == promeniti_veličinu:
            return putanja.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    računar = VM(pozicija / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Mreža_VALUE=False)
    KR = {}
    try:
        računar.komanda('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        računar.komanda('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        računar.komanda('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        računar.komanda('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        računar.komanda('java Missing', ['cannot read class: -2', 'Exit: 1'])
        računar.komanda('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        računar.komanda('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Sadržaj_VALUE = '''public class Calc {
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
        Uredi_VALUE(računar, 'Calc.java', Sadržaj_VALUE)
        računar.komanda('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = računar.komanda('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        KR['guest_output'] = 출력
        stavka_Lista = računar.komanda('ls', ['Calc.class'])
        promeniti_veličinu = int(re.search(r'Calc\.class\s+(\d+) bytes', stavka_Lista).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as Imenik_VALUE:
            putanja = Path(Imenik_VALUE) / 'Calc.class'
            podaci = gost_Datoteka(računar, 3, promeniti_veličinu, putanja)
            stvarni_podaci = subprocess.check_output(['java', '-Xverify:all', '-cp', Imenik_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert stvarni_podaci.splitlines() == 기대, stvarni_podaci
            KR['class_sha256'] = hashlib.sha256(podaci).hexdigest()
            KR['openjdk_output'] = stvarni_podaci
        # 실패한 Uredi_VALUE/컴파일은 기존 class를 보존한다.
        Uredi_VALUE(računar, 'Calc.java', 'not Java at all', Store_VALUE=False)
        računar.komanda('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for nevažeći_KR in [
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
            Uredi_VALUE(računar, 'Calc.java', nevažeći_KR)
            računar.komanda('javac Calc.java', ['javac error:', 'Exit: 1'])
            računar.komanda('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # sprint_VALUE 실행은 korisnik 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            računar.komanda('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        računar.komanda('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        računar.komanda('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        Uredi_VALUE(računar, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        računar.komanda('javac Calc.java', ['Compiled:', 'Exit: 0'])
        računar.komanda('java Calc', ['instruction limit', 'Exit: 1'])
        računar.komanda('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        Uredi_VALUE(računar, 'Bad.class', 'garbage')
        računar.komanda('java Bad', ['JVM error:', 'Exit: 1'])
        računar.komanda('rm Bad.class', ['Removed'])
        računar.komanda('java Bad', ['cannot read class: -2'])
        # Uredi_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        koristiti = len(računar.LOG_snimi)
        računar.직렬.sendall(b'edit Hello.java\n')
        računar.stanje_čekanja('...> ', koristiti)
        koristiti = len(računar.LOG_snimi)
        računar.직렬.sendall(b'x' * 129 + b'\n')
        računar.stanje_čekanja('...> ', koristiti)
        računar.komanda('.save', ['Too much input; original preserved'])
        računar.komanda('javac Hello.java', ['Compiled:', 'Exit: 0'])
        Uredi_VALUE(računar, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            Uredi_VALUE(računar, 'f' + str(수), 'occupied')
        računar.komanda('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        računar.komanda('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in računar.LOG_snimi.decode('utf-8', 'replace')
        KR['serial'] = računar.LOG_snimi.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return KR
    finally:
        računar.Zatvori()


def 주코드(podaci):
    """손상 시험용 main Code의 stvarni_podaci Datoteka 오프셋/길이만 읽는다."""
    pozicija_VALUE = 8
    def 짧():
        nonlocal pozicija_VALUE
        VALUE = struct.unpack_from('>H', podaci, pozicija_VALUE)[0]
        pozicija_VALUE += 2
        return VALUE
    def 정():
        nonlocal pozicija_VALUE
        VALUE = struct.unpack_from('>I', podaci, pozicija_VALUE)[0]
        pozicija_VALUE += 4
        return VALUE
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = podaci[pozicija_VALUE]
        pozicija_VALUE += 1
        if 종류 == 1:
            길이 = 짧()
            문자들[수] = podaci[pozicija_VALUE:pozicija_VALUE + 길이]
            pozicija_VALUE += 길이
        elif 종류 in (7, 8): pozicija_VALUE += 2
        elif 종류 in (3, 9, 10, 12): pozicija_VALUE += 4
        else: raise AssertionError(종류)
    pozicija_VALUE += 6
    stavka_COUNT = 짧()
    pozicija_VALUE += stavka_COUNT * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        ime = 짧()
        짧()
        for 수 in range(짧()):
            atribut_VALUE = 짧()
            promeniti_veličinu = 정()
            if 문자들[ime] == b'main' and 문자들[atribut_VALUE] == b'Code':
                return pozicija_VALUE + 8, struct.unpack_from('>I', podaci, pozicija_VALUE + 4)[0]
            pozicija_VALUE += promeniti_veličinu
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        Imenik_VALUE = Path(임시)
        (Imenik_VALUE / 'build').mkdir()
        izvor = Imenik_VALUE / 'Imported.java'
        izvor.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(izvor)], check=True)
        원본 = (Imenik_VALUE / 'Imported.class').read_bytes()
        kôd_VALUE, 길이 = 주코드(원본)
        변형 = {}
        podaci = bytearray(원본); podaci[0] = 0; 변형['BadMagic'] = podaci
        podaci = bytearray(원본); podaci[7] = 61; 변형['BadVer'] = podaci
        podaci = bytearray(원본); podaci[8:10] = b'\xff\xff'; 변형['BadPool'] = podaci
        podaci = bytearray(원본); podaci[kôd_VALUE:kôd_VALUE + 길이] = bytes(길이)
        podaci[kôd_VALUE:kôd_VALUE + 3] = b'\xa7\x00\x01'; podaci[kôd_VALUE + 길이 - 1] = 177; 변형['BadJump'] = podaci
        podaci = bytearray(원본); podaci[kôd_VALUE:kôd_VALUE + 길이] = bytes(길이)
        podaci[kôd_VALUE] = 87; podaci[kôd_VALUE + 길이 - 1] = 177; 변형['BadStack'] = podaci
        # ime 검사를 통과시켜 stvarni_podaci Izvrši_komanda 중의 operand_stek 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        stavka_VALUE = ['Imported.class=' + str(Imenik_VALUE / 'Imported.class'), 'Imported.java=' + str(izvor)]
        for ime, podaci in 변형.items():
            putanja = Imenik_VALUE / (ime + '.class'); putanja.write_bytes(podaci)
            stavka_VALUE.append(ime + '.class=' + str(putanja))
        Grupa_VALUE = Imenik_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(pozicija / 'Alatke/자바파일묶기.py'), '-o', str(Grupa_VALUE)] + stavka_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(Imenik_VALUE / 'user.o'), str(pozicija / '부팅/korisnik.s')], cwd=str(Imenik_VALUE), check=True)
        jezgro_VALUE = Imenik_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(pozicija / '부팅/Veza_Raspored.ld'), '-o', str(jezgro_VALUE),
                        str(pozicija / 'build/boot.o'), str(pozicija / 'build/java.o'), str(Imenik_VALUE / 'user.o'), str(pozicija / 'build/apps.o')], check=True)
        računar = VM(jezgro_VALUE, Mreža_VALUE=False)
        try:
            računar.komanda('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            računar.komanda('cat Imported.java', ['int[] values = new int[3]'])
            for ime, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                računar.komanda('java ' + ime, [문구, 'Exit: 1'])
                računar.komanda('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return računar.LOG_snimi.decode('utf-8', 'replace')
        finally:
            računar.Zatvori()


if __name__ == '__main__':
    raščlaniti_VALUE = argparse.ArgumentParser()
    raščlaniti_VALUE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = raščlaniti_VALUE.parse_args()
    KR = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    KR['import'] = 적재시험()
    (pozicija / 'build/자바시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2) + '\n')
