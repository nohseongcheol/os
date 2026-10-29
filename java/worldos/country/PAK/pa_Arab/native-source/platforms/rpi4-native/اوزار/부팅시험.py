#!/usr/bin/env python3
"""اصلی_کوائف raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from نفاذ_کرو_حکم import 기준, حکم


def چلاؤ():
    출력결과 = 기준 / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    جواز_دہی_رپورٹ = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = حکم() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        جواز_دہی_رپورٹ['command'] = 명령인수
        عمل = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        منتخب_کرنڑ_آلا = selectors.DefaultSelector()
        منتخب_کرنڑ_آلا.register(عمل.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, آف_سیٹ_قدر=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[آف_سیٹ_قدر:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in منتخب_کرنڑ_آلا.select(0.2):
                    کوائف_بلاک = 누름값.fileobj.read(4096)
                    if کوائف_بلاک:
                        대화기록.extend(کوائف_بلاک)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if عمل.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(عمل.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 اصلی_کوائف GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(سائز):
                    결과 = b''
                    while len(결과) < سائز:
                        조각 = 화면접속자.recv(سائز - len(결과))
                        if not 조각: raise AssertionError('VNC disconnected')
                        결과 += 조각
                    return 결과
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                سرور_قدر = 정확한값(24)
                assert int.from_bytes(سرور_قدر[:2], 'big') == 640 and int.from_bytes(سرور_قدر[2:4], 'big') == 480
                정확한값(int.from_bytes(سرور_قدر[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for حکم_بائٹ, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                آف_سیٹ_قدر = len(대화기록)
                عمل.stdin.write(حکم_بائٹ + b'\n')
                عمل.stdin.flush()
                표시까지받기(b'jkoros-native> ', آف_سیٹ_قدر)
                assert 확인표시 in 대화기록[آف_سیٹ_قدر:], 확인표시
            def شیل(لائن, 예상결과):
                آف_سیٹ_قدر = len(대화기록)
                عمل.stdin.write(لائن.encode('utf-8') + b'\n'); عمل.stdin.flush()
                표시까지받기(b'jkoros-native> ', آف_سیٹ_قدر)
                응답자료 = bytes(대화기록[آف_سیٹ_قدر:])
                for متن in 예상결과:
                    assert متن.encode('utf-8') in 응답자료, (لائن, متن, 응답자료)
                return 응답자료
            def داخل_کرو(لائن, لقمیا):
                آف_سیٹ_قدر = len(대화기록)
                عمل.stdin.write(لائن.encode('utf-8') + b'\n'); عمل.stdin.flush()
                표시까지받기(لقمیا, آف_سیٹ_قدر)
                return bytes(대화기록[آف_سیٹ_قدر:])
            def تدوین_قدر(ناں, اجزاء_قدر, منسوخ_کرو_عمل=False):
                داخل_کرو('edit ' + ناں, b'edit> ')
                for لائن in اجزاء_قدر.splitlines(): داخل_کرو(لائن, b'edit> ')
                if منسوخ_کرو_عمل:
                    آف_سیٹ_قدر = len(대화기록)
                    عمل.stdin.write(b'\x03'); عمل.stdin.flush()
                    표시까지받기(b'jkoros-native> ', آف_سیٹ_قدر)
                    assert b'EDIT CANCELLED' in 대화기록[آف_سیٹ_قدر:]
                else:
                    assert b'SAVED' in داخل_کرو('.', b'jkoros-native> ')
            def اپ_لوڈ_کرو_فائلاں(ناں, کوائف):
                assert len(کوائف) <= 16384
                داخل_کرو('load ' + ناں, b'hex> ')
                for 순번 in range(0, len(کوائف), 64): داخل_کرو(کوائف[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in داخل_کرو('.', b'jkoros-native> ')
            def ڈاؤن_لوڈ(ناں):
                응답자료 = شیل('hex ' + ناں, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                کوائف = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(کوائف) == int(일치.group(1)); return کوائف
            شیل('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            شیل('java -version', ['not OpenJDK', 'exit 0'])
            شیل('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            شیل('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            شیل('python --version', ['MicroPython 1.24.1', 'exit 0'])
            شیل('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 فائل', 'exit 0'])
            شیل('cat python.txt', ['한글 فائل'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(ڈاؤن_لوڈ('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            تدوین_قدر('인사.java', 'public class 인사 { public static void main(String[] args) { int قدر = 7; System.out.println("한글=" + قدر); } }')
            شیل('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            شیل('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(ڈاؤن_لوڈ('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            تدوین_قدر('Hello.java', 'broken', منسوخ_کرو_عمل=True)
            شیل('javac Hello.java', ['Compiled:', 'exit 0'])
            تدوین_قدر('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            شیل('javac Broken.java', ['javac error:', 'exit 1'])
            اپ_لوڈ_کرو_فائلاں('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            شیل('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            شیل('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            اپ_لوڈ_کرو_فائلاں('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            شیل('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            شیل('rm Imported.class', [])
            تدوین_قدر('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            شیل('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = شیل('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            شیل('rm Loop.java', []); شیل('rm Loop.class', [])
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
            تدوین_قدر('checks.py', 파이썬검사)
            شیل('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            شیل('rm checks.py', [])
            تدوین_قدر('helper.py', 'value = 321')
            شیل("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            شیل('rm helper.py', [])
            شیل("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            شیل("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                شیل('python hello.py', ['한글 فائل', 'exit 0'])
                شیل('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            اپ_لوڈ_کرو_فائلاں('app.elf', (기준 / 'build/user/demo.elf').read_bytes())
            assert ڈاؤن_لوڈ('app.elf') == (기준 / 'build/user/demo.elf').read_bytes()
            شیل('run app.elf', ['EL0 C++', 'exit 0'])
            اپ_لوڈ_کرو_فائلاں('app.elf', b'not an ELF')
            شیل('run app.elf', ['exit -8'])
            شیل('rm app.elf', [])
            شیل('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            ڈرائنگ_راہ = 출력결과 / 'java-framebuffer'; ڈرائنگ_راہ.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준 / 'dist/jkoros-native-korean.jar'), '-d', str(ڈرائنگ_راہ), str(기준 / '시험/자바/화면시험.java')])
            اپ_لوڈ_کرو_فائلاں('화면시험.class', (ڈرائنگ_راہ / '화면시험.class').read_bytes())
            شیل('java 화면시험', ['화면 تراشہ 거부', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            شیل('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as گاہک:
                گاہک.settimeout(10)
                گاہک.connect(str(모의제어경로))
                with گاہک.makefile('rwb') as سٹریم_قدر:
                    인사 = json.loads(سٹریم_قدر.readline())
                    def 모의제어접속(نفاذ_کرو_ٹاسک, 전달인수=None):
                        نیٹ_ورک_پیغام = {'execute': نفاذ_کرو_ٹاسک}
                        if 전달인수: نیٹ_ورک_پیغام['arguments'] = 전달인수
                        سٹریم_قدر.write((json.dumps(نیٹ_ورک_پیغام) + '\n').encode())
                        سٹریم_قدر.flush()
                        while True:
                            جواب_دیوؤ = json.loads(سٹریم_قدر.readline())
                            if 'error' in جواب_دیوؤ: raise AssertionError(جواب_دیوؤ)
                            if 'return' in جواب_دیوؤ: return جواب_دیوؤ['return']
                    모의제어접속('qmp_capabilities')
                    سکرین_دی_ویڈیو = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(سکرین_دی_ویڈیو), 'format': 'ppm'})
                    def 예제들(راہ, 지점들):
                        with راہ.open('rb') as دانہ_فائل:
                            assert دانہ_فائل.readline().strip() == b'P6'
                            assert دانہ_فائل.readline().strip() == b'640 480'
                            assert دانہ_فائل.readline().strip() == b'255'
                            دانہ_کوائف = دانہ_فائل.read()
                        assert len(دانہ_کوائف) == 640 * 480 * 3
                        return [list(دانہ_کوائف[(세로좌표 * 640 + x_محدد) * 3:(세로좌표 * 640 + x_محدد) * 3 + 3]) for x_محدد, 세로좌표 in 지점들]
                    assert 예제들(سکرین_دی_ویڈیو, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(سکرین_دی_ویڈیو, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def بھیجو(누름값, 확인표시):
                        آف_سیٹ_قدر = len(대화기록)
                        عمل.stdin.write(누름값); عمل.stdin.flush()
                        표시까지받기(확인표시, آف_سیٹ_قدر)
                    بھیجو(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    بھیجو(b'\r', b'GUI ACTION 0 RESULT 0')
                    بھیجو(b'\t', b'GUI FOCUS 1')
                    بھیجو(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    بھیجو(b'\t', b'GUI FOCUS 2')
                    بھیجو(b'\r', b'GUI ACTION 2 RESULT 0')
                    بھیجو(b'\t', b'GUI FOCUS 3')
                    بھیجو(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    بھیجو(b'q', b'jkoros-native> ')
                    جواز_دہی_رپورٹ['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            عمل.wait(timeout=10)
            # framebuffer 응답뿐 아니라 اصلی_کوائف scanout 픽셀도 확인한다.
            with سکرین_دی_ویڈیو.open('rb') as فائل_داخلہ:
                assert فائل_داخلہ.readline().strip() == b'P6'
                치수 = فائل_داخلہ.readline().strip()
                assert 치수 == b'640 480', 치수
                assert فائل_داخلہ.readline().strip() == b'255'
                화소들 = فائل_داخلہ.read()
            assert len(화소들) == 640 * 480 * 3
            def دانہ(x_محدد, 세로좌표): return list(화소들[(세로좌표 * 640 + x_محدد) * 3:(세로좌표 * 640 + x_محدد) * 3 + 3])
            예제들 = {'background': دانہ(5, 5), 'panel': دانہ(45, 85), 'tile': دانہ(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            جواز_دہی_رپورٹ.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
            if عمل.poll() is None:
                عمل.terminate()
                try: عمل.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    عمل.kill(); عمل.wait(timeout=5)
            منتخب_کرنڑ_آلا.close()
            عمل.stdin.close(); عمل.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(جواز_دہی_رپورٹ, indent=2) + '\n')


if __name__ == '__main__':
    چلاؤ()
