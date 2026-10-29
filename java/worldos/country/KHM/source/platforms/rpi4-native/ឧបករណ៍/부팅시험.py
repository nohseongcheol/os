#!/usr/bin/env python3
"""ដែលពិត_ទិន្នន័យ raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from អនុវត្ត_ពាក្យបញ្ជា import បញ្ចាំង_ឬស, ពាក្យ_បញ្ជា


def រត់():
    출력결과 = បញ្ចាំង_ឬស / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    សុពលភាព_រាយការណ៍ = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = ពាក្យ_បញ្ជា() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        សុពលភាព_រាយការណ៍['command'] = 명령인수
        ដំណើរការ = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        អ្នកជ្រើសរើស = selectors.DefaultSelector()
        អ្នកជ្រើសរើស.register(ដំណើរការ.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, ការបែង_ភាគ_តំលៃ=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[ការបែង_ភាគ_តំលៃ:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in អ្នកជ្រើសរើស.select(0.2):
                    ទិន្នន័យ_ប្លុក = 누름값.fileobj.read(4096)
                    if ទិន្នន័យ_ប្លុក:
                        대화기록.extend(ទិន្នន័យ_ប្លុក)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if ដំណើរការ.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(ដំណើរការ.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 ដែលពិត_ទិន្នន័យ GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(ដាក់ទំហំ):
                    ការវាស់វែង = b''
                    while len(ការវាស់វែង) < ដាក់ទំហំ:
                        조각 = 화면접속자.recv(ដាក់ទំហំ - len(ការវាស់វែង))
                        if not 조각: raise AssertionError('VNC disconnected')
                        ការវាស់វែង += 조각
                    return ការវាស់វែង
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                ម៉ាស៊ីនមេ_តំលៃ = 정확한값(24)
                assert int.from_bytes(ម៉ាស៊ីនមេ_តំលៃ[:2], 'big') == 640 and int.from_bytes(ម៉ាស៊ីនមេ_តំលៃ[2:4], 'big') == 480
                정확한값(int.from_bytes(ម៉ាស៊ីនមេ_តំលៃ[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for ពាក្យបញ្ជា_បៃ, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                ការបែង_ភាគ_តំលៃ = len(대화기록)
                ដំណើរការ.stdin.write(ពាក្យបញ្ជា_បៃ + b'\n')
                ដំណើរការ.stdin.flush()
                표시까지받기(b'jkoros-native> ', ការបែង_ភាគ_តំលៃ)
                assert 확인표시 in 대화기록[ការបែង_ភាគ_តំលៃ:], 확인표시
            def 셸(បន្ទាត់, 예상결과):
                ការបែង_ភាគ_តំលៃ = len(대화기록)
                ដំណើរការ.stdin.write(បន្ទាត់.encode('utf-8') + b'\n'); ដំណើរការ.stdin.flush()
                표시까지받기(b'jkoros-native> ', ការបែង_ភាគ_តំលៃ)
                응답자료 = bytes(대화기록[ការបែង_ភាគ_តំលៃ:])
                for អត្ថបទ in 예상결과:
                    assert អត្ថបទ.encode('utf-8') in 응답자료, (បន្ទាត់, អត្ថបទ, 응답자료)
                return 응답자료
            def បញ្ចូល_851ea840(បន្ទាត់, រហ័ស):
                ការបែង_ភាគ_តំលៃ = len(대화기록)
                ដំណើរការ.stdin.write(បន្ទាត់.encode('utf-8') + b'\n'); ដំណើរការ.stdin.flush()
                표시까지받기(រហ័ស, ការបែង_ភាគ_តំលៃ)
                return bytes(대화기록[ការបែង_ភាគ_តំលៃ:])
            def កែសម្រួល_តំលៃ(ឈ្មោះ, មាតិកា_តំលៃ, បោះបង់_ការវះកាត់=False):
                បញ្ចូល_851ea840('edit ' + ឈ្មោះ, b'edit> ')
                for បន្ទាត់ in មាតិកា_តំលៃ.splitlines(): បញ្ចូល_851ea840(បន្ទាត់, b'edit> ')
                if បោះបង់_ការវះកាត់:
                    ការបែង_ភាគ_តំលៃ = len(대화기록)
                    ដំណើរការ.stdin.write(b'\x03'); ដំណើរការ.stdin.flush()
                    표시까지받기(b'jkoros-native> ', ការបែង_ភាគ_តំលៃ)
                    assert b'EDIT CANCELLED' in 대화기록[ការបែង_ភាគ_តំលៃ:]
                else:
                    assert b'SAVED' in បញ្ចូល_851ea840('.', b'jkoros-native> ')
            def បង្ហោះ_ឯកសារ(ឈ្មោះ, ទិន្នន័យ):
                assert len(ទិន្នន័យ) <= 16384
                បញ្ចូល_851ea840('load ' + ឈ្មោះ, b'hex> ')
                for 순번 in range(0, len(ទិន្នន័យ), 64): បញ្ចូល_851ea840(ទិន្នន័យ[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in បញ្ចូល_851ea840('.', b'jkoros-native> ')
            def ទាញយក(ឈ្មោះ):
                응답자료 = 셸('hex ' + ឈ្មោះ, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                ទិន្នន័យ = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(ទិន្នន័យ) == int(일치.group(1)); return ទិន្នន័យ
            셸('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            셸('java -version', ['not OpenJDK', 'exit 0'])
            셸('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            셸('java Hello "한글 អាគុយម៉ង់ 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 អាគុយម៉ង់ 😀', 'exit 0'])
            셸('python --version', ['MicroPython 1.24.1', 'exit 0'])
            셸('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 ឯកសារ', 'exit 0'])
            셸('cat python.txt', ['한글 ឯកសារ'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(ទាញយក('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 អាគុយម៉ង់ 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 អាគុយម៉ង់ 😀'], 예상결과
            កែសម្រួល_តំលៃ('인사.java', 'public class 인사 { public static void main(String[] args) { int តំលៃ = 7; System.out.println("한글=" + តំលៃ); } }')
            셸('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            셸('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(ទាញយក('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            កែសម្រួល_តំលៃ('Hello.java', 'broken', បោះបង់_ការវះកាត់=True)
            셸('javac Hello.java', ['Compiled:', 'exit 0'])
            កែសម្រួល_តំលៃ('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            셸('javac Broken.java', ['javac error:', 'exit 1'])
            បង្ហោះ_ឯកសារ('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            셸('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            셸('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            បង្ហោះ_ឯកសារ('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            셸('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            셸('rm Imported.class', [])
            កែសម្រួល_តំលៃ('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            셸('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = 셸('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            셸('rm Loop.java', []); 셸('rm Loop.class', [])
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
            កែសម្រួល_តំលៃ('checks.py', 파이썬검사)
            셸('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            셸('rm checks.py', [])
            កែសម្រួល_តំលៃ('helper.py', 'value = 321')
            셸("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            셸('rm helper.py', [])
            셸("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            셸("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                셸('python hello.py', ['한글 ឯកសារ', 'exit 0'])
                셸('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            បង្ហោះ_ឯកសារ('app.elf', (បញ្ចាំង_ឬស / 'build/user/demo.elf').read_bytes())
            assert ទាញយក('app.elf') == (បញ្ចាំង_ឬស / 'build/user/demo.elf').read_bytes()
            셸('run app.elf', ['EL0 C++', 'exit 0'])
            បង្ហោះ_ឯកសារ('app.elf', b'not an ELF')
            셸('run app.elf', ['exit -8'])
            셸('rm app.elf', [])
            셸('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            ការគូរ_ផ្លូវ = 출력결과 / 'java-framebuffer'; ការគូរ_ផ្លូវ.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(បញ្ចាំង_ឬស / 'dist/jkoros-native-korean.jar'), '-d', str(ការគូរ_ផ្លូវ), str(បញ្ចាំង_ឬស / '시험/자바/화면시험.java')])
            បង្ហោះ_ឯកសារ('화면시험.class', (ការគូរ_ផ្លូវ / '화면시험.class').read_bytes())
            셸('java 화면시험', ['화면 មេឌៀខ្លីៗ បដិសេធ_តំលៃ', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            셸('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as អតិថិជន:
                អតិថិជន.settimeout(10)
                អតិថិជន.connect(str(모의제어경로))
                with អតិថិជន.makefile('rwb') as ស្ទ្រីម_តំលៃ:
                    인사 = json.loads(ស្ទ្រីម_តំលៃ.readline())
                    def 모의제어접속(ប្រតិបត្តិ, 전달인수=None):
                        ណិតវឺក_សារ = {'execute': ប្រតិបត្តិ}
                        if 전달인수: ណិតវឺក_សារ['arguments'] = 전달인수
                        ស្ទ្រីម_តំលៃ.write((json.dumps(ណិតវឺក_សារ) + '\n').encode())
                        ស្ទ្រីម_តំលៃ.flush()
                        while True:
                            ឆ្លើយតប = json.loads(ស្ទ្រីម_តំលៃ.readline())
                            if 'error' in ឆ្លើយតប: raise AssertionError(ឆ្លើយតប)
                            if 'return' in ឆ្លើយតប: return ឆ្លើយតប['return']
                    모의제어접속('qmp_capabilities')
                    រូបថតអេក្រង់ = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(រូបថតអេក្រង់), 'format': 'ppm'})
                    def 예제들(ផ្លូវ, 지점들):
                        with ផ្លូវ.open('rb') as ចំនុចតូចៗ_ឯកសារ:
                            assert ចំនុចតូចៗ_ឯកសារ.readline().strip() == b'P6'
                            assert ចំនុចតូចៗ_ឯកសារ.readline().strip() == b'640 480'
                            assert ចំនុចតូចៗ_ឯកសារ.readline().strip() == b'255'
                            ចំនុចតូចៗ_ទិន្នន័យ = ចំនុចតូចៗ_ឯកសារ.read()
                        assert len(ចំនុចតូចៗ_ទិន្នន័យ) == 640 * 480 * 3
                        return [list(ចំនុចតូចៗ_ទិន្នន័យ[(ប៊ូតុង_Y_កូអរដោនេ * 640 + កូអរដោណេ_x) * 3:(ប៊ូតុង_Y_កូអរដោនេ * 640 + កូអរដោណេ_x) * 3 + 3]) for កូអរដោណេ_x, ប៊ូតុង_Y_កូអរដោនេ in 지점들]
                    assert 예제들(រូបថតអេក្រង់, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(រូបថតអេក្រង់, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def ផ្ញើ(누름값, 확인표시):
                        ការបែង_ភាគ_តំលៃ = len(대화기록)
                        ដំណើរការ.stdin.write(누름값); ដំណើរការ.stdin.flush()
                        표시까지받기(확인표시, ការបែង_ភាគ_តំលៃ)
                    ផ្ញើ(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    ផ្ញើ(b'\r', b'GUI ACTION 0 RESULT 0')
                    ផ្ញើ(b'\t', b'GUI FOCUS 1')
                    ផ្ញើ(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    ផ្ញើ(b'\t', b'GUI FOCUS 2')
                    ផ្ញើ(b'\r', b'GUI ACTION 2 RESULT 0')
                    ផ្ញើ(b'\t', b'GUI FOCUS 3')
                    ផ្ញើ(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    ផ្ញើ(b'q', b'jkoros-native> ')
                    សុពលភាព_រាយការណ៍['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            ដំណើរការ.wait(timeout=10)
            # framebuffer 응답뿐 아니라 ដែលពិត_ទិន្នន័យ scanout 픽셀도 확인한다.
            with រូបថតអេក្រង់.open('rb') as ឯកសារ_ការបញ្ចូល:
                assert ឯកសារ_ការបញ្ចូល.readline().strip() == b'P6'
                치수 = ឯកសារ_ការបញ្ចូល.readline().strip()
                assert 치수 == b'640 480', 치수
                assert ឯកសារ_ការបញ្ចូល.readline().strip() == b'255'
                화소들 = ឯកសារ_ការបញ្ចូល.read()
            assert len(화소들) == 640 * 480 * 3
            def ចំនុចតូចៗ(កូអរដោណេ_x, ប៊ូតុង_Y_កូអរដោនេ): return list(화소들[(ប៊ូតុង_Y_កូអរដោនេ * 640 + កូអរដោណេ_x) * 3:(ប៊ូតុង_Y_កូអរដោនេ * 640 + កូអរដោណេ_x) * 3 + 3])
            예제들 = {'background': ចំនុចតូចៗ(5, 5), 'panel': ចំនុចតូចៗ(45, 85), 'tile': ចំនុចតូចៗ(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            សុពលភាព_រាយការណ៍.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((បញ្ចាំង_ឬស / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if ដំណើរការ.poll() is None:
                ដំណើរការ.terminate()
                try: ដំណើរការ.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    ដំណើរការ.kill(); ដំណើរការ.wait(timeout=5)
            អ្នកជ្រើសរើស.close()
            ដំណើរការ.stdin.close(); ដំណើរការ.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(សុពលភាព_រាយការណ៍, indent=2) + '\n')


if __name__ == '__main__':
    រត់()
