#!/usr/bin/env python3
"""တကယ့်ဒေတာ raspi4b စက်တင်, UART ဝင်ဒေတာ, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from စက်မောင်း import စီမံကိန်းအမြစ်, အမိန့်


def လုပ်ဆောင်():
    출력결과 = စီမံကိန်းအမြစ် / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    검증기록 = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as လုပ်ဆောင်လမ်း:
        모의제어경로 = Path(လုပ်ဆောင်လမ်း) / 'qmp.sock'
        အမိန့်ပေးအချက်များ = အမိန့်() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(လုပ်ဆောင်လမ်း) / 'vnc.sock')]
        검증기록['command'] = အမိန့်ပေးအချက်များ
        실행과정 = subprocess.Popen(အမိန့်ပေးအချက်များ, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        준비선택기 = selectors.DefaultSelector()
        준비선택기.register(실행과정.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, အရွေ့တန်ဖိုး=0, လုပ်ဆောင်မှုအချိန်လွန်=45):
            마감시각 = time.monotonic() + လုပ်ဆောင်မှုအချိန်လွန်
            while 확인표시 not in 대화기록[အရွေ့တန်ဖိုး:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in 준비선택기.select(0.2):
                    ဒေတာအတုံး = 누름값.fileobj.read(4096)
                    if ဒေတာအတုံး:
                        대화기록.extend(ဒေတာအတုံး)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if 실행과정.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(실행과정.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 လက်ရှိအချက်အလက်တစ်ခု 호스트에서도 VNC로 တကယ့်ဒေတာ GUI를 볼 ကိန်းတန်ဖိုး 있어야 한다.
            with socket.socket(socket.AF_UNIX) as မျက်နှာပြင်လက်ခံစက်:
                မျက်နှာပြင်လက်ခံစက်.settimeout(5); မျက်နှာပြင်လက်ခံစက်.connect(str(Path(လုပ်ဆောင်လမ်း) / 'vnc.sock'))
                def 정확한값(အရွယ်):
                    ရလဒ် = b''
                    while len(ရလဒ်) < အရွယ်:
                        အစိတ်အပိုင်း = မျက်နှာပြင်လက်ခံစက်.recv(အရွယ် - len(ရလဒ်))
                        if not အစိတ်အပိုင်း: raise AssertionError('VNC disconnected')
                        ရလဒ် += အစိတ်အပိုင်း
                    return ရလဒ်
                assert 정확한값(12) == b'RFB 003.008\n'
                မျက်နှာပြင်လက်ခံစက်.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); မျက်နှာပြင်လက်ခံစက်.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; မျက်နှာပြင်လက်ခံစက်.sendall(b'\x01')
                ဝန်ဆောင်စက်တန်ဖိုး = 정확한값(24)
                assert int.from_bytes(ဝန်ဆောင်စက်တန်ဖိုး[:2], 'big') == 640 and int.from_bytes(ဝန်ဆောင်စက်တန်ဖိုး[2:4], 'big') == 480
                정확한값(int.from_bytes(ဝန်ဆောင်စက်တန်ဖိုး[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for အမိန့်ဘိုက်, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', 'စမ်းသပ်မှု.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                အရွေ့တန်ဖိုး = len(대화기록)
                실행과정.stdin.write(အမိန့်ဘိုက် + b'\n')
                실행과정.stdin.flush()
                표시까지받기(b'jkoros-native> ', အရွေ့တန်ဖိုး)
                assert 확인표시 in 대화기록[အရွေ့တန်ဖိုး:], 확인표시
            def အမိန့်ဝင်း(စာကြောင်း, 예상결과):
                အရွေ့တန်ဖိုး = len(대화기록)
                실행과정.stdin.write(စာကြောင်း.encode('utf-8') + b'\n'); 실행과정.stdin.flush()
                표시까지받기(b'jkoros-native> ', အရွေ့တန်ဖိုး)
                응답자료 = bytes(대화기록[အရွေ့တန်ဖိုး:])
                for စာသား in 예상결과:
                    assert စာသား.encode('utf-8') in 응답자료, (စာကြောင်း, စာသား, 응답자료)
                return 응답자료
            def ဝင်(စာကြောင်း, အမိန့်တောင်းစာ):
                အရွေ့တန်ဖိုး = len(대화기록)
                실행과정.stdin.write(စာကြောင်း.encode('utf-8') + b'\n'); 실행과정.stdin.flush()
                표시까지받기(အမိန့်တောင်းစာ, အရွေ့တန်ဖိုး)
                return bytes(대화기록[အရွေ့တန်ဖိုး:])
            def တည်းဖြတ်တန်ဖိုး(အမည်, အကြောင်းအရာတန်ဖိုး, ပယ်ဖျက်လုပ်ငန်း=False):
                ဝင်('edit ' + အမည်, b'edit> ')
                for စာကြောင်း in အကြောင်းအရာတန်ဖိုး.splitlines(): ဝင်(စာကြောင်း, b'edit> ')
                if ပယ်ဖျက်လုပ်ငန်း:
                    အရွေ့တန်ဖိုး = len(대화기록)
                    실행과정.stdin.write(b'\x03'); 실행과정.stdin.flush()
                    표시까지받기(b'jkoros-native> ', အရွေ့တန်ဖိုး)
                    assert b'EDIT CANCELLED' in 대화기록[အရွေ့တန်ဖိုး:]
                else:
                    assert b'SAVED' in ဝင်('.', b'jkoros-native> ')
            def ဖိုင်တင်(အမည်, ဒေတာ):
                assert len(ဒေတာ) <= 16384
                ဝင်('load ' + အမည်, b'hex> ')
                for အစဉ်အမှတ် in range(0, len(ဒေတာ), 64): ဝင်(ဒေတာ[အစဉ်အမှတ်:အစဉ်အမှတ်+64].hex(), b'hex> ')
                assert b'LOADED' in ဝင်('.', b'jkoros-native> ')
            def ဆွဲယူ(အမည်):
                응답자료 = အမိန့်ဝင်း('hex ' + အမည်, ['HEX BEGIN', 'HEX END'])
                ဖြစ်သောညီ = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                ဒေတာ = bytes.fromhex(''.join(ဖြစ်သောညီ.group(2).decode('ascii').split()))
                assert len(ဒေတာ) == int(ဖြစ်သောညီ.group(1)); return ဒေတာ
            အမိန့်ဝင်း('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            အမိန့်ဝင်း('java -version', ['not OpenJDK', 'exit 0'])
            အမိန့်ဝင်း('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            အမိန့်ဝင်း('java Hello "한글 အချက်များ 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 အချက်များ 😀', 'exit 0'])
            အမိန့်ဝင်း('python --version', ['MicroPython 1.24.1', 'exit 0'])
            အမိန့်ဝင်း('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 ဖိုင်', 'exit 0'])
            အမိန့်ဝင်း('cat python.txt', ['한글 ဖိုင်'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            Javaအတန်း = 출력결과 / 'Hello.class'; Javaအတန်း.write_bytes(ဆွဲယူ('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 အချက်များ 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 အချက်များ 😀'], 예상결과
            တည်းဖြတ်တန်ဖိုး('နှုတ်ဆက်.java', 'public class နှုတ်ဆက် { public static void main(String[] args) { int တန်ဖိုး = 7; System.out.println("한글=" + တန်ဖိုး); } }')
            အမိန့်ဝင်း('javac နှုတ်ဆက်.java', ['Compiled: နှုတ်ဆက်.class', 'exit 0'])
            အမိန့်ဝင်း('java နှုတ်ဆက်', ['한글=7', 'exit 0'])
            (출력결과 / 'နှုတ်ဆက်.class').write_bytes(ဆွဲယူ('နှုတ်ဆက်.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'နှုတ်ဆက်']).decode().strip() == '한글=7'
            တည်းဖြတ်တန်ဖိုး('Hello.java', 'broken', ပယ်ဖျက်လုပ်ငန်း=True)
            အမိန့်ဝင်း('javac Hello.java', ['Compiled:', 'exit 0'])
            တည်းဖြတ်တန်ဖိုး('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            အမိန့်ဝင်း('javac Broken.java', ['javac error:', 'exit 1'])
            ဖိုင်တင်('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            အမိန့်ဝင်း('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            အမိန့်ဝင်း('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            ဖိုင်တင်('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            အမိန့်ဝင်း('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            အမိန့်ဝင်း('rm Imported.class', [])
            တည်းဖြတ်တန်ဖိုး('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            အမိန့်ဝင်း('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = အမိန့်ဝင်း('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            အမိန့်ဝင်း('rm Loop.java', []); အမိန့်ဝင်း('rm Loop.class', [])
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
            တည်းဖြတ်တန်ဖိုး('checks.py', 파이썬검사)
            အမိန့်ဝင်း('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            အမိန့်ဝင်း('rm checks.py', [])
            တည်းဖြတ်တန်ဖိုး('helper.py', 'value = 321')
            အမိန့်ဝင်း("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            အမိန့်ဝင်း('rm helper.py', [])
            အမိန့်ဝင်း("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            အမိန့်ဝင်း("python -c 'while True: pass'", ['exit -1004'])
            for အစဉ်အမှတ် in range(4):
                အမိန့်ဝင်း('python hello.py', ['한글 ဖိုင်', 'exit 0'])
                အမိန့်ဝင်း('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            ဖိုင်တင်('app.elf', (စီမံကိန်းအမြစ် / 'build/user/demo.elf').read_bytes())
            assert ဆွဲယူ('app.elf') == (စီမံကိန်းအမြစ် / 'build/user/demo.elf').read_bytes()
            အမိန့်ဝင်း('run app.elf', ['EL0 C++', 'exit 0'])
            ဖိုင်တင်('app.elf', b'not an ELF')
            အမိန့်ဝင်း('run app.elf', ['exit -8'])
            အမိန့်ဝင်း('rm app.elf', [])
            အမိန့်ဝင်း('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            ပုံရေးဆွဲမှုလမ်းကြောင်း = 출력결과 / 'java-framebuffer'; ပုံရေးဆွဲမှုလမ်းကြောင်း.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(စီမံကိန်းအမြစ် / 'dist/jkoros-native-korean.jar'), '-d', str(ပုံရေးဆွဲမှုလမ်းကြောင်း), str(စီမံကိန်းအမြစ် / 'စမ်းသပ်မှု/Java/မျက်နှာပြင်စမ်းသပ်.java')])
            ဖိုင်တင်('မျက်နှာပြင်စမ်းသပ်.class', (ပုံရေးဆွဲမှုလမ်းကြောင်း / 'မျက်နှာပြင်စမ်းသပ်.class').read_bytes())
            အမိန့်ဝင်း('java မျက်နှာပြင်စမ်းသပ်', ['မျက်နှာပြင် ဖြတ်နယ်ပယ် တန်ဖိုးငြင်းပယ်', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            အမိန့်ဝင်း('rm မျက်နှာပြင်စမ်းသပ်.class', [])
            with socket.socket(socket.AF_UNIX) as လက်ခံစက်:
                လက်ခံစက်.settimeout(10)
                လက်ခံစက်.connect(str(모의제어경로))
                with လက်ခံစက်.makefile('rwb') as စီးကြောင်းတန်ဖိုး:
                    နှုတ်ဆက် = json.loads(စီးကြောင်းတန်ဖိုး.readline())
                    def 모의제어접속(အလုပ်လုပ်ဆောင်, 전달인수=None):
                        ကွန်ရက်စာ = {'execute': အလုပ်လုပ်ဆောင်}
                        if 전달인수: ကွန်ရက်စာ['arguments'] = 전달인수
                        စီးကြောင်းတန်ဖိုး.write((json.dumps(ကွန်ရက်စာ) + '\n').encode())
                        စီးကြောင်းတန်ဖိုး.flush()
                        while True:
                            အကြောင်းပြန်ချက် = json.loads(စီးကြောင်းတန်ဖိုး.readline())
                            if 'error' in အကြောင်းပြန်ချက်: raise AssertionError(အကြောင်းပြန်ချက်)
                            if 'return' in အကြောင်းပြန်ချက်: return အကြောင်းပြန်ချက်['return']
                    모의제어접속('qmp_capabilities')
                    မျက်နှာပြင်ဖမ်းပုံ = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(မျက်နှာပြင်ဖမ်းပုံ), 'format': 'ppm'})
                    def 예제들(လမ်း, 지점들):
                        with လမ်း.open('rb') as ပုံမှတ်ဖိုင်:
                            assert ပုံမှတ်ဖိုင်.readline().strip() == b'P6'
                            assert ပုံမှတ်ဖိုင်.readline().strip() == b'640 480'
                            assert ပုံမှတ်ဖိုင်.readline().strip() == b'255'
                            ပုံမှတ်ဒေတာ = ပုံမှတ်ဖိုင်.read()
                        assert len(ပုံမှတ်ဒေတာ) == 640 * 480 * 3
                        return [list(ပုံမှတ်ဒေတာ[(yတည်နေရာအမှတ် * 640 + xတည်နေရာအမှတ်) * 3:(yတည်နေရာအမှတ် * 640 + xတည်နေရာအမှတ်) * 3 + 3]) for xတည်နေရာအမှတ်, yတည်နေရာအမှတ် in 지점들]
                    assert 예제들(မျက်နှာပြင်ဖမ်းပုံ, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(မျက်နှာပြင်ဖမ်းပုံ, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def ပို့(누름값, 확인표시):
                        အရွေ့တန်ဖိုး = len(대화기록)
                        실행과정.stdin.write(누름값); 실행과정.stdin.flush()
                        표시까지받기(확인표시, အရွေ့တန်ဖိုး)
                    ပို့(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    ပို့(b'\r', b'GUI ACTION 0 RESULT 0')
                    ပို့(b'\t', b'GUI FOCUS 1')
                    ပို့(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    ပို့(b'\t', b'GUI FOCUS 2')
                    ပို့(b'\r', b'GUI ACTION 2 RESULT 0')
                    ပို့(b'\t', b'GUI FOCUS 3')
                    ပို့(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    ပို့(b'q', b'jkoros-native> ')
                    검증기록['qemu'] = နှုတ်ဆက်['QMP']['version']
                    모의제어접속('quit')
            실행과정.wait(timeout=10)
            # framebuffer 응답뿐 아니라 တကယ့်ဒေတာ scanout 픽셀도 확인한다.
            with မျက်နှာပြင်ဖမ်းပုံ.open('rb') as ဖိုင်အချက်:
                assert ဖိုင်အချက်.readline().strip() == b'P6'
                치수 = ဖိုင်အချက်.readline().strip()
                assert 치수 == b'640 480', 치수
                assert ဖိုင်အချက်.readline().strip() == b'255'
                화소들 = ဖိုင်အချက်.read()
            assert len(화소들) == 640 * 480 * 3
            def ပုံမှတ်(xတည်နေရာအမှတ်, yတည်နေရာအမှတ်): return list(화소들[(yတည်နေရာအမှတ် * 640 + xတည်နေရာအမှတ်) * 3:(yတည်နေရာအမှတ် * 640 + xတည်နေရာအမှတ်) * 3 + 3])
            예제들 = {'background': ပုံမှတ်(5, 5), 'panel': ပုံမှတ်(45, 85), 'tile': ပုံမှတ်(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            검증기록.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((စီမံကိန်းအမြစ် / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if 실행과정.poll() is None:
                실행과정.terminate()
                try: 실행과정.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    실행과정.kill(); 실행과정.wait(timeout=5)
            준비선택기.close()
            실행과정.stdin.close(); 실행과정.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(검증기록, indent=2) + '\n')


if __name__ == '__main__':
    လုပ်ဆောင်()
