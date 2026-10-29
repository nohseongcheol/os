#!/usr/bin/env python3
"""प्रत्यक्ष_डेटा raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from पाळो_दिवचो_आदेश import प्रॉजॅक्ट_रूट, आदेश


def चलोवप():
    출력결과 = प्रॉजॅक्ट_रूट / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    वैधताय_अहवाल = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = आदेश() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        वैधताय_अहवाल['command'] = 명령인수
        प्रक्रिया = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        वेंचक = selectors.DefaultSelector()
        वेंचक.register(प्रक्रिया.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, ऑफसॅट_मोल=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[ऑफसॅट_मोल:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in वेंचक.select(0.2):
                    डेटा_आडावचें = 누름값.fileobj.read(4096)
                    if डेटा_आडावचें:
                        대화기록.extend(डेटा_आडावचें)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if प्रक्रिया.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(प्रक्रिया.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 प्रत्यक्ष_डेटा GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def EXACT_मोल(आवाठ):
                    मेजप = b''
                    while len(मेजप) < आवाठ:
                        조각 = 화면접속자.recv(आवाठ - len(मेजप))
                        if not 조각: raise AssertionError('VNC disconnected')
                        मेजप += 조각
                    return मेजप
                assert EXACT_मोल(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in EXACT_मोल(EXACT_मोल(1)[0]); 화면접속자.sendall(b'\x01')
                assert EXACT_मोल(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                सर्वर_मोल = EXACT_मोल(24)
                assert int.from_bytes(सर्वर_मोल[:2], 'big') == 640 and int.from_bytes(सर्वर_मोल[2:4], 'big') == 480
                EXACT_मोल(int.from_bytes(सर्वर_मोल[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for आदेश_बायट, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                ऑफसॅट_मोल = len(대화기록)
                प्रक्रिया.stdin.write(आदेश_बायट + b'\n')
                प्रक्रिया.stdin.flush()
                표시까지받기(b'jkoros-native> ', ऑफसॅट_मोल)
                assert 확인표시 in 대화기록[ऑफसॅट_मोल:], 확인표시
            def शॅल(रेग, 예상결과):
                ऑफसॅट_मोल = len(대화기록)
                प्रक्रिया.stdin.write(रेग.encode('utf-8') + b'\n'); प्रक्रिया.stdin.flush()
                표시까지받기(b'jkoros-native> ', ऑफसॅट_मोल)
                응답자료 = bytes(대화기록[ऑफसॅट_मोल:])
                for SMS in 예상결과:
                    assert SMS.encode('utf-8') in 응답자료, (रेग, SMS, 응답자료)
                return 응답자료
            def प्रवेश_करचो(रेग, तत्पर):
                ऑफसॅट_मोल = len(대화기록)
                प्रक्रिया.stdin.write(रेग.encode('utf-8') + b'\n'); प्रक्रिया.stdin.flush()
                표시까지받기(तत्पर, ऑफसॅट_मोल)
                return bytes(대화기록[ऑफसॅट_मोल:])
            def संपादन_करचें_मोल(नांव, अनुक्रमणिका_मोल, रद्द_करचें_क्रिया=False):
                प्रवेश_करचो('edit ' + नांव, b'edit> ')
                for रेग in अनुक्रमणिका_मोल.splitlines(): प्रवेश_करचो(रेग, b'edit> ')
                if रद्द_करचें_क्रिया:
                    ऑफसॅट_मोल = len(대화기록)
                    प्रक्रिया.stdin.write(b'\x03'); प्रक्रिया.stdin.flush()
                    표시까지받기(b'jkoros-native> ', ऑफसॅट_मोल)
                    assert b'EDIT CANCELLED' in 대화기록[ऑफसॅट_मोल:]
                else:
                    assert b'SAVED' in प्रवेश_करचो('.', b'jkoros-native> ')
            def अपलोड_करचें_फायली(नांव, डेटा):
                assert len(डेटा) <= 16384
                प्रवेश_करचो('load ' + नांव, b'hex> ')
                for 순번 in range(0, len(डेटा), 64): प्रवेश_करचो(डेटा[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in प्रवेश_करचो('.', b'jkoros-native> ')
            def डावनलोड(नांव):
                응답자료 = शॅल('hex ' + नांव, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                डेटा = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(डेटा) == int(일치.group(1)); return डेटा
            शॅल('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            शॅल('java -version', ['not OpenJDK', 'exit 0'])
            शॅल('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            शॅल('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            शॅल('python --version', ['MicroPython 1.24.1', 'exit 0'])
            शॅल('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 फायल', 'exit 0'])
            शॅल('cat python.txt', ['한글 फायल'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(डावनलोड('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            संपादन_करचें_मोल('인사.java', 'public class 인사 { public static void main(String[] args) { int मोल = 7; System.out.println("한글=" + मोल); } }')
            शॅल('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            शॅल('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(डावनलोड('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            संपादन_करचें_मोल('Hello.java', 'broken', रद्द_करचें_क्रिया=True)
            शॅल('javac Hello.java', ['Compiled:', 'exit 0'])
            संपादन_करचें_मोल('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            शॅल('javac Broken.java', ['javac error:', 'exit 1'])
            अपलोड_करचें_फायली('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            शॅल('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            शॅल('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            अपलोड_करचें_फायली('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            शॅल('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            शॅल('rm Imported.class', [])
            संपादन_करचें_मोल('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            शॅल('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = शॅल('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            शॅल('rm Loop.java', []); शॅल('rm Loop.class', [])
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
            संपादन_करचें_मोल('checks.py', 파이썬검사)
            शॅल('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            शॅल('rm checks.py', [])
            संपादन_करचें_मोल('helper.py', 'value = 321')
            शॅल("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            शॅल('rm helper.py', [])
            शॅल("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            शॅल("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                शॅल('python hello.py', ['한글 फायल', 'exit 0'])
                शॅल('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            अपलोड_करचें_फायली('app.elf', (प्रॉजॅक्ट_रूट / 'build/user/demo.elf').read_bytes())
            assert डावनलोड('app.elf') == (प्रॉजॅक्ट_रूट / 'build/user/demo.elf').read_bytes()
            शॅल('run app.elf', ['EL0 C++', 'exit 0'])
            अपलोड_करचें_फायली('app.elf', b'not an ELF')
            शॅल('run app.elf', ['exit -8'])
            शॅल('rm app.elf', [])
            शॅल('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            रेखाटन_पाथ = 출력결과 / 'java-framebuffer'; रेखाटन_पाथ.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(प्रॉजॅक्ट_रूट / 'dist/jkoros-native-korean.jar'), '-d', str(रेखाटन_पाथ), str(प्रॉजॅक्ट_रूट / '시험/자바/화면시험.java')])
            अपलोड_करचें_फायली('화면시험.class', (रेखाटन_पाथ / '화면시험.class').read_bytes())
            शॅल('java 화면시험', ['화면 क्लिप 거부', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            शॅल('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as क्लायंट:
                क्लायंट.settimeout(10)
                क्लायंट.connect(str(모의제어경로))
                with क्लायंट.makefile('rwb') as Stream_मोल:
                    인사 = json.loads(Stream_मोल.readline())
                    def 모의제어접속(पाळो_दिवचो_कार्य, 전달인수=None):
                        नॅटवर्क_संदेश = {'execute': पाळो_दिवचो_कार्य}
                        if 전달인수: नॅटवर्क_संदेश['arguments'] = 전달인수
                        Stream_मोल.write((json.dumps(नॅटवर्क_संदेश) + '\n').encode())
                        Stream_मोल.flush()
                        while True:
                            जाप_दिवप = json.loads(Stream_मोल.readline())
                            if 'error' in जाप_दिवप: raise AssertionError(जाप_दिवप)
                            if 'return' in जाप_दिवप: return जाप_दिवप['return']
                    모의제어접속('qmp_capabilities')
                    स्क्रिन_क्लिपींग = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(स्क्रिन_क्लिपींग), 'format': 'ppm'})
                    def 예제들(पाथ, 지점들):
                        with पाथ.open('rb') as पिक्सॅल_फायल:
                            assert पिक्सॅल_फायल.readline().strip() == b'P6'
                            assert पिक्सॅल_फायल.readline().strip() == b'640 480'
                            assert पिक्सॅल_फायल.readline().strip() == b'255'
                            पिक्सॅल_डेटा = पिक्सॅल_फायल.read()
                        assert len(पिक्सॅल_डेटा) == 640 * 480 * 3
                        return [list(पिक्सॅल_डेटा[(세로좌표 * 640 + x_coordinate) * 3:(세로좌표 * 640 + x_coordinate) * 3 + 3]) for x_coordinate, 세로좌표 in 지점들]
                    assert 예제들(स्क्रिन_क्लिपींग, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(स्क्रिन_क्लिपींग, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def धाडचें(누름값, 확인표시):
                        ऑफसॅट_मोल = len(대화기록)
                        प्रक्रिया.stdin.write(누름값); प्रक्रिया.stdin.flush()
                        표시까지받기(확인표시, ऑफसॅट_मोल)
                    धाडचें(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    धाडचें(b'\r', b'GUI ACTION 0 RESULT 0')
                    धाडचें(b'\t', b'GUI FOCUS 1')
                    धाडचें(b'\r', b'GUI ACTION 1 RESULT 0')
                    SECOND_GUI = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SECOND_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SECOND_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    धाडचें(b'\t', b'GUI FOCUS 2')
                    धाडचें(b'\r', b'GUI ACTION 2 RESULT 0')
                    धाडचें(b'\t', b'GUI FOCUS 3')
                    धाडचें(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    धाडचें(b'q', b'jkoros-native> ')
                    वैधताय_अहवाल['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            प्रक्रिया.wait(timeout=10)
            # framebuffer 응답뿐 아니라 प्रत्यक्ष_डेटा scanout 픽셀도 확인한다.
            with स्क्रिन_क्लिपींग.open('rb') as फायल_प्रवेश:
                assert फायल_प्रवेश.readline().strip() == b'P6'
                치수 = फायल_प्रवेश.readline().strip()
                assert 치수 == b'640 480', 치수
                assert फायल_प्रवेश.readline().strip() == b'255'
                화소들 = फायल_प्रवेश.read()
            assert len(화소들) == 640 * 480 * 3
            def पिक्सॅल(x_coordinate, 세로좌표): return list(화소들[(세로좌표 * 640 + x_coordinate) * 3:(세로좌표 * 640 + x_coordinate) * 3 + 3])
            예제들 = {'background': पिक्सॅल(5, 5), 'panel': पिक्सॅल(45, 85), 'tile': पिक्सॅल(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            वैधताय_अहवाल.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((प्रॉजॅक्ट_रूट / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if प्रक्रिया.poll() is None:
                प्रक्रिया.terminate()
                try: प्रक्रिया.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    प्रक्रिया.kill(); प्रक्रिया.wait(timeout=5)
            वेंचक.close()
            प्रक्रिया.stdin.close(); प्रक्रिया.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(वैधताय_अहवाल, indent=2) + '\n')


if __name__ == '__main__':
    चलोवप()
