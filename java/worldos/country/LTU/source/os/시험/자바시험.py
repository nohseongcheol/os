#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Vykdyti_komanda, triktis_VALUE/ištekliai_VALUE 경계 시험."""
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
from 사용자통신시험 import VM, Pozicija


def redaguoti_VALUE(mašina, Pavadinimas_2, Turinys_VALUE, Store_VALUE=True):
    Paleisti = len(mašina.LOG_RECORD)
    mašina.직렬.sendall(('edit ' + Pavadinimas_2 + '\n').encode())
    mašina.laukimo_būsena('...> ', Paleisti)
    for Eilutė in Turinys_VALUE.splitlines():
        assert len(Eilutė) <= 128
        Paleisti = len(mašina.LOG_RECORD)
        mašina.직렬.sendall((Eilutė + '\n').encode())
        mašina.laukimo_būsena('...> ', Paleisti)
    Paleisti = len(mašina.LOG_RECORD)
    mašina.직렬.sendall(b'.save\n' if Store_VALUE else b'.cancel\n')
    REZULTATAS = mašina.laukimo_būsena('jkoros> ', Paleisti)
    assert ('Saved:' if Store_VALUE else 'Cancelled; original preserved') in REZULTATAS, REZULTATAS


def Failas_ADDRESS():
    REZULTATAS = subprocess.check_output(['nm', '-n', str(Pozicija / 'build/kernel.elf')], universal_newlines=True)
    for Eilutė in REZULTATAS.splitlines():
        if Eilutė.endswith(' ram_files'):
            return int(Eilutė.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def svečias_Failas(mašina, 슬롯, Dydis, KELIAS):
    # 시험 VM의 메모리에서 faktinis_duomenys 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ADDRESS = Failas_ADDRESS() + 슬롯 * 16384
    mašina.stebėti_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ADDRESS, Dydis, KELIAS)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if KELIAS.exists() and KELIAS.stat().st_size == Dydis:
            return KELIAS.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    mašina = VM(Pozicija / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, tinklas_VALUE=False)
    REZULTATAS = {}
    try:
        mašina.Komanda('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        mašina.Komanda('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        mašina.Komanda('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        mašina.Komanda('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        mašina.Komanda('java Missing', ['cannot read class: -2', 'Exit: 1'])
        mašina.Komanda('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        mašina.Komanda('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Turinys_VALUE = '''public class Calc {
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
        redaguoti_VALUE(mašina, 'Calc.java', Turinys_VALUE)
        mašina.Komanda('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Išvestis = mašina.Komanda('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        REZULTATAS['guest_output'] = Išvestis
        įrašas_Sąrašas = mašina.Komanda('ls', ['Calc.class'])
        Dydis = int(re.search(r'Calc\.class\s+(\d+) bytes', įrašas_Sąrašas).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as Katalogas_VALUE:
            KELIAS = Path(Katalogas_VALUE) / 'Calc.class'
            duomenys = svečias_Failas(mašina, 3, Dydis, KELIAS)
            faktinis_duomenys = subprocess.check_output(['java', '-Xverify:all', '-cp', Katalogas_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert faktinis_duomenys.splitlines() == 기대, faktinis_duomenys
            REZULTATAS['class_sha256'] = hashlib.sha256(duomenys).hexdigest()
            REZULTATAS['openjdk_output'] = faktinis_duomenys
        # 실패한 redaguoti_VALUE/컴파일은 기존 class를 보존한다.
        redaguoti_VALUE(mašina, 'Calc.java', 'not Java at all', Store_VALUE=False)
        mašina.Komanda('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for neleistinas_KR in [
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
            redaguoti_VALUE(mašina, 'Calc.java', neleistinas_KR)
            mašina.Komanda('javac Calc.java', ['javac error:', 'Exit: 1'])
            mašina.Komanda('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # sprintas_VALUE 실행은 naudotojas 힙/프레임을 매번 초기화한다.
        for numeris in range(12):
            mašina.Komanda('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        mašina.Komanda('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        mašina.Komanda('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        redaguoti_VALUE(mašina, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        mašina.Komanda('javac Calc.java', ['Compiled:', 'Exit: 0'])
        mašina.Komanda('java Calc', ['instruction limit', 'Exit: 1'])
        mašina.Komanda('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        redaguoti_VALUE(mašina, 'Bad.class', 'garbage')
        mašina.Komanda('java Bad', ['JVM error:', 'Exit: 1'])
        mašina.Komanda('rm Bad.class', ['Removed'])
        mašina.Komanda('java Bad', ['cannot read class: -2'])
        # redaguoti_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Paleisti = len(mašina.LOG_RECORD)
        mašina.직렬.sendall(b'edit Hello.java\n')
        mašina.laukimo_būsena('...> ', Paleisti)
        Paleisti = len(mašina.LOG_RECORD)
        mašina.직렬.sendall(b'x' * 129 + b'\n')
        mašina.laukimo_būsena('...> ', Paleisti)
        mašina.Komanda('.save', ['Too much input; original preserved'])
        mašina.Komanda('javac Hello.java', ['Compiled:', 'Exit: 0'])
        redaguoti_VALUE(mašina, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for numeris in range(3):
            redaguoti_VALUE(mašina, 'f' + str(numeris), 'occupied')
        mašina.Komanda('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        mašina.Komanda('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in mašina.LOG_RECORD.decode('utf-8', 'replace')
        REZULTATAS['serial'] = mašina.LOG_RECORD.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return REZULTATAS
    finally:
        mašina.Užverti()


def 주코드(duomenys):
    """손상 시험용 main Code의 faktinis_duomenys Failas 오프셋/길이만 읽는다."""
    padėtis_VALUE = 8
    def 짧():
        nonlocal padėtis_VALUE
        VALUE = struct.unpack_from('>H', duomenys, padėtis_VALUE)[0]
        padėtis_VALUE += 2
        return VALUE
    def 정():
        nonlocal padėtis_VALUE
        VALUE = struct.unpack_from('>I', duomenys, padėtis_VALUE)[0]
        padėtis_VALUE += 4
        return VALUE
    문자들 = {}
    for numeris in range(1, 짧()):
        종류 = duomenys[padėtis_VALUE]
        padėtis_VALUE += 1
        if 종류 == 1:
            길이 = 짧()
            문자들[numeris] = duomenys[padėtis_VALUE:padėtis_VALUE + 길이]
            padėtis_VALUE += 길이
        elif 종류 in (7, 8): padėtis_VALUE += 2
        elif 종류 in (3, 9, 10, 12): padėtis_VALUE += 4
        else: raise AssertionError(종류)
    padėtis_VALUE += 6
    prekė_COUNT = 짧()
    padėtis_VALUE += prekė_COUNT * 2
    assert 짧() == 0
    for numeris in range(짧()):
        짧()
        Pavadinimas_2 = 짧()
        짧()
        for numeris in range(짧()):
            atributas_VALUE = 짧()
            Dydis = 정()
            if 문자들[Pavadinimas_2] == b'main' and 문자들[atributas_VALUE] == b'Code':
                return padėtis_VALUE + 8, struct.unpack_from('>I', duomenys, padėtis_VALUE + 4)[0]
            padėtis_VALUE += Dydis
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        Katalogas_VALUE = Path(임시)
        (Katalogas_VALUE / 'build').mkdir()
        ŠALTINIS = Katalogas_VALUE / 'Imported.java'
        ŠALTINIS.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ŠALTINIS)], check=True)
        원본 = (Katalogas_VALUE / 'Imported.class').read_bytes()
        CODE_VALUE, 길이 = 주코드(원본)
        variantas_VALUE = {}
        duomenys = bytearray(원본); duomenys[0] = 0; variantas_VALUE['BadMagic'] = duomenys
        duomenys = bytearray(원본); duomenys[7] = 61; variantas_VALUE['BadVer'] = duomenys
        duomenys = bytearray(원본); duomenys[8:10] = b'\xff\xff'; variantas_VALUE['BadPool'] = duomenys
        duomenys = bytearray(원본); duomenys[CODE_VALUE:CODE_VALUE + 길이] = bytes(길이)
        duomenys[CODE_VALUE:CODE_VALUE + 3] = b'\xa7\x00\x01'; duomenys[CODE_VALUE + 길이 - 1] = 177; variantas_VALUE['BadJump'] = duomenys
        duomenys = bytearray(원본); duomenys[CODE_VALUE:CODE_VALUE + 길이] = bytes(길이)
        duomenys[CODE_VALUE] = 87; duomenys[CODE_VALUE + 길이 - 1] = 177; variantas_VALUE['BadStack'] = duomenys
        # Pavadinimas_2 검사를 통과시켜 faktinis_duomenys Vykdyti_komanda 중의 operandas_eilė 오류까지 검사한다.
        variantas_VALUE['BadStack'] = variantas_VALUE['BadStack'].replace(b'Imported', b'BadStack')
        įrašas_VALUE = ['Imported.class=' + str(Katalogas_VALUE / 'Imported.class'), 'Imported.java=' + str(ŠALTINIS)]
        for Pavadinimas_2, duomenys in variantas_VALUE.items():
            KELIAS = Katalogas_VALUE / (Pavadinimas_2 + '.class'); KELIAS.write_bytes(duomenys)
            įrašas_VALUE.append(Pavadinimas_2 + '.class=' + str(KELIAS))
        Grupė_VALUE = Katalogas_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Pozicija / 'Įrankiai/자바파일묶기.py'), '-o', str(Grupė_VALUE)] + įrašas_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(Katalogas_VALUE / 'user.o'), str(Pozicija / '부팅/naudotojas.s')], cwd=str(Katalogas_VALUE), check=True)
        branduolys_VALUE = Katalogas_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Pozicija / '부팅/sieti_schema.ld'), '-o', str(branduolys_VALUE),
                        str(Pozicija / 'build/boot.o'), str(Pozicija / 'build/java.o'), str(Katalogas_VALUE / 'user.o'), str(Pozicija / 'build/apps.o')], check=True)
        mašina = VM(branduolys_VALUE, tinklas_VALUE=False)
        try:
            mašina.Komanda('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            mašina.Komanda('cat Imported.java', ['int[] values = new int[3]'])
            for Pavadinimas_2, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                mašina.Komanda('java ' + Pavadinimas_2, [문구, 'Exit: 1'])
                mašina.Komanda('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return mašina.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            mašina.Užverti()


if __name__ == '__main__':
    analizuoti_sintaksę_VALUE = argparse.ArgumentParser()
    analizuoti_sintaksę_VALUE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    Argumentai = analizuoti_sintaksę_VALUE.parse_args()
    REZULTATAS = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if Argumentai.boot == 'both' else (Argumentai.boot,))}
    REZULTATAS['import'] = 적재시험()
    (Pozicija / 'build/자바시험.json').write_text(json.dumps(REZULTATAS, ensure_ascii=False, indent=2) + '\n')
