#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 執行命令, 失敗值/資源值 邊界位置值 測試."""
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
from 測試用戶網路 import 虛擬機器, 位置


def 編輯值(計算機, 名稱, 內容值, 存儲值=True):
    運行 = len(計算機.日誌記錄)
    計算機.串行值.sendall(('edit ' + 名稱 + '\n').encode())
    計算機.等待狀態狀態('...> ', 運行)
    for 行 in 內容值.splitlines():
        assert len(行) <= 128
        運行 = len(計算機.日誌記錄)
        計算機.串行值.sendall((行 + '\n').encode())
        計算機.等待狀態狀態('...> ', 運行)
    運行 = len(計算機.日誌記錄)
    計算機.串行值.sendall(b'.save\n' if 存儲值 else b'.cancel\n')
    結果 = 計算機.等待狀態狀態('jkoros> ', 運行)
    assert ('Saved:' if 存儲值 else 'Cancelled; original preserved') in 結果, 結果


def 檔案地址():
    結果 = subprocess.check_output(['nm', '-n', str(位置 / 'build/kernel.elf')], universal_newlines=True)
    for 行 in 結果.splitlines():
        if 行.endswith(' ram_files'):
            return int(行.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def 客戶機檔案(計算機, 槽值, 大小, 路徑):
    # 測試 VM의 메모리에서 實際資料 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    地址 = 檔案地址() + 槽值 * 16384
    計算機.監視器值.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(地址, 大小, 路徑)).encode())
    結尾 = time.monotonic() + 5
    while time.monotonic() < 結尾:
        if 路徑.exists() and 路徑.stat().st_size == 大小:
            return 路徑.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 測試運行(種類值):
    計算機 = 虛擬機器(位置 / ('build/kernel.elf' if 種類值 == 'elf' else 'build/kernel.iso'), 種類值, 網路值=False)
    結果 = {}
    try:
        計算機.命令('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        計算機.命令('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        計算機.命令('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        計算機.命令('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        計算機.命令('java Missing', ['cannot read class: -2', 'Exit: 1'])
        計算機.命令('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        計算機.命令('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        內容值 = '''public class Calc {
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
        編輯值(計算機, 'Calc.java', 內容值)
        計算機.命令('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        期望狀態 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        輸出 = 計算機.命令('java Calc 6 guest', ['\r\n' + '\r\n'.join(期望狀態) + '\r\n', 'Exit: 0'])
        結果['guest_output'] = 輸出
        條目列表 = 計算機.命令('ls', ['Calc.class'])
        大小 = int(re.search(r'Calc\.class\s+(\d+) bytes', 條目列表).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as 目錄值:
            路徑 = Path(目錄值) / 'Calc.class'
            資料 = 客戶機檔案(計算機, 3, 大小, 路徑)
            實際資料 = subprocess.check_output(['java', '-Xverify:all', '-cp', 目錄值, 'Calc', '6', 'guest'], universal_newlines=True)
            assert 實際資料.splitlines() == 期望狀態, 實際資料
            結果['class_sha256'] = hashlib.sha256(資料).hexdigest()
            結果['openjdk_output'] = 實際資料
        # 실패한 編輯值/컴파일은 기존 class를 보존한다.
        編輯值(計算機, 'Calc.java', 'not Java at all', 存儲值=False)
        計算機.命令('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for 無效結果 in [
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
            編輯值(計算機, 'Calc.java', 無效結果)
            計算機.命令('javac Calc.java', ['javac error:', 'Exit: 1'])
            計算機.命令('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # 迭代值 실행은 使用者 堆值/프레임을 매번 초기화한다.
        for 數 in range(12):
            計算機.命令('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        計算機.命令('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        計算機.命令('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        編輯值(計算機, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        計算機.命令('javac Calc.java', ['Compiled:', 'Exit: 0'])
        計算機.命令('java Calc', ['instruction limit', 'Exit: 1'])
        計算機.命令('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        編輯值(計算機, 'Bad.class', 'garbage')
        計算機.命令('java Bad', ['JVM error:', 'Exit: 1'])
        計算機.命令('rm Bad.class', ['Removed'])
        計算機.命令('java Bad', ['cannot read class: -2'])
        # 編輯值 입력의 넘친 부분을 잘라서 저장하지 않는다.
        運行 = len(計算機.日誌記錄)
        計算機.串行值.sendall(b'edit Hello.java\n')
        計算機.等待狀態狀態('...> ', 運行)
        運行 = len(計算機.日誌記錄)
        計算機.串行值.sendall(b'x' * 129 + b'\n')
        計算機.等待狀態狀態('...> ', 運行)
        計算機.命令('.save', ['Too much input; original preserved'])
        計算機.命令('javac Hello.java', ['Compiled:', 'Exit: 0'])
        編輯值(計算機, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 數 in range(3):
            編輯值(計算機, 'f' + str(數), 'occupied')
        計算機.命令('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        計算機.命令('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in 計算機.日誌記錄.decode('utf-8', 'replace')
        結果['serial'] = 計算機.日誌記錄.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(種類值))
        return 結果
    finally:
        計算機.關閉()


def 主版本程式碼(資料):
    """손상 시험용 main Code의 實際資料 檔案 오프셋/길이만 읽는다."""
    位置值 = 8
    def 讀取無符號短整數():
        nonlocal 位置值
        值 = struct.unpack_from('>H', 資料, 位置值)[0]
        位置值 += 2
        return 值
    def 讀取無符號整數():
        nonlocal 位置值
        值 = struct.unpack_from('>I', 資料, 位置值)[0]
        位置值 += 4
        return 值
    字元值列 = {}
    for 數 in range(1, 讀取無符號短整數()):
        種類值 = 資料[位置值]
        位置值 += 1
        if 種類值 == 1:
            長度 = 讀取無符號短整數()
            字元值列[數] = 資料[位置值:位置值 + 長度]
            位置值 += 長度
        elif 種類值 in (7, 8): 位置值 += 2
        elif 種類值 in (3, 9, 10, 12): 位置值 += 4
        else: raise AssertionError(種類值)
    位置值 += 6
    項目個數 = 讀取無符號短整數()
    位置值 += 項目個數 * 2
    assert 讀取無符號短整數() == 0
    for 數 in range(讀取無符號短整數()):
        讀取無符號短整數()
        名稱 = 讀取無符號短整數()
        讀取無符號短整數()
        for 數 in range(讀取無符號短整數()):
            屬性值 = 讀取無符號短整數()
            大小 = 讀取無符號整數()
            if 字元值列[名稱] == b'main' and 字元值列[屬性值] == b'Code':
                return 位置值 + 8, struct.unpack_from('>I', 資料, 位置值 + 4)[0]
            位置值 += 大小
    raise AssertionError('main Code missing')


def 測試載入中():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 臨時值:
        目錄值 = Path(臨時值)
        (目錄值 / 'build').mkdir()
        原始碼 = 目錄值 / 'Imported.java'
        原始碼.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(原始碼)], check=True)
        原始 = (目錄值 / 'Imported.class').read_bytes()
        程式碼值, 長度 = 主版本程式碼(原始)
        變體值 = {}
        資料 = bytearray(原始); 資料[0] = 0; 變體值['BadMagic'] = 資料
        資料 = bytearray(原始); 資料[7] = 61; 變體值['BadVer'] = 資料
        資料 = bytearray(原始); 資料[8:10] = b'\xff\xff'; 變體值['BadPool'] = 資料
        資料 = bytearray(原始); 資料[程式碼值:程式碼值 + 長度] = bytes(長度)
        資料[程式碼值:程式碼值 + 3] = b'\xa7\x00\x01'; 資料[程式碼值 + 長度 - 1] = 177; 變體值['BadJump'] = 資料
        資料 = bytearray(原始); 資料[程式碼值:程式碼值 + 長度] = bytes(長度)
        資料[程式碼值] = 87; 資料[程式碼值 + 長度 - 1] = 177; 變體值['BadStack'] = 資料
        # 名稱 검사를 통과시켜 實際資料 執行命令 중의 操作數棧 오류까지 검사한다.
        變體值['BadStack'] = 變體值['BadStack'].replace(b'Imported', b'BadStack')
        條目值 = ['Imported.class=' + str(目錄值 / 'Imported.class'), 'Imported.java=' + str(原始碼)]
        for 名稱, 資料 in 變體值.items():
            路徑 = 目錄值 / (名稱 + '.class'); 路徑.write_bytes(資料)
            條目值.append(名稱 + '.class=' + str(路徑))
        組值 = 目錄值 / 'build/java-files.bin'
        subprocess.run([sys.executable, str(位置 / '工具集/Java檔案打包.py'), '-o', str(組值)] + 條目值, check=True)
        subprocess.run(['as', '--32', '-o', str(目錄值 / 'user.o'), str(位置 / '啓動/使用者.s')], cwd=str(目錄值), check=True)
        內核值 = 目錄值 / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(位置 / '啓動/鏈接佈局.ld'), '-o', str(內核值),
                        str(位置 / 'build/boot.o'), str(位置 / 'build/java.o'), str(目錄值 / 'user.o'), str(位置 / 'build/apps.o')], check=True)
        計算機 = 虛擬機器(內核值, 網路值=False)
        try:
            計算機.命令('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            計算機.命令('cat Imported.java', ['int[] values = new int[3]'])
            for 名稱, 短語值 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                計算機.命令('java ' + 名稱, [短語值, 'Exit: 1'])
                計算機.命令('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return 計算機.日誌記錄.decode('utf-8', 'replace')
        finally:
            計算機.關閉()


if __name__ == '__main__':
    解析值 = argparse.ArgumentParser()
    解析值.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    實參 = 解析值.parse_args()
    結果 = {種類值: 測試運行(種類值) for 種類值 in (('elf', 'iso') if 實參.boot == 'both' else (實參.boot,))}
    結果['import'] = 測試載入中()
    (位置 / 'build/Java測試.json').write_text(json.dumps(結果, ensure_ascii=False, indent=2) + '\n')
