#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 执行命令, 失败值/资源值 边界位置值 测试."""
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
from 测试用户网络 import 虚拟机, 位置


def 编辑值(计算机, 名称, 内容值, 存储值=True):
    运行 = len(计算机.日志记录)
    计算机.串行值.sendall(('edit ' + 名称 + '\n').encode())
    计算机.等待状态状态('...> ', 运行)
    for 行 in 内容值.splitlines():
        assert len(行) <= 128
        运行 = len(计算机.日志记录)
        计算机.串行值.sendall((行 + '\n').encode())
        计算机.等待状态状态('...> ', 运行)
    运行 = len(计算机.日志记录)
    计算机.串行值.sendall(b'.save\n' if 存储值 else b'.cancel\n')
    结果 = 计算机.等待状态状态('jkoros> ', 运行)
    assert ('Saved:' if 存储值 else 'Cancelled; original preserved') in 结果, 结果


def 文件地址():
    结果 = subprocess.check_output(['nm', '-n', str(位置 / 'build/kernel.elf')], universal_newlines=True)
    for 行 in 结果.splitlines():
        if 行.endswith(' ram_files'):
            return int(行.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def 客户机文件(计算机, 槽值, 大小, 路径):
    # 测试 VM의 메모리에서 实际数据 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    地址 = 文件地址() + 槽值 * 16384
    计算机.监视器值.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(地址, 大小, 路径)).encode())
    结尾 = time.monotonic() + 5
    while time.monotonic() < 结尾:
        if 路径.exists() and 路径.stat().st_size == 大小:
            return 路径.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 测试运行(种类值):
    计算机 = 虚拟机(位置 / ('build/kernel.elf' if 种类值 == 'elf' else 'build/kernel.iso'), 种类值, 网络值=False)
    结果 = {}
    try:
        计算机.命令('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        计算机.命令('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        计算机.命令('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        计算机.命令('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        计算机.命令('java Missing', ['cannot read class: -2', 'Exit: 1'])
        计算机.命令('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        计算机.命令('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        内容值 = '''public class Calc {
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
        编辑值(计算机, 'Calc.java', 内容值)
        计算机.命令('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        期望状态 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        输出 = 计算机.命令('java Calc 6 guest', ['\r\n' + '\r\n'.join(期望状态) + '\r\n', 'Exit: 0'])
        结果['guest_output'] = 输出
        条目列表 = 计算机.命令('ls', ['Calc.class'])
        大小 = int(re.search(r'Calc\.class\s+(\d+) bytes', 条目列表).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as 目录值:
            路径 = Path(目录值) / 'Calc.class'
            数据 = 客户机文件(计算机, 3, 大小, 路径)
            实际数据 = subprocess.check_output(['java', '-Xverify:all', '-cp', 目录值, 'Calc', '6', 'guest'], universal_newlines=True)
            assert 实际数据.splitlines() == 期望状态, 实际数据
            结果['class_sha256'] = hashlib.sha256(数据).hexdigest()
            结果['openjdk_output'] = 实际数据
        # 실패한 编辑值/컴파일은 기존 class를 보존한다.
        编辑值(计算机, 'Calc.java', 'not Java at all', 存储值=False)
        计算机.命令('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for 无效结果 in [
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
            编辑值(计算机, 'Calc.java', 无效结果)
            计算机.命令('javac Calc.java', ['javac error:', 'Exit: 1'])
            计算机.命令('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # 迭代值 실행은 用户 堆值/프레임을 매번 초기화한다.
        for 数 in range(12):
            计算机.命令('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        计算机.命令('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        计算机.命令('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        编辑值(计算机, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        计算机.命令('javac Calc.java', ['Compiled:', 'Exit: 0'])
        计算机.命令('java Calc', ['instruction limit', 'Exit: 1'])
        计算机.命令('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        编辑值(计算机, 'Bad.class', 'garbage')
        计算机.命令('java Bad', ['JVM error:', 'Exit: 1'])
        计算机.命令('rm Bad.class', ['Removed'])
        计算机.命令('java Bad', ['cannot read class: -2'])
        # 编辑值 입력의 넘친 부분을 잘라서 저장하지 않는다.
        运行 = len(计算机.日志记录)
        计算机.串行值.sendall(b'edit Hello.java\n')
        计算机.等待状态状态('...> ', 运行)
        运行 = len(计算机.日志记录)
        计算机.串行值.sendall(b'x' * 129 + b'\n')
        计算机.等待状态状态('...> ', 运行)
        计算机.命令('.save', ['Too much input; original preserved'])
        计算机.命令('javac Hello.java', ['Compiled:', 'Exit: 0'])
        编辑值(计算机, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 数 in range(3):
            编辑值(计算机, 'f' + str(数), 'occupied')
        计算机.命令('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        计算机.命令('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in 计算机.日志记录.decode('utf-8', 'replace')
        结果['serial'] = 计算机.日志记录.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(种类值))
        return 结果
    finally:
        计算机.关闭()


def 主版本代码(数据):
    """손상 시험용 main Code의 实际数据 文件 오프셋/길이만 읽는다."""
    位置值 = 8
    def 读取无符号短整数():
        nonlocal 位置值
        值 = struct.unpack_from('>H', 数据, 位置值)[0]
        位置值 += 2
        return 值
    def 读取无符号整数():
        nonlocal 位置值
        值 = struct.unpack_from('>I', 数据, 位置值)[0]
        位置值 += 4
        return 值
    字符值列 = {}
    for 数 in range(1, 读取无符号短整数()):
        种类值 = 数据[位置值]
        位置值 += 1
        if 种类值 == 1:
            长度 = 读取无符号短整数()
            字符值列[数] = 数据[位置值:位置值 + 长度]
            位置值 += 长度
        elif 种类值 in (7, 8): 位置值 += 2
        elif 种类值 in (3, 9, 10, 12): 位置值 += 4
        else: raise AssertionError(种类值)
    位置值 += 6
    项目个数 = 读取无符号短整数()
    位置值 += 项目个数 * 2
    assert 读取无符号短整数() == 0
    for 数 in range(读取无符号短整数()):
        读取无符号短整数()
        名称 = 读取无符号短整数()
        读取无符号短整数()
        for 数 in range(读取无符号短整数()):
            属性值 = 读取无符号短整数()
            大小 = 读取无符号整数()
            if 字符值列[名称] == b'main' and 字符值列[属性值] == b'Code':
                return 位置值 + 8, struct.unpack_from('>I', 数据, 位置值 + 4)[0]
            位置值 += 大小
    raise AssertionError('main Code missing')


def 测试载入中():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 临时值:
        目录值 = Path(临时值)
        (目录值 / 'build').mkdir()
        源代码 = 目录值 / 'Imported.java'
        源代码.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(源代码)], check=True)
        原始 = (目录值 / 'Imported.class').read_bytes()
        代码值, 长度 = 主版本代码(原始)
        变体值 = {}
        数据 = bytearray(原始); 数据[0] = 0; 变体值['BadMagic'] = 数据
        数据 = bytearray(原始); 数据[7] = 61; 变体值['BadVer'] = 数据
        数据 = bytearray(原始); 数据[8:10] = b'\xff\xff'; 变体值['BadPool'] = 数据
        数据 = bytearray(原始); 数据[代码值:代码值 + 长度] = bytes(长度)
        数据[代码值:代码值 + 3] = b'\xa7\x00\x01'; 数据[代码值 + 长度 - 1] = 177; 变体值['BadJump'] = 数据
        数据 = bytearray(原始); 数据[代码值:代码值 + 长度] = bytes(长度)
        数据[代码值] = 87; 数据[代码值 + 长度 - 1] = 177; 变体值['BadStack'] = 数据
        # 名称 검사를 통과시켜 实际数据 执行命令 중의 操作数栈 오류까지 검사한다.
        变体值['BadStack'] = 变体值['BadStack'].replace(b'Imported', b'BadStack')
        条目值 = ['Imported.class=' + str(目录值 / 'Imported.class'), 'Imported.java=' + str(源代码)]
        for 名称, 数据 in 变体值.items():
            路径 = 目录值 / (名称 + '.class'); 路径.write_bytes(数据)
            条目值.append(名称 + '.class=' + str(路径))
        组值 = 目录值 / 'build/java-files.bin'
        subprocess.run([sys.executable, str(位置 / '工具集/Java文件打包.py'), '-o', str(组值)] + 条目值, check=True)
        subprocess.run(['as', '--32', '-o', str(目录值 / 'user.o'), str(位置 / '启动/用户.s')], cwd=str(目录值), check=True)
        内核值 = 目录值 / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(位置 / '启动/链接布局.ld'), '-o', str(内核值),
                        str(位置 / 'build/boot.o'), str(位置 / 'build/java.o'), str(目录值 / 'user.o'), str(位置 / 'build/apps.o')], check=True)
        计算机 = 虚拟机(内核值, 网络值=False)
        try:
            计算机.命令('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            计算机.命令('cat Imported.java', ['int[] values = new int[3]'])
            for 名称, 短语值 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                计算机.命令('java ' + 名称, [短语值, 'Exit: 1'])
                计算机.命令('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return 计算机.日志记录.decode('utf-8', 'replace')
        finally:
            计算机.关闭()


if __name__ == '__main__':
    解析值 = argparse.ArgumentParser()
    解析值.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    实参 = 解析值.parse_args()
    结果 = {种类值: 测试运行(种类值) for 种类值 in (('elf', 'iso') if 实参.boot == 'both' else (实参.boot,))}
    结果['import'] = 测试载入中()
    (位置 / 'build/Java测试.json').write_text(json.dumps(结果, ensure_ascii=False, indent=2) + '\n')
