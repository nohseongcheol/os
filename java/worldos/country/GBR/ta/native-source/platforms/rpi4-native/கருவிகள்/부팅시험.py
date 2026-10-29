#!/usr/bin/env python3
"""அசல்_தரவு raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from இயக்கு_கட்டளை import திட்டப்பணி_மூலம், கட்டளை


def செயல்படுத்துக():
    출력결과 = திட்டப்பணி_மூலம் / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    செல்லுபடியாக்கம்_அறிக்கை = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = கட்டளை() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        செல்லுபடியாக்கம்_அறிக்கை['command'] = 명령인수
        செயல்பாடு = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        தேர்வி = selectors.DefaultSelector()
        தேர்வி.register(செயல்பாடு.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, ஆஃப்செட்_மதிப்பு=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[ஆஃப்செட்_மதிப்பு:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in தேர்வி.select(0.2):
                    தரவு_தடு = 누름값.fileobj.read(4096)
                    if தரவு_தடு:
                        대화기록.extend(தரவு_தடு)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if செயல்பாடு.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(செயல்பாடு.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 அசல்_தரவு GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(அளவு):
                    அளவிடக்கூடியது = b''
                    while len(அளவிடக்கூடியது) < அளவு:
                        조각 = 화면접속자.recv(அளவு - len(அளவிடக்கூடியது))
                        if not 조각: raise AssertionError('VNC disconnected')
                        அளவிடக்கூடியது += 조각
                    return அளவிடக்கூடியது
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                சேவையகம்_மதிப்பு = 정확한값(24)
                assert int.from_bytes(சேவையகம்_மதிப்பு[:2], 'big') == 640 and int.from_bytes(சேவையகம்_மதிப்பு[2:4], 'big') == 480
                정확한값(int.from_bytes(சேவையகம்_மதிப்பு[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for கட்டளை_பைட், 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                ஆஃப்செட்_மதிப்பு = len(대화기록)
                செயல்பாடு.stdin.write(கட்டளை_பைட் + b'\n')
                செயல்பாடு.stdin.flush()
                표시까지받기(b'jkoros-native> ', ஆஃப்செட்_மதிப்பு)
                assert 확인표시 in 대화기록[ஆஃப்செட்_மதிப்பு:], 확인표시
            def கூடு(உள்ளீட்டு_வரி, 예상결과):
                ஆஃப்செட்_மதிப்பு = len(대화기록)
                செயல்பாடு.stdin.write(உள்ளீட்டு_வரி.encode('utf-8') + b'\n'); செயல்பாடு.stdin.flush()
                표시까지받기(b'jkoros-native> ', ஆஃப்செட்_மதிப்பு)
                응답자료 = bytes(대화기록[ஆஃப்செட்_மதிப்பு:])
                for உரை in 예상결과:
                    assert உரை.encode('utf-8') in 응답자료, (உள்ளீட்டு_வரி, உரை, 응답자료)
                return 응답자료
            def உள்ளிடு(உள்ளீட்டு_வரி, செயலழைப்பு):
                ஆஃப்செட்_மதிப்பு = len(대화기록)
                செயல்பாடு.stdin.write(உள்ளீட்டு_வரி.encode('utf-8') + b'\n'); செயல்பாடு.stdin.flush()
                표시까지받기(செயலழைப்பு, ஆஃப்செட்_மதிப்பு)
                return bytes(대화기록[ஆஃப்செட்_மதிப்பு:])
            def திருத்து_மதிப்பு(பெயர், உள்ளடக்கம்_மதிப்பு, ரத்து_இயக்கம்=False):
                உள்ளிடு('edit ' + பெயர், b'edit> ')
                for உள்ளீட்டு_வரி in உள்ளடக்கம்_மதிப்பு.splitlines(): உள்ளிடு(உள்ளீட்டு_வரி, b'edit> ')
                if ரத்து_இயக்கம்:
                    ஆஃப்செட்_மதிப்பு = len(대화기록)
                    செயல்பாடு.stdin.write(b'\x03'); செயல்பாடு.stdin.flush()
                    표시까지받기(b'jkoros-native> ', ஆஃப்செட்_மதிப்பு)
                    assert b'EDIT CANCELLED' in 대화기록[ஆஃப்செட்_மதிப்பு:]
                else:
                    assert b'SAVED' in உள்ளிடு('.', b'jkoros-native> ')
            def பதிவேற்று_கோப்புகள்(பெயர், தரவு):
                assert len(தரவு) <= 16384
                உள்ளிடு('load ' + பெயர், b'hex> ')
                for 순번 in range(0, len(தரவு), 64): உள்ளிடு(தரவு[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in உள்ளிடு('.', b'jkoros-native> ')
            def பதிவிறக்கு(பெயர்):
                응답자료 = கூடு('hex ' + பெயர், ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                தரவு = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(தரவு) == int(일치.group(1)); return தரவு
            கூடு('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            கூடு('java -version', ['not OpenJDK', 'exit 0'])
            கூடு('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            கூடு('java Hello "한글 செயலுருபுகள் 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 செயலுருபுகள் 😀', 'exit 0'])
            கூடு('python --version', ['MicroPython 1.24.1', 'exit 0'])
            கூடு('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 கோப்பின்_பெயர்', 'exit 0'])
            கூடு('cat python.txt', ['한글 கோப்பின்_பெயர்'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(பதிவிறக்கு('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 செயலுருபுகள் 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 செயலுருபுகள் 😀'], 예상결과
            திருத்து_மதிப்பு('인사.java', 'public class 인사 { public static void main(String[] args) { int மதிப்பு = 7; System.out.println("한글=" + மதிப்பு); } }')
            கூடு('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            கூடு('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(பதிவிறக்கு('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            திருத்து_மதிப்பு('Hello.java', 'broken', ரத்து_இயக்கம்=True)
            கூடு('javac Hello.java', ['Compiled:', 'exit 0'])
            திருத்து_மதிப்பு('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            கூடு('javac Broken.java', ['javac error:', 'exit 1'])
            பதிவேற்று_கோப்புகள்('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            கூடு('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            கூடு('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            பதிவேற்று_கோப்புகள்('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            கூடு('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            கூடு('rm Imported.class', [])
            திருத்து_மதிப்பு('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            கூடு('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = கூடு('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            கூடு('rm Loop.java', []); கூடு('rm Loop.class', [])
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
            திருத்து_மதிப்பு('checks.py', 파이썬검사)
            கூடு('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            கூடு('rm checks.py', [])
            திருத்து_மதிப்பு('helper.py', 'value = 321')
            கூடு("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            கூடு('rm helper.py', [])
            கூடு("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            கூடு("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                கூடு('python hello.py', ['한글 கோப்பின்_பெயர்', 'exit 0'])
                கூடு('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            பதிவேற்று_கோப்புகள்('app.elf', (திட்டப்பணி_மூலம் / 'build/user/demo.elf').read_bytes())
            assert பதிவிறக்கு('app.elf') == (திட்டப்பணி_மூலம் / 'build/user/demo.elf').read_bytes()
            கூடு('run app.elf', ['EL0 C++', 'exit 0'])
            பதிவேற்று_கோப்புகள்('app.elf', b'not an ELF')
            கூடு('run app.elf', ['exit -8'])
            கூடு('rm app.elf', [])
            கூடு('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            வரைதல்_பாதை = 출력결과 / 'java-framebuffer'; வரைதல்_பாதை.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(திட்டப்பணி_மூலம் / 'dist/jkoros-native-korean.jar'), '-d', str(வரைதல்_பாதை), str(திட்டப்பணி_மூலம் / '시험/자바/화면시험.java')])
            பதிவேற்று_கோப்புகள்('화면시험.class', (வரைதல்_பாதை / '화면시험.class').read_bytes())
            கூடு('java 화면시험', ['화면 கிளிப் புறக்கணி_மதிப்பு', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            கூடு('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as பயனகம்:
                பயனகம்.settimeout(10)
                பயனகம்.connect(str(모의제어경로))
                with பயனகம்.makefile('rwb') as தொடரோடி_மதிப்பு:
                    인사 = json.loads(தொடரோடி_மதிப்பு.readline())
                    def 모의제어접속(செயற்படுத்துக, 전달인수=None):
                        பிணையம்_செய்தி = {'execute': செயற்படுத்துக}
                        if 전달인수: பிணையம்_செய்தி['arguments'] = 전달인수
                        தொடரோடி_மதிப்பு.write((json.dumps(பிணையம்_செய்தி) + '\n').encode())
                        தொடரோடி_மதிப்பு.flush()
                        while True:
                            பதிலளி = json.loads(தொடரோடி_மதிப்பு.readline())
                            if 'error' in பதிலளி: raise AssertionError(பதிலளி)
                            if 'return' in பதிலளி: return பதிலளி['return']
                    모의제어접속('qmp_capabilities')
                    ஸ்கிரீன்ஷாட் = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(ஸ்கிரீன்ஷாட்), 'format': 'ppm'})
                    def 예제들(பாதை_2, 지점들):
                        with பாதை_2.open('rb') as படக்_கூறு_கோப்பு:
                            assert படக்_கூறு_கோப்பு.readline().strip() == b'P6'
                            assert படக்_கூறு_கோப்பு.readline().strip() == b'640 480'
                            assert படக்_கூறு_கோப்பு.readline().strip() == b'255'
                            படக்_கூறு_தரவு = படக்_கூறு_கோப்பு.read()
                        assert len(படக்_கூறு_தரவு) == 640 * 480 * 3
                        return [list(படக்_கூறு_தரவு[(Y_பொத்தான்_அச்சுத்_தொகுப்பு * 640 + x_ஒத்ததரமுள்ளது) * 3:(Y_பொத்தான்_அச்சுத்_தொகுப்பு * 640 + x_ஒத்ததரமுள்ளது) * 3 + 3]) for x_ஒத்ததரமுள்ளது, Y_பொத்தான்_அச்சுத்_தொகுப்பு in 지점들]
                    assert 예제들(ஸ்கிரீன்ஷாட், [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(ஸ்கிரீன்ஷாட், [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def அனுப்பு(누름값, 확인표시):
                        ஆஃப்செட்_மதிப்பு = len(대화기록)
                        செயல்பாடு.stdin.write(누름값); செயல்பாடு.stdin.flush()
                        표시까지받기(확인표시, ஆஃப்செட்_மதிப்பு)
                    அனுப்பு(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    அனுப்பு(b'\r', b'GUI ACTION 0 RESULT 0')
                    அனுப்பு(b'\t', b'GUI FOCUS 1')
                    அனுப்பு(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    அனுப்பு(b'\t', b'GUI FOCUS 2')
                    அனுப்பு(b'\r', b'GUI ACTION 2 RESULT 0')
                    அனுப்பு(b'\t', b'GUI FOCUS 3')
                    அனுப்பு(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    அனுப்பு(b'q', b'jkoros-native> ')
                    செல்லுபடியாக்கம்_அறிக்கை['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            செயல்பாடு.wait(timeout=10)
            # framebuffer 응답뿐 아니라 அசல்_தரவு scanout 픽셀도 확인한다.
            with ஸ்கிரீன்ஷாட்.open('rb') as கோப்பு_உள்ளீடு:
                assert கோப்பு_உள்ளீடு.readline().strip() == b'P6'
                치수 = கோப்பு_உள்ளீடு.readline().strip()
                assert 치수 == b'640 480', 치수
                assert கோப்பு_உள்ளீடு.readline().strip() == b'255'
                화소들 = கோப்பு_உள்ளீடு.read()
            assert len(화소들) == 640 * 480 * 3
            def படக்_கூறு(x_ஒத்ததரமுள்ளது, Y_பொத்தான்_அச்சுத்_தொகுப்பு): return list(화소들[(Y_பொத்தான்_அச்சுத்_தொகுப்பு * 640 + x_ஒத்ததரமுள்ளது) * 3:(Y_பொத்தான்_அச்சுத்_தொகுப்பு * 640 + x_ஒத்ததரமுள்ளது) * 3 + 3])
            예제들 = {'background': படக்_கூறு(5, 5), 'panel': படக்_கூறு(45, 85), 'tile': படக்_கூறு(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            செல்லுபடியாக்கம்_அறிக்கை.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((திட்டப்பணி_மூலம் / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if செயல்பாடு.poll() is None:
                செயல்பாடு.terminate()
                try: செயல்பாடு.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    செயல்பாடு.kill(); செயல்பாடு.wait(timeout=5)
            தேர்வி.close()
            செயல்பாடு.stdin.close(); செயல்பாடு.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(செல்லுபடியாக்கம்_அறிக்கை, indent=2) + '\n')


if __name__ == '__main__':
    செயல்படுத்துக()
