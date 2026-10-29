#!/usr/bin/env python3
"""實際資料 raspi4b 啓動, UART 輸入值, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from 執行命令 import 項目根, 命令


def 運行():
    輸出結果 = 項目根 / 'build/verification'
    輸出結果.mkdir(parents=True, exist_ok=True)
    執行記錄 = bytearray()
    有效性驗證報告 = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 工作中路徑:
        QMP路徑 = Path(工作中路徑) / 'qmp.sock'
        命令參數列 = 命令() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(QMP路徑),
                           '-vnc', 'unix:{}'.format(Path(工作中路徑) / 'vnc.sock')]
        有效性驗證報告['command'] = 命令參數列
        程序 = subprocess.Popen(命令參數列, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        就緒選擇器 = selectors.DefaultSelector()
        就緒選擇器.register(程序.stdout, selectors.EVENT_READ)
        def 接收直到(標記, 偏移值=0, 執行狀態超時=45):
            截止時間時間 = time.monotonic() + 執行狀態超時
            while 標記 not in 執行記錄[偏移值:]:
                if time.monotonic() > 截止時間時間:
                    raise AssertionError('UART timeout: ' + repr(標記))
                for 已按下值, _ in 就緒選擇器.select(0.2):
                    資料塊 = 已按下值.fileobj.read(4096)
                    if 資料塊:
                        執行記錄.extend(資料塊)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 執行記錄):
                    raise AssertionError('kernel failure')
                if 程序.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(程序.returncode))
        try:
            接收直到(b'jkoros-native> ')
            標記列 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 標記 in 標記列:
                assert 標記 in 執行記錄, 標記
            # GTK 없는 當前項目 호스트에서도 VNC로 實際資料 GUI를 볼 數 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 屏幕客戶端:
                屏幕客戶端.settimeout(5); 屏幕客戶端.connect(str(Path(工作中路徑) / 'vnc.sock'))
                def 精確值(大小):
                    結果 = b''
                    while len(結果) < 大小:
                        片段值 = 屏幕客戶端.recv(大小 - len(結果))
                        if not 片段值: raise AssertionError('VNC disconnected')
                        結果 += 片段值
                    return 結果
                assert 精確值(12) == b'RFB 003.008\n'
                屏幕客戶端.sendall(b'RFB 003.008\n')
                assert 1 in 精確值(精確值(1)[0]); 屏幕客戶端.sendall(b'\x01')
                assert 精確值(4) == b'\x00\x00\x00\x00'; 屏幕客戶端.sendall(b'\x01')
                服務器值 = 精確值(24)
                assert int.from_bytes(服務器值[:2], 'big') == 640 and int.from_bytes(服務器值[2:4], 'big') == 480
                精確值(int.from_bytes(服務器值[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for 命令位元組, 標記 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '測試.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                偏移值 = len(執行記錄)
                程序.stdin.write(命令位元組 + b'\n')
                程序.stdin.flush()
                接收直到(b'jkoros-native> ', 偏移值)
                assert 標記 in 執行記錄[偏移值:], 標記
            def 命令殼(行, 預期):
                偏移值 = len(執行記錄)
                程序.stdin.write(行.encode('utf-8') + b'\n'); 程序.stdin.flush()
                接收直到(b'jkoros-native> ', 偏移值)
                響應 = bytes(執行記錄[偏移值:])
                for 文本 in 預期:
                    assert 文本.encode('utf-8') in 響應, (行, 文本, 響應)
                return 響應
            def 進入(行, 提示):
                偏移值 = len(執行記錄)
                程序.stdin.write(行.encode('utf-8') + b'\n'); 程序.stdin.flush()
                接收直到(提示, 偏移值)
                return bytes(執行記錄[偏移值:])
            def 編輯值(名稱, 內容值, 取消操作=False):
                進入('edit ' + 名稱, b'edit> ')
                for 行 in 內容值.splitlines(): 進入(行, b'edit> ')
                if 取消操作:
                    偏移值 = len(執行記錄)
                    程序.stdin.write(b'\x03'); 程序.stdin.flush()
                    接收直到(b'jkoros-native> ', 偏移值)
                    assert b'EDIT CANCELLED' in 執行記錄[偏移值:]
                else:
                    assert b'SAVED' in 進入('.', b'jkoros-native> ')
            def 上傳檔案集(名稱, 資料):
                assert len(資料) <= 16384
                進入('load ' + 名稱, b'hex> ')
                for 序數索引 in range(0, len(資料), 64): 進入(資料[序數索引:序數索引+64].hex(), b'hex> ')
                assert b'LOADED' in 進入('.', b'jkoros-native> ')
            def 下載(名稱):
                響應 = 命令殼('hex ' + 名稱, ['HEX BEGIN', 'HEX END'])
                是否相等 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 響應, re.S)
                資料 = bytes.fromhex(''.join(是否相等.group(2).decode('ascii').split()))
                assert len(資料) == int(是否相等.group(1)); return 資料
            命令殼('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            命令殼('java -version', ['not OpenJDK', 'exit 0'])
            命令殼('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            命令殼('java Hello "한글 實參 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 實參 😀', 'exit 0'])
            命令殼('python --version', ['MicroPython 1.24.1', 'exit 0'])
            命令殼('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 檔案', 'exit 0'])
            命令殼('cat python.txt', ['한글 檔案'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            Java類別 = 輸出結果 / 'Hello.class'; Java類別.write_bytes(下載('Hello.class'))
            預期 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(輸出結果), 'Hello', '한글 實參 😀']).decode('utf-8')
            assert 預期.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 實參 😀'], 預期
            編輯值('問候例.java', 'public class 問候例 { public static void main(String[] args) { int 值 = 7; System.out.println("한글=" + 值); } }')
            命令殼('javac 問候例.java', ['Compiled: 問候例.class', 'exit 0'])
            命令殼('java 問候例', ['한글=7', 'exit 0'])
            (輸出結果 / '問候例.class').write_bytes(下載('問候例.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(輸出結果), '問候例']).decode().strip() == '한글=7'
            編輯值('Hello.java', 'broken', 取消操作=True)
            命令殼('javac Hello.java', ['Compiled:', 'exit 0'])
            編輯值('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            命令殼('javac Broken.java', ['javac error:', 'exit 1'])
            上傳檔案集('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            命令殼('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            命令殼('rm Broken.java', [])
            已導入 = 輸出結果 / 'Imported.java'
            已導入.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(已導入)])
            上傳檔案集('Imported.class', (輸出結果 / 'Imported.class').read_bytes())
            命令殼('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            命令殼('rm Imported.class', [])
            編輯值('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            命令殼('javac Loop.java', ['Compiled:', 'exit 0'])
            響應 = 命令殼('java Loop', ['exit '])
            assert b'instruction limit' in 響應 or b'exit -1004' in 響應
            命令殼('rm Loop.java', []); 命令殼('rm Loop.class', [])
            # CPython-independent Python runtime: Unicode, big integers, closures/classes,
            # GC roots, file imports, exceptions and UDP queues are exercised in the guest.
            Python檢查項 = """import gc, jkoros
