#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 zbatoj_komandë, dështim_VALUE/burim_VALUE 경계 시험."""
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
from 사용자통신시험 import virtual_makinë, Pozicioni


def redaktim_VALUE(makinë, Emër, Përmbajtje_VALUE, Store_VALUE=True):
    Ekzekuto = len(makinë.LOG_RECORD)
    makinë.직렬.sendall(('edit ' + Emër + '\n').encode())
    makinë.Prit_status('...> ', Ekzekuto)
    for linjë in Përmbajtje_VALUE.splitlines():
        assert len(linjë) <= 128
        Ekzekuto = len(makinë.LOG_RECORD)
        makinë.직렬.sendall((linjë + '\n').encode())
        makinë.Prit_status('...> ', Ekzekuto)
    Ekzekuto = len(makinë.LOG_RECORD)
    makinë.직렬.sendall(b'.save\n' if Store_VALUE else b'.cancel\n')
    llogaritje = makinë.Prit_status('jkoros> ', Ekzekuto)
    assert ('Saved:' if Store_VALUE else 'Cancelled; original preserved') in llogaritje, llogaritje


def skedar_email():
    llogaritje = subprocess.check_output(['nm', '-n', str(Pozicioni / 'build/kernel.elf')], universal_newlines=True)
    for linjë in llogaritje.splitlines():
        if linjë.endswith(' ram_files'):
            return int(linjë.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def i_ftuar_skedar(makinë, hapësirë_për_tekst_VALUE, Madhësi, POZICIONI):
    # 시험 VM의 메모리에서 aktual_të_dhëna 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    email = skedar_email() + hapësirë_për_tekst_VALUE * 16384
    makinë.monitor_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(email, Madhësi, POZICIONI)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if POZICIONI.exists() and POZICIONI.stat().st_size == Madhësi:
            return POZICIONI.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    makinë = virtual_makinë(Pozicioni / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, rrjet_VALUE=False)
    llogaritje = {}
    try:
        makinë.Komanda('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        makinë.Komanda('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        makinë.Komanda('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        makinë.Komanda('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        makinë.Komanda('java Missing', ['cannot read class: -2', 'Exit: 1'])
        makinë.Komanda('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        makinë.Komanda('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Përmbajtje_VALUE = '''public class Calc {
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
        redaktim_VALUE(makinë, 'Calc.java', Përmbajtje_VALUE)
        makinë.Komanda('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = makinë.Komanda('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        llogaritje['guest_output'] = 출력
        futje_Listë = makinë.Komanda('ls', ['Calc.class'])
        Madhësi = int(re.search(r'Calc\.class\s+(\d+) bytes', futje_Listë).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as direktori_VALUE:
            POZICIONI = Path(direktori_VALUE) / 'Calc.class'
            të_dhëna = i_ftuar_skedar(makinë, 3, Madhësi, POZICIONI)
            aktual_të_dhëna = subprocess.check_output(['java', '-Xverify:all', '-cp', direktori_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert aktual_të_dhëna.splitlines() == 기대, aktual_të_dhëna
            llogaritje['class_sha256'] = hashlib.sha256(të_dhëna).hexdigest()
            llogaritje['openjdk_output'] = aktual_të_dhëna
        # 실패한 redaktim_VALUE/컴파일은 기존 class를 보존한다.
        redaktim_VALUE(makinë, 'Calc.java', 'not Java at all', Store_VALUE=False)
        makinë.Komanda('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for i_pavlefshëm_llogaritje in [
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
            redaktim_VALUE(makinë, 'Calc.java', i_pavlefshëm_llogaritje)
            makinë.Komanda('javac Calc.java', ['javac error:', 'Exit: 1'])
            makinë.Komanda('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # përsëritje_VALUE 실행은 përdorues 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            makinë.Komanda('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        makinë.Komanda('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        makinë.Komanda('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        redaktim_VALUE(makinë, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        makinë.Komanda('javac Calc.java', ['Compiled:', 'Exit: 0'])
        makinë.Komanda('java Calc', ['instruction limit', 'Exit: 1'])
        makinë.Komanda('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        redaktim_VALUE(makinë, 'Bad.class', 'garbage')
        makinë.Komanda('java Bad', ['JVM error:', 'Exit: 1'])
        makinë.Komanda('rm Bad.class', ['Removed'])
        makinë.Komanda('java Bad', ['cannot read class: -2'])
        # redaktim_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Ekzekuto = len(makinë.LOG_RECORD)
        makinë.직렬.sendall(b'edit Hello.java\n')
        makinë.Prit_status('...> ', Ekzekuto)
        Ekzekuto = len(makinë.LOG_RECORD)
        makinë.직렬.sendall(b'x' * 129 + b'\n')
        makinë.Prit_status('...> ', Ekzekuto)
        makinë.Komanda('.save', ['Too much input; original preserved'])
        makinë.Komanda('javac Hello.java', ['Compiled:', 'Exit: 0'])
        redaktim_VALUE(makinë, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            redaktim_VALUE(makinë, 'f' + str(수), 'occupied')
        makinë.Komanda('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        makinë.Komanda('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in makinë.LOG_RECORD.decode('utf-8', 'replace')
        llogaritje['serial'] = makinë.LOG_RECORD.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return llogaritje
    finally:
        makinë.Mbyll()


def 주코드(të_dhëna):
    """손상 시험용 main Code의 aktual_të_dhëna Kartelë 오프셋/길이만 읽는다."""
    pozicioni_VALUE = 8
    def 짧():
        nonlocal pozicioni_VALUE
        VALUE = struct.unpack_from('>H', të_dhëna, pozicioni_VALUE)[0]
        pozicioni_VALUE += 2
        return VALUE
    def 정():
        nonlocal pozicioni_VALUE
        VALUE = struct.unpack_from('>I', të_dhëna, pozicioni_VALUE)[0]
        pozicioni_VALUE += 4
        return VALUE
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = të_dhëna[pozicioni_VALUE]
        pozicioni_VALUE += 1
        if 종류 == 1:
            gjatësi_VALUE = 짧()
            문자들[수] = të_dhëna[pozicioni_VALUE:pozicioni_VALUE + gjatësi_VALUE]
            pozicioni_VALUE += gjatësi_VALUE
        elif 종류 in (7, 8): pozicioni_VALUE += 2
        elif 종류 in (3, 9, 10, 12): pozicioni_VALUE += 4
        else: raise AssertionError(종류)
    pozicioni_VALUE += 6
    njësi_COUNT = 짧()
    pozicioni_VALUE += njësi_COUNT * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Emër = 짧()
        짧()
        for 수 in range(짧()):
            atribut_VALUE = 짧()
            Madhësi = 정()
            if 문자들[Emër] == b'main' and 문자들[atribut_VALUE] == b'Code':
                return pozicioni_VALUE + 8, struct.unpack_from('>I', të_dhëna, pozicioni_VALUE + 4)[0]
            pozicioni_VALUE += Madhësi
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        direktori_VALUE = Path(임시)
        (direktori_VALUE / 'build').mkdir()
        BURIMI = direktori_VALUE / 'Imported.java'
        BURIMI.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(BURIMI)], check=True)
        원본 = (direktori_VALUE / 'Imported.class').read_bytes()
        kod_VALUE, gjatësi_VALUE = 주코드(원본)
        변형 = {}
        të_dhëna = bytearray(원본); të_dhëna[0] = 0; 변형['BadMagic'] = të_dhëna
        të_dhëna = bytearray(원본); të_dhëna[7] = 61; 변형['BadVer'] = të_dhëna
        të_dhëna = bytearray(원본); të_dhëna[8:10] = b'\xff\xff'; 변형['BadPool'] = të_dhëna
        të_dhëna = bytearray(원본); të_dhëna[kod_VALUE:kod_VALUE + gjatësi_VALUE] = bytes(gjatësi_VALUE)
        të_dhëna[kod_VALUE:kod_VALUE + 3] = b'\xa7\x00\x01'; të_dhëna[kod_VALUE + gjatësi_VALUE - 1] = 177; 변형['BadJump'] = të_dhëna
        të_dhëna = bytearray(원본); të_dhëna[kod_VALUE:kod_VALUE + gjatësi_VALUE] = bytes(gjatësi_VALUE)
        të_dhëna[kod_VALUE] = 87; të_dhëna[kod_VALUE + gjatësi_VALUE - 1] = 177; 변형['BadStack'] = të_dhëna
        # Emër 검사를 통과시켜 aktual_të_dhëna zbatoj_komandë 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        futje_VALUE = ['Imported.class=' + str(direktori_VALUE / 'Imported.class'), 'Imported.java=' + str(BURIMI)]
        for Emër, të_dhëna in 변형.items():
            POZICIONI = direktori_VALUE / (Emër + '.class'); POZICIONI.write_bytes(të_dhëna)
            futje_VALUE.append(Emër + '.class=' + str(POZICIONI))
        grup_VALUE = direktori_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Pozicioni / 'Mjete/자바파일묶기.py'), '-o', str(grup_VALUE)] + futje_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(direktori_VALUE / 'user.o'), str(Pozicioni / '부팅/përdorues.s')], cwd=str(direktori_VALUE), check=True)
        bërthamë_VALUE = direktori_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Pozicioni / '부팅/lidh_Navigimi.ld'), '-o', str(bërthamë_VALUE),
                        str(Pozicioni / 'build/boot.o'), str(Pozicioni / 'build/java.o'), str(direktori_VALUE / 'user.o'), str(Pozicioni / 'build/apps.o')], check=True)
        makinë = virtual_makinë(bërthamë_VALUE, rrjet_VALUE=False)
        try:
            makinë.Komanda('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            makinë.Komanda('cat Imported.java', ['int[] values = new int[3]'])
            for Emër, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                makinë.Komanda('java ' + Emër, [문구, 'Exit: 1'])
                makinë.Komanda('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return makinë.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            makinë.Mbyll()


if __name__ == '__main__':
    analizoj_VALUE = argparse.ArgumentParser()
    analizoj_VALUE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    Argumente = analizoj_VALUE.parse_args()
    llogaritje = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if Argumente.boot == 'both' else (Argumente.boot,))}
    llogaritje['import'] = 적재시험()
    (Pozicioni / 'build/자바시험.json').write_text(json.dumps(llogaritje, ensure_ascii=False, indent=2) + '\n')
