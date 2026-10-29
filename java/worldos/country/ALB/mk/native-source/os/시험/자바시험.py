#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Изврши_наредба, неуспех_VALUE/извор_VALUE 경계 시험."""
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
from 사용자통신시험 import виртуелен_машина, Позиција


def уреди_VALUE(машина, Име, Содржина_VALUE, Store_VALUE=True):
    Изврши_2 = len(машина.LOG_ред)
    машина.직렬.sendall(('edit ' + Име + '\n').encode())
    машина.почекај_статус('...> ', Изврши_2)
    for ред in Содржина_VALUE.splitlines():
        assert len(ред) <= 128
        Изврши_2 = len(машина.LOG_ред)
        машина.직렬.sendall((ред + '\n').encode())
        машина.почекај_статус('...> ', Изврши_2)
    Изврши_2 = len(машина.LOG_ред)
    машина.직렬.sendall(b'.save\n' if Store_VALUE else b'.cancel\n')
    мерка = машина.почекај_статус('jkoros> ', Изврши_2)
    assert ('Saved:' if Store_VALUE else 'Cancelled; original preserved') in мерка, мерка


def датотека_адреса():
    мерка = subprocess.check_output(['nm', '-n', str(Позиција / 'build/kernel.elf')], universal_newlines=True)
    for ред in мерка.splitlines():
        if ред.endswith(' ram_files'):
            return int(ред.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def гостин_датотека(машина, отвор_VALUE, Големина, ПАТЕКА):
    # 시험 VM의 메모리에서 реален_податоци 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    адреса = датотека_адреса() + отвор_VALUE * 16384
    машина.монитор_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(адреса, Големина, ПАТЕКА)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if ПАТЕКА.exists() and ПАТЕКА.stat().st_size == Големина:
            return ПАТЕКА.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    машина = виртуелен_машина(Позиција / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, Мрежа_VALUE=False)
    мерка = {}
    try:
        машина.Команда('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        машина.Команда('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        машина.Команда('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        машина.Команда('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        машина.Команда('java Missing', ['cannot read class: -2', 'Exit: 1'])
        машина.Команда('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        машина.Команда('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Содржина_VALUE = '''public class Calc {
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
        уреди_VALUE(машина, 'Calc.java', Содржина_VALUE)
        машина.Команда('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = машина.Команда('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        мерка['guest_output'] = 출력
        внес_Список = машина.Команда('ls', ['Calc.class'])
        Големина = int(re.search(r'Calc\.class\s+(\d+) bytes', внес_Список).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as Именик_VALUE:
            ПАТЕКА = Path(Именик_VALUE) / 'Calc.class'
            податоци = гостин_датотека(машина, 3, Големина, ПАТЕКА)
            реален_податоци = subprocess.check_output(['java', '-Xverify:all', '-cp', Именик_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert реален_податоци.splitlines() == 기대, реален_податоци
            мерка['class_sha256'] = hashlib.sha256(податоци).hexdigest()
            мерка['openjdk_output'] = реален_податоци
        # 실패한 уреди_VALUE/컴파일은 기존 class를 보존한다.
        уреди_VALUE(машина, 'Calc.java', 'not Java at all', Store_VALUE=False)
        машина.Команда('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for неважечки_мерка in [
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
            уреди_VALUE(машина, 'Calc.java', неважечки_мерка)
            машина.Команда('javac Calc.java', ['javac error:', 'Exit: 1'])
            машина.Команда('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # повторување_VALUE 실행은 корисник 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            машина.Команда('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        машина.Команда('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        машина.Команда('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        уреди_VALUE(машина, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        машина.Команда('javac Calc.java', ['Compiled:', 'Exit: 0'])
        машина.Команда('java Calc', ['instruction limit', 'Exit: 1'])
        машина.Команда('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        уреди_VALUE(машина, 'Bad.class', 'garbage')
        машина.Команда('java Bad', ['JVM error:', 'Exit: 1'])
        машина.Команда('rm Bad.class', ['Removed'])
        машина.Команда('java Bad', ['cannot read class: -2'])
        # уреди_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Изврши_2 = len(машина.LOG_ред)
        машина.직렬.sendall(b'edit Hello.java\n')
        машина.почекај_статус('...> ', Изврши_2)
        Изврши_2 = len(машина.LOG_ред)
        машина.직렬.sendall(b'x' * 129 + b'\n')
        машина.почекај_статус('...> ', Изврши_2)
        машина.Команда('.save', ['Too much input; original preserved'])
        машина.Команда('javac Hello.java', ['Compiled:', 'Exit: 0'])
        уреди_VALUE(машина, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            уреди_VALUE(машина, 'f' + str(수), 'occupied')
        машина.Команда('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        машина.Команда('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in машина.LOG_ред.decode('utf-8', 'replace')
        мерка['serial'] = машина.LOG_ред.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return мерка
    finally:
        машина.Затвори()


def 주코드(податоци):
    """손상 시험용 main Code의 реален_податоци Датотека 오프셋/길이만 읽는다."""
    позиционирање_VALUE = 8
    def 짧():
        nonlocal позиционирање_VALUE
        VALUE = struct.unpack_from('>H', податоци, позиционирање_VALUE)[0]
        позиционирање_VALUE += 2
        return VALUE
    def 정():
        nonlocal позиционирање_VALUE
        VALUE = struct.unpack_from('>I', податоци, позиционирање_VALUE)[0]
        позиционирање_VALUE += 4
        return VALUE
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = податоци[позиционирање_VALUE]
        позиционирање_VALUE += 1
        if 종류 == 1:
            должина_VALUE = 짧()
            문자들[수] = податоци[позиционирање_VALUE:позиционирање_VALUE + должина_VALUE]
            позиционирање_VALUE += должина_VALUE
        elif 종류 in (7, 8): позиционирање_VALUE += 2
        elif 종류 in (3, 9, 10, 12): позиционирање_VALUE += 4
        else: raise AssertionError(종류)
    позиционирање_VALUE += 6
    ставка_COUNT = 짧()
    позиционирање_VALUE += ставка_COUNT * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Име = 짧()
        짧()
        for 수 in range(짧()):
            атрибут_VALUE = 짧()
            Големина = 정()
            if 문자들[Име] == b'main' and 문자들[атрибут_VALUE] == b'Code':
                return позиционирање_VALUE + 8, struct.unpack_from('>I', податоци, позиционирање_VALUE + 4)[0]
            позиционирање_VALUE += Големина
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        Именик_VALUE = Path(임시)
        (Именик_VALUE / 'build').mkdir()
        ИЗВОР = Именик_VALUE / 'Imported.java'
        ИЗВОР.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ИЗВОР)], check=True)
        원본 = (Именик_VALUE / 'Imported.class').read_bytes()
        CODE_VALUE, должина_VALUE = 주코드(원본)
        변형 = {}
        податоци = bytearray(원본); податоци[0] = 0; 변형['BadMagic'] = податоци
        податоци = bytearray(원본); податоци[7] = 61; 변형['BadVer'] = податоци
        податоци = bytearray(원본); податоци[8:10] = b'\xff\xff'; 변형['BadPool'] = податоци
        податоци = bytearray(원본); податоци[CODE_VALUE:CODE_VALUE + должина_VALUE] = bytes(должина_VALUE)
        податоци[CODE_VALUE:CODE_VALUE + 3] = b'\xa7\x00\x01'; податоци[CODE_VALUE + должина_VALUE - 1] = 177; 변형['BadJump'] = податоци
        податоци = bytearray(원본); податоци[CODE_VALUE:CODE_VALUE + должина_VALUE] = bytes(должина_VALUE)
        податоци[CODE_VALUE] = 87; податоци[CODE_VALUE + должина_VALUE - 1] = 177; 변형['BadStack'] = податоци
        # Име 검사를 통과시켜 реален_податоци Изврши_наредба 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        внес_VALUE = ['Imported.class=' + str(Именик_VALUE / 'Imported.class'), 'Imported.java=' + str(ИЗВОР)]
        for Име, податоци in 변형.items():
            ПАТЕКА = Именик_VALUE / (Име + '.class'); ПАТЕКА.write_bytes(податоци)
            внес_VALUE.append(Име + '.class=' + str(ПАТЕКА))
        Група_VALUE = Именик_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Позиција / 'Алатки/자바파일묶기.py'), '-o', str(Група_VALUE)] + внес_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(Именик_VALUE / 'user.o'), str(Позиција / '부팅/корисник.s')], cwd=str(Именик_VALUE), check=True)
        јадро_VALUE = Именик_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Позиција / '부팅/Врска_Распоред.ld'), '-o', str(јадро_VALUE),
                        str(Позиција / 'build/boot.o'), str(Позиција / 'build/java.o'), str(Именик_VALUE / 'user.o'), str(Позиција / 'build/apps.o')], check=True)
        машина = виртуелен_машина(јадро_VALUE, Мрежа_VALUE=False)
        try:
            машина.Команда('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            машина.Команда('cat Imported.java', ['int[] values = new int[3]'])
            for Име, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                машина.Команда('java ' + Име, [문구, 'Exit: 1'])
                машина.Команда('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return машина.LOG_ред.decode('utf-8', 'replace')
        finally:
            машина.Затвори()


if __name__ == '__main__':
    разложи_VALUE = argparse.ArgumentParser()
    разложи_VALUE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    Аргументи = разложи_VALUE.parse_args()
    мерка = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if Аргументи.boot == 'both' else (Аргументи.boot,))}
    мерка['import'] = 적재시험()
    (Позиција / 'build/자바시험.json').write_text(json.dumps(мерка, ensure_ascii=False, indent=2) + '\n')
