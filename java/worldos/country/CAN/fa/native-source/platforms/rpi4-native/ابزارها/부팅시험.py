#!/usr/bin/env python3
"""واقعی_داده_ها raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from اجرا_فرمان import نمایش_دادن_جذر, فرمان


def اجرا_2():
    출력결과 = نمایش_دادن_جذر / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    اعتبارسنجی_گزارش = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = فرمان() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        اعتبارسنجی_گزارش['command'] = 명령인수
        فرآیند = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        انتخاب_کننده = selectors.DefaultSelector()
        انتخاب_کننده.register(فرآیند.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, جابجایی_لایه_ای_مقدار=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[جابجایی_لایه_ای_مقدار:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in انتخاب_کننده.select(0.2):
                    داده_ها_مسدود_کردن = 누름값.fileobj.read(4096)
                    if داده_ها_مسدود_کردن:
                        대화기록.extend(داده_ها_مسدود_کردن)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if فرآیند.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(فرآیند.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 واقعی_داده_ها GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(اندازه):
                    سنجش = b''
                    while len(سنجش) < اندازه:
                        조각 = 화면접속자.recv(اندازه - len(سنجش))
                        if not 조각: raise AssertionError('VNC disconnected')
                        سنجش += 조각
                    return سنجش
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                سرور_مقدار = 정확한값(24)
                assert int.from_bytes(سرور_مقدار[:2], 'big') == 640 and int.from_bytes(سرور_مقدار[2:4], 'big') == 480
                정확한값(int.from_bytes(سرور_مقدار[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for فرمان_بایت, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                جابجایی_لایه_ای_مقدار = len(대화기록)
                فرآیند.stdin.write(فرمان_بایت + b'\n')
                فرآیند.stdin.flush()
                표시까지받기(b'jkoros-native> ', جابجایی_لایه_ای_مقدار)
                assert 확인표시 in 대화기록[جابجایی_لایه_ای_مقدار:], 확인표시
            def واسط(خط, 예상결과):
                جابجایی_لایه_ای_مقدار = len(대화기록)
                فرآیند.stdin.write(خط.encode('utf-8') + b'\n'); فرآیند.stdin.flush()
                표시까지받기(b'jkoros-native> ', جابجایی_لایه_ای_مقدار)
                응답자료 = bytes(대화기록[جابجایی_لایه_ای_مقدار:])
                for متن in 예상결과:
                    assert متن.encode('utf-8') in 응답자료, (خط, متن, 응답자료)
                return 응답자료
            def وارد_کردن(خط, فرمان_1dd14da4):
                جابجایی_لایه_ای_مقدار = len(대화기록)
                فرآیند.stdin.write(خط.encode('utf-8') + b'\n'); فرآیند.stdin.flush()
                표시까지받기(فرمان_1dd14da4, جابجایی_لایه_ای_مقدار)
                return bytes(대화기록[جابجایی_لایه_ای_مقدار:])
            def ویرایش_مقدار(نام, محتوا_مقدار, لغو_عملیات=False):
                وارد_کردن('edit ' + نام, b'edit> ')
                for خط in محتوا_مقدار.splitlines(): وارد_کردن(خط, b'edit> ')
                if لغو_عملیات:
                    جابجایی_لایه_ای_مقدار = len(대화기록)
                    فرآیند.stdin.write(b'\x03'); فرآیند.stdin.flush()
                    표시까지받기(b'jkoros-native> ', جابجایی_لایه_ای_مقدار)
                    assert b'EDIT CANCELLED' in 대화기록[جابجایی_لایه_ای_مقدار:]
                else:
                    assert b'SAVED' in وارد_کردن('.', b'jkoros-native> ')
            def آپلود_فایل(نام, داده_ها):
                assert len(داده_ها) <= 16384
                وارد_کردن('load ' + نام, b'hex> ')
                for 순번 in range(0, len(داده_ها), 64): وارد_کردن(داده_ها[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in وارد_کردن('.', b'jkoros-native> ')
            def دانلود(نام):
                응답자료 = واسط('hex ' + نام, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                داده_ها = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(داده_ها) == int(일치.group(1)); return داده_ها
            واسط('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            واسط('java -version', ['not OpenJDK', 'exit 0'])
            واسط('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            واسط('java Hello "한글 نشانوندها 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 نشانوندها 😀', 'exit 0'])
            واسط('python --version', ['MicroPython 1.24.1', 'exit 0'])
            واسط('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 پرونده', 'exit 0'])
            واسط('cat python.txt', ['한글 پرونده'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(دانلود('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 نشانوندها 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 نشانوندها 😀'], 예상결과
            ویرایش_مقدار('인사.java', 'public class 인사 { public static void main(String[] args) { int مقدار = 7; System.out.println("한글=" + مقدار); } }')
            واسط('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            واسط('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(دانلود('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            ویرایش_مقدار('Hello.java', 'broken', لغو_عملیات=True)
            واسط('javac Hello.java', ['Compiled:', 'exit 0'])
            ویرایش_مقدار('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            واسط('javac Broken.java', ['javac error:', 'exit 1'])
            آپلود_فایل('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            واسط('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            واسط('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            آپلود_فایل('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            واسط('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            واسط('rm Imported.class', [])
            ویرایش_مقدار('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            واسط('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = واسط('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            واسط('rm Loop.java', []); واسط('rm Loop.class', [])
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
            ویرایش_مقدار('checks.py', 파이썬검사)
            واسط('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            واسط('rm checks.py', [])
            ویرایش_مقدار('helper.py', 'value = 321')
            واسط("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            واسط('rm helper.py', [])
            واسط("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            واسط("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                واسط('python hello.py', ['한글 پرونده', 'exit 0'])
                واسط('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            آپلود_فایل('app.elf', (نمایش_دادن_جذر / 'build/user/demo.elf').read_bytes())
            assert دانلود('app.elf') == (نمایش_دادن_جذر / 'build/user/demo.elf').read_bytes()
            واسط('run app.elf', ['EL0 C++', 'exit 0'])
            آپلود_فایل('app.elf', b'not an ELF')
            واسط('run app.elf', ['exit -8'])
            واسط('rm app.elf', [])
            واسط('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            نقاشی_مسیر = 출력결과 / 'java-framebuffer'; نقاشی_مسیر.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(نمایش_دادن_جذر / 'dist/jkoros-native-korean.jar'), '-d', str(نقاشی_مسیر), str(نمایش_دادن_جذر / '시험/자바/화면시험.java')])
            آپلود_فایل('화면시험.class', (نقاشی_مسیر / '화면시험.class').read_bytes())
            واسط('java 화면시험', ['화면 کلیپ رد_کردن_مقدار', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            واسط('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as سرویس_گیرنده:
                سرویس_گیرنده.settimeout(10)
                سرویس_گیرنده.connect(str(모의제어경로))
                with سرویس_گیرنده.makefile('rwb') as جریان_مقدار:
                    인사 = json.loads(جریان_مقدار.readline())
                    def 모의제어접속(اجرا, 전달인수=None):
                        شبکه_پیام = {'execute': اجرا}
                        if 전달인수: شبکه_پیام['arguments'] = 전달인수
                        جریان_مقدار.write((json.dumps(شبکه_پیام) + '\n').encode())
                        جریان_مقدار.flush()
                        while True:
                            پاسخ_دادن = json.loads(جریان_مقدار.readline())
                            if 'error' in پاسخ_دادن: raise AssertionError(پاسخ_دادن)
                            if 'return' in پاسخ_دادن: return پاسخ_دادن['return']
                    모의제어접속('qmp_capabilities')
                    برش_صفحه = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(برش_صفحه), 'format': 'ppm'})
                    def 예제들(مسیر, 지점들):
                        with مسیر.open('rb') as پیکسل_فایل:
                            assert پیکسل_فایل.readline().strip() == b'P6'
                            assert پیکسل_فایل.readline().strip() == b'640 480'
                            assert پیکسل_فایل.readline().strip() == b'255'
                            پیکسل_داده_ها = پیکسل_فایل.read()
                        assert len(پیکسل_داده_ها) == 640 * 480 * 3
                        return [list(پیکسل_داده_ها[(دکمه_Y_مختصات * 640 + مختصات_x) * 3:(دکمه_Y_مختصات * 640 + مختصات_x) * 3 + 3]) for مختصات_x, دکمه_Y_مختصات in 지점들]
                    assert 예제들(برش_صفحه, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(برش_صفحه, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def ارسال(누름값, 확인표시):
                        جابجایی_لایه_ای_مقدار = len(대화기록)
                        فرآیند.stdin.write(누름값); فرآیند.stdin.flush()
                        표시까지받기(확인표시, جابجایی_لایه_ای_مقدار)
                    ارسال(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    ارسال(b'\r', b'GUI ACTION 0 RESULT 0')
                    ارسال(b'\t', b'GUI FOCUS 1')
                    ارسال(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    ارسال(b'\t', b'GUI FOCUS 2')
                    ارسال(b'\r', b'GUI ACTION 2 RESULT 0')
                    ارسال(b'\t', b'GUI FOCUS 3')
                    ارسال(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    ارسال(b'q', b'jkoros-native> ')
                    اعتبارسنجی_گزارش['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            فرآیند.wait(timeout=10)
            # framebuffer 응답뿐 아니라 واقعی_داده_ها scanout 픽셀도 확인한다.
            with برش_صفحه.open('rb') as فایل_ورودی:
                assert فایل_ورودی.readline().strip() == b'P6'
                치수 = فایل_ورودی.readline().strip()
                assert 치수 == b'640 480', 치수
                assert فایل_ورودی.readline().strip() == b'255'
                화소들 = فایل_ورودی.read()
            assert len(화소들) == 640 * 480 * 3
            def پیکسل(مختصات_x, دکمه_Y_مختصات): return list(화소들[(دکمه_Y_مختصات * 640 + مختصات_x) * 3:(دکمه_Y_مختصات * 640 + مختصات_x) * 3 + 3])
            예제들 = {'background': پیکسل(5, 5), 'panel': پیکسل(45, 85), 'tile': پیکسل(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            اعتبارسنجی_گزارش.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((نمایش_دادن_جذر / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if فرآیند.poll() is None:
                فرآیند.terminate()
                try: فرآیند.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    فرآیند.kill(); فرآیند.wait(timeout=5)
            انتخاب_کننده.close()
            فرآیند.stdin.close(); فرآیند.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(اعتبارسنجی_گزارش, indent=2) + '\n')


if __name__ == '__main__':
    اجرا_2()
