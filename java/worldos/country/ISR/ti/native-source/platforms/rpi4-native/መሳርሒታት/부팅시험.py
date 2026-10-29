#!/usr/bin/env python3
"""ትኽክለኛ_ሓበሬታ raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from ተግብር_ትእዛዝ import 기준, ትእዛዝ


def ኣኺድ():
    출력결과 = 기준 / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    ምርግጋፅ_ጸብጻብ = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = ትእዛዝ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        ምርግጋፅ_ጸብጻብ['command'] = 명령인수
        መስርሕ = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        መራፂ = selectors.DefaultSelector()
        መራፂ.register(መስርሕ.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, ሽፋን_ዋጋ=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[ሽፋን_ዋጋ:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in መራፂ.select(0.2):
                    ሓበሬታ_ምዕጋት = 누름값.fileobj.read(4096)
                    if ሓበሬታ_ምዕጋት:
                        대화기록.extend(ሓበሬታ_ምዕጋት)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if መስርሕ.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(መስርሕ.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 ትኽክለኛ_ሓበሬታ GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(መጠን):
                    결과 = b''
                    while len(결과) < መጠን:
                        조각 = 화면접속자.recv(መጠን - len(결과))
                        if not 조각: raise AssertionError('VNC disconnected')
                        결과 += 조각
                    return 결과
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                ኣገልጋሊ_ዋጋ = 정확한값(24)
                assert int.from_bytes(ኣገልጋሊ_ዋጋ[:2], 'big') == 640 and int.from_bytes(ኣገልጋሊ_ዋጋ[2:4], 'big') == 480
                정확한값(int.from_bytes(ኣገልጋሊ_ዋጋ[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for ትእዛዝ_ባይት, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                ሽፋን_ዋጋ = len(대화기록)
                መስርሕ.stdin.write(ትእዛዝ_ባይት + b'\n')
                መስርሕ.stdin.flush()
                표시까지받기(b'jkoros-native> ', ሽፋን_ዋጋ)
                assert 확인표시 in 대화기록[ሽፋን_ዋጋ:], 확인표시
            def ሽፋን(መስመር, 예상결과):
                ሽፋን_ዋጋ = len(대화기록)
                መስርሕ.stdin.write(መስመር.encode('utf-8') + b'\n'); መስርሕ.stdin.flush()
                표시까지받기(b'jkoros-native> ', ሽፋን_ዋጋ)
                응답자료 = bytes(대화기록[ሽፋን_ዋጋ:])
                for ጽሑፍ in 예상결과:
                    assert ጽሑፍ.encode('utf-8') in 응답자료, (መስመር, ጽሑፍ, 응답자료)
                return 응답자료
            def የእትው_851ea840(መስመር, ናይ_ቀጽል_ምልክት):
                ሽፋን_ዋጋ = len(대화기록)
                መስርሕ.stdin.write(መስመር.encode('utf-8') + b'\n'); መስርሕ.stdin.flush()
                표시까지받기(ናይ_ቀጽል_ምልክት, ሽፋን_ዋጋ)
                return bytes(대화기록[ሽፋን_ዋጋ:])
            def ምዕራይ_ዋጋ(ሽም, ትሕዝቶ_ዋጋ, ግደፍ_ስርሒት=False):
                የእትው_851ea840('edit ' + ሽም, b'edit> ')
                for መስመር in ትሕዝቶ_ዋጋ.splitlines(): የእትው_851ea840(መስመር, b'edit> ')
                if ግደፍ_ስርሒት:
                    ሽፋን_ዋጋ = len(대화기록)
                    መስርሕ.stdin.write(b'\x03'); መስርሕ.stdin.flush()
                    표시까지받기(b'jkoros-native> ', ሽፋን_ዋጋ)
                    assert b'EDIT CANCELLED' in 대화기록[ሽፋን_ዋጋ:]
                else:
                    assert b'SAVED' in የእትው_851ea840('.', b'jkoros-native> ')
            def ስቐል_ፋይላት(ሽም, ሓበሬታ):
                assert len(ሓበሬታ) <= 16384
                የእትው_851ea840('load ' + ሽም, b'hex> ')
                for 순번 in range(0, len(ሓበሬታ), 64): የእትው_851ea840(ሓበሬታ[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in የእትው_851ea840('.', b'jkoros-native> ')
            def ምውራድ(ሽም):
                응답자료 = ሽፋን('hex ' + ሽም, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                ሓበሬታ = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(ሓበሬታ) == int(일치.group(1)); return ሓበሬታ
            ሽፋን('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            ሽፋን('java -version', ['not OpenJDK', 'exit 0'])
            ሽፋን('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            ሽፋን('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            ሽፋን('python --version', ['MicroPython 1.24.1', 'exit 0'])
            ሽፋን('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 ፋይል', 'exit 0'])
            ሽፋን('cat python.txt', ['한글 ፋይል'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(ምውራድ('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            ምዕራይ_ዋጋ('인사.java', 'public class 인사 { public static void main(String[] args) { int ዋጋ = 7; System.out.println("한글=" + ዋጋ); } }')
            ሽፋን('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            ሽፋን('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(ምውራድ('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            ምዕራይ_ዋጋ('Hello.java', 'broken', ግደፍ_ስርሒት=True)
            ሽፋን('javac Hello.java', ['Compiled:', 'exit 0'])
            ምዕራይ_ዋጋ('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            ሽፋን('javac Broken.java', ['javac error:', 'exit 1'])
            ስቐል_ፋይላት('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            ሽፋን('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            ሽፋን('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            ስቐል_ፋይላት('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            ሽፋን('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            ሽፋን('rm Imported.class', [])
            ምዕራይ_ዋጋ('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            ሽፋን('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = ሽፋን('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            ሽፋን('rm Loop.java', []); ሽፋን('rm Loop.class', [])
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
            ምዕራይ_ዋጋ('checks.py', 파이썬검사)
            ሽፋን('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            ሽፋን('rm checks.py', [])
            ምዕራይ_ዋጋ('helper.py', 'value = 321')
            ሽፋን("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            ሽፋን('rm helper.py', [])
            ሽፋን("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            ሽፋን("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                ሽፋን('python hello.py', ['한글 ፋይል', 'exit 0'])
                ሽፋን('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            ስቐል_ፋይላት('app.elf', (기준 / 'build/user/demo.elf').read_bytes())
            assert ምውራድ('app.elf') == (기준 / 'build/user/demo.elf').read_bytes()
            ሽፋን('run app.elf', ['EL0 C++', 'exit 0'])
            ስቐል_ፋይላት('app.elf', b'not an ELF')
            ሽፋን('run app.elf', ['exit -8'])
            ሽፋን('rm app.elf', [])
            ሽፋን('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            ስእሊ_መገዲ = 출력결과 / 'java-framebuffer'; ስእሊ_መገዲ.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준 / 'dist/jkoros-native-korean.jar'), '-d', str(ስእሊ_መገዲ), str(기준 / '시험/자바/화면시험.java')])
            ስቐል_ፋይላት('화면시험.class', (ስእሊ_መገዲ / '화면시험.class').read_bytes())
            ሽፋን('java 화면시험', ['화면 ቅንጣብ 거부', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            ሽፋን('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as ዓሚል:
                ዓሚል.settimeout(10)
                ዓሚል.connect(str(모의제어경로))
                with ዓሚል.makefile('rwb') as ወሓዚ_ዋጋ:
                    인사 = json.loads(ወሓዚ_ዋጋ.readline())
                    def 모의제어접속(ተግብር_ዕማም, 전달인수=None):
                        ማሕበራዊ_ኔትወርክ_መልእኽቲ = {'execute': ተግብር_ዕማም}
                        if 전달인수: ማሕበራዊ_ኔትወርክ_መልእኽቲ['arguments'] = 전달인수
                        ወሓዚ_ዋጋ.write((json.dumps(ማሕበራዊ_ኔትወርክ_መልእኽቲ) + '\n').encode())
                        ወሓዚ_ዋጋ.flush()
                        while True:
                            መልስ = json.loads(ወሓዚ_ዋጋ.readline())
                            if 'error' in መልስ: raise AssertionError(መልስ)
                            if 'return' in መልስ: return መልስ['return']
                    모의제어접속('qmp_capabilities')
                    ምንፃል_መርዓዪ = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(ምንፃል_መርዓዪ), 'format': 'ppm'})
                    def 예제들(መገዲ, 지점들):
                        with መገዲ.open('rb') as ንጣብ_ፋይል:
                            assert ንጣብ_ፋይል.readline().strip() == b'P6'
                            assert ንጣብ_ፋይል.readline().strip() == b'640 480'
                            assert ንጣብ_ፋይል.readline().strip() == b'255'
                            ንጣብ_ሓበሬታ = ንጣብ_ፋይል.read()
                        assert len(ንጣብ_ሓበሬታ) == 640 * 480 * 3
                        return [list(ንጣብ_ሓበሬታ[(세로좌표 * 640 + 가로좌표) * 3:(세로좌표 * 640 + 가로좌표) * 3 + 3]) for 가로좌표, 세로좌표 in 지점들]
                    assert 예제들(ምንፃል_መርዓዪ, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(ምንፃል_መርዓዪ, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def ለኣኽ(누름값, 확인표시):
                        ሽፋን_ዋጋ = len(대화기록)
                        መስርሕ.stdin.write(누름값); መስርሕ.stdin.flush()
                        표시까지받기(확인표시, ሽፋን_ዋጋ)
                    ለኣኽ(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    ለኣኽ(b'\r', b'GUI ACTION 0 RESULT 0')
                    ለኣኽ(b'\t', b'GUI FOCUS 1')
                    ለኣኽ(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    ለኣኽ(b'\t', b'GUI FOCUS 2')
                    ለኣኽ(b'\r', b'GUI ACTION 2 RESULT 0')
                    ለኣኽ(b'\t', b'GUI FOCUS 3')
                    ለኣኽ(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    ለኣኽ(b'q', b'jkoros-native> ')
                    ምርግጋፅ_ጸብጻብ['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            መስርሕ.wait(timeout=10)
            # framebuffer 응답뿐 아니라 ትኽክለኛ_ሓበሬታ scanout 픽셀도 확인한다.
            with ምንፃል_መርዓዪ.open('rb') as ፋይል_ምእታው:
                assert ፋይል_ምእታው.readline().strip() == b'P6'
                치수 = ፋይል_ምእታው.readline().strip()
                assert 치수 == b'640 480', 치수
                assert ፋይል_ምእታው.readline().strip() == b'255'
                화소들 = ፋይል_ምእታው.read()
            assert len(화소들) == 640 * 480 * 3
            def ንጣብ(가로좌표, 세로좌표): return list(화소들[(세로좌표 * 640 + 가로좌표) * 3:(세로좌표 * 640 + 가로좌표) * 3 + 3])
            예제들 = {'background': ንጣብ(5, 5), 'panel': ንጣብ(45, 85), 'tile': ንጣብ(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            ምርግጋፅ_ጸብጻብ.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
            if መስርሕ.poll() is None:
                መስርሕ.terminate()
                try: መስርሕ.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    መስርሕ.kill(); መስርሕ.wait(timeout=5)
            መራፂ.close()
            መስርሕ.stdin.close(); መስርሕ.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(ምርግጋፅ_ጸብጻብ, indent=2) + '\n')


if __name__ == '__main__':
    ኣኺድ()
