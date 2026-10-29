#!/usr/bin/env python3
"""实际数据 raspi4b 启动, UART 输入值, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from 执行命令 import 项目根, 命令


def 运行():
    输出结果 = 项目根 / 'build/verification'
    输出结果.mkdir(parents=True, exist_ok=True)
    执行记录 = bytearray()
    有效性验证报告 = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 工作中路径:
        QMP路径 = Path(工作中路径) / 'qmp.sock'
        命令参数列 = 命令() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(QMP路径),
                           '-vnc', 'unix:{}'.format(Path(工作中路径) / 'vnc.sock')]
        有效性验证报告['command'] = 命令参数列
        进程 = subprocess.Popen(命令参数列, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        就绪选择器 = selectors.DefaultSelector()
        就绪选择器.register(进程.stdout, selectors.EVENT_READ)
        def 接收直到(标记, 偏移值=0, 执行状态超时=45):
            截止时间时间 = time.monotonic() + 执行状态超时
            while 标记 not in 执行记录[偏移值:]:
                if time.monotonic() > 截止时间时间:
                    raise AssertionError('UART timeout: ' + repr(标记))
                for 已按下值, _ in 就绪选择器.select(0.2):
                    数据块 = 已按下值.fileobj.read(4096)
                    if 数据块:
                        执行记录.extend(数据块)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 执行记录):
                    raise AssertionError('kernel failure')
                if 进程.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(进程.returncode))
        try:
            接收直到(b'jkoros-native> ')
            标记列 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 标记 in 标记列:
                assert 标记 in 执行记录, 标记
            # GTK 없는 当前项目 호스트에서도 VNC로 实际数据 GUI를 볼 数 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 屏幕客户端:
                屏幕客户端.settimeout(5); 屏幕客户端.connect(str(Path(工作中路径) / 'vnc.sock'))
                def 精确值(大小):
                    结果 = b''
                    while len(结果) < 大小:
                        片段值 = 屏幕客户端.recv(大小 - len(结果))
                        if not 片段值: raise AssertionError('VNC disconnected')
                        结果 += 片段值
                    return 结果
                assert 精确值(12) == b'RFB 003.008\n'
                屏幕客户端.sendall(b'RFB 003.008\n')
                assert 1 in 精确值(精确值(1)[0]); 屏幕客户端.sendall(b'\x01')
                assert 精确值(4) == b'\x00\x00\x00\x00'; 屏幕客户端.sendall(b'\x01')
                服务器值 = 精确值(24)
                assert int.from_bytes(服务器值[:2], 'big') == 640 and int.from_bytes(服务器值[2:4], 'big') == 480
                精确值(int.from_bytes(服务器值[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for 命令字节, 标记 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '测试.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                偏移值 = len(执行记录)
                进程.stdin.write(命令字节 + b'\n')
                进程.stdin.flush()
                接收直到(b'jkoros-native> ', 偏移值)
                assert 标记 in 执行记录[偏移值:], 标记
            def 命令壳(行, 预期):
                偏移值 = len(执行记录)
                进程.stdin.write(行.encode('utf-8') + b'\n'); 进程.stdin.flush()
                接收直到(b'jkoros-native> ', 偏移值)
                响应 = bytes(执行记录[偏移值:])
                for 文本 in 预期:
                    assert 文本.encode('utf-8') in 响应, (行, 文本, 响应)
                return 响应
            def 进入(行, 提示):
                偏移值 = len(执行记录)
                进程.stdin.write(行.encode('utf-8') + b'\n'); 进程.stdin.flush()
                接收直到(提示, 偏移值)
                return bytes(执行记录[偏移值:])
            def 编辑值(名称, 内容值, 取消操作=False):
                进入('edit ' + 名称, b'edit> ')
                for 行 in 内容值.splitlines(): 进入(行, b'edit> ')
                if 取消操作:
                    偏移值 = len(执行记录)
                    进程.stdin.write(b'\x03'); 进程.stdin.flush()
                    接收直到(b'jkoros-native> ', 偏移值)
                    assert b'EDIT CANCELLED' in 执行记录[偏移值:]
                else:
                    assert b'SAVED' in 进入('.', b'jkoros-native> ')
            def 上传文件集(名称, 数据):
                assert len(数据) <= 16384
                进入('load ' + 名称, b'hex> ')
                for 序数索引 in range(0, len(数据), 64): 进入(数据[序数索引:序数索引+64].hex(), b'hex> ')
                assert b'LOADED' in 进入('.', b'jkoros-native> ')
            def 下载(名称):
                响应 = 命令壳('hex ' + 名称, ['HEX BEGIN', 'HEX END'])
                是否相等 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 响应, re.S)
                数据 = bytes.fromhex(''.join(是否相等.group(2).decode('ascii').split()))
                assert len(数据) == int(是否相等.group(1)); return 数据
            命令壳('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            命令壳('java -version', ['not OpenJDK', 'exit 0'])
            命令壳('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            命令壳('java Hello "한글 实参 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 实参 😀', 'exit 0'])
            命令壳('python --version', ['MicroPython 1.24.1', 'exit 0'])
            命令壳('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 文件', 'exit 0'])
            命令壳('cat python.txt', ['한글 文件'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            Java类 = 输出结果 / 'Hello.class'; Java类.write_bytes(下载('Hello.class'))
            预期 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(输出结果), 'Hello', '한글 实参 😀']).decode('utf-8')
            assert 预期.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 实参 😀'], 预期
            编辑值('问候例.java', 'public class 问候例 { public static void main(String[] args) { int 值 = 7; System.out.println("한글=" + 值); } }')
            命令壳('javac 问候例.java', ['Compiled: 问候例.class', 'exit 0'])
            命令壳('java 问候例', ['한글=7', 'exit 0'])
            (输出结果 / '问候例.class').write_bytes(下载('问候例.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(输出结果), '问候例']).decode().strip() == '한글=7'
            编辑值('Hello.java', 'broken', 取消操作=True)
            命令壳('javac Hello.java', ['Compiled:', 'exit 0'])
            编辑值('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            命令壳('javac Broken.java', ['javac error:', 'exit 1'])
            上传文件集('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            命令壳('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            命令壳('rm Broken.java', [])
            已导入 = 输出结果 / 'Imported.java'
            已导入.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(已导入)])
            上传文件集('Imported.class', (输出结果 / 'Imported.class').read_bytes())
            命令壳('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            命令壳('rm Imported.class', [])
            编辑值('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            命令壳('javac Loop.java', ['Compiled:', 'exit 0'])
            响应 = 命令壳('java Loop', ['exit '])
            assert b'instruction limit' in 响应 or b'exit -1004' in 响应
            命令壳('rm Loop.java', []); 命令壳('rm Loop.class', [])
            # CPython-independent Python runtime: Unicode, big integers, closures/classes,
            # GC roots, file imports, exceptions and UDP queues are exercised in the guest.
            Python检查项 = """import gc, jkoros
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
            编辑值('checks.py', Python检查项)
            命令壳('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            命令壳('rm checks.py', [])
            编辑值('helper.py', 'value = 321')
            命令壳("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            命令壳('rm helper.py', [])
            命令壳("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            命令壳("python -c 'while True: pass'", ['exit -1004'])
            for 序数索引 in range(4):
                命令壳('python hello.py', ['한글 文件', 'exit 0'])
                命令壳('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            上传文件集('app.elf', (项目根 / 'build/user/demo.elf').read_bytes())
            assert 下载('app.elf') == (项目根 / 'build/user/demo.elf').read_bytes()
            命令壳('run app.elf', ['EL0 C++', 'exit 0'])
            上传文件集('app.elf', b'not an ELF')
            命令壳('run app.elf', ['exit -8'])
            命令壳('rm app.elf', [])
            命令壳('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            绘图路径 = 输出结果 / 'java-framebuffer'; 绘图路径.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(项目根 / 'dist/jkoros-native-korean.jar'), '-d', str(绘图路径), str(项目根 / '测试/Java/测试屏幕.java')])
            上传文件集('测试屏幕.class', (绘图路径 / '测试屏幕.class').read_bytes())
            命令壳('java 测试屏幕', ['屏幕 裁剪 拒绝值', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            命令壳('rm 测试屏幕.class', [])
            with socket.socket(socket.AF_UNIX) as 客户端:
                客户端.settimeout(10)
                客户端.connect(str(QMP路径))
                with 客户端.makefile('rwb') as 流值:
                    问候例 = json.loads(流值.readline())
                    def 测试替身控制连接状态(执行任务, 已转发参数=None):
                        网络消息 = {'execute': 执行任务}
                        if 已转发参数: 网络消息['arguments'] = 已转发参数
                        流值.write((json.dumps(网络消息) + '\n').encode())
                        流值.flush()
                        while True:
                            回复 = json.loads(流值.readline())
                            if 'error' in 回复: raise AssertionError(回复)
                            if 'return' in 回复: return 回复['return']
                    测试替身控制连接状态('qmp_capabilities')
                    屏幕剪辑 = 输出结果 / 'framebuffer.ppm'
                    测试替身控制连接状态('screendump', {'filename': str(屏幕剪辑), 'format': 'ppm'})
                    def 示例条目列(路径, 点列):
                        with 路径.open('rb') as 像素文件:
                            assert 像素文件.readline().strip() == b'P6'
                            assert 像素文件.readline().strip() == b'640 480'
                            assert 像素文件.readline().strip() == b'255'
                            像素数据 = 像素文件.read()
                        assert len(像素数据) == 640 * 480 * 3
                        return [list(像素数据[(Y_按钮坐标 * 640 + 横坐标坐标) * 3:(Y_按钮坐标 * 640 + 横坐标坐标) * 3 + 3]) for 横坐标坐标, Y_按钮坐标 in 点列]
                    assert 示例条目列(屏幕剪辑, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 示例条目列(屏幕剪辑, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def 发送(已按下值, 标记):
                        偏移值 = len(执行记录)
                        进程.stdin.write(已按下值); 进程.stdin.flush()
                        接收直到(标记, 偏移值)
                    发送(b'gui\n', b'GUI READY:')
                    首位GUI = 输出结果 / 'gui-programs.ppm'
                    测试替身控制连接状态('screendump', {'filename': str(首位GUI), 'format': 'ppm'})
                    测试替身控制连接状态('screendump', {'filename': str(输出结果 / 'gui-programs.png'), 'format': 'png'})
                    assert 示例条目列(首位GUI, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    发送(b'\r', b'GUI ACTION 0 RESULT 0')
                    发送(b'\t', b'GUI FOCUS 1')
                    发送(b'\r', b'GUI ACTION 1 RESULT 0')
                    第二GUI = 输出结果 / 'gui-network.ppm'
                    测试替身控制连接状态('screendump', {'filename': str(第二GUI), 'format': 'ppm'})
                    测试替身控制连接状态('screendump', {'filename': str(输出结果 / 'gui-network.png'), 'format': 'png'})
                    assert 示例条目列(第二GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    发送(b'\t', b'GUI FOCUS 2')
                    发送(b'\r', b'GUI ACTION 2 RESULT 0')
                    发送(b'\t', b'GUI FOCUS 3')
                    发送(b'\r', b'GUI ACTION 3 RESULT 0')
                    测试替身控制连接状态('screendump', {'filename': str(输出结果 / 'gui-python.png'), 'format': 'png'})
                    发送(b'q', b'jkoros-native> ')
                    有效性验证报告['qemu'] = 问候例['QMP']['version']
                    测试替身控制连接状态('quit')
            进程.wait(timeout=10)
            # framebuffer 응답뿐 아니라 实际数据 scanout 픽셀도 확인한다.
            with 屏幕剪辑.open('rb') as 文件条目:
                assert 文件条目.readline().strip() == b'P6'
                尺寸值 = 文件条目.readline().strip()
                assert 尺寸值 == b'640 480', 尺寸值
                assert 文件条目.readline().strip() == b'255'
                像素列列表 = 文件条目.read()
            assert len(像素列列表) == 640 * 480 * 3
            def 像素(横坐标坐标, Y_按钮坐标): return list(像素列列表[(Y_按钮坐标 * 640 + 横坐标坐标) * 3:(Y_按钮坐标 * 640 + 横坐标坐标) * 3 + 3])
            示例条目列 = {'background': 像素(5, 5), 'panel': 像素(45, 85), 'tile': 像素(65, 115)}
            assert 示例条目列 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 示例条目列
            有效性验证报告.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=示例条目列, kernel_sha256=hashlib.sha256((项目根 / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if 进程.poll() is None:
                进程.terminate()
                try: 进程.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    进程.kill(); 进程.wait(timeout=5)
            就绪选择器.close()
            进程.stdin.close(); 进程.stdout.close()
            (输出结果 / 'serial.log').write_bytes(执行记录)
            (输出结果 / 'report.json').write_text(json.dumps(有效性验证报告, indent=2) + '\n')


if __name__ == '__main__':
    运行()
