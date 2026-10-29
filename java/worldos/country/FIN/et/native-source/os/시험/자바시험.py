#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Täida_käsk, tõrge_VALUE/ressurss_VALUE 경계 시험."""
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
from 사용자통신시험 import VM, Asukoht


def muudatus_VALUE(arvuti, Nimi_2, Sisu_VALUE, salv_VALUE=True):
    Käivita_2 = len(arvuti.LOG_kirje)
    arvuti.직렬.sendall(('edit ' + Nimi_2 + '\n').encode())
    arvuti.ooteolek('...> ', Käivita_2)
    for Joon in Sisu_VALUE.splitlines():
        assert len(Joon) <= 128
        Käivita_2 = len(arvuti.LOG_kirje)
        arvuti.직렬.sendall((Joon + '\n').encode())
        arvuti.ooteolek('...> ', Käivita_2)
    Käivita_2 = len(arvuti.LOG_kirje)
    arvuti.직렬.sendall(b'.save\n' if salv_VALUE else b'.cancel\n')
    TULEMUS = arvuti.ooteolek('jkoros> ', Käivita_2)
    assert ('Saved:' if salv_VALUE else 'Cancelled; original preserved') in TULEMUS, TULEMUS


def Fail_ADDRESS():
    TULEMUS = subprocess.check_output(['nm', '-n', str(Asukoht / 'build/kernel.elf')], universal_newlines=True)
    for Joon in TULEMUS.splitlines():
        if Joon.endswith(' ram_files'):
            return int(Joon.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def külaline_Fail(arvuti, 슬롯, Suurus, RADA):
    # 시험 VM의 메모리에서 tegelik_andmed 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ADDRESS = Fail_ADDRESS() + 슬롯 * 16384
    arvuti.kuvar_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ADDRESS, Suurus, RADA)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if RADA.exists() and RADA.stat().st_size == Suurus:
            return RADA.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    arvuti = VM(Asukoht / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, võrk_VALUE=False)
    TULEMUS = {}
    try:
        arvuti.Käsk('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        arvuti.Käsk('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        arvuti.Käsk('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        arvuti.Käsk('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        arvuti.Käsk('java Missing', ['cannot read class: -2', 'Exit: 1'])
        arvuti.Käsk('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        arvuti.Käsk('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Sisu_VALUE = '''public class Calc {
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
        muudatus_VALUE(arvuti, 'Calc.java', Sisu_VALUE)
        arvuti.Käsk('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Väljund = arvuti.Käsk('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        TULEMUS['guest_output'] = Väljund
        kirje_Loend = arvuti.Käsk('ls', ['Calc.class'])
        Suurus = int(re.search(r'Calc\.class\s+(\d+) bytes', kirje_Loend).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as kaust_VALUE:
            RADA = Path(kaust_VALUE) / 'Calc.class'
            andmed = külaline_Fail(arvuti, 3, Suurus, RADA)
            tegelik_andmed = subprocess.check_output(['java', '-Xverify:all', '-cp', kaust_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert tegelik_andmed.splitlines() == 기대, tegelik_andmed
            TULEMUS['class_sha256'] = hashlib.sha256(andmed).hexdigest()
            TULEMUS['openjdk_output'] = tegelik_andmed
        # 실패한 muudatus_VALUE/컴파일은 기존 class를 보존한다.
        muudatus_VALUE(arvuti, 'Calc.java', 'not Java at all', salv_VALUE=False)
        arvuti.Käsk('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for kehtetu_näitaja in [
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
            muudatus_VALUE(arvuti, 'Calc.java', kehtetu_näitaja)
            arvuti.Käsk('javac Calc.java', ['javac error:', 'Exit: 1'])
            arvuti.Käsk('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # sprint_VALUE 실행은 kasutaja 힙/프레임을 매번 초기화한다.
        for number in range(12):
            arvuti.Käsk('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        arvuti.Käsk('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        arvuti.Käsk('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        muudatus_VALUE(arvuti, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        arvuti.Käsk('javac Calc.java', ['Compiled:', 'Exit: 0'])
        arvuti.Käsk('java Calc', ['instruction limit', 'Exit: 1'])
        arvuti.Käsk('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        muudatus_VALUE(arvuti, 'Bad.class', 'garbage')
        arvuti.Käsk('java Bad', ['JVM error:', 'Exit: 1'])
        arvuti.Käsk('rm Bad.class', ['Removed'])
        arvuti.Käsk('java Bad', ['cannot read class: -2'])
        # muudatus_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Käivita_2 = len(arvuti.LOG_kirje)
        arvuti.직렬.sendall(b'edit Hello.java\n')
        arvuti.ooteolek('...> ', Käivita_2)
        Käivita_2 = len(arvuti.LOG_kirje)
        arvuti.직렬.sendall(b'x' * 129 + b'\n')
        arvuti.ooteolek('...> ', Käivita_2)
        arvuti.Käsk('.save', ['Too much input; original preserved'])
        arvuti.Käsk('javac Hello.java', ['Compiled:', 'Exit: 0'])
        muudatus_VALUE(arvuti, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for number in range(3):
            muudatus_VALUE(arvuti, 'f' + str(number), 'occupied')
        arvuti.Käsk('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        arvuti.Käsk('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in arvuti.LOG_kirje.decode('utf-8', 'replace')
        TULEMUS['serial'] = arvuti.LOG_kirje.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return TULEMUS
    finally:
        arvuti.Suletud()


def 주코드(andmed):
    """손상 시험용 main Code의 tegelik_andmed Fail 오프셋/길이만 읽는다."""
    ametikoht_VALUE = 8
    def 짧():
        nonlocal ametikoht_VALUE
        VALUE = struct.unpack_from('>H', andmed, ametikoht_VALUE)[0]
        ametikoht_VALUE += 2
        return VALUE
    def 정():
        nonlocal ametikoht_VALUE
        VALUE = struct.unpack_from('>I', andmed, ametikoht_VALUE)[0]
        ametikoht_VALUE += 4
        return VALUE
    문자들 = {}
    for number in range(1, 짧()):
        종류 = andmed[ametikoht_VALUE]
        ametikoht_VALUE += 1
        if 종류 == 1:
            길이 = 짧()
            문자들[number] = andmed[ametikoht_VALUE:ametikoht_VALUE + 길이]
            ametikoht_VALUE += 길이
        elif 종류 in (7, 8): ametikoht_VALUE += 2
        elif 종류 in (3, 9, 10, 12): ametikoht_VALUE += 4
        else: raise AssertionError(종류)
    ametikoht_VALUE += 6
    kaup_COUNT = 짧()
    ametikoht_VALUE += kaup_COUNT * 2
    assert 짧() == 0
    for number in range(짧()):
        짧()
        Nimi_2 = 짧()
        짧()
        for number in range(짧()):
            atribuut_VALUE = 짧()
            Suurus = 정()
            if 문자들[Nimi_2] == b'main' and 문자들[atribuut_VALUE] == b'Code':
                return ametikoht_VALUE + 8, struct.unpack_from('>I', andmed, ametikoht_VALUE + 4)[0]
            ametikoht_VALUE += Suurus
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        kaust_VALUE = Path(임시)
        (kaust_VALUE / 'build').mkdir()
        ALLIKAS = kaust_VALUE / 'Imported.java'
        ALLIKAS.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ALLIKAS)], check=True)
        원본 = (kaust_VALUE / 'Imported.class').read_bytes()
        CODE_VALUE, 길이 = 주코드(원본)
        variant_VALUE = {}
        andmed = bytearray(원본); andmed[0] = 0; variant_VALUE['BadMagic'] = andmed
        andmed = bytearray(원본); andmed[7] = 61; variant_VALUE['BadVer'] = andmed
        andmed = bytearray(원본); andmed[8:10] = b'\xff\xff'; variant_VALUE['BadPool'] = andmed
        andmed = bytearray(원본); andmed[CODE_VALUE:CODE_VALUE + 길이] = bytes(길이)
        andmed[CODE_VALUE:CODE_VALUE + 3] = b'\xa7\x00\x01'; andmed[CODE_VALUE + 길이 - 1] = 177; variant_VALUE['BadJump'] = andmed
        andmed = bytearray(원본); andmed[CODE_VALUE:CODE_VALUE + 길이] = bytes(길이)
        andmed[CODE_VALUE] = 87; andmed[CODE_VALUE + 길이 - 1] = 177; variant_VALUE['BadStack'] = andmed
        # Nimi_2 검사를 통과시켜 tegelik_andmed Täida_käsk 중의 operand_Virn 오류까지 검사한다.
        variant_VALUE['BadStack'] = variant_VALUE['BadStack'].replace(b'Imported', b'BadStack')
        kirje_VALUE = ['Imported.class=' + str(kaust_VALUE / 'Imported.class'), 'Imported.java=' + str(ALLIKAS)]
        for Nimi_2, andmed in variant_VALUE.items():
            RADA = kaust_VALUE / (Nimi_2 + '.class'); RADA.write_bytes(andmed)
            kirje_VALUE.append(Nimi_2 + '.class=' + str(RADA))
        Rühm_VALUE = kaust_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Asukoht / 'Tööriistad/자바파일묶기.py'), '-o', str(Rühm_VALUE)] + kirje_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(kaust_VALUE / 'user.o'), str(Asukoht / '부팅/kasutaja.s')], cwd=str(kaust_VALUE), check=True)
        tuum_VALUE = kaust_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Asukoht / '부팅/Link_küljend.ld'), '-o', str(tuum_VALUE),
                        str(Asukoht / 'build/boot.o'), str(Asukoht / 'build/java.o'), str(kaust_VALUE / 'user.o'), str(Asukoht / 'build/apps.o')], check=True)
        arvuti = VM(tuum_VALUE, võrk_VALUE=False)
        try:
            arvuti.Käsk('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            arvuti.Käsk('cat Imported.java', ['int[] values = new int[3]'])
            for Nimi_2, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                arvuti.Käsk('java ' + Nimi_2, [문구, 'Exit: 1'])
                arvuti.Käsk('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return arvuti.LOG_kirje.decode('utf-8', 'replace')
        finally:
            arvuti.Suletud()


if __name__ == '__main__':
    sõeluma_VALUE = argparse.ArgumentParser()
    sõeluma_VALUE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    Argumendid = sõeluma_VALUE.parse_args()
    TULEMUS = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if Argumendid.boot == 'both' else (Argumendid.boot,))}
    TULEMUS['import'] = 적재시험()
    (Asukoht / 'build/자바시험.json').write_text(json.dumps(TULEMUS, ensure_ascii=False, indent=2) + '\n')
