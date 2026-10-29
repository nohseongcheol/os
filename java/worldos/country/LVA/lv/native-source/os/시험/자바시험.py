#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Izpildīt_komanda, kļūme_VALUE/resurss_VALUE 경계 시험."""
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
from 사용자통신시험 import VM, Novietojums


def Rediģēt_VALUE(mašīna, Nosaukums, Saturs_VALUE, Store_VALUE=True):
    Palaist = len(mašīna.LOG_RECORD)
    mašīna.직렬.sendall(('edit ' + Nosaukums + '\n').encode())
    mašīna.nogaides_stāvoklis('...> ', Palaist)
    for Līniju in Saturs_VALUE.splitlines():
        assert len(Līniju) <= 128
        Palaist = len(mašīna.LOG_RECORD)
        mašīna.직렬.sendall((Līniju + '\n').encode())
        mašīna.nogaides_stāvoklis('...> ', Palaist)
    Palaist = len(mašīna.LOG_RECORD)
    mašīna.직렬.sendall(b'.save\n' if Store_VALUE else b'.cancel\n')
    mērs = mašīna.nogaides_stāvoklis('jkoros> ', Palaist)
    assert ('Saved:' if Store_VALUE else 'Cancelled; original preserved') in mērs, mērs


def Fails_adrese():
    mērs = subprocess.check_output(['nm', '-n', str(Novietojums / 'build/kernel.elf')], universal_newlines=True)
    for Līniju in mērs.splitlines():
        if Līniju.endswith(' ram_files'):
            return int(Līniju.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def viesis_Fails(mašīna, 슬롯, Izmērs, CEĻŠ):
    # 시험 VM의 메모리에서 faktisks_dati 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    adrese = Fails_adrese() + 슬롯 * 16384
    mašīna.monitors_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(adrese, Izmērs, CEĻŠ)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if CEĻŠ.exists() and CEĻŠ.stat().st_size == Izmērs:
            return CEĻŠ.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    mašīna = VM(Novietojums / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, tīkls_VALUE=False)
    mērs = {}
    try:
        mašīna.Komanda('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        mašīna.Komanda('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        mašīna.Komanda('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        mašīna.Komanda('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        mašīna.Komanda('java Missing', ['cannot read class: -2', 'Exit: 1'])
        mašīna.Komanda('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        mašīna.Komanda('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Saturs_VALUE = '''public class Calc {
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
        Rediģēt_VALUE(mašīna, 'Calc.java', Saturs_VALUE)
        mašīna.Komanda('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Izvade = mašīna.Komanda('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        mērs['guest_output'] = Izvade
        ievade_Saraksts = mašīna.Komanda('ls', ['Calc.class'])
        Izmērs = int(re.search(r'Calc\.class\s+(\d+) bytes', ievade_Saraksts).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as Direktorijs_VALUE:
            CEĻŠ = Path(Direktorijs_VALUE) / 'Calc.class'
            dati = viesis_Fails(mašīna, 3, Izmērs, CEĻŠ)
            faktisks_dati = subprocess.check_output(['java', '-Xverify:all', '-cp', Direktorijs_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert faktisks_dati.splitlines() == 기대, faktisks_dati
            mērs['class_sha256'] = hashlib.sha256(dati).hexdigest()
            mērs['openjdk_output'] = faktisks_dati
        # 실패한 Rediģēt_VALUE/컴파일은 기존 class를 보존한다.
        Rediģēt_VALUE(mašīna, 'Calc.java', 'not Java at all', Store_VALUE=False)
        mašīna.Komanda('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for nederīgs_mērs in [
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
            Rediģēt_VALUE(mašīna, 'Calc.java', nederīgs_mērs)
            mašīna.Komanda('javac Calc.java', ['javac error:', 'Exit: 1'])
            mašīna.Komanda('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # sprints_VALUE 실행은 lietotājs kaudze_VALUE/프레임을 매번 초기화한다.
        for numurs in range(12):
            mašīna.Komanda('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        mašīna.Komanda('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        mašīna.Komanda('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        Rediģēt_VALUE(mašīna, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        mašīna.Komanda('javac Calc.java', ['Compiled:', 'Exit: 0'])
        mašīna.Komanda('java Calc', ['instruction limit', 'Exit: 1'])
        mašīna.Komanda('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        Rediģēt_VALUE(mašīna, 'Bad.class', 'garbage')
        mašīna.Komanda('java Bad', ['JVM error:', 'Exit: 1'])
        mašīna.Komanda('rm Bad.class', ['Removed'])
        mašīna.Komanda('java Bad', ['cannot read class: -2'])
        # Rediģēt_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Palaist = len(mašīna.LOG_RECORD)
        mašīna.직렬.sendall(b'edit Hello.java\n')
        mašīna.nogaides_stāvoklis('...> ', Palaist)
        Palaist = len(mašīna.LOG_RECORD)
        mašīna.직렬.sendall(b'x' * 129 + b'\n')
        mašīna.nogaides_stāvoklis('...> ', Palaist)
        mašīna.Komanda('.save', ['Too much input; original preserved'])
        mašīna.Komanda('javac Hello.java', ['Compiled:', 'Exit: 0'])
        Rediģēt_VALUE(mašīna, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for numurs in range(3):
            Rediģēt_VALUE(mašīna, 'f' + str(numurs), 'occupied')
        mašīna.Komanda('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        mašīna.Komanda('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in mašīna.LOG_RECORD.decode('utf-8', 'replace')
        mērs['serial'] = mašīna.LOG_RECORD.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return mērs
    finally:
        mašīna.Aizvērt()


def 주코드(dati):
    """손상 시험용 main Code의 faktisks_dati Fails 오프셋/길이만 읽는다."""
    amats_VALUE = 8
    def 짧():
        nonlocal amats_VALUE
        VALUE = struct.unpack_from('>H', dati, amats_VALUE)[0]
        amats_VALUE += 2
        return VALUE
    def 정():
        nonlocal amats_VALUE
        VALUE = struct.unpack_from('>I', dati, amats_VALUE)[0]
        amats_VALUE += 4
        return VALUE
    문자들 = {}
    for numurs in range(1, 짧()):
        종류 = dati[amats_VALUE]
        amats_VALUE += 1
        if 종류 == 1:
            길이 = 짧()
            문자들[numurs] = dati[amats_VALUE:amats_VALUE + 길이]
            amats_VALUE += 길이
        elif 종류 in (7, 8): amats_VALUE += 2
        elif 종류 in (3, 9, 10, 12): amats_VALUE += 4
        else: raise AssertionError(종류)
    amats_VALUE += 6
    krājums_COUNT = 짧()
    amats_VALUE += krājums_COUNT * 2
    assert 짧() == 0
    for numurs in range(짧()):
        짧()
        Nosaukums = 짧()
        짧()
        for numurs in range(짧()):
            atribūts_VALUE = 짧()
            Izmērs = 정()
            if 문자들[Nosaukums] == b'main' and 문자들[atribūts_VALUE] == b'Code':
                return amats_VALUE + 8, struct.unpack_from('>I', dati, amats_VALUE + 4)[0]
            amats_VALUE += Izmērs
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        Direktorijs_VALUE = Path(임시)
        (Direktorijs_VALUE / 'build').mkdir()
        AVOTS = Direktorijs_VALUE / 'Imported.java'
        AVOTS.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(AVOTS)], check=True)
        원본 = (Direktorijs_VALUE / 'Imported.class').read_bytes()
        CODE_VALUE, 길이 = 주코드(원본)
        variants_VALUE = {}
        dati = bytearray(원본); dati[0] = 0; variants_VALUE['BadMagic'] = dati
        dati = bytearray(원본); dati[7] = 61; variants_VALUE['BadVer'] = dati
        dati = bytearray(원본); dati[8:10] = b'\xff\xff'; variants_VALUE['BadPool'] = dati
        dati = bytearray(원본); dati[CODE_VALUE:CODE_VALUE + 길이] = bytes(길이)
        dati[CODE_VALUE:CODE_VALUE + 3] = b'\xa7\x00\x01'; dati[CODE_VALUE + 길이 - 1] = 177; variants_VALUE['BadJump'] = dati
        dati = bytearray(원본); dati[CODE_VALUE:CODE_VALUE + 길이] = bytes(길이)
        dati[CODE_VALUE] = 87; dati[CODE_VALUE + 길이 - 1] = 177; variants_VALUE['BadStack'] = dati
        # Nosaukums 검사를 통과시켜 faktisks_dati Izpildīt_komanda 중의 operands_kopa 오류까지 검사한다.
        variants_VALUE['BadStack'] = variants_VALUE['BadStack'].replace(b'Imported', b'BadStack')
        ievade_VALUE = ['Imported.class=' + str(Direktorijs_VALUE / 'Imported.class'), 'Imported.java=' + str(AVOTS)]
        for Nosaukums, dati in variants_VALUE.items():
            CEĻŠ = Direktorijs_VALUE / (Nosaukums + '.class'); CEĻŠ.write_bytes(dati)
            ievade_VALUE.append(Nosaukums + '.class=' + str(CEĻŠ))
        Grupa_VALUE = Direktorijs_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Novietojums / 'Rīki/자바파일묶기.py'), '-o', str(Grupa_VALUE)] + ievade_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(Direktorijs_VALUE / 'user.o'), str(Novietojums / '부팅/lietotājs.s')], cwd=str(Direktorijs_VALUE), check=True)
        kodols_VALUE = Direktorijs_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Novietojums / '부팅/Saite_shēma.ld'), '-o', str(kodols_VALUE),
                        str(Novietojums / 'build/boot.o'), str(Novietojums / 'build/java.o'), str(Direktorijs_VALUE / 'user.o'), str(Novietojums / 'build/apps.o')], check=True)
        mašīna = VM(kodols_VALUE, tīkls_VALUE=False)
        try:
            mašīna.Komanda('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            mašīna.Komanda('cat Imported.java', ['int[] values = new int[3]'])
            for Nosaukums, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                mašīna.Komanda('java ' + Nosaukums, [문구, 'Exit: 1'])
                mašīna.Komanda('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return mašīna.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            mašīna.Aizvērt()


if __name__ == '__main__':
    parsēt_VALUE = argparse.ArgumentParser()
    parsēt_VALUE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    Parametri = parsēt_VALUE.parse_args()
    mērs = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if Parametri.boot == 'both' else (Parametri.boot,))}
    mērs['import'] = 적재시험()
    (Novietojums / 'build/자바시험.json').write_text(json.dumps(mērs, ensure_ascii=False, indent=2) + '\n')
