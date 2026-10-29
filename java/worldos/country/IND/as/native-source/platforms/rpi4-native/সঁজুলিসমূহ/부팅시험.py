#!/usr/bin/env python3
"""প্ৰকৃত_ডাটা raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from নিষ্পাদন_আদেশ import 기준, কমান্ড


def সঞ্চালন():
    출력결과 = 기준 / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    বৈধতা_ৰিপ_ৰ্ট = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = কমান্ড() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        বৈধতা_ৰিপ_ৰ্ট['command'] = 명령인수
        প্ৰসেস = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        চয়নকাৰী = selectors.DefaultSelector()
        চয়নকাৰী.register(প্ৰসেস.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, অফছেট_মান=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[অফছেট_মান:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in চয়নকাৰী.select(0.2):
                    ডাটা_অৱৰুদ্ধ_কৰক = 누름값.fileobj.read(4096)
                    if ডাটা_অৱৰুদ্ধ_কৰক:
                        대화기록.extend(ডাটা_অৱৰুদ্ধ_কৰক)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if প্ৰসেস.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(প্ৰসেস.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 প্ৰকৃত_ডাটা GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(মাপ):
                    পৰিমাপ = b''
                    while len(পৰিমাপ) < মাপ:
                        조각 = 화면접속자.recv(মাপ - len(পৰিমাপ))
                        if not 조각: raise AssertionError('VNC disconnected')
                        পৰিমাপ += 조각
                    return পৰিমাপ
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                ছাৰ্ভাৰ_মান = 정확한값(24)
                assert int.from_bytes(ছাৰ্ভাৰ_মান[:2], 'big') == 640 and int.from_bytes(ছাৰ্ভাৰ_মান[2:4], 'big') == 480
                정확한값(int.from_bytes(ছাৰ্ভাৰ_মান[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for আদেশ_বাইট, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                অফছেট_মান = len(대화기록)
                প্ৰসেস.stdin.write(আদেশ_বাইট + b'\n')
                প্ৰসেস.stdin.flush()
                표시까지받기(b'jkoros-native> ', অফছেট_মান)
                assert 확인표시 in 대화기록[অফছেট_মান:], 확인표시
            def শ্বেল(লাইন, 예상결과):
                অফছেট_মান = len(대화기록)
                প্ৰসেস.stdin.write(লাইন.encode('utf-8') + b'\n'); প্ৰসেস.stdin.flush()
                표시까지받기(b'jkoros-native> ', অফছেট_মান)
                응답자료 = bytes(대화기록[অফছেট_মান:])
                for টেক্সট in 예상결과:
                    assert টেক্সট.encode('utf-8') in 응답자료, (লাইন, টেক্সট, 응답자료)
                return 응답자료
            def প্ৰৱেশ_কৰক(লাইন, সংকেত):
                অফছেট_মান = len(대화기록)
                প্ৰসেস.stdin.write(লাইন.encode('utf-8') + b'\n'); প্ৰসেস.stdin.flush()
                표시까지받기(সংকেত, অফছেট_মান)
                return bytes(대화기록[অফছেট_মান:])
            def সম্পাদনা_মান(নাম, সামগ্ৰী_মান, বাতিল_কৰক_অপাৰেচন=False):
                প্ৰৱেশ_কৰক('edit ' + নাম, b'edit> ')
                for লাইন in সামগ্ৰী_মান.splitlines(): প্ৰৱেশ_কৰক(লাইন, b'edit> ')
                if বাতিল_কৰক_অপাৰেচন:
                    অফছেট_মান = len(대화기록)
                    প্ৰসেস.stdin.write(b'\x03'); প্ৰসেস.stdin.flush()
                    표시까지받기(b'jkoros-native> ', অফছেট_মান)
                    assert b'EDIT CANCELLED' in 대화기록[অফছেট_মান:]
                else:
                    assert b'SAVED' in প্ৰৱেশ_কৰক('.', b'jkoros-native> ')
            def আপল_ড_কৰক_ফাইলসমূহ(নাম, ডাটা):
                assert len(ডাটা) <= 16384
                প্ৰৱেশ_কৰক('load ' + নাম, b'hex> ')
                for 순번 in range(0, len(ডাটা), 64): প্ৰৱেশ_কৰক(ডাটা[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in প্ৰৱেশ_কৰক('.', b'jkoros-native> ')
            def ডাউনলোড(নাম):
                응답자료 = শ্বেল('hex ' + নাম, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                ডাটা = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(ডাটা) == int(일치.group(1)); return ডাটা
            শ্বেল('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            শ্বেল('java -version', ['not OpenJDK', 'exit 0'])
            শ্বেল('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            শ্বেল('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            শ্বেল('python --version', ['MicroPython 1.24.1', 'exit 0'])
            শ্বেল('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 নথিপত্ৰ', 'exit 0'])
            শ্বেল('cat python.txt', ['한글 নথিপত্ৰ'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(ডাউনলোড('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            সম্পাদনা_মান('인사.java', 'public class 인사 { public static void main(String[] args) { int মান = 7; System.out.println("한글=" + মান); } }')
            শ্বেল('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            শ্বেল('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(ডাউনলোড('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            সম্পাদনা_মান('Hello.java', 'broken', বাতিল_কৰক_অপাৰেচন=True)
            শ্বেল('javac Hello.java', ['Compiled:', 'exit 0'])
            সম্পাদনা_মান('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            শ্বেল('javac Broken.java', ['javac error:', 'exit 1'])
            আপল_ড_কৰক_ফাইলসমূহ('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            শ্বেল('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            শ্বেল('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            আপল_ড_কৰক_ফাইলসমূহ('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            শ্বেল('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            শ্বেল('rm Imported.class', [])
            সম্পাদনা_মান('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            শ্বেল('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = শ্বেল('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            শ্বেল('rm Loop.java', []); শ্বেল('rm Loop.class', [])
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
            সম্পাদনা_মান('checks.py', 파이썬검사)
            শ্বেল('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            শ্বেল('rm checks.py', [])
            সম্পাদনা_মান('helper.py', 'value = 321')
            শ্বেল("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            শ্বেল('rm helper.py', [])
            শ্বেল("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            শ্বেল("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                শ্বেল('python hello.py', ['한글 নথিপত্ৰ', 'exit 0'])
                শ্বেল('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            আপল_ড_কৰক_ফাইলসমূহ('app.elf', (기준 / 'build/user/demo.elf').read_bytes())
            assert ডাউনলোড('app.elf') == (기준 / 'build/user/demo.elf').read_bytes()
            শ্বেল('run app.elf', ['EL0 C++', 'exit 0'])
            আপল_ড_কৰক_ফাইলসমূহ('app.elf', b'not an ELF')
            শ্বেল('run app.elf', ['exit -8'])
            শ্বেল('rm app.elf', [])
            শ্বেল('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            অংকন_পথ = 출력결과 / 'java-framebuffer'; অংকন_পথ.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준 / 'dist/jkoros-native-korean.jar'), '-d', str(অংকন_পথ), str(기준 / '시험/자바/화면시험.java')])
            আপল_ড_কৰক_ফাইলসমূহ('화면시험.class', (অংকন_পথ / '화면시험.class').read_bytes())
            শ্বেল('java 화면시험', ['화면 ক্লিপ 거부', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            শ্বেল('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as ক্লায়েণ্ট:
                ক্লায়েণ্ট.settimeout(10)
                ক্লায়েণ্ট.connect(str(모의제어경로))
                with ক্লায়েণ্ট.makefile('rwb') as ষ্ট্ৰিম_মান:
                    인사 = json.loads(ষ্ট্ৰিম_মান.readline())
                    def 모의제어접속(চলাওক, 전달인수=None):
                        নেটৱৰ্ক_বাৰ্তা = {'execute': চলাওক}
                        if 전달인수: নেটৱৰ্ক_বাৰ্তা['arguments'] = 전달인수
                        ষ্ট্ৰিম_মান.write((json.dumps(নেটৱৰ্ক_বাৰ্তা) + '\n').encode())
                        ষ্ট্ৰিম_মান.flush()
                        while True:
                            প্ৰত্যুত্তৰ_দিয়ক = json.loads(ষ্ট্ৰিম_মান.readline())
                            if 'error' in প্ৰত্যুত্তৰ_দিয়ক: raise AssertionError(প্ৰত্যুত্তৰ_দিয়ক)
                            if 'return' in প্ৰত্যুত্তৰ_দিয়ক: return প্ৰত্যুত্তৰ_দিয়ক['return']
                    모의제어접속('qmp_capabilities')
                    স্ক্ৰীণ_ক্লিপিং = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(স্ক্ৰীণ_ক্লিপিং), 'format': 'ppm'})
                    def 예제들(পথ, 지점들):
                        with পথ.open('rb') as পিক্সেল_ফাইল:
                            assert পিক্সেল_ফাইল.readline().strip() == b'P6'
                            assert পিক্সেল_ফাইল.readline().strip() == b'640 480'
                            assert পিক্সেল_ফাইল.readline().strip() == b'255'
                            পিক্সেল_ডাটা = পিক্সেল_ফাইল.read()
                        assert len(পিক্সেল_ডাটা) == 640 * 480 * 3
                        return [list(পিক্সেল_ডাটা[(세로좌표 * 640 + x_ক_ৰ্ডিনেট) * 3:(세로좌표 * 640 + x_ক_ৰ্ডিনেট) * 3 + 3]) for x_ক_ৰ্ডিনেট, 세로좌표 in 지점들]
                    assert 예제들(স্ক্ৰীণ_ক্লিপিং, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(স্ক্ৰীণ_ক্লিপিং, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def ই_মেইল_কৰক(누름값, 확인표시):
                        অফছেট_মান = len(대화기록)
                        প্ৰসেস.stdin.write(누름값); প্ৰসেস.stdin.flush()
                        표시까지받기(확인표시, অফছেট_মান)
                    ই_মেইল_কৰক(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    ই_মেইল_কৰক(b'\r', b'GUI ACTION 0 RESULT 0')
                    ই_মেইল_কৰক(b'\t', b'GUI FOCUS 1')
                    ই_মেইল_কৰক(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    ই_মেইল_কৰক(b'\t', b'GUI FOCUS 2')
                    ই_মেইল_কৰক(b'\r', b'GUI ACTION 2 RESULT 0')
                    ই_মেইল_কৰক(b'\t', b'GUI FOCUS 3')
                    ই_মেইল_কৰক(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    ই_মেইল_কৰক(b'q', b'jkoros-native> ')
                    বৈধতা_ৰিপ_ৰ্ট['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            প্ৰসেস.wait(timeout=10)
            # framebuffer 응답뿐 아니라 প্ৰকৃত_ডাটা scanout 픽셀도 확인한다.
            with স্ক্ৰীণ_ক্লিপিং.open('rb') as ফাইল_প্রবিষ্ট:
                assert ফাইল_প্রবিষ্ট.readline().strip() == b'P6'
                치수 = ফাইল_প্রবিষ্ট.readline().strip()
                assert 치수 == b'640 480', 치수
                assert ফাইল_প্রবিষ্ট.readline().strip() == b'255'
                화소들 = ফাইল_প্রবিষ্ট.read()
            assert len(화소들) == 640 * 480 * 3
            def পিক্সেল(x_ক_ৰ্ডিনেট, 세로좌표): return list(화소들[(세로좌표 * 640 + x_ক_ৰ্ডিনেট) * 3:(세로좌표 * 640 + x_ক_ৰ্ডিনেট) * 3 + 3])
            예제들 = {'background': পিক্সেল(5, 5), 'panel': পিক্সেল(45, 85), 'tile': পিক্সেল(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            বৈধতা_ৰিপ_ৰ্ট.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
            if প্ৰসেস.poll() is None:
                প্ৰসেস.terminate()
                try: প্ৰসেস.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    প্ৰসেস.kill(); প্ৰসেস.wait(timeout=5)
            চয়নকাৰী.close()
            প্ৰসেস.stdin.close(); প্ৰসেস.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(বৈধতা_ৰিপ_ৰ্ট, indent=2) + '\n')


if __name__ == '__main__':
    সঞ্চালন()
