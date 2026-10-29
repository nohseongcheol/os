#!/usr/bin/env python3
"""ትክክለኛ_ውሂብ raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from ፈጽም_ትእዛዝ import አሳይ_ስር, ትእዛዝ


def ማስኬጃ():
    출력결과 = አሳይ_ስር / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    ማረጋገጥ_ዘገባ = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = ትእዛዝ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        ማረጋገጥ_ዘገባ['command'] = 명령인수
        ሂደቶች = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        መራጭ = selectors.DefaultSelector()
        መራጭ.register(ሂደቶች.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, ዝንፍ_እሴት=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[ዝንፍ_እሴት:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in መራጭ.select(0.2):
                    ውሂብ_አግድ = 누름값.fileobj.read(4096)
                    if ውሂብ_አግድ:
                        대화기록.extend(ውሂብ_አግድ)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if ሂደቶች.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(ሂደቶች.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 ትክክለኛ_ውሂብ GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(መጠን):
                    ልኬት = b''
                    while len(ልኬት) < መጠን:
                        조각 = 화면접속자.recv(መጠን - len(ልኬት))
                        if not 조각: raise AssertionError('VNC disconnected')
                        ልኬት += 조각
                    return ልኬት
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                አገልጋይ_እሴት = 정확한값(24)
                assert int.from_bytes(አገልጋይ_እሴት[:2], 'big') == 640 and int.from_bytes(አገልጋይ_እሴት[2:4], 'big') == 480
                정확한값(int.from_bytes(አገልጋይ_እሴት[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for ትእዛዝ_ባይት, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                ዝንፍ_እሴት = len(대화기록)
                ሂደቶች.stdin.write(ትእዛዝ_ባይት + b'\n')
                ሂደቶች.stdin.flush()
                표시까지받기(b'jkoros-native> ', ዝንፍ_እሴት)
                assert 확인표시 in 대화기록[ዝንፍ_እሴት:], 확인표시
            def ሼል(መስመር, 예상결과):
                ዝንፍ_እሴት = len(대화기록)
                ሂደቶች.stdin.write(መስመር.encode('utf-8') + b'\n'); ሂደቶች.stdin.flush()
                표시까지받기(b'jkoros-native> ', ዝንፍ_እሴት)
                응답자료 = bytes(대화기록[ዝንፍ_እሴት:])
                for ጽሁፍ in 예상결과:
                    assert ጽሁፍ.encode('utf-8') in 응답자료, (መስመር, ጽሁፍ, 응답자료)
                return 응답자료
            def አስገባ_851ea840(መስመር, ጥሪ):
                ዝንፍ_እሴት = len(대화기록)
                ሂደቶች.stdin.write(መስመር.encode('utf-8') + b'\n'); ሂደቶች.stdin.flush()
                표시까지받기(ጥሪ, ዝንፍ_እሴት)
                return bytes(대화기록[ዝንፍ_እሴት:])
            def አርትዕ_እሴት(ስም, ይዘት_እሴት, ሰርዝ_ክወና=False):
                አስገባ_851ea840('edit ' + ስም, b'edit> ')
                for መስመር in ይዘት_እሴት.splitlines(): አስገባ_851ea840(መስመር, b'edit> ')
                if ሰርዝ_ክወና:
                    ዝንፍ_እሴት = len(대화기록)
                    ሂደቶች.stdin.write(b'\x03'); ሂደቶች.stdin.flush()
                    표시까지받기(b'jkoros-native> ', ዝንፍ_እሴት)
                    assert b'EDIT CANCELLED' in 대화기록[ዝንፍ_እሴት:]
                else:
                    assert b'SAVED' in አስገባ_851ea840('.', b'jkoros-native> ')
            def መጫን_ፋይሎች(ስም, ውሂብ):
                assert len(ውሂብ) <= 16384
                አስገባ_851ea840('load ' + ስም, b'hex> ')
                for 순번 in range(0, len(ውሂብ), 64): አስገባ_851ea840(ውሂብ[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in አስገባ_851ea840('.', b'jkoros-native> ')
            def ወራጅ(ስም):
                응답자료 = ሼል('hex ' + ስም, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                ውሂብ = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(ውሂብ) == int(일치.group(1)); return ውሂብ
            ሼል('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            ሼል('java -version', ['not OpenJDK', 'exit 0'])
            ሼል('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            ሼል('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            ሼል('python --version', ['MicroPython 1.24.1', 'exit 0'])
            ሼል('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 ፋይል', 'exit 0'])
            ሼል('cat python.txt', ['한글 ፋይል'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(ወራጅ('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            አርትዕ_እሴት('인사.java', 'public class 인사 { public static void main(String[] args) { int እሴት = 7; System.out.println("한글=" + እሴት); } }')
            ሼል('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            ሼል('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(ወራጅ('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            አርትዕ_እሴት('Hello.java', 'broken', ሰርዝ_ክወና=True)
            ሼል('javac Hello.java', ['Compiled:', 'exit 0'])
            አርትዕ_እሴት('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            ሼል('javac Broken.java', ['javac error:', 'exit 1'])
            መጫን_ፋይሎች('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            ሼል('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            ሼል('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            መጫን_ፋይሎች('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            ሼል('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            ሼል('rm Imported.class', [])
            አርትዕ_እሴት('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            ሼል('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = ሼል('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            ሼል('rm Loop.java', []); ሼል('rm Loop.class', [])
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
            አርትዕ_እሴት('checks.py', 파이썬검사)
            ሼል('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            ሼል('rm checks.py', [])
            አርትዕ_እሴት('helper.py', 'value = 321')
            ሼል("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            ሼል('rm helper.py', [])
            ሼል("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            ሼል("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                ሼል('python hello.py', ['한글 ፋይል', 'exit 0'])
                ሼል('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            መጫን_ፋይሎች('app.elf', (አሳይ_ስር / 'build/user/demo.elf').read_bytes())
            assert ወራጅ('app.elf') == (አሳይ_ስር / 'build/user/demo.elf').read_bytes()
            ሼል('run app.elf', ['EL0 C++', 'exit 0'])
            መጫን_ፋይሎች('app.elf', b'not an ELF')
            ሼል('run app.elf', ['exit -8'])
            ሼል('rm app.elf', [])
            ሼል('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            ስዕል_ዱካ = 출력결과 / 'java-framebuffer'; ስዕል_ዱካ.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(አሳይ_ስር / 'dist/jkoros-native-korean.jar'), '-d', str(ስዕል_ዱካ), str(አሳይ_ስር / '시험/자바/화면시험.java')])
            መጫን_ፋይሎች('화면시험.class', (ስዕል_ዱካ / '화면시험.class').read_bytes())
            ሼል('java 화면시험', ['화면 ቅንጥብ አትቀበል_እሴት', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            ሼል('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as ተገልጋይ:
                ተገልጋይ.settimeout(10)
                ተገልጋይ.connect(str(모의제어경로))
                with ተገልጋይ.makefile('rwb') as ልቀቅ_እሴት:
                    인사 = json.loads(ልቀቅ_እሴት.readline())
                    def 모의제어접속(መፈጸሚያ, 전달인수=None):
                        መረብ_ኢሜይል = {'execute': መፈጸሚያ}
                        if 전달인수: መረብ_ኢሜይል['arguments'] = 전달인수
                        ልቀቅ_እሴት.write((json.dumps(መረብ_ኢሜይል) + '\n').encode())
                        ልቀቅ_እሴት.flush()
                        while True:
                            መልስ = json.loads(ልቀቅ_እሴት.readline())
                            if 'error' in መልስ: raise AssertionError(መልስ)
                            if 'return' in መልስ: return መልስ['return']
                    모의제어접속('qmp_capabilities')
                    ማያ_ቅንጠባ = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(ማያ_ቅንጠባ), 'format': 'ppm'})
                    def 예제들(መተላለፊያ, 지점들):
                        with መተላለፊያ.open('rb') as ፒክስል_ፋይል:
                            assert ፒክስል_ፋይል.readline().strip() == b'P6'
                            assert ፒክስል_ፋይል.readline().strip() == b'640 480'
                            assert ፒክስል_ፋይል.readline().strip() == b'255'
                            ፒክስል_ውሂብ = ፒክስል_ፋይል.read()
                        assert len(ፒክስል_ውሂብ) == 640 * 480 * 3
                        return [list(ፒክስል_ውሂብ[(세로좌표 * 640 + ኤክስ_አስተባባሪ) * 3:(세로좌표 * 640 + ኤክስ_አስተባባሪ) * 3 + 3]) for ኤክስ_አስተባባሪ, 세로좌표 in 지점들]
                    assert 예제들(ማያ_ቅንጠባ, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(ማያ_ቅንጠባ, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def ላክ(누름값, 확인표시):
                        ዝንፍ_እሴት = len(대화기록)
                        ሂደቶች.stdin.write(누름값); ሂደቶች.stdin.flush()
                        표시까지받기(확인표시, ዝንፍ_እሴት)
                    ላክ(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    ላክ(b'\r', b'GUI ACTION 0 RESULT 0')
                    ላክ(b'\t', b'GUI FOCUS 1')
                    ላክ(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    ላክ(b'\t', b'GUI FOCUS 2')
                    ላክ(b'\r', b'GUI ACTION 2 RESULT 0')
                    ላክ(b'\t', b'GUI FOCUS 3')
                    ላክ(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    ላክ(b'q', b'jkoros-native> ')
                    ማረጋገጥ_ዘገባ['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            ሂደቶች.wait(timeout=10)
            # framebuffer 응답뿐 아니라 ትክክለኛ_ውሂብ scanout 픽셀도 확인한다.
            with ማያ_ቅንጠባ.open('rb') as ፋይል_ምዝግብ:
                assert ፋይል_ምዝግብ.readline().strip() == b'P6'
                치수 = ፋይል_ምዝግብ.readline().strip()
                assert 치수 == b'640 480', 치수
                assert ፋይል_ምዝግብ.readline().strip() == b'255'
                화소들 = ፋይል_ምዝግብ.read()
            assert len(화소들) == 640 * 480 * 3
            def ፒክስል(ኤክስ_አስተባባሪ, 세로좌표): return list(화소들[(세로좌표 * 640 + ኤክስ_አስተባባሪ) * 3:(세로좌표 * 640 + ኤክስ_አስተባባሪ) * 3 + 3])
            예제들 = {'background': ፒክስል(5, 5), 'panel': ፒክስል(45, 85), 'tile': ፒክስል(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            ማረጋገጥ_ዘገባ.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((አሳይ_ስር / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if ሂደቶች.poll() is None:
                ሂደቶች.terminate()
                try: ሂደቶች.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    ሂደቶች.kill(); ሂደቶች.wait(timeout=5)
            መራጭ.close()
            ሂደቶች.stdin.close(); ሂደቶች.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(ማረጋገጥ_ዘገባ, indent=2) + '\n')


if __name__ == '__main__':
    ማስኬጃ()
