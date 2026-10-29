#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 executeCommand, failureValue/resourceValue boundaryValue tests."""
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
from testUserNetwork import VirtualMachine, position


def editValue(machine, name, contentValue, storeValue=True):
    run = len(machine.logRecord)
    machine.serialValue.sendall(('edit ' + name + '\n').encode())
    machine.waitState('...> ', run)
    for line in contentValue.splitlines():
        assert len(line) <= 128
        run = len(machine.logRecord)
        machine.serialValue.sendall((line + '\n').encode())
        machine.waitState('...> ', run)
    run = len(machine.logRecord)
    machine.serialValue.sendall(b'.save\n' if storeValue else b'.cancel\n')
    result = machine.waitState('jkoros> ', run)
    assert ('Saved:' if storeValue else 'Cancelled; original preserved') in result, result


def fileAddress():
    result = subprocess.check_output(['nm', '-n', str(position / 'build/kernel.elf')], universal_newlines=True)
    for line in result.splitlines():
        if line.endswith(' ram_files'):
            return int(line.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def guestFile(machine, slotValue, size, path):
    # tests VM의 메모리에서 actualData 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    address = fileAddress() + slotValue * 16384
    machine.monitorValue.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(address, size, path)).encode())
    ending = time.monotonic() + 5
    while time.monotonic() < ending:
        if path.exists() and path.stat().st_size == size:
            return path.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def testRun(kindValue):
    machine = VirtualMachine(position / ('build/kernel.elf' if kindValue == 'elf' else 'build/kernel.iso'), kindValue, networkValue=False)
    result = {}
    try:
        machine.command('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        machine.command('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        machine.command('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        machine.command('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        machine.command('java Missing', ['cannot read class: -2', 'Exit: 1'])
        machine.command('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        machine.command('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        contentValue = '''public class Calc {
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
        editValue(machine, 'Calc.java', contentValue)
        machine.command('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        expectation = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        Output = machine.command('java Calc 6 guest', ['\r\n' + '\r\n'.join(expectation) + '\r\n', 'Exit: 0'])
        result['guest_output'] = Output
        entryList = machine.command('ls', ['Calc.class'])
        size = int(re.search(r'Calc\.class\s+(\d+) bytes', entryList).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as directoryValue:
            path = Path(directoryValue) / 'Calc.class'
            data = guestFile(machine, 3, size, path)
            actualData = subprocess.check_output(['java', '-Xverify:all', '-cp', directoryValue, 'Calc', '6', 'guest'], universal_newlines=True)
            assert actualData.splitlines() == expectation, actualData
            result['class_sha256'] = hashlib.sha256(data).hexdigest()
            result['openjdk_output'] = actualData
        # 실패한 editValue/컴파일은 기존 class를 보존한다.
        editValue(machine, 'Calc.java', 'not Java at all', storeValue=False)
        machine.command('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for invalidResult in [
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
            editValue(machine, 'Calc.java', invalidResult)
            machine.command('javac Calc.java', ['javac error:', 'Exit: 1'])
            machine.command('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # iterationValue 실행은 User heapValue/프레임을 매번 초기화한다.
        for number in range(12):
            machine.command('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        machine.command('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        machine.command('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        editValue(machine, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        machine.command('javac Calc.java', ['Compiled:', 'Exit: 0'])
        machine.command('java Calc', ['instruction limit', 'Exit: 1'])
        machine.command('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        editValue(machine, 'Bad.class', 'garbage')
        machine.command('java Bad', ['JVM error:', 'Exit: 1'])
        machine.command('rm Bad.class', ['Removed'])
        machine.command('java Bad', ['cannot read class: -2'])
        # editValue 입력의 넘친 부분을 잘라서 저장하지 않는다.
        run = len(machine.logRecord)
        machine.serialValue.sendall(b'edit Hello.java\n')
        machine.waitState('...> ', run)
        run = len(machine.logRecord)
        machine.serialValue.sendall(b'x' * 129 + b'\n')
        machine.waitState('...> ', run)
        machine.command('.save', ['Too much input; original preserved'])
        machine.command('javac Hello.java', ['Compiled:', 'Exit: 0'])
        editValue(machine, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for number in range(3):
            editValue(machine, 'f' + str(number), 'occupied')
        machine.command('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        machine.command('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in machine.logRecord.decode('utf-8', 'replace')
        result['serial'] = machine.logRecord.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(kindValue))
        return result
    finally:
        machine.close()


def majorCode(data):
    """손상 시험용 main Code의 actualData file 오프셋/길이만 읽는다."""
    positionValue = 8
    def readUnsignedShort():
        nonlocal positionValue
        value = struct.unpack_from('>H', data, positionValue)[0]
        positionValue += 2
        return value
    def readUnsignedInteger():
        nonlocal positionValue
        value = struct.unpack_from('>I', data, positionValue)[0]
        positionValue += 4
        return value
    characterValues = {}
    for number in range(1, readUnsignedShort()):
        kindValue = data[positionValue]
        positionValue += 1
        if kindValue == 1:
            lengthValue = readUnsignedShort()
            characterValues[number] = data[positionValue:positionValue + lengthValue]
            positionValue += lengthValue
        elif kindValue in (7, 8): positionValue += 2
        elif kindValue in (3, 9, 10, 12): positionValue += 4
        else: raise AssertionError(kindValue)
    positionValue += 6
    itemCount = readUnsignedShort()
    positionValue += itemCount * 2
    assert readUnsignedShort() == 0
    for number in range(readUnsignedShort()):
        readUnsignedShort()
        name = readUnsignedShort()
        readUnsignedShort()
        for number in range(readUnsignedShort()):
            attributeValue = readUnsignedShort()
            size = readUnsignedInteger()
            if characterValues[name] == b'main' and characterValues[attributeValue] == b'Code':
                return positionValue + 8, struct.unpack_from('>I', data, positionValue + 4)[0]
            positionValue += size
    raise AssertionError('main Code missing')


def testLoading():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as temporaryValue:
        directoryValue = Path(temporaryValue)
        (directoryValue / 'build').mkdir()
        source = directoryValue / 'Imported.java'
        source.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(source)], check=True)
        original = (directoryValue / 'Imported.class').read_bytes()
        codeValue, lengthValue = majorCode(original)
        variantValue = {}
        data = bytearray(original); data[0] = 0; variantValue['BadMagic'] = data
        data = bytearray(original); data[7] = 61; variantValue['BadVer'] = data
        data = bytearray(original); data[8:10] = b'\xff\xff'; variantValue['BadPool'] = data
        data = bytearray(original); data[codeValue:codeValue + lengthValue] = bytes(lengthValue)
        data[codeValue:codeValue + 3] = b'\xa7\x00\x01'; data[codeValue + lengthValue - 1] = 177; variantValue['BadJump'] = data
        data = bytearray(original); data[codeValue:codeValue + lengthValue] = bytes(lengthValue)
        data[codeValue] = 87; data[codeValue + lengthValue - 1] = 177; variantValue['BadStack'] = data
        # name 검사를 통과시켜 actualData executeCommand 중의 operandStack 오류까지 검사한다.
        variantValue['BadStack'] = variantValue['BadStack'].replace(b'Imported', b'BadStack')
        entryValue = ['Imported.class=' + str(directoryValue / 'Imported.class'), 'Imported.java=' + str(source)]
        for name, data in variantValue.items():
            path = directoryValue / (name + '.class'); path.write_bytes(data)
            entryValue.append(name + '.class=' + str(path))
        groupValue = directoryValue / 'build/java-files.bin'
        subprocess.run([sys.executable, str(position / 'tools/bundleJavaFiles.py'), '-o', str(groupValue)] + entryValue, check=True)
        subprocess.run(['as', '--32', '-o', str(directoryValue / 'user.o'), str(position / 'machine_boot/User.s')], cwd=str(directoryValue), check=True)
        kernelValue = directoryValue / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(position / 'machine_boot/link_layout.ld'), '-o', str(kernelValue),
                        str(position / 'build/boot.o'), str(position / 'build/java.o'), str(directoryValue / 'user.o'), str(position / 'build/apps.o')], check=True)
        machine = VirtualMachine(kernelValue, networkValue=False)
        try:
            machine.command('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            machine.command('cat Imported.java', ['int[] values = new int[3]'])
            for name, phraseValue in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                machine.command('java ' + name, [phraseValue, 'Exit: 1'])
                machine.command('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return machine.logRecord.decode('utf-8', 'replace')
        finally:
            machine.close()


if __name__ == '__main__':
    parseValue = argparse.ArgumentParser()
    parseValue.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    arguments = parseValue.parse_args()
    result = {kindValue: testRun(kindValue) for kindValue in (('elf', 'iso') if arguments.boot == 'both' else (arguments.boot,))}
    result['import'] = testLoading()
    (position / 'build/testJava.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
