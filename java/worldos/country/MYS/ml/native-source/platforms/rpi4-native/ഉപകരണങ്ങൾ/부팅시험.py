#!/usr/bin/env python3
"""വാസ്തവമായ_ഡാറ്റാ raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from നടപ്പാക്കുക_കമാന്_ഡ് import പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം, ആജ്ഞ


def നടപ്പിലാക്കുക():
    출력결과 = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    నిర్ధారణ_నివేదిక = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = ആജ്ഞ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        నిర్ధారణ_నివేదిక['command'] = 명령인수
        പ്രക്രിയ = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        సెలక్టర్ = selectors.DefaultSelector()
        సెలక్టర్.register(പ്രക്രിയ.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, ഓഫ്_സെറ്റ്_മൂല്യം=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[ഓഫ്_സെറ്റ്_മൂല്യം:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in సెలక్టర్.select(0.2):
                    ഡാറ്റാ_തടയുക = 누름값.fileobj.read(4096)
                    if ഡാറ്റാ_തടയുക:
                        대화기록.extend(ഡാറ്റാ_തടയുക)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if പ്രക്രിയ.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(പ്രക്രിയ.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 വാസ്തവമായ_ഡാറ്റാ GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(വലിപ്പം):
                    അളവ് = b''
                    while len(അളവ്) < വലിപ്പം:
                        조각 = 화면접속자.recv(വലിപ്പം - len(അളവ്))
                        if not 조각: raise AssertionError('VNC disconnected')
                        അളവ് += 조각
                    return അളവ്
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                സെര്_വര്_മൂല്യം = 정확한값(24)
                assert int.from_bytes(സെര്_വര്_മൂല്യം[:2], 'big') == 640 and int.from_bytes(സെര്_വര്_മൂല്യം[2:4], 'big') == 480
                정확한값(int.from_bytes(സെര്_വര്_മൂല്യം[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for കമാന്_ഡ്_బైట్, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                ഓഫ്_സെറ്റ്_മൂല്യം = len(대화기록)
                പ്രക്രിയ.stdin.write(കമാന്_ഡ്_బైట్ + b'\n')
                പ്രക്രിയ.stdin.flush()
                표시까지받기(b'jkoros-native> ', ഓഫ്_സെറ്റ്_മൂല്യം)
                assert 확인표시 in 대화기록[ഓഫ്_സെറ്റ്_മൂല്യം:], 확인표시
            def ഷെല്(ലൈൻ, 예상결과):
                ഓഫ്_സെറ്റ്_മൂല്യം = len(대화기록)
                പ്രക്രിയ.stdin.write(ലൈൻ.encode('utf-8') + b'\n'); പ്രക്രിയ.stdin.flush()
                표시까지받기(b'jkoros-native> ', ഓഫ്_സെറ്റ്_മൂല്യം)
                응답자료 = bytes(대화기록[ഓഫ്_സെറ്റ്_മൂല്യം:])
                for പദാവലി in 예상결과:
                    assert പദാവലി.encode('utf-8') in 응답자료, (ലൈൻ, പദാവലി, 응답자료)
                return 응답자료
            def നല്_കുക(ലൈൻ, പ്രോംപ്റ്റ്):
                ഓഫ്_സെറ്റ്_മൂല്യം = len(대화기록)
                പ്രക്രിയ.stdin.write(ലൈൻ.encode('utf-8') + b'\n'); പ്രക്രിയ.stdin.flush()
                표시까지받기(പ്രോംപ്റ്റ്, ഓഫ്_സെറ്റ്_മൂല്യം)
                return bytes(대화기록[ഓഫ്_സെറ്റ്_മൂല്യം:])
            def ചിട്ടപ്പെടുത്തല്_മൂല്യം(പേരു്, ഉള്ളടക്കം_മൂല്യം, റദ്ദാക്കുക_ഓപ്പറേഷൻ=False):
                നല്_കുക('edit ' + പേരു്, b'edit> ')
                for ലൈൻ in ഉള്ളടക്കം_മൂല്യം.splitlines(): നല്_കുക(ലൈൻ, b'edit> ')
                if റദ്ദാക്കുക_ഓപ്പറേഷൻ:
                    ഓഫ്_സെറ്റ്_മൂല്യം = len(대화기록)
                    പ്രക്രിയ.stdin.write(b'\x03'); പ്രക്രിയ.stdin.flush()
                    표시까지받기(b'jkoros-native> ', ഓഫ്_സെറ്റ്_മൂല്യം)
                    assert b'EDIT CANCELLED' in 대화기록[ഓഫ്_സെറ്റ്_മൂല്യം:]
                else:
                    assert b'SAVED' in നല്_കുക('.', b'jkoros-native> ')
            def അപ്_ലോഡ്_ഫയലുകൾ(പേരു്, ഡാറ്റാ):
                assert len(ഡാറ്റാ) <= 16384
                നല്_കുക('load ' + പേരു്, b'hex> ')
                for 순번 in range(0, len(ഡാറ്റാ), 64): നല്_കുക(ഡാറ്റാ[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in നല്_കുക('.', b'jkoros-native> ')
            def ഡൗൺലോഡ്(പേരു്):
                응답자료 = ഷെല്('hex ' + പേരു്, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                ഡാറ്റാ = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(ഡാറ്റാ) == int(일치.group(1)); return ഡാറ്റാ
            ഷെല്('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            ഷെല്('java -version', ['not OpenJDK', 'exit 0'])
            ഷെല്('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            ഷെല്('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            ഷെല്('python --version', ['MicroPython 1.24.1', 'exit 0'])
            ഷെല്('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 ഫയല്', 'exit 0'])
            ഷെല്('cat python.txt', ['한글 ഫയല്'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(ഡൗൺലോഡ്('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            ചിട്ടപ്പെടുത്തല്_മൂല്യം('인사.java', 'public class 인사 { public static void main(String[] args) { int മൂല്യം = 7; System.out.println("한글=" + മൂല്യം); } }')
            ഷെല്('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            ഷെല്('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(ഡൗൺലോഡ്('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            ചിട്ടപ്പെടുത്തല്_മൂല്യം('Hello.java', 'broken', റദ്ദാക്കുക_ഓപ്പറേഷൻ=True)
            ഷെല്('javac Hello.java', ['Compiled:', 'exit 0'])
            ചിട്ടപ്പെടുത്തല്_മൂല്യം('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            ഷെല്('javac Broken.java', ['javac error:', 'exit 1'])
            അപ്_ലോഡ്_ഫയലുകൾ('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            ഷെല്('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            ഷെല്('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            അപ്_ലോഡ്_ഫയലുകൾ('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            ഷെല്('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            ഷെല്('rm Imported.class', [])
            ചിട്ടപ്പെടുത്തല്_മൂല്യം('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            ഷെല്('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = ഷെല്('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            ഷെല്('rm Loop.java', []); ഷെല്('rm Loop.class', [])
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
            ചിട്ടപ്പെടുത്തല്_മൂല്യം('checks.py', 파이썬검사)
            ഷെല്('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            ഷെല്('rm checks.py', [])
            ചിട്ടപ്പെടുത്തല്_മൂല്യം('helper.py', 'value = 321')
            ഷെല്("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            ഷെല്('rm helper.py', [])
            ഷെല്("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            ഷെല്("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                ഷെല്('python hello.py', ['한글 ഫയല്', 'exit 0'])
                ഷെല്('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            അപ്_ലോഡ്_ഫയലുകൾ('app.elf', (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/user/demo.elf').read_bytes())
            assert ഡൗൺലോഡ്('app.elf') == (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/user/demo.elf').read_bytes()
            ഷെല്('run app.elf', ['EL0 C++', 'exit 0'])
            അപ്_ലോഡ്_ഫയലുകൾ('app.elf', b'not an ELF')
            ഷെല്('run app.elf', ['exit -8'])
            ഷെല്('rm app.elf', [])
            ഷെല്('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            ഡ്രോയിംഗ്_പാത = 출력결과 / 'java-framebuffer'; ഡ്രോയിംഗ്_പാത.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'dist/jkoros-native-korean.jar'), '-d', str(ഡ്രോയിംഗ്_പാത), str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / '시험/자바/화면시험.java')])
            അപ്_ലോഡ്_ഫയലുകൾ('화면시험.class', (ഡ്രോയിംഗ്_പാത / '화면시험.class').read_bytes())
            ഷെല്('java 화면시험', ['화면 ക്ലിപ്പ് നിരസിക്കുക_മൂല്യം', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            ഷെല്('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as ക്ലയന്_റ്:
                ക്ലയന്_റ്.settimeout(10)
                ക്ലയന്_റ്.connect(str(모의제어경로))
                with ക്ലയന്_റ്.makefile('rwb') as സ്ട്രീം_മൂല്യം:
                    인사 = json.loads(സ്ട്രീം_മൂല്യം.readline())
                    def 모의제어접속(പ്രവര്_ത്തിപ്പിയ്ക്കുക, 전달인수=None):
                        നെറ്റ്_വർക്ക്_ഇമെയിൽ = {'execute': പ്രവര്_ത്തിപ്പിയ്ക്കുക}
                        if 전달인수: നെറ്റ്_വർക്ക്_ഇമെയിൽ['arguments'] = 전달인수
                        സ്ട്രീം_മൂല്യം.write((json.dumps(നെറ്റ്_വർക്ക്_ഇമെയിൽ) + '\n').encode())
                        സ്ട്രീം_മൂല്യം.flush()
                        while True:
                            മറുപടി_നൽകുക = json.loads(സ്ട്രീം_മൂല്യം.readline())
                            if 'error' in മറുപടി_നൽകുക: raise AssertionError(മറുപടി_നൽകുക)
                            if 'return' in മറുപടി_നൽകുക: return മറുപടി_നൽകുക['return']
                    모의제어접속('qmp_capabilities')
                    സ്ക്രീൻഷോട്ട് = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(സ്ക്രീൻഷോട്ട്), 'format': 'ppm'})
                    def 예제들(വഴി, 지점들):
                        with വഴി.open('rb') as പെല്_ഫയല്:
                            assert പെല്_ഫയല്.readline().strip() == b'P6'
                            assert പെല്_ഫയല്.readline().strip() == b'640 480'
                            assert പെല്_ഫയല്.readline().strip() == b'255'
                            പെല്_ഡാറ്റാ = പെല്_ഫയല്.read()
                        assert len(പെല്_ഡാറ്റാ) == 640 * 480 * 3
                        return [list(പെല്_ഡാറ്റാ[(Y_ബട്ടൺ_ഏകോപനം * 640 + x_ഏകോപനം) * 3:(Y_ബട്ടൺ_ഏകോപനം * 640 + x_ഏകോപനം) * 3 + 3]) for x_ഏകോപനം, Y_ബട്ടൺ_ഏകോപനം in 지점들]
                    assert 예제들(സ്ക്രീൻഷോട്ട്, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(സ്ക്രീൻഷോട്ട്, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def അയയ്ക്കുക(누름값, 확인표시):
                        ഓഫ്_സെറ്റ്_മൂല്യം = len(대화기록)
                        പ്രക്രിയ.stdin.write(누름값); പ്രക്രിയ.stdin.flush()
                        표시까지받기(확인표시, ഓഫ്_സെറ്റ്_മൂല്യം)
                    അയയ്ക്കുക(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    അയയ്ക്കുക(b'\r', b'GUI ACTION 0 RESULT 0')
                    അയയ്ക്കുക(b'\t', b'GUI FOCUS 1')
                    അയയ്ക്കുക(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    അയയ്ക്കുക(b'\t', b'GUI FOCUS 2')
                    അയയ്ക്കുക(b'\r', b'GUI ACTION 2 RESULT 0')
                    അയയ്ക്കുക(b'\t', b'GUI FOCUS 3')
                    അയയ്ക്കുക(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    അയയ്ക്കുക(b'q', b'jkoros-native> ')
                    నిర్ధారణ_నివేదిక['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            പ്രക്രിയ.wait(timeout=10)
            # framebuffer 응답뿐 아니라 വാസ്തവമായ_ഡാറ്റാ scanout 픽셀도 확인한다.
            with സ്ക്രീൻഷോട്ട്.open('rb') as ഫയല്_എന്_ട്രി:
                assert ഫയല്_എന്_ട്രി.readline().strip() == b'P6'
                치수 = ഫയല്_എന്_ട്രി.readline().strip()
                assert 치수 == b'640 480', 치수
                assert ഫയല്_എന്_ട്രി.readline().strip() == b'255'
                화소들 = ഫയല്_എന്_ട്രി.read()
            assert len(화소들) == 640 * 480 * 3
            def പെല്(x_ഏകോപനം, Y_ബട്ടൺ_ഏകോപനം): return list(화소들[(Y_ബട്ടൺ_ഏകോപനം * 640 + x_ഏകോപനം) * 3:(Y_ബട്ടൺ_ഏകോപനം * 640 + x_ഏകോപനം) * 3 + 3])
            예제들 = {'background': പെല്(5, 5), 'panel': പെല്(45, 85), 'tile': പെല്(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            నిర్ధారణ_నివేదిక.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if പ്രക്രിയ.poll() is None:
                പ്രക്രിയ.terminate()
                try: പ്രക്രിയ.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    പ്രക്രിയ.kill(); പ്രക്രിയ.wait(timeout=5)
            సెలక్టర్.close()
            പ്രക്രിയ.stdin.close(); പ്രക്രിയ.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక, indent=2) + '\n')


if __name__ == '__main__':
    നടപ്പിലാക്കുക()
