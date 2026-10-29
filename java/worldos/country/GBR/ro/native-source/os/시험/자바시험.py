#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 executa_comandă, eroare_VALUE/resursă_VALUE 경계 시험."""
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
from 사용자통신시험 import VM, Poziție


def edita_VALUE(mașină, Nume, Conținut_VALUE, Store_VALUE=True):
    Pornește = len(mașină.LOG_RECORD)
    mașină.직렬.sendall(('edit ' + Nume + '\n').encode())
    mașină.stare_de_așteptare('...> ', Pornește)
    for Linie in Conținut_VALUE.splitlines():
        assert len(Linie) <= 128
        Pornește = len(mașină.LOG_RECORD)
        mașină.직렬.sendall((Linie + '\n').encode())
        mașină.stare_de_așteptare('...> ', Pornește)
    Pornește = len(mașină.LOG_RECORD)
    mașină.직렬.sendall(b'.save\n' if Store_VALUE else b'.cancel\n')
    KR = mașină.stare_de_așteptare('jkoros> ', Pornește)
    assert ('Saved:' if Store_VALUE else 'Cancelled; original preserved') in KR, KR


def Fișier_adresa():
    KR = subprocess.check_output(['nm', '-n', str(Poziție / 'build/kernel.elf')], universal_newlines=True)
    for Linie in KR.splitlines():
        if Linie.endswith(' ram_files'):
            return int(Linie.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def invitat_Fișier(mașină, 슬롯, Mărime, Cale):
    # 시험 VM의 메모리에서 real_date 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    adresa = Fișier_adresa() + 슬롯 * 16384
    mașină.monitor_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(adresa, Mărime, Cale)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if Cale.exists() and Cale.stat().st_size == Mărime:
            return Cale.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    mașină = VM(Poziție / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, rețea_VALUE=False)
    KR = {}
    try:
        mașină.Comandă('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        mașină.Comandă('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        mașină.Comandă('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        mașină.Comandă('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        mașină.Comandă('java Missing', ['cannot read class: -2', 'Exit: 1'])
        mașină.Comandă('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        mașină.Comandă('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Conținut_VALUE = '''public class Calc {
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
        edita_VALUE(mașină, 'Calc.java', Conținut_VALUE)
        mașină.Comandă('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Rezultat = mașină.Comandă('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        KR['guest_output'] = Rezultat
        intrare_Listă = mașină.Comandă('ls', ['Calc.class'])
        Mărime = int(re.search(r'Calc\.class\s+(\d+) bytes', intrare_Listă).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as Director_VALUE:
            Cale = Path(Director_VALUE) / 'Calc.class'
            date = invitat_Fișier(mașină, 3, Mărime, Cale)
            real_date = subprocess.check_output(['java', '-Xverify:all', '-cp', Director_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert real_date.splitlines() == 기대, real_date
            KR['class_sha256'] = hashlib.sha256(date).hexdigest()
            KR['openjdk_output'] = real_date
        # 실패한 edita_VALUE/컴파일은 기존 class를 보존한다.
        edita_VALUE(mașină, 'Calc.java', 'not Java at all', Store_VALUE=False)
        mașină.Comandă('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for nul_KR in [
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
            edita_VALUE(mașină, 'Calc.java', nul_KR)
            mașină.Comandă('javac Calc.java', ['javac error:', 'Exit: 1'])
            mașină.Comandă('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # sprint_VALUE 실행은 utilizator 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            mașină.Comandă('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        mașină.Comandă('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        mașină.Comandă('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        edita_VALUE(mașină, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        mașină.Comandă('javac Calc.java', ['Compiled:', 'Exit: 0'])
        mașină.Comandă('java Calc', ['instruction limit', 'Exit: 1'])
        mașină.Comandă('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        edita_VALUE(mașină, 'Bad.class', 'garbage')
        mașină.Comandă('java Bad', ['JVM error:', 'Exit: 1'])
        mașină.Comandă('rm Bad.class', ['Removed'])
        mașină.Comandă('java Bad', ['cannot read class: -2'])
        # edita_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Pornește = len(mașină.LOG_RECORD)
        mașină.직렬.sendall(b'edit Hello.java\n')
        mașină.stare_de_așteptare('...> ', Pornește)
        Pornește = len(mașină.LOG_RECORD)
        mașină.직렬.sendall(b'x' * 129 + b'\n')
        mașină.stare_de_așteptare('...> ', Pornește)
        mașină.Comandă('.save', ['Too much input; original preserved'])
        mașină.Comandă('javac Hello.java', ['Compiled:', 'Exit: 0'])
        edita_VALUE(mașină, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            edita_VALUE(mașină, 'f' + str(수), 'occupied')
        mașină.Comandă('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        mașină.Comandă('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in mașină.LOG_RECORD.decode('utf-8', 'replace')
        KR['serial'] = mașină.LOG_RECORD.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return KR
    finally:
        mașină.Închide()


def 주코드(date):
    """손상 시험용 main Code의 real_date Fișier 오프셋/길이만 읽는다."""
    poziție_VALUE = 8
    def 짧():
        nonlocal poziție_VALUE
        VALUE = struct.unpack_from('>H', date, poziție_VALUE)[0]
        poziție_VALUE += 2
        return VALUE
    def 정():
        nonlocal poziție_VALUE
        VALUE = struct.unpack_from('>I', date, poziție_VALUE)[0]
        poziție_VALUE += 4
        return VALUE
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = date[poziție_VALUE]
        poziție_VALUE += 1
        if 종류 == 1:
            lungime_VALUE = 짧()
            문자들[수] = date[poziție_VALUE:poziție_VALUE + lungime_VALUE]
            poziție_VALUE += lungime_VALUE
        elif 종류 in (7, 8): poziție_VALUE += 2
        elif 종류 in (3, 9, 10, 12): poziție_VALUE += 4
        else: raise AssertionError(종류)
    poziție_VALUE += 6
    element_COUNT = 짧()
    poziție_VALUE += element_COUNT * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Nume = 짧()
        짧()
        for 수 in range(짧()):
            atribut_VALUE = 짧()
            Mărime = 정()
            if 문자들[Nume] == b'main' and 문자들[atribut_VALUE] == b'Code':
                return poziție_VALUE + 8, struct.unpack_from('>I', date, poziție_VALUE + 4)[0]
            poziție_VALUE += Mărime
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        Director_VALUE = Path(임시)
        (Director_VALUE / 'build').mkdir()
        SURSĂ = Director_VALUE / 'Imported.java'
        SURSĂ.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(SURSĂ)], check=True)
        원본 = (Director_VALUE / 'Imported.class').read_bytes()
        cod_VALUE, lungime_VALUE = 주코드(원본)
        변형 = {}
        date = bytearray(원본); date[0] = 0; 변형['BadMagic'] = date
        date = bytearray(원본); date[7] = 61; 변형['BadVer'] = date
        date = bytearray(원본); date[8:10] = b'\xff\xff'; 변형['BadPool'] = date
        date = bytearray(원본); date[cod_VALUE:cod_VALUE + lungime_VALUE] = bytes(lungime_VALUE)
        date[cod_VALUE:cod_VALUE + 3] = b'\xa7\x00\x01'; date[cod_VALUE + lungime_VALUE - 1] = 177; 변형['BadJump'] = date
        date = bytearray(원본); date[cod_VALUE:cod_VALUE + lungime_VALUE] = bytes(lungime_VALUE)
        date[cod_VALUE] = 87; date[cod_VALUE + lungime_VALUE - 1] = 177; 변형['BadStack'] = date
        # Nume 검사를 통과시켜 real_date executa_comandă 중의 operand_Teanc 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        intrare_VALUE = ['Imported.class=' + str(Director_VALUE / 'Imported.class'), 'Imported.java=' + str(SURSĂ)]
        for Nume, date in 변형.items():
            Cale = Director_VALUE / (Nume + '.class'); Cale.write_bytes(date)
            intrare_VALUE.append(Nume + '.class=' + str(Cale))
        grup_VALUE = Director_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Poziție / 'Instrumente/자바파일묶기.py'), '-o', str(grup_VALUE)] + intrare_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(Director_VALUE / 'user.o'), str(Poziție / '부팅/utilizator.s')], cwd=str(Director_VALUE), check=True)
        nucleu_VALUE = Director_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Poziție / '부팅/Link_Aspect.ld'), '-o', str(nucleu_VALUE),
                        str(Poziție / 'build/boot.o'), str(Poziție / 'build/java.o'), str(Director_VALUE / 'user.o'), str(Poziție / 'build/apps.o')], check=True)
        mașină = VM(nucleu_VALUE, rețea_VALUE=False)
        try:
            mașină.Comandă('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            mașină.Comandă('cat Imported.java', ['int[] values = new int[3]'])
            for Nume, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                mașină.Comandă('java ' + Nume, [문구, 'Exit: 1'])
                mașină.Comandă('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return mașină.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            mașină.Închide()


if __name__ == '__main__':
    analiza_VALUE = argparse.ArgumentParser()
    analiza_VALUE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    Argumente = analiza_VALUE.parse_args()
    KR = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if Argumente.boot == 'both' else (Argumente.boot,))}
    KR['import'] = 적재시험()
    (Poziție / 'build/자바시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2) + '\n')
