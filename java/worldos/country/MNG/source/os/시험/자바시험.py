#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Гүйцэтгэх_команд, гэмтэл_утга/хэрэгсэл_утга 경계 시험."""
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
from 사용자통신시험 import виртуал_компьютер, 위치


def засварлах_утга(компьютер, Нэр, Агуулга_утга, хадгалах_утга=True):
    Ажиллуулах = len(компьютер.бичих_мөр_6e8b375a)
    компьютер.직렬.sendall(('edit ' + Нэр + '\n').encode())
    компьютер.기다림('...> ', Ажиллуулах)
    for Шугам in Агуулга_утга.splitlines():
        assert len(Шугам) <= 128
        Ажиллуулах = len(компьютер.бичих_мөр_6e8b375a)
        компьютер.직렬.sendall((Шугам + '\n').encode())
        компьютер.기다림('...> ', Ажиллуулах)
    Ажиллуулах = len(компьютер.бичих_мөр_6e8b375a)
    компьютер.직렬.sendall(b'.save\n' if хадгалах_утга else b'.cancel\n')
    결과 = компьютер.기다림('jkoros> ', Ажиллуулах)
    assert ('Saved:' if хадгалах_утга else 'Cancelled; original preserved') in 결과, 결과


def файл_хаяг():
    결과 = subprocess.check_output(['nm', '-n', str(위치 / 'build/kernel.elf')], universal_newlines=True)
    for Шугам in 결과.splitlines():
        if Шугам.endswith(' ram_files'):
            return int(Шугам.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def 게스트파일(компьютер, зай_утга, Хэмжээ, ЗАМ):
    # 시험 VM의 메모리에서 бодит_өгөгдөл 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    хаяг = файл_хаяг() + зай_утга * 16384
    компьютер.хяналтын_төхөөрөмж_утга.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(хаяг, Хэмжээ, ЗАМ)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if ЗАМ.exists() and ЗАМ.stat().st_size == Хэмжээ:
            return ЗАМ.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    компьютер = виртуал_компьютер(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Сүлжээ_утга=False)
    결과 = {}
    try:
        компьютер.Тушаал('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        компьютер.Тушаал('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        компьютер.Тушаал('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        компьютер.Тушаал('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        компьютер.Тушаал('java Missing', ['cannot read class: -2', 'Exit: 1'])
        компьютер.Тушаал('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        компьютер.Тушаал('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Агуулга_утга = '''public class Calc {
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
        засварлах_утга(компьютер, 'Calc.java', Агуулга_утга)
        компьютер.Тушаал('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = компьютер.Тушаал('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        결과['guest_output'] = 출력
        оролт_Жагсаалт = компьютер.Тушаал('ls', ['Calc.class'])
        Хэмжээ = int(re.search(r'Calc\.class\s+(\d+) bytes', оролт_Жагсаалт).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as лавлах_утга:
            ЗАМ = Path(лавлах_утга) / 'Calc.class'
            өгөгдөл = 게스트파일(компьютер, 3, Хэмжээ, ЗАМ)
            бодит_өгөгдөл = subprocess.check_output(['java', '-Xverify:all', '-cp', лавлах_утга, 'Calc', '6', 'guest'], universal_newlines=True)
            assert бодит_өгөгдөл.splitlines() == 기대, бодит_өгөгдөл
            결과['class_sha256'] = hashlib.sha256(өгөгдөл).hexdigest()
            결과['openjdk_output'] = бодит_өгөгдөл
        # 실패한 засварлах_утга/컴파일은 기존 class를 보존한다.
        засварлах_утга(компьютер, 'Calc.java', 'not Java at all', хадгалах_утга=False)
        компьютер.Тушаал('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for 잘못 in [
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
            засварлах_утга(компьютер, 'Calc.java', 잘못)
            компьютер.Тушаал('javac Calc.java', ['javac error:', 'Exit: 1'])
            компьютер.Тушаал('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # давталт_утга 실행은 хэрэглэгч 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            компьютер.Тушаал('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        компьютер.Тушаал('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        компьютер.Тушаал('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        засварлах_утга(компьютер, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        компьютер.Тушаал('javac Calc.java', ['Compiled:', 'Exit: 0'])
        компьютер.Тушаал('java Calc', ['instruction limit', 'Exit: 1'])
        компьютер.Тушаал('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        засварлах_утга(компьютер, 'Bad.class', 'garbage')
        компьютер.Тушаал('java Bad', ['JVM error:', 'Exit: 1'])
        компьютер.Тушаал('rm Bad.class', ['Removed'])
        компьютер.Тушаал('java Bad', ['cannot read class: -2'])
        # засварлах_утга 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Ажиллуулах = len(компьютер.бичих_мөр_6e8b375a)
        компьютер.직렬.sendall(b'edit Hello.java\n')
        компьютер.기다림('...> ', Ажиллуулах)
        Ажиллуулах = len(компьютер.бичих_мөр_6e8b375a)
        компьютер.직렬.sendall(b'x' * 129 + b'\n')
        компьютер.기다림('...> ', Ажиллуулах)
        компьютер.Тушаал('.save', ['Too much input; original preserved'])
        компьютер.Тушаал('javac Hello.java', ['Compiled:', 'Exit: 0'])
        засварлах_утга(компьютер, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            засварлах_утга(компьютер, 'f' + str(수), 'occupied')
        компьютер.Тушаал('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        компьютер.Тушаал('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in компьютер.бичих_мөр_6e8b375a.decode('utf-8', 'replace')
        결과['serial'] = компьютер.бичих_мөр_6e8b375a.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return 결과
    finally:
        компьютер.Хаах()


def 주코드(өгөгдөл):
    """손상 시험용 main Code의 бодит_өгөгдөл Файл 오프셋/길이만 읽는다."""
    위치값 = 8
    def 짧():
        nonlocal 위치값
        утга = struct.unpack_from('>H', өгөгдөл, 위치값)[0]
        위치값 += 2
        return утга
    def 정():
        nonlocal 위치값
        утга = struct.unpack_from('>I', өгөгдөл, 위치값)[0]
        위치값 += 4
        return утга
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = өгөгдөл[위치값]
        위치값 += 1
        if 종류 == 1:
            урт_утга = 짧()
            문자들[수] = өгөгдөл[위치값:위치값 + урт_утга]
            위치값 += урт_утга
        elif 종류 in (7, 8): 위치값 += 2
        elif 종류 in (3, 9, 10, 12): 위치값 += 4
        else: raise AssertionError(종류)
    위치값 += 6
    개수 = 짧()
    위치값 += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Нэр = 짧()
        짧()
        for 수 in range(짧()):
            аттрибут_утга = 짧()
            Хэмжээ = 정()
            if 문자들[Нэр] == b'main' and 문자들[аттрибут_утга] == b'Code':
                return 위치값 + 8, struct.unpack_from('>I', өгөгдөл, 위치값 + 4)[0]
            위치값 += Хэмжээ
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        лавлах_утга = Path(임시)
        (лавлах_утга / 'build').mkdir()
        ЭХ = лавлах_утга / 'Imported.java'
        ЭХ.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ЭХ)], check=True)
        원본 = (лавлах_утга / 'Imported.class').read_bytes()
        코드, урт_утга = 주코드(원본)
        변형 = {}
        өгөгдөл = bytearray(원본); өгөгдөл[0] = 0; 변형['BadMagic'] = өгөгдөл
        өгөгдөл = bytearray(원본); өгөгдөл[7] = 61; 변형['BadVer'] = өгөгдөл
        өгөгдөл = bytearray(원본); өгөгдөл[8:10] = b'\xff\xff'; 변형['BadPool'] = өгөгдөл
        өгөгдөл = bytearray(원본); өгөгдөл[코드:코드 + урт_утга] = bytes(урт_утга)
        өгөгдөл[코드:코드 + 3] = b'\xa7\x00\x01'; өгөгдөл[코드 + урт_утга - 1] = 177; 변형['BadJump'] = өгөгдөл
        өгөгдөл = bytearray(원본); өгөгдөл[코드:코드 + урт_утга] = bytes(урт_утга)
        өгөгдөл[코드] = 87; өгөгдөл[코드 + урт_утга - 1] = 177; 변형['BadStack'] = өгөгдөл
        # Нэр 검사를 통과시켜 бодит_өгөгдөл Гүйцэтгэх_команд 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        оролт_утга = ['Imported.class=' + str(лавлах_утга / 'Imported.class'), 'Imported.java=' + str(ЭХ)]
        for Нэр, өгөгдөл in 변형.items():
            ЗАМ = лавлах_утга / (Нэр + '.class'); ЗАМ.write_bytes(өгөгдөл)
            оролт_утга.append(Нэр + '.class=' + str(ЗАМ))
        бүлэг_утга = лавлах_утга / 'build/java-files.bin'
        subprocess.run([sys.executable, str(위치 / 'Хэрэгслүүд/자바파일묶기.py'), '-o', str(бүлэг_утга)] + оролт_утга, check=True)
        subprocess.run(['as', '--32', '-o', str(лавлах_утга / 'user.o'), str(위치 / '부팅/хэрэглэгч.s')], cwd=str(лавлах_утга), check=True)
        кернел_утга = лавлах_утга / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/Холбох_Бүдүүвч.ld'), '-o', str(кернел_утга),
                        str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(лавлах_утга / 'user.o'), str(위치 / 'build/apps.o')], check=True)
        компьютер = виртуал_компьютер(кернел_утга, Сүлжээ_утга=False)
        try:
            компьютер.Тушаал('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            компьютер.Тушаал('cat Imported.java', ['int[] values = new int[3]'])
            for Нэр, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                компьютер.Тушаал('java ' + Нэр, [문구, 'Exit: 1'])
                компьютер.Тушаал('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return компьютер.бичих_мөр_6e8b375a.decode('utf-8', 'replace')
        finally:
            компьютер.Хаах()


if __name__ == '__main__':
    задлан_ялгал_хийх_утга = argparse.ArgumentParser()
    задлан_ялгал_хийх_утга.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = задлан_ялгал_хийх_утга.parse_args()
    결과 = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    결과['import'] = 적재시험()
    (위치 / 'build/자바시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n')
