#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 eżegwixxa_kmand, żball_VALUE/riżorsa_VALUE 경계 시험."""
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
from 사용자통신시험 import virtwali_kompjuter, pożizzjoni


def editja_VALUE(kompjuter, isem, Kontenut_VALUE, Store_VALUE=True):
    serje = len(kompjuter.LOG_RECORD)
    kompjuter.직렬.sendall(('edit ' + isem + '\n').encode())
    kompjuter.기다림('...> ', serje)
    for linja in Kontenut_VALUE.splitlines():
        assert len(linja) <= 128
        serje = len(kompjuter.LOG_RECORD)
        kompjuter.직렬.sendall((linja + '\n').encode())
        kompjuter.기다림('...> ', serje)
    serje = len(kompjuter.LOG_RECORD)
    kompjuter.직렬.sendall(b'.save\n' if Store_VALUE else b'.cancel\n')
    miżura = kompjuter.기다림('jkoros> ', serje)
    assert ('Saved:' if Store_VALUE else 'Cancelled; original preserved') in miżura, miżura


def fajl_ADDRESS():
    miżura = subprocess.check_output(['nm', '-n', str(pożizzjoni / 'build/kernel.elf')], universal_newlines=True)
    for linja in miżura.splitlines():
        if linja.endswith(' ram_files'):
            return int(linja.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def mistieden_fajl(kompjuter, slott_VALUE, daqqas, mogħdija):
    # 시험 VM의 메모리에서 attwali_data 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ADDRESS = fajl_ADDRESS() + slott_VALUE * 16384
    kompjuter.moniter_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ADDRESS, daqqas, mogħdija)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if mogħdija.exists() and mogħdija.stat().st_size == daqqas:
            return mogħdija.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    kompjuter = virtwali_kompjuter(pożizzjoni / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, netwerk_VALUE=False)
    miżura = {}
    try:
        kompjuter.kmand('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        kompjuter.kmand('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        kompjuter.kmand('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        kompjuter.kmand('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        kompjuter.kmand('java Missing', ['cannot read class: -2', 'Exit: 1'])
        kompjuter.kmand('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        kompjuter.kmand('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Kontenut_VALUE = '''public class Calc {
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
        editja_VALUE(kompjuter, 'Calc.java', Kontenut_VALUE)
        kompjuter.kmand('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = kompjuter.kmand('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        miżura['guest_output'] = 출력
        entrata_Lista = kompjuter.kmand('ls', ['Calc.class'])
        daqqas = int(re.search(r'Calc\.class\s+(\d+) bytes', entrata_Lista).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as direttorju_VALUE:
            mogħdija = Path(direttorju_VALUE) / 'Calc.class'
            data = mistieden_fajl(kompjuter, 3, daqqas, mogħdija)
            attwali_data = subprocess.check_output(['java', '-Xverify:all', '-cp', direttorju_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert attwali_data.splitlines() == 기대, attwali_data
            miżura['class_sha256'] = hashlib.sha256(data).hexdigest()
            miżura['openjdk_output'] = attwali_data
        # 실패한 editja_VALUE/컴파일은 기존 class를 보존한다.
        editja_VALUE(kompjuter, 'Calc.java', 'not Java at all', Store_VALUE=False)
        kompjuter.kmand('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for invalidu_miżura in [
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
            editja_VALUE(kompjuter, 'Calc.java', invalidu_miżura)
            kompjuter.kmand('javac Calc.java', ['javac error:', 'Exit: 1'])
            kompjuter.kmand('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # iterazzjoni_VALUE 실행은 utent 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            kompjuter.kmand('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        kompjuter.kmand('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        kompjuter.kmand('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        editja_VALUE(kompjuter, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        kompjuter.kmand('javac Calc.java', ['Compiled:', 'Exit: 0'])
        kompjuter.kmand('java Calc', ['instruction limit', 'Exit: 1'])
        kompjuter.kmand('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        editja_VALUE(kompjuter, 'Bad.class', 'garbage')
        kompjuter.kmand('java Bad', ['JVM error:', 'Exit: 1'])
        kompjuter.kmand('rm Bad.class', ['Removed'])
        kompjuter.kmand('java Bad', ['cannot read class: -2'])
        # editja_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        serje = len(kompjuter.LOG_RECORD)
        kompjuter.직렬.sendall(b'edit Hello.java\n')
        kompjuter.기다림('...> ', serje)
        serje = len(kompjuter.LOG_RECORD)
        kompjuter.직렬.sendall(b'x' * 129 + b'\n')
        kompjuter.기다림('...> ', serje)
        kompjuter.kmand('.save', ['Too much input; original preserved'])
        kompjuter.kmand('javac Hello.java', ['Compiled:', 'Exit: 0'])
        editja_VALUE(kompjuter, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            editja_VALUE(kompjuter, 'f' + str(수), 'occupied')
        kompjuter.kmand('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        kompjuter.kmand('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in kompjuter.LOG_RECORD.decode('utf-8', 'replace')
        miżura['serial'] = kompjuter.LOG_RECORD.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return miżura
    finally:
        kompjuter.agħlaq()


def 주코드(data):
    """손상 시험용 main Code의 attwali_data fajl 오프셋/길이만 읽는다."""
    pożizzjoni_VALUE = 8
    def 짧():
        nonlocal pożizzjoni_VALUE
        VALUE = struct.unpack_from('>H', data, pożizzjoni_VALUE)[0]
        pożizzjoni_VALUE += 2
        return VALUE
    def 정():
        nonlocal pożizzjoni_VALUE
        VALUE = struct.unpack_from('>I', data, pożizzjoni_VALUE)[0]
        pożizzjoni_VALUE += 4
        return VALUE
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = data[pożizzjoni_VALUE]
        pożizzjoni_VALUE += 1
        if 종류 == 1:
            tul_VALUE = 짧()
            문자들[수] = data[pożizzjoni_VALUE:pożizzjoni_VALUE + tul_VALUE]
            pożizzjoni_VALUE += tul_VALUE
        elif 종류 in (7, 8): pożizzjoni_VALUE += 2
        elif 종류 in (3, 9, 10, 12): pożizzjoni_VALUE += 4
        else: raise AssertionError(종류)
    pożizzjoni_VALUE += 6
    element_COUNT = 짧()
    pożizzjoni_VALUE += element_COUNT * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        isem = 짧()
        짧()
        for 수 in range(짧()):
            attribut_VALUE = 짧()
            daqqas = 정()
            if 문자들[isem] == b'main' and 문자들[attribut_VALUE] == b'Code':
                return pożizzjoni_VALUE + 8, struct.unpack_from('>I', data, pożizzjoni_VALUE + 4)[0]
            pożizzjoni_VALUE += daqqas
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        direttorju_VALUE = Path(임시)
        (direttorju_VALUE / 'build').mkdir()
        sors = direttorju_VALUE / 'Imported.java'
        sors.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(sors)], check=True)
        원본 = (direttorju_VALUE / 'Imported.class').read_bytes()
        CODE_VALUE, tul_VALUE = 주코드(원본)
        변형 = {}
        data = bytearray(원본); data[0] = 0; 변형['BadMagic'] = data
        data = bytearray(원본); data[7] = 61; 변형['BadVer'] = data
        data = bytearray(원본); data[8:10] = b'\xff\xff'; 변형['BadPool'] = data
        data = bytearray(원본); data[CODE_VALUE:CODE_VALUE + tul_VALUE] = bytes(tul_VALUE)
        data[CODE_VALUE:CODE_VALUE + 3] = b'\xa7\x00\x01'; data[CODE_VALUE + tul_VALUE - 1] = 177; 변형['BadJump'] = data
        data = bytearray(원본); data[CODE_VALUE:CODE_VALUE + tul_VALUE] = bytes(tul_VALUE)
        data[CODE_VALUE] = 87; data[CODE_VALUE + tul_VALUE - 1] = 177; 변형['BadStack'] = data
        # isem 검사를 통과시켜 attwali_data eżegwixxa_kmand 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        entrata_VALUE = ['Imported.class=' + str(direttorju_VALUE / 'Imported.class'), 'Imported.java=' + str(sors)]
        for isem, data in 변형.items():
            mogħdija = direttorju_VALUE / (isem + '.class'); mogħdija.write_bytes(data)
            entrata_VALUE.append(isem + '.class=' + str(mogħdija))
        grupp_VALUE = direttorju_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(pożizzjoni / 'Għodod/자바파일묶기.py'), '-o', str(grupp_VALUE)] + entrata_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(direttorju_VALUE / 'user.o'), str(pożizzjoni / '부팅/utent.s')], cwd=str(direttorju_VALUE), check=True)
        kernel_VALUE = direttorju_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(pożizzjoni / '부팅/Link_Tqassim.ld'), '-o', str(kernel_VALUE),
                        str(pożizzjoni / 'build/boot.o'), str(pożizzjoni / 'build/java.o'), str(direttorju_VALUE / 'user.o'), str(pożizzjoni / 'build/apps.o')], check=True)
        kompjuter = virtwali_kompjuter(kernel_VALUE, netwerk_VALUE=False)
        try:
            kompjuter.kmand('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            kompjuter.kmand('cat Imported.java', ['int[] values = new int[3]'])
            for isem, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                kompjuter.kmand('java ' + isem, [문구, 'Exit: 1'])
                kompjuter.kmand('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return kompjuter.LOG_RECORD.decode('utf-8', 'replace')
        finally:
            kompjuter.agħlaq()


if __name__ == '__main__':
    analizza_VALUE = argparse.ArgumentParser()
    analizza_VALUE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = analizza_VALUE.parse_args()
    miżura = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    miżura['import'] = 적재시험()
    (pożizzjoni / 'build/자바시험.json').write_text(json.dumps(miżura, ensure_ascii=False, indent=2) + '\n')
