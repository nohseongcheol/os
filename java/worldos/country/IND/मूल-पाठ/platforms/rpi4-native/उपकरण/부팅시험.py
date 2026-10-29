#!/usr/bin/env python3
"""वास्तविक_डेटा raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from निष्पादित_करें_आदेश import प्रोजेक्ट_करें_मूल, आदेश


def चलाएँ():
    출력결과 = प्रोजेक्ट_करें_मूल / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    बोला_गया_पाठ = bytearray()
    प्रमाणीकरण_रिपोर्ट = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = आदेश() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        प्रमाणीकरण_रिपोर्ट['command'] = 명령인수
        प्रक्रिया = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        सिलेक्टर = selectors.DefaultSelector()
        सिलेक्टर.register(प्रक्रिया.stdout, selectors.EVENT_READ)
        def 표시까지받기(मार्कर, ऑफ़सेट_मान=0, 시간제한=45):
            अंति_म_समय_सीमा_समय = time.monotonic() + 시간제한
            while मार्कर not in बोला_गया_पाठ[ऑफ़सेट_मान:]:
                if time.monotonic() > अंति_म_समय_सीमा_समय:
                    raise AssertionError('UART timeout: ' + repr(मार्कर))
                for 누름값, _ in सिलेक्टर.select(0.2):
                    डेटा_ब्_लॉक = 누름값.fileobj.read(4096)
                    if डेटा_ब्_लॉक:
                        बोला_गया_पाठ.extend(डेटा_ब्_लॉक)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', बोला_गया_पाठ):
                    raise AssertionError('kernel failure')
                if प्रक्रिया.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(प्रक्रिया.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for मार्कर in 확인표시들:
                assert मार्कर in बोला_गया_पाठ, मार्कर
            # GTK 없는 अद्यतित_आइटम 호스트에서도 VNC로 वास्तविक_डेटा GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(आकार):
                    परिणाम = b''
                    while len(परिणाम) < आकार:
                        조각 = 화면접속자.recv(आकार - len(परिणाम))
                        if not 조각: raise AssertionError('VNC disconnected')
                        परिणाम += 조각
                    return परिणाम
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                서버 = 정확한값(24)
                assert int.from_bytes(서버[:2], 'big') == 640 and int.from_bytes(서버[2:4], 'big') == 480
                정확한값(int.from_bytes(서버[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for आदेश_बाइट, मार्कर in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                ऑफ़सेट_मान = len(बोला_गया_पाठ)
                प्रक्रिया.stdin.write(आदेश_बाइट + b'\n')
                प्रक्रिया.stdin.flush()
                표시까지받기(b'jkoros-native> ', ऑफ़सेट_मान)
                assert मार्कर in बोला_गया_पाठ[ऑफ़सेट_मान:], मार्कर
            def शेल(पंक्ति, 예상결과):
                ऑफ़सेट_मान = len(बोला_गया_पाठ)
                प्रक्रिया.stdin.write(पंक्ति.encode('utf-8') + b'\n'); प्रक्रिया.stdin.flush()
                표시까지받기(b'jkoros-native> ', ऑफ़सेट_मान)
                प्रतिसाद = bytes(बोला_गया_पाठ[ऑफ़सेट_मान:])
                for पाठ in 예상결과:
                    assert पाठ.encode('utf-8') in प्रतिसाद, (पंक्ति, पाठ, प्रतिसाद)
                return प्रतिसाद
            def दर्ज_करें(पंक्ति, संकेत):
                ऑफ़सेट_मान = len(बोला_गया_पाठ)
                प्रक्रिया.stdin.write(पंक्ति.encode('utf-8') + b'\n'); प्रक्रिया.stdin.flush()
                표시까지받기(संकेत, ऑफ़सेट_मान)
                return bytes(बोला_गया_पाठ[ऑफ़सेट_मान:])
            def संपादन_मान(नाम, सामग्री_मान, रद्द_करें_ऑपरेशन=False):
                दर्ज_करें('edit ' + नाम, b'edit> ')
                for पंक्ति in सामग्री_मान.splitlines(): दर्ज_करें(पंक्ति, b'edit> ')
                if रद्द_करें_ऑपरेशन:
                    ऑफ़सेट_मान = len(बोला_गया_पाठ)
                    प्रक्रिया.stdin.write(b'\x03'); प्रक्रिया.stdin.flush()
                    표시까지받기(b'jkoros-native> ', ऑफ़सेट_मान)
                    assert b'EDIT CANCELLED' in बोला_गया_पाठ[ऑफ़सेट_मान:]
                else:
                    assert b'SAVED' in दर्ज_करें('.', b'jkoros-native> ')
            def अपलोड_फ़ाइलें(नाम, आँकड़े):
                assert len(आँकड़े) <= 16384
                दर्ज_करें('load ' + नाम, b'hex> ')
                for 순번 in range(0, len(आँकड़े), 64): दर्ज_करें(आँकड़े[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in दर्ज_करें('.', b'jkoros-native> ')
            def डाउनलोड(नाम):
                प्रतिसाद = शेल('hex ' + नाम, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', प्रतिसाद, re.S)
                आँकड़े = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(आँकड़े) == int(일치.group(1)); return आँकड़े
            शेल('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            शेल('java -version', ['not OpenJDK', 'exit 0'])
            शेल('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            शेल('java Hello "한글 तर्क 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 तर्क 😀', 'exit 0'])
            शेल('python --version', ['MicroPython 1.24.1', 'exit 0'])
            शेल('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 संचिका', 'exit 0'])
            शेल('cat python.txt', ['한글 संचिका'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(डाउनलोड('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 तर्क 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 तर्क 😀'], 예상결과
            संपादन_मान('अभिनन्दन_ae353e94.java', 'public class अभिनन्दन_ae353e94 { public static void main(String[] args) { int मान = 7; System.out.println("한글=" + मान); } }')
            शेल('javac अभिनन्दन_ae353e94.java', ['Compiled: अभिनन्दन_ae353e94.class', 'exit 0'])
            शेल('java अभिनन्दन_ae353e94', ['한글=7', 'exit 0'])
            (출력결과 / 'अभिनन्दन_ae353e94.class').write_bytes(डाउनलोड('अभिनन्दन_ae353e94.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'अभिनन्दन_ae353e94']).decode().strip() == '한글=7'
            संपादन_मान('Hello.java', 'broken', रद्द_करें_ऑपरेशन=True)
            शेल('javac Hello.java', ['Compiled:', 'exit 0'])
            संपादन_मान('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            शेल('javac Broken.java', ['javac error:', 'exit 1'])
            अपलोड_फ़ाइलें('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            शेल('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            शेल('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            अपलोड_फ़ाइलें('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            शेल('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            शेल('rm Imported.class', [])
            संपादन_मान('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            शेल('javac Loop.java', ['Compiled:', 'exit 0'])
            प्रतिसाद = शेल('java Loop', ['exit '])
            assert b'instruction limit' in प्रतिसाद or b'exit -1004' in प्रतिसाद
            शेल('rm Loop.java', []); शेल('rm Loop.class', [])
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
            संपादन_मान('checks.py', 파이썬검사)
            शेल('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            शेल('rm checks.py', [])
            संपादन_मान('helper.py', 'value = 321')
            शेल("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            शेल('rm helper.py', [])
            शेल("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            शेल("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                शेल('python hello.py', ['한글 संचिका', 'exit 0'])
                शेल('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            अपलोड_फ़ाइलें('app.elf', (प्रोजेक्ट_करें_मूल / 'build/user/demo.elf').read_bytes())
            assert डाउनलोड('app.elf') == (प्रोजेक्ट_करें_मूल / 'build/user/demo.elf').read_bytes()
            शेल('run app.elf', ['EL0 C++', 'exit 0'])
            अपलोड_फ़ाइलें('app.elf', b'not an ELF')
            शेल('run app.elf', ['exit -8'])
            शेल('rm app.elf', [])
            शेल('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            ड्रॉइंग_पथ = 출력결과 / 'java-framebuffer'; ड्रॉइंग_पथ.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(प्रोजेक्ट_करें_मूल / 'dist/jkoros-native-korean.jar'), '-d', str(ड्रॉइंग_पथ), str(प्रोजेक्ट_करें_मूल / '시험/자바/화면시험.java')])
            अपलोड_फ़ाइलें('화면시험.class', (ड्रॉइंग_पथ / '화면시험.class').read_bytes())
            शेल('java 화면시험', ['화면 क्लिप अस्वीकृत_करें_मान', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            शेल('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as क्लायंट:
                क्लायंट.settimeout(10)
                क्लायंट.connect(str(모의제어경로))
                with क्लायंट.makefile('rwb') as स्ट्रीम_मान:
                    अभिनन्दन_ae353e94 = json.loads(स्ट्रीम_मान.readline())
                    def 모의제어접속(निष्पादन, 전달인수=None):
                        नेटवर्क_ईमेल = {'execute': निष्पादन}
                        if 전달인수: नेटवर्क_ईमेल['arguments'] = 전달인수
                        स्ट्रीम_मान.write((json.dumps(नेटवर्क_ईमेल) + '\n').encode())
                        स्ट्रीम_मान.flush()
                        while True:
                            उत्तर = json.loads(स्ट्रीम_मान.readline())
                            if 'error' in उत्तर: raise AssertionError(उत्तर)
                            if 'return' in उत्तर: return उत्तर['return']
                    모의제어접속('qmp_capabilities')
                    स्क्रीनशॉट = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(स्क्रीनशॉट), 'format': 'ppm'})
                    def 예제들(पथ, 지점들):
                        with पथ.open('rb') as पिक्सेल_फ़ाइल:
                            assert पिक्सेल_फ़ाइल.readline().strip() == b'P6'
                            assert पिक्सेल_फ़ाइल.readline().strip() == b'640 480'
                            assert पिक्सेल_फ़ाइल.readline().strip() == b'255'
                            पिक्सेल_डेटा = पिक्सेल_फ़ाइल.read()
                        assert len(पिक्सेल_डेटा) == 640 * 480 * 3
                        return [list(पिक्सेल_डेटा[(세로좌표 * 640 + x_निर्देशांक) * 3:(세로좌표 * 640 + x_निर्देशांक) * 3 + 3]) for x_निर्देशांक, 세로좌표 in 지점들]
                    assert 예제들(स्क्रीनशॉट, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(स्क्रीनशॉट, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def भेजें(누름값, मार्कर):
                        ऑफ़सेट_मान = len(बोला_गया_पाठ)
                        प्रक्रिया.stdin.write(누름값); प्रक्रिया.stdin.flush()
                        표시까지받기(मार्कर, ऑफ़सेट_मान)
                    भेजें(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    भेजें(b'\r', b'GUI ACTION 0 RESULT 0')
                    भेजें(b'\t', b'GUI FOCUS 1')
                    भेजें(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    भेजें(b'\t', b'GUI FOCUS 2')
                    भेजें(b'\r', b'GUI ACTION 2 RESULT 0')
                    भेजें(b'\t', b'GUI FOCUS 3')
                    भेजें(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    भेजें(b'q', b'jkoros-native> ')
                    प्रमाणीकरण_रिपोर्ट['qemu'] = अभिनन्दन_ae353e94['QMP']['version']
                    모의제어접속('quit')
            प्रक्रिया.wait(timeout=10)
            # framebuffer 응답뿐 아니라 वास्तविक_डेटा scanout 픽셀도 확인한다.
            with स्क्रीनशॉट.open('rb') as फ़ाइल_एन्ट्री:
                assert फ़ाइल_एन्ट्री.readline().strip() == b'P6'
                치수 = फ़ाइल_एन्ट्री.readline().strip()
                assert 치수 == b'640 480', 치수
                assert फ़ाइल_एन्ट्री.readline().strip() == b'255'
                화소들 = फ़ाइल_एन्ट्री.read()
            assert len(화소들) == 640 * 480 * 3
            def पिक्सेल(x_निर्देशांक, 세로좌표): return list(화소들[(세로좌표 * 640 + x_निर्देशांक) * 3:(세로좌표 * 640 + x_निर्देशांक) * 3 + 3])
            예제들 = {'background': पिक्सेल(5, 5), 'panel': पिक्सेल(45, 85), 'tile': पिक्सेल(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            प्रमाणीकरण_रिपोर्ट.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((प्रोजेक्ट_करें_मूल / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if प्रक्रिया.poll() is None:
                प्रक्रिया.terminate()
                try: प्रक्रिया.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    प्रक्रिया.kill(); प्रक्रिया.wait(timeout=5)
            सिलेक्टर.close()
            प्रक्रिया.stdin.close(); प्रक्रिया.stdout.close()
            (출력결과 / 'serial.log').write_bytes(बोला_गया_पाठ)
            (출력결과 / 'report.json').write_text(json.dumps(प्रमाणीकरण_रिपोर्ट, indent=2) + '\n')


if __name__ == '__main__':
    चलाएँ()
