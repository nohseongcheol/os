#!/usr/bin/env python3
"""প্রকৃত_ডাটা raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from কার্যকর_করুন_আদেশ import প্রকল্প_মূল, আদেশ


def চালনা():
    출력결과 = প্রকল্প_মূল / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    বৈধকরণ_রিপোর্ট = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = আদেশ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        বৈধকরণ_রিপোর্ট['command'] = 명령인수
        প্রসেস = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        নির্বাচক = selectors.DefaultSelector()
        নির্বাচক.register(প্রসেস.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, অফসেট_মান=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[অফসেট_মান:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in নির্বাচক.select(0.2):
                    ডাটা_আটক_করা = 누름값.fileobj.read(4096)
                    if ডাটা_আটক_করা:
                        대화기록.extend(ডাটা_আটক_করা)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if প্রসেস.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(প্রসেস.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 প্রকৃত_ডাটা GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(আকার):
                    পরিমাপ = b''
                    while len(পরিমাপ) < আকার:
                        조각 = 화면접속자.recv(আকার - len(পরিমাপ))
                        if not 조각: raise AssertionError('VNC disconnected')
                        পরিমাপ += 조각
                    return পরিমাপ
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                সার্ভার_মান = 정확한값(24)
                assert int.from_bytes(সার্ভার_মান[:2], 'big') == 640 and int.from_bytes(সার্ভার_মান[2:4], 'big') == 480
                정확한값(int.from_bytes(সার্ভার_মান[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for আদেশ_বাইট, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                অফসেট_মান = len(대화기록)
                প্রসেস.stdin.write(আদেশ_বাইট + b'\n')
                প্রসেস.stdin.flush()
                표시까지받기(b'jkoros-native> ', অফসেট_মান)
                assert 확인표시 in 대화기록[অফসেট_মান:], 확인표시
            def শেল(নিবেশের_পঙ্_ক্তি, 예상결과):
                অফসেট_মান = len(대화기록)
                প্রসেস.stdin.write(নিবেশের_পঙ্_ক্তি.encode('utf-8') + b'\n'); প্রসেস.stdin.flush()
                표시까지받기(b'jkoros-native> ', অফসেট_মান)
                응답자료 = bytes(대화기록[অফসেট_মান:])
                for পাঠ in 예상결과:
                    assert পাঠ.encode('utf-8') in 응답자료, (নিবেশের_পঙ্_ক্তি, পাঠ, 응답자료)
                return 응답자료
            def প্রবেশ_করা(নিবেশের_পঙ্_ক্তি, সত্বর):
                অফসেট_মান = len(대화기록)
                প্রসেস.stdin.write(নিবেশের_পঙ্_ক্তি.encode('utf-8') + b'\n'); প্রসেস.stdin.flush()
                표시까지받기(সত্বর, অফসেট_মান)
                return bytes(대화기록[অফসেট_মান:])
            def সম্পাদন_মান(নাম, সামগ্রি_মান, বাতিল_অপারেশন=False):
                প্রবেশ_করা('edit ' + নাম, b'edit> ')
                for নিবেশের_পঙ্_ক্তি in সামগ্রি_মান.splitlines(): প্রবেশ_করা(নিবেশের_পঙ্_ক্তি, b'edit> ')
                if বাতিল_অপারেশন:
                    অফসেট_মান = len(대화기록)
                    প্রসেস.stdin.write(b'\x03'); প্রসেস.stdin.flush()
                    표시까지받기(b'jkoros-native> ', অফসেট_মান)
                    assert b'EDIT CANCELLED' in 대화기록[অফসেট_মান:]
                else:
                    assert b'SAVED' in প্রবেশ_করা('.', b'jkoros-native> ')
            def আপলোড_ফাইলগুলি(নাম, ডাটা):
                assert len(ডাটা) <= 16384
                প্রবেশ_করা('load ' + নাম, b'hex> ')
                for 순번 in range(0, len(ডাটা), 64): প্রবেশ_করা(ডাটা[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in প্রবেশ_করা('.', b'jkoros-native> ')
            def ডাউনলোড(নাম):
                응답자료 = শেল('hex ' + নাম, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                ডাটা = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(ডাটা) == int(일치.group(1)); return ডাটা
            শেল('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            শেল('java -version', ['not OpenJDK', 'exit 0'])
            শেল('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            শেল('java Hello "한글 আর্গুমেন্ট_তালিকা 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 আর্গুমেন্ট_তালিকা 😀', 'exit 0'])
            শেল('python --version', ['MicroPython 1.24.1', 'exit 0'])
            শেল('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 নথির_নাম', 'exit 0'])
            শেল('cat python.txt', ['한글 নথির_নাম'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(ডাউনলোড('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 আর্গুমেন্ট_তালিকা 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 আর্গুমেন্ট_তালিকা 😀'], 예상결과
            সম্পাদন_মান('인사.java', 'public class 인사 { public static void main(String[] args) { int মান = 7; System.out.println("한글=" + মান); } }')
            শেল('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            শেল('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(ডাউনলোড('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            সম্পাদন_মান('Hello.java', 'broken', বাতিল_অপারেশন=True)
            শেল('javac Hello.java', ['Compiled:', 'exit 0'])
            সম্পাদন_মান('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            শেল('javac Broken.java', ['javac error:', 'exit 1'])
            আপলোড_ফাইলগুলি('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            শেল('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            শেল('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            আপলোড_ফাইলগুলি('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            শেল('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            শেল('rm Imported.class', [])
            সম্পাদন_মান('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            শেল('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = শেল('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            শেল('rm Loop.java', []); শেল('rm Loop.class', [])
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
            সম্পাদন_মান('checks.py', 파이썬검사)
            শেল('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            শেল('rm checks.py', [])
            সম্পাদন_মান('helper.py', 'value = 321')
            শেল("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            শেল('rm helper.py', [])
            শেল("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            শেল("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                শেল('python hello.py', ['한글 নথির_নাম', 'exit 0'])
                শেল('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            আপলোড_ফাইলগুলি('app.elf', (প্রকল্প_মূল / 'build/user/demo.elf').read_bytes())
            assert ডাউনলোড('app.elf') == (প্রকল্প_মূল / 'build/user/demo.elf').read_bytes()
            শেল('run app.elf', ['EL0 C++', 'exit 0'])
            আপলোড_ফাইলগুলি('app.elf', b'not an ELF')
            শেল('run app.elf', ['exit -8'])
            শেল('rm app.elf', [])
            শেল('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            অঙ্কন_পথ = 출력결과 / 'java-framebuffer'; অঙ্কন_পথ.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(প্রকল্প_মূল / 'dist/jkoros-native-korean.jar'), '-d', str(অঙ্কন_পথ), str(প্রকল্প_মূল / '시험/자바/화면시험.java')])
            আপলোড_ফাইলগুলি('화면시험.class', (অঙ্কন_পথ / '화면시험.class').read_bytes())
            শেল('java 화면시험', ['화면 ক্লিপ প্রত্যাখ্যান_মান', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            শেল('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as গ্রাহক:
                গ্রাহক.settimeout(10)
                গ্রাহক.connect(str(모의제어경로))
                with গ্রাহক.makefile('rwb') as প্রবাহ_মান:
                    인사 = json.loads(প্রবাহ_মান.readline())
                    def 모의제어접속(চালানো, 전달인수=None):
                        নেটওয়ার্ক_ইমেইল = {'execute': চালানো}
                        if 전달인수: নেটওয়ার্ক_ইমেইল['arguments'] = 전달인수
                        প্রবাহ_মান.write((json.dumps(নেটওয়ার্ক_ইমেইল) + '\n').encode())
                        প্রবাহ_মান.flush()
                        while True:
                            উত্তর_দিন = json.loads(প্রবাহ_মান.readline())
                            if 'error' in উত্তর_দিন: raise AssertionError(উত্তর_দিন)
                            if 'return' in উত্তর_দিন: return উত্তর_দিন['return']
                    모의제어접속('qmp_capabilities')
                    স্ক্রিনশট = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(স্ক্রিনশট), 'format': 'ppm'})
                    def 예제들(পথ_2, 지점들):
                        with পথ_2.open('rb') as পেল্_ফাইল:
                            assert পেল্_ফাইল.readline().strip() == b'P6'
                            assert পেল্_ফাইল.readline().strip() == b'640 480'
                            assert পেল্_ফাইল.readline().strip() == b'255'
                            পেল্_ডাটা = পেল্_ফাইল.read()
                        assert len(পেল্_ডাটা) == 640 * 480 * 3
                        return [list(পেল্_ডাটা[(Y_বোতাম_অক্ষবিন্দু * 640 + X_বোতাম_অক্ষবিন্দু) * 3:(Y_বোতাম_অক্ষবিন্দু * 640 + X_বোতাম_অক্ষবিন্দু) * 3 + 3]) for X_বোতাম_অক্ষবিন্দু, Y_বোতাম_অক্ষবিন্দু in 지점들]
                    assert 예제들(স্ক্রিনশট, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(স্ক্রিনশট, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def পাঠান(누름값, 확인표시):
                        অফসেট_মান = len(대화기록)
                        প্রসেস.stdin.write(누름값); প্রসেস.stdin.flush()
                        표시까지받기(확인표시, অফসেট_মান)
                    পাঠান(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    পাঠান(b'\r', b'GUI ACTION 0 RESULT 0')
                    পাঠান(b'\t', b'GUI FOCUS 1')
                    পাঠান(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    পাঠান(b'\t', b'GUI FOCUS 2')
                    পাঠান(b'\r', b'GUI ACTION 2 RESULT 0')
                    পাঠান(b'\t', b'GUI FOCUS 3')
                    পাঠান(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    পাঠান(b'q', b'jkoros-native> ')
                    বৈধকরণ_রিপোর্ট['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            প্রসেস.wait(timeout=10)
            # framebuffer 응답뿐 아니라 প্রকৃত_ডাটা scanout 픽셀도 확인한다.
            with স্ক্রিনশট.open('rb') as ফাইল_ভুক্তি:
                assert ফাইল_ভুক্তি.readline().strip() == b'P6'
                치수 = ফাইল_ভুক্তি.readline().strip()
                assert 치수 == b'640 480', 치수
                assert ফাইল_ভুক্তি.readline().strip() == b'255'
                화소들 = ফাইল_ভুক্তি.read()
            assert len(화소들) == 640 * 480 * 3
            def পেল্(X_বোতাম_অক্ষবিন্দু, Y_বোতাম_অক্ষবিন্দু): return list(화소들[(Y_বোতাম_অক্ষবিন্দু * 640 + X_বোতাম_অক্ষবিন্দু) * 3:(Y_বোতাম_অক্ষবিন্দু * 640 + X_বোতাম_অক্ষবিন্দু) * 3 + 3])
            예제들 = {'background': পেল্(5, 5), 'panel': পেল্(45, 85), 'tile': পেল্(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            বৈধকরণ_রিপোর্ট.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((প্রকল্প_মূল / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if প্রসেস.poll() is None:
                প্রসেস.terminate()
                try: প্রসেস.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    প্রসেস.kill(); প্রসেস.wait(timeout=5)
            নির্বাচক.close()
            প্রসেস.stdin.close(); প্রসেস.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(বৈধকরণ_রিপোর্ট, indent=2) + '\n')


if __name__ == '__main__':
    চালনা()