assert len('한글😀') == 3
assert 2**100 == 1267650600228229401496703205376
class Counter:
    def __init__(self, n): self.n = n
    def value(self): return self.n + 1
keep = Counter(41)
for i in range(300):
    garbage = [str(j) for j in range(80)]
    gc.collect()
assert keep.value() == 42
try:
    1 // 0
except ZeroDivisionError:
    print('PY EXCEPTION OK')
a = jkoros.udp_open(9401)
b = jkoros.udp_open(9402)
assert jkoros.udp_send(a, 9402, b'udp-python') == 10
assert jkoros.udp_recv(b) == (b'udp-python', 9401)
try:
    jkoros.udp_recv(b)
except OSError as e:
    assert e.args[0] == 11
jkoros.udp_close(a)
jkoros.udp_close(b)
print('PY GC UNICODE MPZ CLASS UDP OK')
"""
            編輯值('checks.py', Python檢查項)
            命令殼('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            命令殼('rm checks.py', [])
            編輯值('helper.py', 'value = 321')
            命令殼("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            命令殼('rm helper.py', [])
            命令殼("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            命令殼("python -c 'while True: pass'", ['exit -1004'])
            for 序數索引 in range(4):
                命令殼('python hello.py', ['한글 檔案', 'exit 0'])
                命令殼('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            上傳檔案集('app.elf', (項目根 / 'build/user/demo.elf').read_bytes())
            assert 下載('app.elf') == (項目根 / 'build/user/demo.elf').read_bytes()
            命令殼('run app.elf', ['EL0 C++', 'exit 0'])
            上傳檔案集('app.elf', b'not an ELF')
            命令殼('run app.elf', ['exit -8'])
            命令殼('rm app.elf', [])
            命令殼('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            繪圖路徑 = 輸出結果 / 'java-framebuffer'; 繪圖路徑.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(項目根 / 'dist/jkoros-native-korean.jar'), '-d', str(繪圖路徑), str(項目根 / '測試/Java/測試屏幕.java')])
            上傳檔案集('測試屏幕.class', (繪圖路徑 / '測試屏幕.class').read_bytes())
            命令殼('java 測試屏幕', ['屏幕 裁剪 拒絕值', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            命令殼('rm 測試屏幕.class', [])
            with socket.socket(socket.AF_UNIX) as 客戶端:
                客戶端.settimeout(10)
                客戶端.connect(str(QMP路徑))
                with 客戶端.makefile('rwb') as 流值:
                    問候例 = json.loads(流值.readline())
                    def 測試替身控制連接狀態(執行任務, 已轉發實際參數=None):
                        網路消息 = {'execute': 執行任務}
                        if 已轉發實際參數: 網路消息['arguments'] = 已轉發實際參數
                        流值.write((json.dumps(網路消息) + '\n').encode())
                        流值.flush()
                        while True:
                            回覆 = json.loads(流值.readline())
                            if 'error' in 回覆: raise AssertionError(回覆)
                            if 'return' in 回覆: return 回覆['return']
                    測試替身控制連接狀態('qmp_capabilities')
                    屏幕剪輯 = 輸出結果 / 'framebuffer.ppm'
                    測試替身控制連接狀態('screendump', {'filename': str(屏幕剪輯), 'format': 'ppm'})
                    def 範例條目列(路徑, 點列):
                        with 路徑.open('rb') as 像素檔案:
                            assert 像素檔案.readline().strip() == b'P6'
                            assert 像素檔案.readline().strip() == b'640 480'
                            assert 像素檔案.readline().strip() == b'255'
                            像素資料 = 像素檔案.read()
                        assert len(像素資料) == 640 * 480 * 3
                        return [list(像素資料[(Y_按鈕座標 * 640 + 橫座標座標) * 3:(Y_按鈕座標 * 640 + 橫座標座標) * 3 + 3]) for 橫座標座標, Y_按鈕座標 in 點列]
                    assert 範例條目列(屏幕剪輯, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 範例條目列(屏幕剪輯, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def 發送(已按下值, 標記):
                        偏移值 = len(執行記錄)
                        程序.stdin.write(已按下值); 程序.stdin.flush()
                        接收直到(標記, 偏移值)
                    發送(b'gui\n', b'GUI READY:')
                    首位GUI = 輸出結果 / 'gui-programs.ppm'
                    測試替身控制連接狀態('screendump', {'filename': str(首位GUI), 'format': 'ppm'})
                    測試替身控制連接狀態('screendump', {'filename': str(輸出結果 / 'gui-programs.png'), 'format': 'png'})
                    assert 範例條目列(首位GUI, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    發送(b'\r', b'GUI ACTION 0 RESULT 0')
                    發送(b'\t', b'GUI FOCUS 1')
                    發送(b'\r', b'GUI ACTION 1 RESULT 0')
                    第二GUI = 輸出結果 / 'gui-network.ppm'
                    測試替身控制連接狀態('screendump', {'filename': str(第二GUI), 'format': 'ppm'})
                    測試替身控制連接狀態('screendump', {'filename': str(輸出結果 / 'gui-network.png'), 'format': 'png'})
                    assert 範例條目列(第二GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    發送(b'\t', b'GUI FOCUS 2')
                    發送(b'\r', b'GUI ACTION 2 RESULT 0')
                    發送(b'\t', b'GUI FOCUS 3')
                    發送(b'\r', b'GUI ACTION 3 RESULT 0')
                    測試替身控制連接狀態('screendump', {'filename': str(輸出結果 / 'gui-python.png'), 'format': 'png'})
                    發送(b'q', b'jkoros-native> ')
                    有效性驗證報告['qemu'] = 問候例['QMP']['version']
                    測試替身控制連接狀態('quit')
            程序.wait(timeout=10)
            # framebuffer 응답뿐 아니라 實際資料 scanout 픽셀도 확인한다.
            with 屏幕剪輯.open('rb') as 檔案條目:
                assert 檔案條目.readline().strip() == b'P6'
                尺寸值 = 檔案條目.readline().strip()
                assert 尺寸值 == b'640 480', 尺寸值
                assert 檔案條目.readline().strip() == b'255'
                像素列列表 = 檔案條目.read()
            assert len(像素列列表) == 640 * 480 * 3
            def 像素(橫座標座標, Y_按鈕座標): return list(像素列列表[(Y_按鈕座標 * 640 + 橫座標座標) * 3:(Y_按鈕座標 * 640 + 橫座標座標) * 3 + 3])
            範例條目列 = {'background': 像素(5, 5), 'panel': 像素(45, 85), 'tile': 像素(65, 115)}
            assert 範例條目列 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 範例條目列
            有效性驗證報告.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
                'UTF-8 Korean/Japanese/Arabic/emoji UART', 'C++ direct RAM file API (21 runs)',
                'cooperative independent stacks (4 runs)', 'line shell/UTF-8/quotes/edit/cancel/hex upload/download',
                'guest Java compiler/JVM and OpenJDK two-way class verification',
                'Korean Java framebuffer library bounds and actual scanout pixels',
                'Korean Java identifiers, UTF-8 validation, malformed source and bounded execution',
                'MicroPython GC/classes/Unicode/MPZ/imports/exceptions/files/UDP and timeout recovery',
                'load and run custom ELF with malformed image rejection', 'RGB32 framebuffer pixels',
                'ELF64 rejection fixtures: 22', 'EL0 C++ constructors/RAII/FP/files/heap/pointer validation',
                'kernel/text/MMIO/guard/NX/privileged instruction protection', 'timer terminates EL0 infinite loop',
                'repeated EL0 program exit closes leaked descriptors', 'UDP loopback payload/peer/reply/truncation/queue/zero datagram/errors/cleanup',
                'GUI focus/keyboard activation/C++/UDP/Java/MicroPython launch/exit and framebuffer pixels'],
                vnc='RFB 3.8 / 640x480 / UART input',
                framebuffer=範例條目列, kernel_sha256=hashlib.sha256((項目根 / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if 程序.poll() is None:
                程序.terminate()
                try: 程序.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    程序.kill(); 程序.wait(timeout=5)
            就緒選擇器.close()
            程序.stdin.close(); 程序.stdout.close()
            (輸出結果 / 'serial.log').write_bytes(執行記錄)
            (輸出結果 / 'report.json').write_text(json.dumps(有效性驗證報告, indent=2) + '\n')


if __name__ == '__main__':
    運行()
