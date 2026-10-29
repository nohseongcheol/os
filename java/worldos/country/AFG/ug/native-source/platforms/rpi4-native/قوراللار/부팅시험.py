#!/usr/bin/env python3
"""ھەقىقىي_مەلۇمات raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from ئىجرا_قىلىش_بۇيرۇق import كۆرسىتىش_يىلتىز, بۇيرۇق


def ئىجرا_قىل_2():
    출력결과 = كۆرسىتىش_يىلتىز / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    دەلىللەش_خەۋەر = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = بۇيرۇق() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        دەلىللەش_خەۋەر['command'] = 명령인수
        جەريان = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        تاللىغۇچ = selectors.DefaultSelector()
        تاللىغۇچ.register(جەريان.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, ئاغما_قىممىتى=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[ئاغما_قىممىتى:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in تاللىغۇچ.select(0.2):
                    مەلۇمات_چەكلەش = 누름값.fileobj.read(4096)
                    if مەلۇمات_چەكلەش:
                        대화기록.extend(مەلۇمات_چەكلەش)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if جەريان.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(جەريان.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 ھەقىقىي_مەلۇمات GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(چوڭلۇقى):
                    ئۆلچەم = b''
                    while len(ئۆلچەم) < چوڭلۇقى:
                        조각 = 화면접속자.recv(چوڭلۇقى - len(ئۆلچەم))
                        if not 조각: raise AssertionError('VNC disconnected')
                        ئۆلچەم += 조각
                    return ئۆلچەم
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                مۇلازىمىتېر_قىممىتى = 정확한값(24)
                assert int.from_bytes(مۇلازىمىتېر_قىممىتى[:2], 'big') == 640 and int.from_bytes(مۇلازىمىتېر_قىممىتى[2:4], 'big') == 480
                정확한값(int.from_bytes(مۇلازىمىتېر_قىممىتى[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for بۇيرۇق_بايت, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                ئاغما_قىممىتى = len(대화기록)
                جەريان.stdin.write(بۇيرۇق_بايت + b'\n')
                جەريان.stdin.flush()
                표시까지받기(b'jkoros-native> ', ئاغما_قىممىتى)
                assert 확인표시 in 대화기록[ئاغما_قىممىتى:], 확인표시
            def قاپ(قۇر, 예상결과):
                ئاغما_قىممىتى = len(대화기록)
                جەريان.stdin.write(قۇر.encode('utf-8') + b'\n'); جەريان.stdin.flush()
                표시까지받기(b'jkoros-native> ', ئاغما_قىممىتى)
                응답자료 = bytes(대화기록[ئاغما_قىممىتى:])
                for تېكىست in 예상결과:
                    assert تېكىست.encode('utf-8') in 응답자료, (قۇر, تېكىست, 응답자료)
                return 응답자료
            def كىرمەك(قۇر, ئەسكەرتمە):
                ئاغما_قىممىتى = len(대화기록)
                جەريان.stdin.write(قۇر.encode('utf-8') + b'\n'); جەريان.stdin.flush()
                표시까지받기(ئەسكەرتمە, ئاغما_قىممىتى)
                return bytes(대화기록[ئاغما_قىممىتى:])
            def تەھرىرلەش_قىممىتى(ئاتى, مەزمۇن_قىممىتى, ئىناۋەتسىز_مەشغۇلات=False):
                كىرمەك('edit ' + ئاتى, b'edit> ')
                for قۇر in مەزمۇن_قىممىتى.splitlines(): كىرمەك(قۇر, b'edit> ')
                if ئىناۋەتسىز_مەشغۇلات:
                    ئاغما_قىممىتى = len(대화기록)
                    جەريان.stdin.write(b'\x03'); جەريان.stdin.flush()
                    표시까지받기(b'jkoros-native> ', ئاغما_قىممىتى)
                    assert b'EDIT CANCELLED' in 대화기록[ئاغما_قىممىتى:]
                else:
                    assert b'SAVED' in كىرمەك('.', b'jkoros-native> ')
            def يۈكلىمەك_ھۆججەت(ئاتى, مەلۇمات):
                assert len(مەلۇمات) <= 16384
                كىرمەك('load ' + ئاتى, b'hex> ')
                for 순번 in range(0, len(مەلۇمات), 64): كىرمەك(مەلۇمات[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in كىرمەك('.', b'jkoros-native> ')
            def چۈشۈرۈش(ئاتى):
                응답자료 = قاپ('hex ' + ئاتى, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                مەلۇمات = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(مەلۇمات) == int(일치.group(1)); return مەلۇمات
            قاپ('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            قاپ('java -version', ['not OpenJDK', 'exit 0'])
            قاپ('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            قاپ('java Hello "한글 ئۆزگەرگۈچىلەر 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 ئۆزگەرگۈچىلەر 😀', 'exit 0'])
            قاپ('python --version', ['MicroPython 1.24.1', 'exit 0'])
            قاپ('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 ھۆججەت', 'exit 0'])
            قاپ('cat python.txt', ['한글 ھۆججەت'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(چۈشۈرۈش('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 ئۆزگەرگۈچىلەر 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 ئۆزگەرگۈچىلەر 😀'], 예상결과
            تەھرىرلەش_قىممىتى('인사.java', 'public class 인사 { public static void main(String[] args) { int قىممىتى = 7; System.out.println("한글=" + قىممىتى); } }')
            قاپ('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            قاپ('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(چۈشۈرۈش('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            تەھرىرلەش_قىممىتى('Hello.java', 'broken', ئىناۋەتسىز_مەشغۇلات=True)
            قاپ('javac Hello.java', ['Compiled:', 'exit 0'])
            تەھرىرلەش_قىممىتى('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            قاپ('javac Broken.java', ['javac error:', 'exit 1'])
            يۈكلىمەك_ھۆججەت('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            قاپ('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            قاپ('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            يۈكلىمەك_ھۆججەت('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            قاپ('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            قاپ('rm Imported.class', [])
            تەھرىرلەش_قىممىتى('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            قاپ('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = قاپ('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            قاپ('rm Loop.java', []); قاپ('rm Loop.class', [])
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
            تەھرىرلەش_قىممىتى('checks.py', 파이썬검사)
            قاپ('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            قاپ('rm checks.py', [])
            تەھرىرلەش_قىممىتى('helper.py', 'value = 321')
            قاپ("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            قاپ('rm helper.py', [])
            قاپ("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            قاپ("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                قاپ('python hello.py', ['한글 ھۆججەت', 'exit 0'])
                قاپ('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            يۈكلىمەك_ھۆججەت('app.elf', (كۆرسىتىش_يىلتىز / 'build/user/demo.elf').read_bytes())
            assert چۈشۈرۈش('app.elf') == (كۆرسىتىش_يىلتىز / 'build/user/demo.elf').read_bytes()
            قاپ('run app.elf', ['EL0 C++', 'exit 0'])
            يۈكلىمەك_ھۆججەت('app.elf', b'not an ELF')
            قاپ('run app.elf', ['exit -8'])
            قاپ('rm app.elf', [])
            قاپ('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            سىزىش_يول = 출력결과 / 'java-framebuffer'; سىزىش_يول.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(كۆرسىتىش_يىلتىز / 'dist/jkoros-native-korean.jar'), '-d', str(سىزىش_يول), str(كۆرسىتىش_يىلتىز / '시험/자바/화면시험.java')])
            يۈكلىمەك_ھۆججەت('화면시험.class', (سىزىش_يول / '화면시험.class').read_bytes())
            قاپ('java 화면시험', ['화면 كەسمە 거부', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            قاپ('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as ئابۇنىتېر:
                ئابۇنىتېر.settimeout(10)
                ئابۇنىتېر.connect(str(모의제어경로))
                with ئابۇنىتېر.makefile('rwb') as ئېقىم_قىممىتى:
                    인사 = json.loads(ئېقىم_قىممىتى.readline())
                    def 모의제어접속(ئىجرا_قىل, 전달인수=None):
                        تور_ئۇچۇر = {'execute': ئىجرا_قىل}
                        if 전달인수: تور_ئۇچۇر['arguments'] = 전달인수
                        ئېقىم_قىممىتى.write((json.dumps(تور_ئۇچۇر) + '\n').encode())
                        ئېقىم_قىممىتى.flush()
                        while True:
                            جاۋابلاش = json.loads(ئېقىم_قىممىتى.readline())
                            if 'error' in جاۋابلاش: raise AssertionError(جاۋابلاش)
                            if 'return' in جاۋابلاش: return جاۋابلاش['return']
                    모의제어접속('qmp_capabilities')
                    ئېكراندىن_تۇتۇش = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(ئېكراندىن_تۇتۇش), 'format': 'ppm'})
                    def 예제들(يول, 지점들):
                        with يول.open('rb') as پىكسېل_ھۆججەت:
                            assert پىكسېل_ھۆججەت.readline().strip() == b'P6'
                            assert پىكسېل_ھۆججەت.readline().strip() == b'640 480'
                            assert پىكسېل_ھۆججەت.readline().strip() == b'255'
                            پىكسېل_مەلۇمات = پىكسېل_ھۆججەت.read()
                        assert len(پىكسېل_مەلۇمات) == 640 * 480 * 3
                        return [list(پىكسېل_مەلۇمات[(세로좌표 * 640 + x_كوردىنات) * 3:(세로좌표 * 640 + x_كوردىنات) * 3 + 3]) for x_كوردىنات, 세로좌표 in 지점들]
                    assert 예제들(ئېكراندىن_تۇتۇش, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(ئېكراندىن_تۇتۇش, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def ئەۋەتمەك(누름값, 확인표시):
                        ئاغما_قىممىتى = len(대화기록)
                        جەريان.stdin.write(누름값); جەريان.stdin.flush()
                        표시까지받기(확인표시, ئاغما_قىممىتى)
                    ئەۋەتمەك(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    ئەۋەتمەك(b'\r', b'GUI ACTION 0 RESULT 0')
                    ئەۋەتمەك(b'\t', b'GUI FOCUS 1')
                    ئەۋەتمەك(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    ئەۋەتمەك(b'\t', b'GUI FOCUS 2')
                    ئەۋەتمەك(b'\r', b'GUI ACTION 2 RESULT 0')
                    ئەۋەتمەك(b'\t', b'GUI FOCUS 3')
                    ئەۋەتمەك(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    ئەۋەتمەك(b'q', b'jkoros-native> ')
                    دەلىللەش_خەۋەر['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            جەريان.wait(timeout=10)
            # framebuffer 응답뿐 아니라 ھەقىقىي_مەلۇمات scanout 픽셀도 확인한다.
            with ئېكراندىن_تۇتۇش.open('rb') as ھۆججەت_كىرگۈزۈش:
                assert ھۆججەت_كىرگۈزۈش.readline().strip() == b'P6'
                치수 = ھۆججەت_كىرگۈزۈش.readline().strip()
                assert 치수 == b'640 480', 치수
                assert ھۆججەت_كىرگۈزۈش.readline().strip() == b'255'
                화소들 = ھۆججەت_كىرگۈزۈش.read()
            assert len(화소들) == 640 * 480 * 3
            def پىكسېل(x_كوردىنات, 세로좌표): return list(화소들[(세로좌표 * 640 + x_كوردىنات) * 3:(세로좌표 * 640 + x_كوردىنات) * 3 + 3])
            예제들 = {'background': پىكسېل(5, 5), 'panel': پىكسېل(45, 85), 'tile': پىكسېل(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            دەلىللەش_خەۋەر.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((كۆرسىتىش_يىلتىز / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if جەريان.poll() is None:
                جەريان.terminate()
                try: جەريان.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    جەريان.kill(); جەريان.wait(timeout=5)
            تاللىغۇچ.close()
            جەريان.stdin.close(); جەريان.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(دەلىللەش_خەۋەر, indent=2) + '\n')


if __name__ == '__main__':
    ئىجرا_قىل_2()
