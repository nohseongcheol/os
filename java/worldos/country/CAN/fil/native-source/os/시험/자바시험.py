#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Mag_execute_utos, pagpalya_VALUE/resource_VALUE 경계 시험."""
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
from 사용자통신시험 import virtual_machine, posisyon


def edit_VALUE(machine, pangalan, Nilalaman_VALUE, Store_VALUE=True):
    run = len(machine.LOG_hanay)
    machine.직렬.sendall(('edit ' + pangalan + '\n').encode())
    machine.maghintay_katayuan('...> ', run)
    for linya in Nilalaman_VALUE.splitlines():
        assert len(linya) <= 128
        run = len(machine.LOG_hanay)
        machine.직렬.sendall((linya + '\n').encode())
        machine.maghintay_katayuan('...> ', run)
    run = len(machine.LOG_hanay)
    machine.직렬.sendall(b'.save\n' if Store_VALUE else b'.cancel\n')
    sukat = machine.maghintay_katayuan('jkoros> ', run)
    assert ('Saved:' if Store_VALUE else 'Cancelled; original preserved') in sukat, sukat


def file_email():
    sukat = subprocess.check_output(['nm', '-n', str(posisyon / 'build/kernel.elf')], universal_newlines=True)
    for linya in sukat.splitlines():
        if linya.endswith(' ram_files'):
            return int(linya.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def bisita_file(machine, espasyo_VALUE, sukat_82232621, path):
    # 시험 VM의 메모리에서 totoo_data 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    email = file_email() + espasyo_VALUE * 16384
    machine.monitor_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(email, sukat_82232621, path)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if path.exists() and path.stat().st_size == sukat_82232621:
            return path.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    machine = virtual_machine(posisyon / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Network_VALUE=False)
    sukat = {}
    try:
        machine.utos('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        machine.utos('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        machine.utos('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        machine.utos('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        machine.utos('java Missing', ['cannot read class: -2', 'Exit: 1'])
        machine.utos('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        machine.utos('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Nilalaman_VALUE = '''public class Calc {
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
        edit_VALUE(machine, 'Calc.java', Nilalaman_VALUE)
        machine.utos('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = machine.utos('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        sukat['guest_output'] = 출력
        pagpasok_list = machine.utos('ls', ['Calc.class'])
        sukat_82232621 = int(re.search(r'Calc\.class\s+(\d+) bytes', pagpasok_list).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as Directory_VALUE:
            path = Path(Directory_VALUE) / 'Calc.class'
            data = bisita_file(machine, 3, sukat_82232621, path)
            totoo_data = subprocess.check_output(['java', '-Xverify:all', '-cp', Directory_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert totoo_data.splitlines() == 기대, totoo_data
            sukat['class_sha256'] = hashlib.sha256(data).hexdigest()
            sukat['openjdk_output'] = totoo_data
        # 실패한 edit_VALUE/컴파일은 기존 class를 보존한다.
        edit_VALUE(machine, 'Calc.java', 'not Java at all', Store_VALUE=False)
        machine.utos('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for hindi_tama_sukat in [
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
            edit_VALUE(machine, 'Calc.java', hindi_tama_sukat)
            machine.utos('javac Calc.java', ['javac error:', 'Exit: 1'])
            machine.utos('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # sprint_VALUE 실행은 gumagamit 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            machine.utos('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        machine.utos('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        machine.utos('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        edit_VALUE(machine, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        machine.utos('javac Calc.java', ['Compiled:', 'Exit: 0'])
        machine.utos('java Calc', ['instruction limit', 'Exit: 1'])
        machine.utos('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        edit_VALUE(machine, 'Bad.class', 'garbage')
        machine.utos('java Bad', ['JVM error:', 'Exit: 1'])
        machine.utos('rm Bad.class', ['Removed'])
        machine.utos('java Bad', ['cannot read class: -2'])
        # edit_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        run = len(machine.LOG_hanay)
        machine.직렬.sendall(b'edit Hello.java\n')
        machine.maghintay_katayuan('...> ', run)
        run = len(machine.LOG_hanay)
        machine.직렬.sendall(b'x' * 129 + b'\n')
        machine.maghintay_katayuan('...> ', run)
        machine.utos('.save', ['Too much input; original preserved'])
        machine.utos('javac Hello.java', ['Compiled:', 'Exit: 0'])
        edit_VALUE(machine, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            edit_VALUE(machine, 'f' + str(수), 'occupied')
        machine.utos('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        machine.utos('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in machine.LOG_hanay.decode('utf-8', 'replace')
        sukat['serial'] = machine.LOG_hanay.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return sukat
    finally:
        machine.isara()


def 주코드(data):
    """손상 시험용 main Code의 totoo_data file 오프셋/길이만 읽는다."""
    posisyon_VALUE = 8
    def 짧():
        nonlocal posisyon_VALUE
        VALUE = struct.unpack_from('>H', data, posisyon_VALUE)[0]
        posisyon_VALUE += 2
        return VALUE
    def 정():
        nonlocal posisyon_VALUE
        VALUE = struct.unpack_from('>I', data, posisyon_VALUE)[0]
        posisyon_VALUE += 4
        return VALUE
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = data[posisyon_VALUE]
        posisyon_VALUE += 1
        if 종류 == 1:
            haba_VALUE = 짧()
            문자들[수] = data[posisyon_VALUE:posisyon_VALUE + haba_VALUE]
            posisyon_VALUE += haba_VALUE
        elif 종류 in (7, 8): posisyon_VALUE += 2
        elif 종류 in (3, 9, 10, 12): posisyon_VALUE += 4
        else: raise AssertionError(종류)
    posisyon_VALUE += 6
    item_COUNT = 짧()
    posisyon_VALUE += item_COUNT * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        pangalan = 짧()
        짧()
        for 수 in range(짧()):
            katangian_VALUE = 짧()
            sukat_82232621 = 정()
            if 문자들[pangalan] == b'main' and 문자들[katangian_VALUE] == b'Code':
                return posisyon_VALUE + 8, struct.unpack_from('>I', data, posisyon_VALUE + 4)[0]
            posisyon_VALUE += sukat_82232621
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        Directory_VALUE = Path(임시)
        (Directory_VALUE / 'build').mkdir()
        pinagmulan = Directory_VALUE / 'Imported.java'
        pinagmulan.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(pinagmulan)], check=True)
        원본 = (Directory_VALUE / 'Imported.class').read_bytes()
        CODE_VALUE, haba_VALUE = 주코드(원본)
        변형 = {}
        data = bytearray(원본); data[0] = 0; 변형['BadMagic'] = data
        data = bytearray(원본); data[7] = 61; 변형['BadVer'] = data
        data = bytearray(원본); data[8:10] = b'\xff\xff'; 변형['BadPool'] = data
        data = bytearray(원본); data[CODE_VALUE:CODE_VALUE + haba_VALUE] = bytes(haba_VALUE)
        data[CODE_VALUE:CODE_VALUE + 3] = b'\xa7\x00\x01'; data[CODE_VALUE + haba_VALUE - 1] = 177; 변형['BadJump'] = data
        data = bytearray(원본); data[CODE_VALUE:CODE_VALUE + haba_VALUE] = bytes(haba_VALUE)
        data[CODE_VALUE] = 87; data[CODE_VALUE + haba_VALUE - 1] = 177; 변형['BadStack'] = data
        # pangalan 검사를 통과시켜 totoo_data Mag_execute_utos 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        pagpasok_VALUE = ['Imported.class=' + str(Directory_VALUE / 'Imported.class'), 'Imported.java=' + str(pinagmulan)]
        for pangalan, data in 변형.items():
            path = Directory_VALUE / (pangalan + '.class'); path.write_bytes(data)
            pagpasok_VALUE.append(pangalan + '.class=' + str(path))
        Grupo_VALUE = Directory_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(posisyon / 'Mga_Tool/자바파일묶기.py'), '-o', str(Grupo_VALUE)] + pagpasok_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(Directory_VALUE / 'user.o'), str(posisyon / '부팅/gumagamit.s')], cwd=str(Directory_VALUE), check=True)
        kernel_VALUE = Directory_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(posisyon / '부팅/Link_Layout.ld'), '-o', str(kernel_VALUE),
                        str(posisyon / 'build/boot.o'), str(posisyon / 'build/java.o'), str(Directory_VALUE / 'user.o'), str(posisyon / 'build/apps.o')], check=True)
        machine = virtual_machine(kernel_VALUE, Network_VALUE=False)
        try:
            machine.utos('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            machine.utos('cat Imported.java', ['int[] values = new int[3]'])
            for pangalan, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                machine.utos('java ' + pangalan, [문구, 'Exit: 1'])
                machine.utos('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return machine.LOG_hanay.decode('utf-8', 'replace')
        finally:
            machine.isara()


if __name__ == '__main__':
    mag_parse_VALUE = argparse.ArgumentParser()
    mag_parse_VALUE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = mag_parse_VALUE.parse_args()
    sukat = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    sukat['import'] = 적재시험()
    (posisyon / 'build/자바시험.json').write_text(json.dumps(sukat, ensure_ascii=False, indent=2) + '\n')
