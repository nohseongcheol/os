#!/usr/bin/env python3
"""තථ්_ය_දත්ත raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from ක්_රියාත්මක_කරන්න_විධානය import 기준, විධානය


def ක්_රියාත්මක_කරන්න_2():
    출력결과 = 기준 / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    වලංගුකරණය_වාර්තාව = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = විධානය() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        වලංගුකරණය_වාර්තාව['command'] = 명령인수
        සැකසුම = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        වරකය = selectors.DefaultSelector()
        වරකය.register(සැකසුම.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, ඕෆ්සෙට්_අගය=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[ඕෆ්සෙට්_අගය:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in වරකය.select(0.2):
                    දත්ත_අවහිර_කරන්න = 누름값.fileobj.read(4096)
                    if දත්ත_අවහිර_කරන්න:
                        대화기록.extend(දත්ත_අවහිර_කරන්න)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if සැකසුම.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(සැකසුම.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 තථ්_ය_දත්ත GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(ප්_රමාණය):
                    결과 = b''
                    while len(결과) < ප්_රමාණය:
                        조각 = 화면접속자.recv(ප්_රමාණය - len(결과))
                        if not 조각: raise AssertionError('VNC disconnected')
                        결과 += 조각
                    return 결과
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                සේවාදායකය_අගය = 정확한값(24)
                assert int.from_bytes(සේවාදායකය_අගය[:2], 'big') == 640 and int.from_bytes(සේවාදායකය_අගය[2:4], 'big') == 480
                정확한값(int.from_bytes(සේවාදායකය_අගය[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for විධානය_බයිටය, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                ඕෆ්සෙට්_අගය = len(대화기록)
                සැකසුම.stdin.write(විධානය_බයිටය + b'\n')
                සැකසුම.stdin.flush()
                표시까지받기(b'jkoros-native> ', ඕෆ්සෙට්_අගය)
                assert 확인표시 in 대화기록[ඕෆ්සෙට්_අගය:], 확인표시
            def කවචය(පේළිය, 예상결과):
                ඕෆ්සෙට්_අගය = len(대화기록)
                සැකසුම.stdin.write(පේළිය.encode('utf-8') + b'\n'); සැකසුම.stdin.flush()
                표시까지받기(b'jkoros-native> ', ඕෆ්සෙට්_අගය)
                응답자료 = bytes(대화기록[ඕෆ්සෙට්_අගය:])
                for පෙළ in 예상결과:
                    assert පෙළ.encode('utf-8') in 응답자료, (පේළිය, පෙළ, 응답자료)
                return 응답자료
            def ඇතුල්_කිරීම(පේළිය, ප්_රේරකය):
                ඕෆ්සෙට්_අගය = len(대화기록)
                සැකසුම.stdin.write(පේළිය.encode('utf-8') + b'\n'); සැකසුම.stdin.flush()
                표시까지받기(ප්_රේරකය, ඕෆ්සෙට්_අගය)
                return bytes(대화기록[ඕෆ්සෙට්_අගය:])
            def සකසන්න_අගය(නම, අන්තර්ගතය_අගය, එපා_මෙහෙයුම=False):
                ඇතුල්_කිරීම('edit ' + නම, b'edit> ')
                for පේළිය in අන්තර්ගතය_අගය.splitlines(): ඇතුල්_කිරීම(පේළිය, b'edit> ')
                if එපා_මෙහෙයුම:
                    ඕෆ්සෙට්_අගය = len(대화기록)
                    සැකසුම.stdin.write(b'\x03'); සැකසුම.stdin.flush()
                    표시까지받기(b'jkoros-native> ', ඕෆ්සෙට්_අගය)
                    assert b'EDIT CANCELLED' in 대화기록[ඕෆ්සෙට්_අගය:]
                else:
                    assert b'SAVED' in ඇතුල්_කිරීම('.', b'jkoros-native> ')
            def උඩුගත_කරන්න_ගොනු(නම, දත්ත):
                assert len(දත්ත) <= 16384
                ඇතුල්_කිරීම('load ' + නම, b'hex> ')
                for 순번 in range(0, len(දත්ත), 64): ඇතුල්_කිරීම(දත්ත[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in ඇතුල්_කිරීම('.', b'jkoros-native> ')
            def බාගන්න(නම):
                응답자료 = කවචය('hex ' + නම, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                දත්ත = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(දත්ත) == int(일치.group(1)); return දත්ත
            කවචය('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            කවචය('java -version', ['not OpenJDK', 'exit 0'])
            කවචය('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            කවචය('java Hello "한글 විස්තාරක 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 විස්තාරක 😀', 'exit 0'])
            කවචය('python --version', ['MicroPython 1.24.1', 'exit 0'])
            කවචය('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 ගොනු', 'exit 0'])
            කවචය('cat python.txt', ['한글 ගොනු'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(බාගන්න('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 විස්තාරක 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 විස්තාරක 😀'], 예상결과
            සකසන්න_අගය('인사.java', 'public class 인사 { public static void main(String[] args) { int අගය = 7; System.out.println("한글=" + අගය); } }')
            කවචය('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            කවචය('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(බාගන්න('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            සකසන්න_අගය('Hello.java', 'broken', එපා_මෙහෙයුම=True)
            කවචය('javac Hello.java', ['Compiled:', 'exit 0'])
            සකසන්න_අගය('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            කවචය('javac Broken.java', ['javac error:', 'exit 1'])
            උඩුගත_කරන්න_ගොනු('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            කවචය('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            කවචය('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            උඩුගත_කරන්න_ගොනු('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            කවචය('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            කවචය('rm Imported.class', [])
            සකසන්න_අගය('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            කවචය('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = කවචය('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            කවචය('rm Loop.java', []); කවචය('rm Loop.class', [])
            # CPython-independent Python runtime: Unicode, big integers, closures/classes,
            # GC roots, file imports, exceptions and UDP queues are exercised in the guest.
            파이썬검사 = """import gc, jkoros
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
            සකසන්න_අගය('checks.py', 파이썬검사)
            කවචය('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            කවචය('rm checks.py', [])
            සකසන්න_අගය('helper.py', 'value = 321')
            කවචය("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            කවචය('rm helper.py', [])
            කවචය("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            කවචය("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                කවචය('python hello.py', ['한글 ගොනු', 'exit 0'])
                කවචය('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            උඩුගත_කරන්න_ගොනු('app.elf', (기준 / 'build/user/demo.elf').read_bytes())
            assert බාගන්න('app.elf') == (기준 / 'build/user/demo.elf').read_bytes()
            කවචය('run app.elf', ['EL0 C++', 'exit 0'])
            උඩුගත_කරන්න_ගොනු('app.elf', b'not an ELF')
            කවචය('run app.elf', ['exit -8'])
            කවචය('rm app.elf', [])
            කවචය('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            චිත්_රය_පෙත = 출력결과 / 'java-framebuffer'; චිත්_රය_පෙත.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준 / 'dist/jkoros-native-korean.jar'), '-d', str(චිත්_රය_පෙත), str(기준 / '시험/자바/화면시험.java')])
            උඩුගත_කරන්න_ගොනු('화면시험.class', (චිත්_රය_පෙත / '화면시험.class').read_bytes())
            කවචය('java 화면시험', ['화면 පසුර 거부', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            කවචය('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as සේවාලාභීයා:
                සේවාලාභීයා.settimeout(10)
                සේවාලාභීයා.connect(str(모의제어경로))
                with සේවාලාභීයා.makefile('rwb') as දහර_අගය:
                    인사 = json.loads(දහර_අගය.readline())
                    def 모의제어접속(ක්_රියාත්මක_කරන්න, 전달인수=None):
                        ජාලය_පණිවිඩය = {'execute': ක්_රියාත්මක_කරන්න}
                        if 전달인수: ජාලය_පණිවිඩය['arguments'] = 전달인수
                        දහර_අගය.write((json.dumps(ජාලය_පණිවිඩය) + '\n').encode())
                        දහර_අගය.flush()
                        while True:
                            පිළිතුරු_දෙන්න = json.loads(දහර_අගය.readline())
                            if 'error' in පිළිතුරු_දෙන්න: raise AssertionError(පිළිතුරු_දෙන්න)
                            if 'return' in පිළිතුරු_දෙන්න: return පිළිතුරු_දෙන්න['return']
                    모의제어접속('qmp_capabilities')
                    තිර_ඇමිණුම = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(තිර_ඇමිණුම), 'format': 'ppm'})
                    def 예제들(මාර්_ගය, 지점들):
                        with මාර්_ගය.open('rb') as පික්සලය_ගොනුව:
                            assert පික්සලය_ගොනුව.readline().strip() == b'P6'
                            assert පික්සලය_ගොනුව.readline().strip() == b'640 480'
                            assert පික්සලය_ගොනුව.readline().strip() == b'255'
                            පික්සලය_දත්ත = පික්සලය_ගොනුව.read()
                        assert len(පික්සලය_දත්ත) == 640 * 480 * 3
                        return [list(පික්සලය_දත්ත[(세로좌표 * 640 + x_ඛණ්ඩාංකය) * 3:(세로좌표 * 640 + x_ඛණ්ඩාංකය) * 3 + 3]) for x_ඛණ්ඩාංකය, 세로좌표 in 지점들]
                    assert 예제들(තිර_ඇමිණුම, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(තිර_ඇමිණුම, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def ඊමේල්(누름값, 확인표시):
                        ඕෆ්සෙට්_අගය = len(대화기록)
                        සැකසුම.stdin.write(누름값); සැකසුම.stdin.flush()
                        표시까지받기(확인표시, ඕෆ්සෙට්_අගය)
                    ඊමේල්(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    ඊමේල්(b'\r', b'GUI ACTION 0 RESULT 0')
                    ඊමේල්(b'\t', b'GUI FOCUS 1')
                    ඊමේල්(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    ඊමේල්(b'\t', b'GUI FOCUS 2')
                    ඊමේල්(b'\r', b'GUI ACTION 2 RESULT 0')
                    ඊමේල්(b'\t', b'GUI FOCUS 3')
                    ඊමේල්(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    ඊමේල්(b'q', b'jkoros-native> ')
                    වලංගුකරණය_වාර්තාව['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            සැකසුම.wait(timeout=10)
            # framebuffer 응답뿐 아니라 තථ්_ය_දත්ත scanout 픽셀도 확인한다.
            with තිර_ඇමිණුම.open('rb') as ගොනුව_පිවිසුම:
                assert ගොනුව_පිවිසුම.readline().strip() == b'P6'
                치수 = ගොනුව_පිවිසුම.readline().strip()
                assert 치수 == b'640 480', 치수
                assert ගොනුව_පිවිසුම.readline().strip() == b'255'
                화소들 = ගොනුව_පිවිසුම.read()
            assert len(화소들) == 640 * 480 * 3
            def පික්සලය(x_ඛණ්ඩාංකය, 세로좌표): return list(화소들[(세로좌표 * 640 + x_ඛණ්ඩාංකය) * 3:(세로좌표 * 640 + x_ඛණ්ඩාංකය) * 3 + 3])
            예제들 = {'background': පික්සලය(5, 5), 'panel': පික්සලය(45, 85), 'tile': පික්සලය(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            වලංගුකරණය_වාර්තාව.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if සැකසුම.poll() is None:
                සැකසුම.terminate()
                try: සැකසුම.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    සැකසුම.kill(); සැකසුම.wait(timeout=5)
            වරකය.close()
            සැකසුම.stdin.close(); සැකසුම.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(වලංගුකරණය_වාර්තාව, indent=2) + '\n')


if __name__ == '__main__':
    ක්_රියාත්මක_කරන්න_2()
