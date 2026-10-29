#!/usr/bin/env python3
"""ପ୍ରକୃତ_ଡାଟା raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ import ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍, ନିର୍ଦ୍ଦେଶ


def ଚଳାନ୍ତୁ():
    출력결과 = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    ବୈଧକରଣ_ରିପୋର୍ଟ = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = ନିର୍ଦ୍ଦେଶ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        ବୈଧକରଣ_ରିପୋର୍ଟ['command'] = 명령인수
        ପ୍ରକ୍ରିୟା = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        ଚୟନକାରୀ = selectors.DefaultSelector()
        ଚୟନକାରୀ.register(ପ୍ରକ୍ରିୟା.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in ଚୟନକାରୀ.select(0.2):
                    ଡାଟା_ଅବରୋଧ_କରିବା = 누름값.fileobj.read(4096)
                    if ଡାଟା_ଅବରୋଧ_କରିବା:
                        대화기록.extend(ଡାଟା_ଅବରୋଧ_କରିବା)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if ପ୍ରକ୍ରିୟା.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(ପ୍ରକ୍ରିୟା.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 ପ୍ରକୃତ_ଡାଟା GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(ଆକାର):
                    ମାପ = b''
                    while len(ମାପ) < ଆକାର:
                        조각 = 화면접속자.recv(ଆକାର - len(ମାପ))
                        if not 조각: raise AssertionError('VNC disconnected')
                        ମାପ += 조각
                    return ମାପ
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                ସର୍ଭର୍_ମୂଲ୍ୟ = 정확한값(24)
                assert int.from_bytes(ସର୍ଭର୍_ମୂଲ୍ୟ[:2], 'big') == 640 and int.from_bytes(ସର୍ଭର୍_ମୂଲ୍ୟ[2:4], 'big') == 480
                정확한값(int.from_bytes(ସର୍ଭର୍_ମୂଲ୍ୟ[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for ନିର୍ଦ୍ଦେଶ_ବାଇଟ୍, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ = len(대화기록)
                ପ୍ରକ୍ରିୟା.stdin.write(ନିର୍ଦ୍ଦେଶ_ବାଇଟ୍ + b'\n')
                ପ୍ରକ୍ରିୟା.stdin.flush()
                표시까지받기(b'jkoros-native> ', ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ)
                assert 확인표시 in 대화기록[ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ:], 확인표시
            def ଖୋଳ(ରେଖା, 예상결과):
                ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ = len(대화기록)
                ପ୍ରକ୍ରିୟା.stdin.write(ରେଖା.encode('utf-8') + b'\n'); ପ୍ରକ୍ରିୟା.stdin.flush()
                표시까지받기(b'jkoros-native> ', ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ)
                응답자료 = bytes(대화기록[ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ:])
                for ପାଠ୍ଯ in 예상결과:
                    assert ପାଠ୍ଯ.encode('utf-8') in 응답자료, (ରେଖା, ପାଠ୍ଯ, 응답자료)
                return 응답자료
            def ଏଣ୍ଟର୍_କରନ୍ତୁ(ରେଖା, ତୁରନ୍ତ):
                ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ = len(대화기록)
                ପ୍ରକ୍ରିୟା.stdin.write(ରେଖା.encode('utf-8') + b'\n'); ପ୍ରକ୍ରିୟା.stdin.flush()
                표시까지받기(ତୁରନ୍ତ, ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ)
                return bytes(대화기록[ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ:])
            def ସଂପାଦନା_ମୂଲ୍ୟ(ନାମ, ବିଷୟ_ମୂଲ୍ୟ, ବାତିଲ୍_ସଂଚାଳନ=False):
                ଏଣ୍ଟର୍_କରନ୍ତୁ('edit ' + ନାମ, b'edit> ')
                for ରେଖା in ବିଷୟ_ମୂଲ୍ୟ.splitlines(): ଏଣ୍ଟର୍_କରନ୍ତୁ(ରେଖା, b'edit> ')
                if ବାତିଲ୍_ସଂଚାଳନ:
                    ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ = len(대화기록)
                    ପ୍ରକ୍ରିୟା.stdin.write(b'\x03'); ପ୍ରକ୍ରିୟା.stdin.flush()
                    표시까지받기(b'jkoros-native> ', ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ)
                    assert b'EDIT CANCELLED' in 대화기록[ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ:]
                else:
                    assert b'SAVED' in ଏଣ୍ଟର୍_କରନ୍ତୁ('.', b'jkoros-native> ')
            def ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ(ନାମ, ଡାଟା):
                assert len(ଡାଟା) <= 16384
                ଏଣ୍ଟର୍_କରନ୍ତୁ('load ' + ନାମ, b'hex> ')
                for 순번 in range(0, len(ଡାଟା), 64): ଏଣ୍ଟର୍_କରନ୍ତୁ(ଡାଟା[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in ଏଣ୍ଟର୍_କରନ୍ତୁ('.', b'jkoros-native> ')
            def ଡାଉନ୍_ଲୋଡ଼(ନାମ):
                응답자료 = ଖୋଳ('hex ' + ନାମ, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                ଡାଟା = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(ଡାଟା) == int(일치.group(1)); return ଡାଟା
            ଖୋଳ('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            ଖୋଳ('java -version', ['not OpenJDK', 'exit 0'])
            ଖୋଳ('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            ଖୋଳ('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            ଖୋଳ('python --version', ['MicroPython 1.24.1', 'exit 0'])
            ଖୋଳ('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 ଫାଇଲ', 'exit 0'])
            ଖୋଳ('cat python.txt', ['한글 ଫାଇଲ'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(ଡାଉନ୍_ଲୋଡ଼('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            ସଂପାଦନା_ମୂଲ୍ୟ('인사.java', 'public class 인사 { public static void main(String[] args) { int ମୂଲ୍ୟ = 7; System.out.println("한글=" + ମୂଲ୍ୟ); } }')
            ଖୋଳ('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            ଖୋଳ('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(ଡାଉନ୍_ଲୋଡ଼('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            ସଂପାଦନା_ମୂଲ୍ୟ('Hello.java', 'broken', ବାତିଲ୍_ସଂଚାଳନ=True)
            ଖୋଳ('javac Hello.java', ['Compiled:', 'exit 0'])
            ସଂପାଦନା_ମୂଲ୍ୟ('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            ଖୋଳ('javac Broken.java', ['javac error:', 'exit 1'])
            ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            ଖୋଳ('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            ଖୋଳ('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            ଖୋଳ('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            ଖୋଳ('rm Imported.class', [])
            ସଂପାଦନା_ମୂଲ୍ୟ('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            ଖୋଳ('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = ଖୋଳ('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            ଖୋଳ('rm Loop.java', []); ଖୋଳ('rm Loop.class', [])
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
            ସଂପାଦନା_ମୂଲ୍ୟ('checks.py', 파이썬검사)
            ଖୋଳ('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            ଖୋଳ('rm checks.py', [])
            ସଂପାଦନା_ମୂଲ୍ୟ('helper.py', 'value = 321')
            ଖୋଳ("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            ଖୋଳ('rm helper.py', [])
            ଖୋଳ("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            ଖୋଳ("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                ଖୋଳ('python hello.py', ['한글 ଫାଇଲ', 'exit 0'])
                ଖୋଳ('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ('app.elf', (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/user/demo.elf').read_bytes())
            assert ଡାଉନ୍_ଲୋଡ଼('app.elf') == (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/user/demo.elf').read_bytes()
            ଖୋଳ('run app.elf', ['EL0 C++', 'exit 0'])
            ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ('app.elf', b'not an ELF')
            ଖୋଳ('run app.elf', ['exit -8'])
            ଖୋଳ('rm app.elf', [])
            ଖୋଳ('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            ଅଙ୍କନ_ପଥ = 출력결과 / 'java-framebuffer'; ଅଙ୍କନ_ପଥ.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'dist/jkoros-native-korean.jar'), '-d', str(ଅଙ୍କନ_ପଥ), str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / '시험/자바/화면시험.java')])
            ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ('화면시험.class', (ଅଙ୍କନ_ପଥ / '화면시험.class').read_bytes())
            ଖୋଳ('java 화면시험', ['화면 କ୍ଲିପ୍ ପ୍ରତ୍ୟାକ୍ଷାନ_ମୂଲ୍ୟ', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            ଖୋଳ('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as କ୍ଲାଏଣ୍ଟ:
                କ୍ଲାଏଣ୍ଟ.settimeout(10)
                କ୍ଲାଏଣ୍ଟ.connect(str(모의제어경로))
                with କ୍ଲାଏଣ୍ଟ.makefile('rwb') as ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ:
                    인사 = json.loads(ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.readline())
                    def 모의제어접속(ନିଷ୍ପାଦନ_କରନ୍ତୁ, 전달인수=None):
                        ନେଟ୍_ୱାର୍କ୍_ବାର୍ତ୍ତା = {'execute': ନିଷ୍ପାଦନ_କରନ୍ତୁ}
                        if 전달인수: ନେଟ୍_ୱାର୍କ୍_ବାର୍ତ୍ତା['arguments'] = 전달인수
                        ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.write((json.dumps(ନେଟ୍_ୱାର୍କ୍_ବାର୍ତ୍ତା) + '\n').encode())
                        ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.flush()
                        while True:
                            ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ = json.loads(ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.readline())
                            if 'error' in ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ: raise AssertionError(ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ)
                            if 'return' in ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ: return ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ['return']
                    모의제어접속('qmp_capabilities')
                    ସ୍କ୍ରିନ୍_କ୍ଲିପିଂ = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(ସ୍କ୍ରିନ୍_କ୍ଲିପିଂ), 'format': 'ppm'})
                    def 예제들(ପଥ, 지점들):
                        with ପଥ.open('rb') as ପିକ୍ସେଲ୍_ଫାଇଲ୍:
                            assert ପିକ୍ସେଲ୍_ଫାଇଲ୍.readline().strip() == b'P6'
                            assert ପିକ୍ସେଲ୍_ଫାଇଲ୍.readline().strip() == b'640 480'
                            assert ପିକ୍ସେଲ୍_ଫାଇଲ୍.readline().strip() == b'255'
                            ପିକ୍ସେଲ୍_ଡାଟା = ପିକ୍ସେଲ୍_ଫାଇଲ୍.read()
                        assert len(ପିକ୍ସେଲ୍_ଡାଟା) == 640 * 480 * 3
                        return [list(ପିକ୍ସେଲ୍_ଡାଟା[(세로좌표 * 640 + x_ସଂଯୋଜନ) * 3:(세로좌표 * 640 + x_ସଂଯୋଜନ) * 3 + 3]) for x_ସଂଯୋଜନ, 세로좌표 in 지점들]
                    assert 예제들(ସ୍କ୍ରିନ୍_କ୍ଲିପିଂ, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(ସ୍କ୍ରିନ୍_କ୍ଲିପିଂ, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def ପଠାନ୍ତୁ(누름값, 확인표시):
                        ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ = len(대화기록)
                        ପ୍ରକ୍ରିୟା.stdin.write(누름값); ପ୍ରକ୍ରିୟା.stdin.flush()
                        표시까지받기(확인표시, ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ)
                    ପଠାନ୍ତୁ(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    ପଠାନ୍ତୁ(b'\r', b'GUI ACTION 0 RESULT 0')
                    ପଠାନ୍ତୁ(b'\t', b'GUI FOCUS 1')
                    ପଠାନ୍ତୁ(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    ପଠାନ୍ତୁ(b'\t', b'GUI FOCUS 2')
                    ପଠାନ୍ତୁ(b'\r', b'GUI ACTION 2 RESULT 0')
                    ପଠାନ୍ତୁ(b'\t', b'GUI FOCUS 3')
                    ପଠାନ୍ତୁ(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    ପଠାନ୍ତୁ(b'q', b'jkoros-native> ')
                    ବୈଧକରଣ_ରିପୋର୍ଟ['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            ପ୍ରକ୍ରିୟା.wait(timeout=10)
            # framebuffer 응답뿐 아니라 ପ୍ରକୃତ_ଡାଟା scanout 픽셀도 확인한다.
            with ସ୍କ୍ରିନ୍_କ୍ଲିପିଂ.open('rb') as ଫାଇଲ୍_ଏଣ୍ଟ୍ରି:
                assert ଫାଇଲ୍_ଏଣ୍ଟ୍ରି.readline().strip() == b'P6'
                치수 = ଫାଇଲ୍_ଏଣ୍ଟ୍ରି.readline().strip()
                assert 치수 == b'640 480', 치수
                assert ଫାଇଲ୍_ଏଣ୍ଟ୍ରି.readline().strip() == b'255'
                화소들 = ଫାଇଲ୍_ଏଣ୍ଟ୍ରି.read()
            assert len(화소들) == 640 * 480 * 3
            def ପିକ୍ସେଲ୍(x_ସଂଯୋଜନ, 세로좌표): return list(화소들[(세로좌표 * 640 + x_ସଂଯୋଜନ) * 3:(세로좌표 * 640 + x_ସଂଯୋଜନ) * 3 + 3])
            예제들 = {'background': ପିକ୍ସେଲ୍(5, 5), 'panel': ପିକ୍ସେଲ୍(45, 85), 'tile': ପିକ୍ସେଲ୍(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            ବୈଧକରଣ_ରିପୋର୍ଟ.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if ପ୍ରକ୍ରିୟା.poll() is None:
                ପ୍ରକ୍ରିୟା.terminate()
                try: ପ୍ରକ୍ରିୟା.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    ପ୍ରକ୍ରିୟା.kill(); ପ୍ରକ୍ରିୟା.wait(timeout=5)
            ଚୟନକାରୀ.close()
            ପ୍ରକ୍ରିୟା.stdin.close(); ପ୍ରକ୍ରିୟା.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(ବୈଧକରଣ_ରିପୋର୍ଟ, indent=2) + '\n')


if __name__ == '__main__':
    ଚଳାନ୍ତୁ()
