#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 命令実行, 失敗値/資源値 境界位置値 試験."""
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
from 利用者通信網試験 import 仮想機械, 位置


def 編集値(機械, 名前, 内容物値, 格納値=True):
    起動処理 = len(機械.履歴記録記録)
    機械.直列値.sendall(('edit ' + 名前 + '\n').encode())
    機械.状況待合('...> ', 起動処理)
    for 行 in 内容物値.splitlines():
        assert len(行) <= 128
        起動処理 = len(機械.履歴記録記録)
        機械.直列値.sendall((行 + '\n').encode())
        機械.状況待合('...> ', 起動処理)
    起動処理 = len(機械.履歴記録記録)
    機械.直列値.sendall(b'.save\n' if 格納値 else b'.cancel\n')
    結果 = 機械.状況待合('jkoros> ', 起動処理)
    assert ('Saved:' if 格納値 else 'Cancelled; original preserved') in 結果, 結果


def ファイル番地():
    結果 = subprocess.check_output(['nm', '-n', str(位置 / 'build/kernel.elf')], universal_newlines=True)
    for 行 in 結果.splitlines():
        if 行.endswith(' ram_files'):
            return int(行.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def ゲストファイル(機械, 槽値, 容量, 経路):
    # 試験 VM의 메모리에서 実際データ 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    番地 = ファイル番地() + 槽値 * 16384
    機械.監視器値.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(番地, 容量, 経路)).encode())
    終端 = time.monotonic() + 5
    while time.monotonic() < 終端:
        if 経路.exists() and 経路.stat().st_size == 容量:
            return 経路.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 起動処理試験(種別値):
    機械 = 仮想機械(位置 / ('build/kernel.elf' if 種別値 == 'elf' else 'build/kernel.iso'), 種別値, 通信網値=False)
    結果 = {}
    try:
        機械.命令('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        機械.命令('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        機械.命令('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        機械.命令('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        機械.命令('java Missing', ['cannot read class: -2', 'Exit: 1'])
        機械.命令('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        機械.命令('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        内容物値 = '''public class Calc {
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
        編集値(機械, 'Calc.java', 内容物値)
        機械.命令('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        期待状態 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        出力 = 機械.命令('java Calc 6 guest', ['\r\n' + '\r\n'.join(期待状態) + '\r\n', 'Exit: 0'])
        結果['guest_output'] = 出力
        入口一覧 = 機械.命令('ls', ['Calc.class'])
        容量 = int(re.search(r'Calc\.class\s+(\d+) bytes', 入口一覧).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as ディレクトリ値:
            経路 = Path(ディレクトリ値) / 'Calc.class'
            データ = ゲストファイル(機械, 3, 容量, 経路)
            実際データ = subprocess.check_output(['java', '-Xverify:all', '-cp', ディレクトリ値, 'Calc', '6', 'guest'], universal_newlines=True)
            assert 実際データ.splitlines() == 期待状態, 実際データ
            結果['class_sha256'] = hashlib.sha256(データ).hexdigest()
            結果['openjdk_output'] = 実際データ
        # 실패한 編集値/컴파일은 기존 class를 보존한다.
        編集値(機械, 'Calc.java', 'not Java at all', 格納値=False)
        機械.命令('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for 無効結果 in [
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
            編集値(機械, 'Calc.java', 無効結果)
            機械.命令('javac Calc.java', ['javac error:', 'Exit: 1'])
            機械.命令('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # 反復回値 실행은 利用者 ヒープ値/프레임을 매번 초기화한다.
        for 数 in range(12):
            機械.命令('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        機械.命令('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        機械.命令('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        編集値(機械, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        機械.命令('javac Calc.java', ['Compiled:', 'Exit: 0'])
        機械.命令('java Calc', ['instruction limit', 'Exit: 1'])
        機械.命令('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        編集値(機械, 'Bad.class', 'garbage')
        機械.命令('java Bad', ['JVM error:', 'Exit: 1'])
        機械.命令('rm Bad.class', ['Removed'])
        機械.命令('java Bad', ['cannot read class: -2'])
        # 編集値 입력의 넘친 부분을 잘라서 저장하지 않는다.
        起動処理 = len(機械.履歴記録記録)
        機械.直列値.sendall(b'edit Hello.java\n')
        機械.状況待合('...> ', 起動処理)
        起動処理 = len(機械.履歴記録記録)
        機械.直列値.sendall(b'x' * 129 + b'\n')
        機械.状況待合('...> ', 起動処理)
        機械.命令('.save', ['Too much input; original preserved'])
        機械.命令('javac Hello.java', ['Compiled:', 'Exit: 0'])
        編集値(機械, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 数 in range(3):
            編集値(機械, 'f' + str(数), 'occupied')
        機械.命令('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        機械.命令('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in 機械.履歴記録記録.decode('utf-8', 'replace')
        結果['serial'] = 機械.履歴記録記録.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(種別値))
        return 結果
    finally:
        機械.閉鎖()


def 主版コード(データ):
    """손상 시험용 main Code의 実際データ ファイル 오프셋/길이만 읽는다."""
    位置値 = 8
    def 符号なし短整数読取():
        nonlocal 位置値
        値 = struct.unpack_from('>H', データ, 位置値)[0]
        位置値 += 2
        return 値
    def 符号なし整数値読取():
        nonlocal 位置値
        値 = struct.unpack_from('>I', データ, 位置値)[0]
        位置値 += 4
        return 値
    文字値一覧 = {}
    for 数 in range(1, 符号なし短整数読取()):
        種別値 = データ[位置値]
        位置値 += 1
        if 種別値 == 1:
            長さ = 符号なし短整数読取()
            文字値一覧[数] = データ[位置値:位置値 + 長さ]
            位置値 += 長さ
        elif 種別値 in (7, 8): 位置値 += 2
        elif 種別値 in (3, 9, 10, 12): 位置値 += 4
        else: raise AssertionError(種別値)
    位置値 += 6
    項目個数 = 符号なし短整数読取()
    位置値 += 項目個数 * 2
    assert 符号なし短整数読取() == 0
    for 数 in range(符号なし短整数読取()):
        符号なし短整数読取()
        名前 = 符号なし短整数読取()
        符号なし短整数読取()
        for 数 in range(符号なし短整数読取()):
            属性値 = 符号なし短整数読取()
            容量 = 符号なし整数値読取()
            if 文字値一覧[名前] == b'main' and 文字値一覧[属性値] == b'Code':
                return 位置値 + 8, struct.unpack_from('>I', データ, 位置値 + 4)[0]
            位置値 += 容量
    raise AssertionError('main Code missing')


def 読込中試験():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 一時値:
        ディレクトリ値 = Path(一時値)
        (ディレクトリ値 / 'build').mkdir()
        ソース = ディレクトリ値 / 'Imported.java'
        ソース.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(ソース)], check=True)
        原本 = (ディレクトリ値 / 'Imported.class').read_bytes()
        コード値, 長さ = 主版コード(原本)
        派生値 = {}
        データ = bytearray(原本); データ[0] = 0; 派生値['BadMagic'] = データ
        データ = bytearray(原本); データ[7] = 61; 派生値['BadVer'] = データ
        データ = bytearray(原本); データ[8:10] = b'\xff\xff'; 派生値['BadPool'] = データ
        データ = bytearray(原本); データ[コード値:コード値 + 長さ] = bytes(長さ)
        データ[コード値:コード値 + 3] = b'\xa7\x00\x01'; データ[コード値 + 長さ - 1] = 177; 派生値['BadJump'] = データ
        データ = bytearray(原本); データ[コード値:コード値 + 長さ] = bytes(長さ)
        データ[コード値] = 87; データ[コード値 + 長さ - 1] = 177; 派生値['BadStack'] = データ
        # 名前 검사를 통과시켜 実際データ 命令実行 중의 被演算子スタック 오류까지 검사한다.
        派生値['BadStack'] = 派生値['BadStack'].replace(b'Imported', b'BadStack')
        入口値 = ['Imported.class=' + str(ディレクトリ値 / 'Imported.class'), 'Imported.java=' + str(ソース)]
        for 名前, データ in 派生値.items():
            経路 = ディレクトリ値 / (名前 + '.class'); 経路.write_bytes(データ)
            入口値.append(名前 + '.class=' + str(経路))
        集合値 = ディレクトリ値 / 'build/java-files.bin'
        subprocess.run([sys.executable, str(位置 / '道具/Javaファイル梱包.py'), '-o', str(集合値)] + 入口値, check=True)
        subprocess.run(['as', '--32', '-o', str(ディレクトリ値 / 'user.o'), str(位置 / '起動/利用者.s')], cwd=str(ディレクトリ値), check=True)
        中核値 = ディレクトリ値 / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(位置 / '起動/連結配置.ld'), '-o', str(中核値),
                        str(位置 / 'build/boot.o'), str(位置 / 'build/java.o'), str(ディレクトリ値 / 'user.o'), str(位置 / 'build/apps.o')], check=True)
        機械 = 仮想機械(中核値, 通信網値=False)
        try:
            機械.命令('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            機械.命令('cat Imported.java', ['int[] values = new int[3]'])
            for 名前, 句値 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                機械.命令('java ' + 名前, [句値, 'Exit: 1'])
                機械.命令('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return 機械.履歴記録記録.decode('utf-8', 'replace')
        finally:
            機械.閉鎖()


if __name__ == '__main__':
    値解析 = argparse.ArgumentParser()
    値解析.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    引数 = 値解析.parse_args()
    結果 = {種別値: 起動処理試験(種別値) for 種別値 in (('elf', 'iso') if 引数.boot == 'both' else (引数.boot,))}
    結果['import'] = 読込中試験()
    (位置 / 'build/Java試験.json').write_text(json.dumps(結果, ensure_ascii=False, indent=2) + '\n')
