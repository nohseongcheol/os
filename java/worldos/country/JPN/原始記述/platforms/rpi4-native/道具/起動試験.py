#!/usr/bin/env python3
"""実際データ raspi4b 起動, UART 入力値, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from 命令実行 import 計画根, 命令


def 起動処理():
    出力結果 = 計画根 / 'build/verification'
    出力結果.mkdir(parents=True, exist_ok=True)
    実行記録 = bytearray()
    妥当性報告 = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 作業中経路:
        QMP経路 = Path(作業中経路) / 'qmp.sock'
        命令引数列 = 命令() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(QMP経路),
                           '-vnc', 'unix:{}'.format(Path(作業中経路) / 'vnc.sock')]
        妥当性報告['command'] = 命令引数列
        プロセス = subprocess.Popen(命令引数列, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        準備監視器 = selectors.DefaultSelector()
        準備監視器.register(プロセス.stdout, selectors.EVENT_READ)
        def 到達待ち受取(標識, 変位量値=0, 実行状態待機期限=45):
            期限時間 = time.monotonic() + 実行状態待機期限
            while 標識 not in 実行記録[変位量値:]:
                if time.monotonic() > 期限時間:
                    raise AssertionError('UART timeout: ' + repr(標識))
                for 押下済み値, _ in 準備監視器.select(0.2):
                    データブロック = 押下済み値.fileobj.read(4096)
                    if データブロック:
                        実行記録.extend(データブロック)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 実行記録):
                    raise AssertionError('kernel failure')
                if プロセス.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(プロセス.returncode))
        try:
            到達待ち受取(b'jkoros-native> ')
            標識一覧 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 標識 in 標識一覧:
                assert 標識 in 実行記録, 標識
            # GTK 없는 現在項目 호스트에서도 VNC로 実際データ GUI를 볼 数 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 画面接続元:
                画面接続元.settimeout(5); 画面接続元.connect(str(Path(作業中経路) / 'vnc.sock'))
                def 厳密値(容量):
                    結果 = b''
                    while len(結果) < 容量:
                        断片値 = 画面接続元.recv(容量 - len(結果))
                        if not 断片値: raise AssertionError('VNC disconnected')
                        結果 += 断片値
                    return 結果
                assert 厳密値(12) == b'RFB 003.008\n'
                画面接続元.sendall(b'RFB 003.008\n')
                assert 1 in 厳密値(厳密値(1)[0]); 画面接続元.sendall(b'\x01')
                assert 厳密値(4) == b'\x00\x00\x00\x00'; 画面接続元.sendall(b'\x01')
                サーバー値 = 厳密値(24)
                assert int.from_bytes(サーバー値[:2], 'big') == 640 and int.from_bytes(サーバー値[2:4], 'big') == 480
                厳密値(int.from_bytes(サーバー値[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for 命令バイト, 標識 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '試験.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                変位量値 = len(実行記録)
                プロセス.stdin.write(命令バイト + b'\n')
                プロセス.stdin.flush()
                到達待ち受取(b'jkoros-native> ', 変位量値)
                assert 標識 in 実行記録[変位量値:], 標識
            def シェル(行, 期待):
                変位量値 = len(実行記録)
                プロセス.stdin.write(行.encode('utf-8') + b'\n'); プロセス.stdin.flush()
                到達待ち受取(b'jkoros-native> ', 変位量値)
                応答 = bytes(実行記録[変位量値:])
                for 文 in 期待:
                    assert 文.encode('utf-8') in 応答, (行, 文, 応答)
                return 応答
            def 入場(行, 入力案内):
                変位量値 = len(実行記録)
                プロセス.stdin.write(行.encode('utf-8') + b'\n'); プロセス.stdin.flush()
                到達待ち受取(入力案内, 変位量値)
                return bytes(実行記録[変位量値:])
            def 編集値(名前, 内容物値, 取消処理操作=False):
                入場('edit ' + 名前, b'edit> ')
                for 行 in 内容物値.splitlines(): 入場(行, b'edit> ')
                if 取消処理操作:
                    変位量値 = len(実行記録)
                    プロセス.stdin.write(b'\x03'); プロセス.stdin.flush()
                    到達待ち受取(b'jkoros-native> ', 変位量値)
                    assert b'EDIT CANCELLED' in 実行記録[変位量値:]
                else:
                    assert b'SAVED' in 入場('.', b'jkoros-native> ')
            def 送出転送ファイル群(名前, データ):
                assert len(データ) <= 16384
                入場('load ' + 名前, b'hex> ')
                for 序数添字 in range(0, len(データ), 64): 入場(データ[序数添字:序数添字+64].hex(), b'hex> ')
                assert b'LOADED' in 入場('.', b'jkoros-native> ')
            def 取得転送(名前):
                応答 = シェル('hex ' + 名前, ['HEX BEGIN', 'HEX END'])
                判定等価 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 応答, re.S)
                データ = bytes.fromhex(''.join(判定等価.group(2).decode('ascii').split()))
                assert len(データ) == int(判定等価.group(1)); return データ
            シェル('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            シェル('java -version', ['not OpenJDK', 'exit 0'])
            シェル('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            シェル('java Hello "한글 引数 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 引数 😀', 'exit 0'])
            シェル('python --version', ['MicroPython 1.24.1', 'exit 0'])
            シェル('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 ファイル', 'exit 0'])
            シェル('cat python.txt', ['한글 ファイル'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            Javaクラス = 出力結果 / 'Hello.class'; Javaクラス.write_bytes(取得転送('Hello.class'))
            期待 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(出力結果), 'Hello', '한글 引数 😀']).decode('utf-8')
            assert 期待.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 引数 😀'], 期待
            編集値('挨拶例.java', 'public class 挨拶例 { public static void main(String[] args) { int 値 = 7; System.out.println("한글=" + 値); } }')
            シェル('javac 挨拶例.java', ['Compiled: 挨拶例.class', 'exit 0'])
            シェル('java 挨拶例', ['한글=7', 'exit 0'])
            (出力結果 / '挨拶例.class').write_bytes(取得転送('挨拶例.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(出力結果), '挨拶例']).decode().strip() == '한글=7'
            編集値('Hello.java', 'broken', 取消処理操作=True)
            シェル('javac Hello.java', ['Compiled:', 'exit 0'])
            編集値('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            シェル('javac Broken.java', ['javac error:', 'exit 1'])
            送出転送ファイル群('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            シェル('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            シェル('rm Broken.java', [])
            取込済み = 出力結果 / 'Imported.java'
            取込済み.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(取込済み)])
            送出転送ファイル群('Imported.class', (出力結果 / 'Imported.class').read_bytes())
            シェル('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            シェル('rm Imported.class', [])
            編集値('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            シェル('javac Loop.java', ['Compiled:', 'exit 0'])
            応答 = シェル('java Loop', ['exit '])
            assert b'instruction limit' in 応答 or b'exit -1004' in 応答
            シェル('rm Loop.java', []); シェル('rm Loop.class', [])
            # CPython-independent Python runtime: Unicode, big integers, closures/classes,
            # GC roots, file imports, exceptions and UDP queues are exercised in the guest.
            Python検査項目 = """import gc, jkoros
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
            編集値('checks.py', Python検査項目)
            シェル('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            シェル('rm checks.py', [])
            編集値('helper.py', 'value = 321')
            シェル("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            シェル('rm helper.py', [])
            シェル("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            シェル("python -c 'while True: pass'", ['exit -1004'])
            for 序数添字 in range(4):
                シェル('python hello.py', ['한글 ファイル', 'exit 0'])
                シェル('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            送出転送ファイル群('app.elf', (計画根 / 'build/user/demo.elf').read_bytes())
            assert 取得転送('app.elf') == (計画根 / 'build/user/demo.elf').read_bytes()
            シェル('run app.elf', ['EL0 C++', 'exit 0'])
            送出転送ファイル群('app.elf', b'not an ELF')
            シェル('run app.elf', ['exit -8'])
            シェル('rm app.elf', [])
            シェル('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            描画中経路 = 出力結果 / 'java-framebuffer'; 描画中経路.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(計画根 / 'dist/jkoros-native-korean.jar'), '-d', str(描画中経路), str(計画根 / '試験/Java/画面試験.java')])
            送出転送ファイル群('画面試験.class', (描画中経路 / '画面試験.class').read_bytes())
            シェル('java 画面試験', ['画面 切抜き 値却下', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            シェル('rm 画面試験.class', [])
            with socket.socket(socket.AF_UNIX) as 接続元:
                接続元.settimeout(10)
                接続元.connect(str(QMP経路))
                with 接続元.makefile('rwb') as ストリーム値:
                    挨拶例 = json.loads(ストリーム値.readline())
                    def 試験用模擬制御接続状態(作業実行, 転送済み引数=None):
                        通信網メッセージ = {'execute': 作業実行}
                        if 転送済み引数: 通信網メッセージ['arguments'] = 転送済み引数
                        ストリーム値.write((json.dumps(通信網メッセージ) + '\n').encode())
                        ストリーム値.flush()
                        while True:
                            返答 = json.loads(ストリーム値.readline())
                            if 'error' in 返答: raise AssertionError(返答)
                            if 'return' in 返答: return 返答['return']
                    試験用模擬制御接続状態('qmp_capabilities')
                    画面記録 = 出力結果 / 'framebuffer.ppm'
                    試験用模擬制御接続状態('screendump', {'filename': str(画面記録), 'format': 'ppm'})
                    def 例登録項目一覧(経路, 点一覧):
                        with 経路.open('rb') as 画素ファイル:
                            assert 画素ファイル.readline().strip() == b'P6'
                            assert 画素ファイル.readline().strip() == b'640 480'
                            assert 画素ファイル.readline().strip() == b'255'
                            画素データ = 画素ファイル.read()
                        assert len(画素データ) == 640 * 480 * 3
                        return [list(画素データ[(縦座標 * 640 + 横座標) * 3:(縦座標 * 640 + 横座標) * 3 + 3]) for 横座標, 縦座標 in 点一覧]
                    assert 例登録項目一覧(画面記録, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 例登録項目一覧(画面記録, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def 送信(押下済み値, 標識):
                        変位量値 = len(実行記録)
                        プロセス.stdin.write(押下済み値); プロセス.stdin.flush()
                        到達待ち受取(標識, 変位量値)
                    送信(b'gui\n', b'GUI READY:')
                    先頭位置GUI = 出力結果 / 'gui-programs.ppm'
                    試験用模擬制御接続状態('screendump', {'filename': str(先頭位置GUI), 'format': 'ppm'})
                    試験用模擬制御接続状態('screendump', {'filename': str(出力結果 / 'gui-programs.png'), 'format': 'png'})
                    assert 例登録項目一覧(先頭位置GUI, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    送信(b'\r', b'GUI ACTION 0 RESULT 0')
                    送信(b'\t', b'GUI FOCUS 1')
                    送信(b'\r', b'GUI ACTION 1 RESULT 0')
                    第二GUI = 出力結果 / 'gui-network.ppm'
                    試験用模擬制御接続状態('screendump', {'filename': str(第二GUI), 'format': 'ppm'})
                    試験用模擬制御接続状態('screendump', {'filename': str(出力結果 / 'gui-network.png'), 'format': 'png'})
                    assert 例登録項目一覧(第二GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    送信(b'\t', b'GUI FOCUS 2')
                    送信(b'\r', b'GUI ACTION 2 RESULT 0')
                    送信(b'\t', b'GUI FOCUS 3')
                    送信(b'\r', b'GUI ACTION 3 RESULT 0')
                    試験用模擬制御接続状態('screendump', {'filename': str(出力結果 / 'gui-python.png'), 'format': 'png'})
                    送信(b'q', b'jkoros-native> ')
                    妥当性報告['qemu'] = 挨拶例['QMP']['version']
                    試験用模擬制御接続状態('quit')
            プロセス.wait(timeout=10)
            # framebuffer 응답뿐 아니라 実際データ scanout 픽셀도 확인한다.
            with 画面記録.open('rb') as ファイル入口:
                assert ファイル入口.readline().strip() == b'P6'
                寸法値 = ファイル入口.readline().strip()
                assert 寸法値 == b'640 480', 寸法値
                assert ファイル入口.readline().strip() == b'255'
                画素列一覧 = ファイル入口.read()
            assert len(画素列一覧) == 640 * 480 * 3
            def 画素(横座標, 縦座標): return list(画素列一覧[(縦座標 * 640 + 横座標) * 3:(縦座標 * 640 + 横座標) * 3 + 3])
            例登録項目一覧 = {'background': 画素(5, 5), 'panel': 画素(45, 85), 'tile': 画素(65, 115)}
            assert 例登録項目一覧 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 例登録項目一覧
            妥当性報告.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=例登録項目一覧, kernel_sha256=hashlib.sha256((計画根 / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if プロセス.poll() is None:
                プロセス.terminate()
                try: プロセス.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    プロセス.kill(); プロセス.wait(timeout=5)
            準備監視器.close()
            プロセス.stdin.close(); プロセス.stdout.close()
            (出力結果 / 'serial.log').write_bytes(実行記録)
            (出力結果 / 'report.json').write_text(json.dumps(妥当性報告, indent=2) + '\n')


if __name__ == '__main__':
    起動処理()
