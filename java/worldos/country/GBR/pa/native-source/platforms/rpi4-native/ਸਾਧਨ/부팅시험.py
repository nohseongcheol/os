#!/usr/bin/env python3
"""ਅਸਲ_ਸਮੱਗਰੀ raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ import ਪ੍ਰੋਜੈਕਟ_ਰੂਟ, ਕਮਾਂਡ


def ਚਲਾਓ_2():
    출력결과 = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    ਮਾਨਤਾ_ਵਿਵਰਨ = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = ਕਮਾਂਡ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        ਮਾਨਤਾ_ਵਿਵਰਨ['command'] = 명령인수
        ਪਰੋਸੈੱਸ = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        ਚੋਣਕਰਤਾ = selectors.DefaultSelector()
        ਚੋਣਕਰਤਾ.register(ਪਰੋਸੈੱਸ.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, ਔਫਸੈਟ_ਕੀਮਤ=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[ਔਫਸੈਟ_ਕੀਮਤ:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in ਚੋਣਕਰਤਾ.select(0.2):
                    ਸਮੱਗਰੀ_ਬਲੌਕ_ਕਰੋ = 누름값.fileobj.read(4096)
                    if ਸਮੱਗਰੀ_ਬਲੌਕ_ਕਰੋ:
                        대화기록.extend(ਸਮੱਗਰੀ_ਬਲੌਕ_ਕਰੋ)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if ਪਰੋਸੈੱਸ.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(ਪਰੋਸੈੱਸ.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 ਅਸਲ_ਸਮੱਗਰੀ GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(ਆਕਾਰ):
                    ਮਾਪ = b''
                    while len(ਮਾਪ) < ਆਕਾਰ:
                        조각 = 화면접속자.recv(ਆਕਾਰ - len(ਮਾਪ))
                        if not 조각: raise AssertionError('VNC disconnected')
                        ਮਾਪ += 조각
                    return ਮਾਪ
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                ਸਰਵਰ_ਕੀਮਤ = 정확한값(24)
                assert int.from_bytes(ਸਰਵਰ_ਕੀਮਤ[:2], 'big') == 640 and int.from_bytes(ਸਰਵਰ_ਕੀਮਤ[2:4], 'big') == 480
                정확한값(int.from_bytes(ਸਰਵਰ_ਕੀਮਤ[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for ਆਦੇਸ਼_ਬਾਈਟ, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                ਔਫਸੈਟ_ਕੀਮਤ = len(대화기록)
                ਪਰੋਸੈੱਸ.stdin.write(ਆਦੇਸ਼_ਬਾਈਟ + b'\n')
                ਪਰੋਸੈੱਸ.stdin.flush()
                표시까지받기(b'jkoros-native> ', ਔਫਸੈਟ_ਕੀਮਤ)
                assert 확인표시 in 대화기록[ਔਫਸੈਟ_ਕੀਮਤ:], 확인표시
            def ਸ਼ੈਲ(ਲਾਈਨ, 예상결과):
                ਔਫਸੈਟ_ਕੀਮਤ = len(대화기록)
                ਪਰੋਸੈੱਸ.stdin.write(ਲਾਈਨ.encode('utf-8') + b'\n'); ਪਰੋਸੈੱਸ.stdin.flush()
                표시까지받기(b'jkoros-native> ', ਔਫਸੈਟ_ਕੀਮਤ)
                응답자료 = bytes(대화기록[ਔਫਸੈਟ_ਕੀਮਤ:])
                for ਟੈਕਸਟ in 예상결과:
                    assert ਟੈਕਸਟ.encode('utf-8') in 응답자료, (ਲਾਈਨ, ਟੈਕਸਟ, 응답자료)
                return 응답자료
            def ਦਾਖ਼ਲ_ਕਰੋ(ਲਾਈਨ, ਤਤਪਰ):
                ਔਫਸੈਟ_ਕੀਮਤ = len(대화기록)
                ਪਰੋਸੈੱਸ.stdin.write(ਲਾਈਨ.encode('utf-8') + b'\n'); ਪਰੋਸੈੱਸ.stdin.flush()
                표시까지받기(ਤਤਪਰ, ਔਫਸੈਟ_ਕੀਮਤ)
                return bytes(대화기록[ਔਫਸੈਟ_ਕੀਮਤ:])
            def ਸੰਪਾਦਨ_ਕੀਮਤ(ਨਾਂ, ਤਤਕਰਾ_ਕੀਮਤ, ਰੱਦ_ਕਰੋ_ਕਰਵਾਈ=False):
                ਦਾਖ਼ਲ_ਕਰੋ('edit ' + ਨਾਂ, b'edit> ')
                for ਲਾਈਨ in ਤਤਕਰਾ_ਕੀਮਤ.splitlines(): ਦਾਖ਼ਲ_ਕਰੋ(ਲਾਈਨ, b'edit> ')
                if ਰੱਦ_ਕਰੋ_ਕਰਵਾਈ:
                    ਔਫਸੈਟ_ਕੀਮਤ = len(대화기록)
                    ਪਰੋਸੈੱਸ.stdin.write(b'\x03'); ਪਰੋਸੈੱਸ.stdin.flush()
                    표시까지받기(b'jkoros-native> ', ਔਫਸੈਟ_ਕੀਮਤ)
                    assert b'EDIT CANCELLED' in 대화기록[ਔਫਸੈਟ_ਕੀਮਤ:]
                else:
                    assert b'SAVED' in ਦਾਖ਼ਲ_ਕਰੋ('.', b'jkoros-native> ')
            def ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ(ਨਾਂ, ਸਮੱਗਰੀ):
                assert len(ਸਮੱਗਰੀ) <= 16384
                ਦਾਖ਼ਲ_ਕਰੋ('load ' + ਨਾਂ, b'hex> ')
                for 순번 in range(0, len(ਸਮੱਗਰੀ), 64): ਦਾਖ਼ਲ_ਕਰੋ(ਸਮੱਗਰੀ[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in ਦਾਖ਼ਲ_ਕਰੋ('.', b'jkoros-native> ')
            def ਡਾਉਨਲਡ(ਨਾਂ):
                응답자료 = ਸ਼ੈਲ('hex ' + ਨਾਂ, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                ਸਮੱਗਰੀ = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(ਸਮੱਗਰੀ) == int(일치.group(1)); return ਸਮੱਗਰੀ
            ਸ਼ੈਲ('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            ਸ਼ੈਲ('java -version', ['not OpenJDK', 'exit 0'])
            ਸ਼ੈਲ('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            ਸ਼ੈਲ('java Hello "한글 ਆਰਗੂਮੈਂਟ 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 ਆਰਗੂਮੈਂਟ 😀', 'exit 0'])
            ਸ਼ੈਲ('python --version', ['MicroPython 1.24.1', 'exit 0'])
            ਸ਼ੈਲ('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 ਫਾਇਲ', 'exit 0'])
            ਸ਼ੈਲ('cat python.txt', ['한글 ਫਾਇਲ'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(ਡਾਉਨਲਡ('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 ਆਰਗੂਮੈਂਟ 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 ਆਰਗੂਮੈਂਟ 😀'], 예상결과
            ਸੰਪਾਦਨ_ਕੀਮਤ('인사.java', 'public class 인사 { public static void main(String[] args) { int ਕੀਮਤ = 7; System.out.println("한글=" + ਕੀਮਤ); } }')
            ਸ਼ੈਲ('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            ਸ਼ੈਲ('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(ਡਾਉਨਲਡ('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            ਸੰਪਾਦਨ_ਕੀਮਤ('Hello.java', 'broken', ਰੱਦ_ਕਰੋ_ਕਰਵਾਈ=True)
            ਸ਼ੈਲ('javac Hello.java', ['Compiled:', 'exit 0'])
            ਸੰਪਾਦਨ_ਕੀਮਤ('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            ਸ਼ੈਲ('javac Broken.java', ['javac error:', 'exit 1'])
            ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            ਸ਼ੈਲ('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            ਸ਼ੈਲ('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            ਸ਼ੈਲ('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            ਸ਼ੈਲ('rm Imported.class', [])
            ਸੰਪਾਦਨ_ਕੀਮਤ('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            ਸ਼ੈਲ('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = ਸ਼ੈਲ('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            ਸ਼ੈਲ('rm Loop.java', []); ਸ਼ੈਲ('rm Loop.class', [])
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
            ਸੰਪਾਦਨ_ਕੀਮਤ('checks.py', 파이썬검사)
            ਸ਼ੈਲ('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            ਸ਼ੈਲ('rm checks.py', [])
            ਸੰਪਾਦਨ_ਕੀਮਤ('helper.py', 'value = 321')
            ਸ਼ੈਲ("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            ਸ਼ੈਲ('rm helper.py', [])
            ਸ਼ੈਲ("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            ਸ਼ੈਲ("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                ਸ਼ੈਲ('python hello.py', ['한글 ਫਾਇਲ', 'exit 0'])
                ਸ਼ੈਲ('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ('app.elf', (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/user/demo.elf').read_bytes())
            assert ਡਾਉਨਲਡ('app.elf') == (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/user/demo.elf').read_bytes()
            ਸ਼ੈਲ('run app.elf', ['EL0 C++', 'exit 0'])
            ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ('app.elf', b'not an ELF')
            ਸ਼ੈਲ('run app.elf', ['exit -8'])
            ਸ਼ੈਲ('rm app.elf', [])
            ਸ਼ੈਲ('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਰਸਤਾ = 출력결과 / 'java-framebuffer'; ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਰਸਤਾ.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'dist/jkoros-native-korean.jar'), '-d', str(ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਰਸਤਾ), str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / '시험/자바/화면시험.java')])
            ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ('화면시험.class', (ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਰਸਤਾ / '화면시험.class').read_bytes())
            ਸ਼ੈਲ('java 화면시험', ['화면 ਕਲਿਪ 거부', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            ਸ਼ੈਲ('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as ਗਾਹਕ:
                ਗਾਹਕ.settimeout(10)
                ਗਾਹਕ.connect(str(모의제어경로))
                with ਗਾਹਕ.makefile('rwb') as ਸਟ੍ਰੀਮ_ਕੀਮਤ:
                    인사 = json.loads(ਸਟ੍ਰੀਮ_ਕੀਮਤ.readline())
                    def 모의제어접속(ਚਲਾਓ, 전달인수=None):
                        ਨੈਟਵਰਕ_ਸੁਨੇਹਾ = {'execute': ਚਲਾਓ}
                        if 전달인수: ਨੈਟਵਰਕ_ਸੁਨੇਹਾ['arguments'] = 전달인수
                        ਸਟ੍ਰੀਮ_ਕੀਮਤ.write((json.dumps(ਨੈਟਵਰਕ_ਸੁਨੇਹਾ) + '\n').encode())
                        ਸਟ੍ਰੀਮ_ਕੀਮਤ.flush()
                        while True:
                            ਜਵਾਬ_ਦਿਓ = json.loads(ਸਟ੍ਰੀਮ_ਕੀਮਤ.readline())
                            if 'error' in ਜਵਾਬ_ਦਿਓ: raise AssertionError(ਜਵਾਬ_ਦਿਓ)
                            if 'return' in ਜਵਾਬ_ਦਿਓ: return ਜਵਾਬ_ਦਿਓ['return']
                    모의제어접속('qmp_capabilities')
                    ਸਕ੍ਰੀਨ_ਕਲਿਪਿੰਗ = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(ਸਕ੍ਰੀਨ_ਕਲਿਪਿੰਗ), 'format': 'ppm'})
                    def 예제들(ਮਾਰਗ, 지점들):
                        with ਮਾਰਗ.open('rb') as ਬਿੰਦੂ_ਲਿਖਤ_ਪੱਤਰ:
                            assert ਬਿੰਦੂ_ਲਿਖਤ_ਪੱਤਰ.readline().strip() == b'P6'
                            assert ਬਿੰਦੂ_ਲਿਖਤ_ਪੱਤਰ.readline().strip() == b'640 480'
                            assert ਬਿੰਦੂ_ਲਿਖਤ_ਪੱਤਰ.readline().strip() == b'255'
                            ਬਿੰਦੂ_ਸਮੱਗਰੀ = ਬਿੰਦੂ_ਲਿਖਤ_ਪੱਤਰ.read()
                        assert len(ਬਿੰਦੂ_ਸਮੱਗਰੀ) == 640 * 480 * 3
                        return [list(ਬਿੰਦੂ_ਸਮੱਗਰੀ[(세로좌표 * 640 + x_ਕੌਔਰਡੀਨੇਟ) * 3:(세로좌표 * 640 + x_ਕੌਔਰਡੀਨੇਟ) * 3 + 3]) for x_ਕੌਔਰਡੀਨੇਟ, 세로좌표 in 지점들]
                    assert 예제들(ਸਕ੍ਰੀਨ_ਕਲਿਪਿੰਗ, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(ਸਕ੍ਰੀਨ_ਕਲਿਪਿੰਗ, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def ਈਮੇਲ(누름값, 확인표시):
                        ਔਫਸੈਟ_ਕੀਮਤ = len(대화기록)
                        ਪਰੋਸੈੱਸ.stdin.write(누름값); ਪਰੋਸੈੱਸ.stdin.flush()
                        표시까지받기(확인표시, ਔਫਸੈਟ_ਕੀਮਤ)
                    ਈਮੇਲ(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    ਈਮੇਲ(b'\r', b'GUI ACTION 0 RESULT 0')
                    ਈਮੇਲ(b'\t', b'GUI FOCUS 1')
                    ਈਮੇਲ(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    ਈਮੇਲ(b'\t', b'GUI FOCUS 2')
                    ਈਮੇਲ(b'\r', b'GUI ACTION 2 RESULT 0')
                    ਈਮੇਲ(b'\t', b'GUI FOCUS 3')
                    ਈਮੇਲ(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    ਈਮੇਲ(b'q', b'jkoros-native> ')
                    ਮਾਨਤਾ_ਵਿਵਰਨ['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            ਪਰੋਸੈੱਸ.wait(timeout=10)
            # framebuffer 응답뿐 아니라 ਅਸਲ_ਸਮੱਗਰੀ scanout 픽셀도 확인한다.
            with ਸਕ੍ਰੀਨ_ਕਲਿਪਿੰਗ.open('rb') as ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ:
                assert ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ.readline().strip() == b'P6'
                치수 = ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ.readline().strip()
                assert 치수 == b'640 480', 치수
                assert ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ.readline().strip() == b'255'
                화소들 = ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ.read()
            assert len(화소들) == 640 * 480 * 3
            def ਬਿੰਦੂ(x_ਕੌਔਰਡੀਨੇਟ, 세로좌표): return list(화소들[(세로좌표 * 640 + x_ਕੌਔਰਡੀਨੇਟ) * 3:(세로좌표 * 640 + x_ਕੌਔਰਡੀਨੇਟ) * 3 + 3])
            예제들 = {'background': ਬਿੰਦੂ(5, 5), 'panel': ਬਿੰਦੂ(45, 85), 'tile': ਬਿੰਦੂ(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            ਮਾਨਤਾ_ਵਿਵਰਨ.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if ਪਰੋਸੈੱਸ.poll() is None:
                ਪਰੋਸੈੱਸ.terminate()
                try: ਪਰੋਸੈੱਸ.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    ਪਰੋਸੈੱਸ.kill(); ਪਰੋਸੈੱਸ.wait(timeout=5)
            ਚੋਣਕਰਤਾ.close()
            ਪਰੋਸੈੱਸ.stdin.close(); ਪਰੋਸੈੱਸ.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(ਮਾਨਤਾ_ਵਿਵਰਨ, indent=2) + '\n')


if __name__ == '__main__':
    ਚਲਾਓ_2()
