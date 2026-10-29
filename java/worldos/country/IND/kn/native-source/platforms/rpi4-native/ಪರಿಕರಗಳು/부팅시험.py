#!/usr/bin/env python3
"""ನಿಜವಾದ_ಡೇಟಾ raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from ಪೂರೈಸು_ಆದೇಶ import ಬಿಂಬಿಸು_ಮೂಲ, ಆಜ್ಞೆ


def ಚಲಾಯಿಸು_2():
    출력결과 = ಬಿಂಬಿಸು_ಮೂಲ / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    ದೃಢೀಕರಣ_ವರದಿ = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = ಆಜ್ಞೆ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        ದೃಢೀಕರಣ_ವರದಿ['command'] = 명령인수
        ಪ್ರಕ್ರಿಯೆ = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        ಸೆಲೆಕ್ಟರ್ = selectors.DefaultSelector()
        ಸೆಲೆಕ್ಟರ್.register(ಪ್ರಕ್ರಿಯೆ.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in ಸೆಲೆಕ್ಟರ್.select(0.2):
                    ಡೇಟಾ_ನಿರ್ಬಂಧಿಸು = 누름값.fileobj.read(4096)
                    if ಡೇಟಾ_ನಿರ್ಬಂಧಿಸು:
                        대화기록.extend(ಡೇಟಾ_ನಿರ್ಬಂಧಿಸು)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if ಪ್ರಕ್ರಿಯೆ.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(ಪ್ರಕ್ರಿಯೆ.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 ನಿಜವಾದ_ಡೇಟಾ GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(ಗಾತ್ರ):
                    ಮಾಪನ = b''
                    while len(ಮಾಪನ) < ಗಾತ್ರ:
                        조각 = 화면접속자.recv(ಗಾತ್ರ - len(ಮಾಪನ))
                        if not 조각: raise AssertionError('VNC disconnected')
                        ಮಾಪನ += 조각
                    return ಮಾಪನ
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                ಸರ್ವರ್_ಮೌಲ್ಯ = 정확한값(24)
                assert int.from_bytes(ಸರ್ವರ್_ಮೌಲ್ಯ[:2], 'big') == 640 and int.from_bytes(ಸರ್ವರ್_ಮೌಲ್ಯ[2:4], 'big') == 480
                정확한값(int.from_bytes(ಸರ್ವರ್_ಮೌಲ್ಯ[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for ಆದೇಶ_ಬೈಟ್, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ = len(대화기록)
                ಪ್ರಕ್ರಿಯೆ.stdin.write(ಆದೇಶ_ಬೈಟ್ + b'\n')
                ಪ್ರಕ್ರಿಯೆ.stdin.flush()
                표시까지받기(b'jkoros-native> ', ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
                assert 확인표시 in 대화기록[ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ:], 확인표시
            def ಶೆಲ್(ಸಾಲು, 예상결과):
                ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ = len(대화기록)
                ಪ್ರಕ್ರಿಯೆ.stdin.write(ಸಾಲು.encode('utf-8') + b'\n'); ಪ್ರಕ್ರಿಯೆ.stdin.flush()
                표시까지받기(b'jkoros-native> ', ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
                응답자료 = bytes(대화기록[ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ:])
                for ಪಠ್ಯ in 예상결과:
                    assert ಪಠ್ಯ.encode('utf-8') in 응답자료, (ಸಾಲು, ಪಠ್ಯ, 응답자료)
                return 응답자료
            def ನಮೂದಿಸು(ಸಾಲು, ಪ್ರಾಂಪ್ಟ್):
                ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ = len(대화기록)
                ಪ್ರಕ್ರಿಯೆ.stdin.write(ಸಾಲು.encode('utf-8') + b'\n'); ಪ್ರಕ್ರಿಯೆ.stdin.flush()
                표시까지받기(ಪ್ರಾಂಪ್ಟ್, ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
                return bytes(대화기록[ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ:])
            def ಸಂಪಾದನೆ_ಮೌಲ್ಯ(ಹೆಸರು, ವಿಷಯ_ಮೌಲ್ಯ, ರದ್ದು_ಆಪರೇಶನ್=False):
                ನಮೂದಿಸು('edit ' + ಹೆಸರು, b'edit> ')
                for ಸಾಲು in ವಿಷಯ_ಮೌಲ್ಯ.splitlines(): ನಮೂದಿಸು(ಸಾಲು, b'edit> ')
                if ರದ್ದು_ಆಪರೇಶನ್:
                    ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ = len(대화기록)
                    ಪ್ರಕ್ರಿಯೆ.stdin.write(b'\x03'); ಪ್ರಕ್ರಿಯೆ.stdin.flush()
                    표시까지받기(b'jkoros-native> ', ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
                    assert b'EDIT CANCELLED' in 대화기록[ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ:]
                else:
                    assert b'SAVED' in ನಮೂದಿಸು('.', b'jkoros-native> ')
            def ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು(ಹೆಸರು, ಡೇಟಾ):
                assert len(ಡೇಟಾ) <= 16384
                ನಮೂದಿಸು('load ' + ಹೆಸರು, b'hex> ')
                for 순번 in range(0, len(ಡೇಟಾ), 64): ನಮೂದಿಸು(ಡೇಟಾ[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in ನಮೂದಿಸು('.', b'jkoros-native> ')
            def ಡೌನ್_ಲೋಡ್(ಹೆಸರು):
                응답자료 = ಶೆಲ್('hex ' + ಹೆಸರು, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                ಡೇಟಾ = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(ಡೇಟಾ) == int(일치.group(1)); return ಡೇಟಾ
            ಶೆಲ್('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            ಶೆಲ್('java -version', ['not OpenJDK', 'exit 0'])
            ಶೆಲ್('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            ಶೆಲ್('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            ಶೆಲ್('python --version', ['MicroPython 1.24.1', 'exit 0'])
            ಶೆಲ್('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 ಕಡತ', 'exit 0'])
            ಶೆಲ್('cat python.txt', ['한글 ಕಡತ'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(ಡೌನ್_ಲೋಡ್('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            ಸಂಪಾದನೆ_ಮೌಲ್ಯ('인사.java', 'public class 인사 { public static void main(String[] args) { int ಮೌಲ್ಯ = 7; System.out.println("한글=" + ಮೌಲ್ಯ); } }')
            ಶೆಲ್('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            ಶೆಲ್('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(ಡೌನ್_ಲೋಡ್('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            ಸಂಪಾದನೆ_ಮೌಲ್ಯ('Hello.java', 'broken', ರದ್ದು_ಆಪರೇಶನ್=True)
            ಶೆಲ್('javac Hello.java', ['Compiled:', 'exit 0'])
            ಸಂಪಾದನೆ_ಮೌಲ್ಯ('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            ಶೆಲ್('javac Broken.java', ['javac error:', 'exit 1'])
            ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            ಶೆಲ್('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            ಶೆಲ್('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            ಶೆಲ್('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            ಶೆಲ್('rm Imported.class', [])
            ಸಂಪಾದನೆ_ಮೌಲ್ಯ('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            ಶೆಲ್('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = ಶೆಲ್('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            ಶೆಲ್('rm Loop.java', []); ಶೆಲ್('rm Loop.class', [])
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
            ಸಂಪಾದನೆ_ಮೌಲ್ಯ('checks.py', 파이썬검사)
            ಶೆಲ್('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            ಶೆಲ್('rm checks.py', [])
            ಸಂಪಾದನೆ_ಮೌಲ್ಯ('helper.py', 'value = 321')
            ಶೆಲ್("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            ಶೆಲ್('rm helper.py', [])
            ಶೆಲ್("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            ಶೆಲ್("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                ಶೆಲ್('python hello.py', ['한글 ಕಡತ', 'exit 0'])
                ಶೆಲ್('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು('app.elf', (ಬಿಂಬಿಸು_ಮೂಲ / 'build/user/demo.elf').read_bytes())
            assert ಡೌನ್_ಲೋಡ್('app.elf') == (ಬಿಂಬಿಸು_ಮೂಲ / 'build/user/demo.elf').read_bytes()
            ಶೆಲ್('run app.elf', ['EL0 C++', 'exit 0'])
            ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು('app.elf', b'not an ELF')
            ಶೆಲ್('run app.elf', ['exit -8'])
            ಶೆಲ್('rm app.elf', [])
            ಶೆಲ್('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            ಚಿತ್ರರಚನೆ_ಹಾದಿ = 출력결과 / 'java-framebuffer'; ಚಿತ್ರರಚನೆ_ಹಾದಿ.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(ಬಿಂಬಿಸು_ಮೂಲ / 'dist/jkoros-native-korean.jar'), '-d', str(ಚಿತ್ರರಚನೆ_ಹಾದಿ), str(ಬಿಂಬಿಸು_ಮೂಲ / '시험/자바/화면시험.java')])
            ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು('화면시험.class', (ಚಿತ್ರರಚನೆ_ಹಾದಿ / '화면시험.class').read_bytes())
            ಶೆಲ್('java 화면시험', ['화면 ಕ್ಲಿಪ್ ನಿರಾಕರಿಸು_ಮೌಲ್ಯ', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            ಶೆಲ್('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as ಕ್ಲೈಂಟ್:
                ಕ್ಲೈಂಟ್.settimeout(10)
                ಕ್ಲೈಂಟ್.connect(str(모의제어경로))
                with ಕ್ಲೈಂಟ್.makefile('rwb') as ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ:
                    인사 = json.loads(ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.readline())
                    def 모의제어접속(ಚಲಾಯಿಸು, 전달인수=None):
                        ನೆಟ್_ವರ್ಕ್_ಇಮೇಲ್ = {'execute': ಚಲಾಯಿಸು}
                        if 전달인수: ನೆಟ್_ವರ್ಕ್_ಇಮೇಲ್['arguments'] = 전달인수
                        ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.write((json.dumps(ನೆಟ್_ವರ್ಕ್_ಇಮೇಲ್) + '\n').encode())
                        ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.flush()
                        while True:
                            ಪ್ರತ್ಯುತ್ತರ = json.loads(ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.readline())
                            if 'error' in ಪ್ರತ್ಯುತ್ತರ: raise AssertionError(ಪ್ರತ್ಯುತ್ತರ)
                            if 'return' in ಪ್ರತ್ಯುತ್ತರ: return ಪ್ರತ್ಯುತ್ತರ['return']
                    모의제어접속('qmp_capabilities')
                    ಸ್ಕ್ರೀನ್_ಶಾಟ್ = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(ಸ್ಕ್ರೀನ್_ಶಾಟ್), 'format': 'ppm'})
                    def 예제들(ಮಾರ್ಗ, 지점들):
                        with ಮಾರ್ಗ.open('rb') as ಪೆಲ್_ಫೈಲ್:
                            assert ಪೆಲ್_ಫೈಲ್.readline().strip() == b'P6'
                            assert ಪೆಲ್_ಫೈಲ್.readline().strip() == b'640 480'
                            assert ಪೆಲ್_ಫೈಲ್.readline().strip() == b'255'
                            ಪೆಲ್_ಡೇಟಾ = ಪೆಲ್_ಫೈಲ್.read()
                        assert len(ಪೆಲ್_ಡೇಟಾ) == 640 * 480 * 3
                        return [list(ಪೆಲ್_ಡೇಟಾ[(Y_ಬಟನ್_ಸಮನ್ವಯ * 640 + x_ಸಮಭಾಜಕ) * 3:(Y_ಬಟನ್_ಸಮನ್ವಯ * 640 + x_ಸಮಭಾಜಕ) * 3 + 3]) for x_ಸಮಭಾಜಕ, Y_ಬಟನ್_ಸಮನ್ವಯ in 지점들]
                    assert 예제들(ಸ್ಕ್ರೀನ್_ಶಾಟ್, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(ಸ್ಕ್ರೀನ್_ಶಾಟ್, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def ಕಳುಹಿಸಿ(누름값, 확인표시):
                        ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ = len(대화기록)
                        ಪ್ರಕ್ರಿಯೆ.stdin.write(누름값); ಪ್ರಕ್ರಿಯೆ.stdin.flush()
                        표시까지받기(확인표시, ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
                    ಕಳುಹಿಸಿ(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    ಕಳುಹಿಸಿ(b'\r', b'GUI ACTION 0 RESULT 0')
                    ಕಳುಹಿಸಿ(b'\t', b'GUI FOCUS 1')
                    ಕಳುಹಿಸಿ(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    ಕಳುಹಿಸಿ(b'\t', b'GUI FOCUS 2')
                    ಕಳುಹಿಸಿ(b'\r', b'GUI ACTION 2 RESULT 0')
                    ಕಳುಹಿಸಿ(b'\t', b'GUI FOCUS 3')
                    ಕಳುಹಿಸಿ(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    ಕಳುಹಿಸಿ(b'q', b'jkoros-native> ')
                    ದೃಢೀಕರಣ_ವರದಿ['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            ಪ್ರಕ್ರಿಯೆ.wait(timeout=10)
            # framebuffer 응답뿐 아니라 ನಿಜವಾದ_ಡೇಟಾ scanout 픽셀도 확인한다.
            with ಸ್ಕ್ರೀನ್_ಶಾಟ್.open('rb') as ಫೈಲ್_ನಮೂದು:
                assert ಫೈಲ್_ನಮೂದು.readline().strip() == b'P6'
                치수 = ಫೈಲ್_ನಮೂದು.readline().strip()
                assert 치수 == b'640 480', 치수
                assert ಫೈಲ್_ನಮೂದು.readline().strip() == b'255'
                화소들 = ಫೈಲ್_ನಮೂದು.read()
            assert len(화소들) == 640 * 480 * 3
            def ಪೆಲ್(x_ಸಮಭಾಜಕ, Y_ಬಟನ್_ಸಮನ್ವಯ): return list(화소들[(Y_ಬಟನ್_ಸಮನ್ವಯ * 640 + x_ಸಮಭಾಜಕ) * 3:(Y_ಬಟನ್_ಸಮನ್ವಯ * 640 + x_ಸಮಭಾಜಕ) * 3 + 3])
            예제들 = {'background': ಪೆಲ್(5, 5), 'panel': ಪೆಲ್(45, 85), 'tile': ಪೆಲ್(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            ದೃಢೀಕರಣ_ವರದಿ.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((ಬಿಂಬಿಸು_ಮೂಲ / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if ಪ್ರಕ್ರಿಯೆ.poll() is None:
                ಪ್ರಕ್ರಿಯೆ.terminate()
                try: ಪ್ರಕ್ರಿಯೆ.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    ಪ್ರಕ್ರಿಯೆ.kill(); ಪ್ರಕ್ರಿಯೆ.wait(timeout=5)
            ಸೆಲೆಕ್ಟರ್.close()
            ಪ್ರಕ್ರಿಯೆ.stdin.close(); ಪ್ರಕ್ರಿಯೆ.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(ದೃಢೀಕರಣ_ವರದಿ, indent=2) + '\n')


if __name__ == '__main__':
    ಚಲಾಯಿಸು_2()
