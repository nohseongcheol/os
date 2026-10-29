#!/usr/bin/env python3
"""რეალური_მონაცემები raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from შესრულება_ბრძანება import პროეცირება_ფესვი, ბრძანება


def გაშვება():
    출력결과 = პროეცირება_ფესვი / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    გადამოწმება_ანგარიში = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = ბრძანება() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        გადამოწმება_ანგარიში['command'] = 명령인수
        პროცესი = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        სელექტორი = selectors.DefaultSelector()
        სელექტორი.register(პროცესი.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, ოფსეტი_მნიშვნელობა=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[ოფსეტი_მნიშვნელობა:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in სელექტორი.select(0.2):
                    მონაცემები_დაბლოკვა = 누름값.fileobj.read(4096)
                    if მონაცემები_დაბლოკვა:
                        대화기록.extend(მონაცემები_დაბლოკვა)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if პროცესი.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(პროცესი.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 რეალური_მონაცემები GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(ზომა):
                    გაზომვა = b''
                    while len(გაზომვა) < ზომა:
                        조각 = 화면접속자.recv(ზომა - len(გაზომვა))
                        if not 조각: raise AssertionError('VNC disconnected')
                        გაზომვა += 조각
                    return გაზომვა
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                სერვერი_მნიშვნელობა = 정확한값(24)
                assert int.from_bytes(სერვერი_მნიშვნელობა[:2], 'big') == 640 and int.from_bytes(სერვერი_მნიშვნელობა[2:4], 'big') == 480
                정확한값(int.from_bytes(სერვერი_მნიშვნელობა[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for ბრძანება_ბაიტი, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                ოფსეტი_მნიშვნელობა = len(대화기록)
                პროცესი.stdin.write(ბრძანება_ბაიტი + b'\n')
                პროცესი.stdin.flush()
                표시까지받기(b'jkoros-native> ', ოფსეტი_მნიშვნელობა)
                assert 확인표시 in 대화기록[ოფსეტი_მნიშვნელობა:], 확인표시
            def გარემო(ხაზი, 예상결과):
                ოფსეტი_მნიშვნელობა = len(대화기록)
                პროცესი.stdin.write(ხაზი.encode('utf-8') + b'\n'); პროცესი.stdin.flush()
                표시까지받기(b'jkoros-native> ', ოფსეტი_მნიშვნელობა)
                პასუხი_1262b476 = bytes(대화기록[ოფსეტი_მნიშვნელობა:])
                for ტექსტი in 예상결과:
                    assert ტექსტი.encode('utf-8') in პასუხი_1262b476, (ხაზი, ტექსტი, პასუხი_1262b476)
                return პასუხი_1262b476
            def შეყვანა(ხაზი, მოთხოვნა):
                ოფსეტი_მნიშვნელობა = len(대화기록)
                პროცესი.stdin.write(ხაზი.encode('utf-8') + b'\n'); პროცესი.stdin.flush()
                표시까지받기(მოთხოვნა, ოფსეტი_მნიშვნელობა)
                return bytes(대화기록[ოფსეტი_მნიშვნელობა:])
            def რედაქტირება_მნიშვნელობა(სახელი, შიგთავსი_მნიშვნელობა, გაუქმება_ოპერაცია=False):
                შეყვანა('edit ' + სახელი, b'edit> ')
                for ხაზი in შიგთავსი_მნიშვნელობა.splitlines(): შეყვანა(ხაზი, b'edit> ')
                if გაუქმება_ოპერაცია:
                    ოფსეტი_მნიშვნელობა = len(대화기록)
                    პროცესი.stdin.write(b'\x03'); პროცესი.stdin.flush()
                    표시까지받기(b'jkoros-native> ', ოფსეტი_მნიშვნელობა)
                    assert b'EDIT CANCELLED' in 대화기록[ოფსეტი_მნიშვნელობა:]
                else:
                    assert b'SAVED' in შეყვანა('.', b'jkoros-native> ')
            def ატვირთვა_ფაილები(სახელი, მონაცემები):
                assert len(მონაცემები) <= 16384
                შეყვანა('load ' + სახელი, b'hex> ')
                for 순번 in range(0, len(მონაცემები), 64): შეყვანა(მონაცემები[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in შეყვანა('.', b'jkoros-native> ')
            def ჩამოტვირთვა(სახელი):
                პასუხი_1262b476 = გარემო('hex ' + სახელი, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', პასუხი_1262b476, re.S)
                მონაცემები = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(მონაცემები) == int(일치.group(1)); return მონაცემები
            გარემო('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            გარემო('java -version', ['not OpenJDK', 'exit 0'])
            გარემო('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            გარემო('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            გარემო('python --version', ['MicroPython 1.24.1', 'exit 0'])
            გარემო('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 ფაილი', 'exit 0'])
            გარემო('cat python.txt', ['한글 ფაილი'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(ჩამოტვირთვა('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            რედაქტირება_მნიშვნელობა('인사.java', 'public class 인사 { public static void main(String[] args) { int მნიშვნელობა = 7; System.out.println("한글=" + მნიშვნელობა); } }')
            გარემო('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            გარემო('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(ჩამოტვირთვა('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            რედაქტირება_მნიშვნელობა('Hello.java', 'broken', გაუქმება_ოპერაცია=True)
            გარემო('javac Hello.java', ['Compiled:', 'exit 0'])
            რედაქტირება_მნიშვნელობა('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            გარემო('javac Broken.java', ['javac error:', 'exit 1'])
            ატვირთვა_ფაილები('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            გარემო('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            გარემო('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            ატვირთვა_ფაილები('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            გარემო('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            გარემო('rm Imported.class', [])
            რედაქტირება_მნიშვნელობა('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            გარემო('javac Loop.java', ['Compiled:', 'exit 0'])
            პასუხი_1262b476 = გარემო('java Loop', ['exit '])
            assert b'instruction limit' in პასუხი_1262b476 or b'exit -1004' in პასუხი_1262b476
            გარემო('rm Loop.java', []); გარემო('rm Loop.class', [])
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
            რედაქტირება_მნიშვნელობა('checks.py', 파이썬검사)
            გარემო('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            გარემო('rm checks.py', [])
            რედაქტირება_მნიშვნელობა('helper.py', 'value = 321')
            გარემო("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            გარემო('rm helper.py', [])
            გარემო("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            გარემო("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                გარემო('python hello.py', ['한글 ფაილი', 'exit 0'])
                გარემო('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            ატვირთვა_ფაილები('app.elf', (პროეცირება_ფესვი / 'build/user/demo.elf').read_bytes())
            assert ჩამოტვირთვა('app.elf') == (პროეცირება_ფესვი / 'build/user/demo.elf').read_bytes()
            გარემო('run app.elf', ['EL0 C++', 'exit 0'])
            ატვირთვა_ფაილები('app.elf', b'not an ELF')
            გარემო('run app.elf', ['exit -8'])
            გარემო('rm app.elf', [])
            გარემო('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            ნახატი_მდებარეობა = 출력결과 / 'java-framebuffer'; ნახატი_მდებარეობა.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(პროეცირება_ფესვი / 'dist/jkoros-native-korean.jar'), '-d', str(ნახატი_მდებარეობა), str(პროეცირება_ფესვი / '시험/자바/화면시험.java')])
            ატვირთვა_ფაილები('화면시험.class', (ნახატი_მდებარეობა / '화면시험.class').read_bytes())
            გარემო('java 화면시험', ['화면 კლიპი 거부', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            გარემო('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as კლიენტი:
                კლიენტი.settimeout(10)
                კლიენტი.connect(str(모의제어경로))
                with კლიენტი.makefile('rwb') as ნაკადი_მნიშვნელობა:
                    인사 = json.loads(ნაკადი_მნიშვნელობა.readline())
                    def 모의제어접속(შესრულება, 전달인수=None):
                        ქსელი_წერილი = {'execute': შესრულება}
                        if 전달인수: ქსელი_წერილი['arguments'] = 전달인수
                        ნაკადი_მნიშვნელობა.write((json.dumps(ქსელი_წერილი) + '\n').encode())
                        ნაკადი_მნიშვნელობა.flush()
                        while True:
                            პასუხი = json.loads(ნაკადი_მნიშვნელობა.readline())
                            if 'error' in პასუხი: raise AssertionError(პასუხი)
                            if 'return' in პასუხი: return პასუხი['return']
                    모의제어접속('qmp_capabilities')
                    ეკრანის_ამოჭრა = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(ეკრანის_ამოჭრა), 'format': 'ppm'})
                    def 예제들(გეზი, 지점들):
                        with გეზი.open('rb') as პიქსელი_ფაილი:
                            assert პიქსელი_ფაილი.readline().strip() == b'P6'
                            assert პიქსელი_ფაილი.readline().strip() == b'640 480'
                            assert პიქსელი_ფაილი.readline().strip() == b'255'
                            პიქსელი_მონაცემები = პიქსელი_ფაილი.read()
                        assert len(პიქსელი_მონაცემები) == 640 * 480 * 3
                        return [list(პიქსელი_მონაცემები[(Y_ღილაკი_კოორდინატი * 640 + x_კოორდინატა) * 3:(Y_ღილაკი_კოორდინატი * 640 + x_კოორდინატა) * 3 + 3]) for x_კოორდინატა, Y_ღილაკი_კოორდინატი in 지점들]
                    assert 예제들(ეკრანის_ამოჭრა, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(ეკრანის_ამოჭრა, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def გაგზავნა(누름값, 확인표시):
                        ოფსეტი_მნიშვნელობა = len(대화기록)
                        პროცესი.stdin.write(누름값); პროცესი.stdin.flush()
                        표시까지받기(확인표시, ოფსეტი_მნიშვნელობა)
                    გაგზავნა(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    გაგზავნა(b'\r', b'GUI ACTION 0 RESULT 0')
                    გაგზავნა(b'\t', b'GUI FOCUS 1')
                    გაგზავნა(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    გაგზავნა(b'\t', b'GUI FOCUS 2')
                    გაგზავნა(b'\r', b'GUI ACTION 2 RESULT 0')
                    გაგზავნა(b'\t', b'GUI FOCUS 3')
                    გაგზავნა(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    გაგზავნა(b'q', b'jkoros-native> ')
                    გადამოწმება_ანგარიში['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            პროცესი.wait(timeout=10)
            # framebuffer 응답뿐 아니라 რეალური_მონაცემები scanout 픽셀도 확인한다.
            with ეკრანის_ამოჭრა.open('rb') as ფაილი_შენატანი:
                assert ფაილი_შენატანი.readline().strip() == b'P6'
                치수 = ფაილი_შენატანი.readline().strip()
                assert 치수 == b'640 480', 치수
                assert ფაილი_შენატანი.readline().strip() == b'255'
                화소들 = ფაილი_შენატანი.read()
            assert len(화소들) == 640 * 480 * 3
            def პიქსელი(x_კოორდინატა, Y_ღილაკი_კოორდინატი): return list(화소들[(Y_ღილაკი_კოორდინატი * 640 + x_კოორდინატა) * 3:(Y_ღილაკი_კოორდინატი * 640 + x_კოორდინატა) * 3 + 3])
            예제들 = {'background': პიქსელი(5, 5), 'panel': პიქსელი(45, 85), 'tile': პიქსელი(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            გადამოწმება_ანგარიში.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((პროეცირება_ფესვი / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if პროცესი.poll() is None:
                პროცესი.terminate()
                try: პროცესი.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    პროცესი.kill(); პროცესი.wait(timeout=5)
            სელექტორი.close()
            პროცესი.stdin.close(); პროცესი.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(გადამოწმება_ანგარიში, indent=2) + '\n')


if __name__ == '__main__':
    გაშვება()
