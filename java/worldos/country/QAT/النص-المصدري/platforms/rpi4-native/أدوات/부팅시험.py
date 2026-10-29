#!/usr/bin/env python3
"""الفعلي_بيانات raspi4b إقلاع_الآلة, UART إدخال_قيمة, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from ينفذ_أمر import يعرض_جذر, أمر


def تشغيل():
    الناتج = يعرض_جذر / 'build/verification'
    الناتج.mkdir(parents=True, exist_ok=True)
    نسخة_مكتوبة = bytearray()
    التحقق_من_صحة_إبلاغ = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = أمر() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        التحقق_من_صحة_إبلاغ['command'] = 명령인수
        عملية = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        محدد = selectors.DefaultSelector()
        محدد.register(عملية.stdout, selectors.EVENT_READ)
        def 표시까지받기(علامة, إزاحة_قيمة=0, 시간제한=45):
            موعد_نهائي_وقت = time.monotonic() + 시간제한
            while علامة not in نسخة_مكتوبة[إزاحة_قيمة:]:
                if time.monotonic() > موعد_نهائي_وقت:
                    raise AssertionError('UART timeout: ' + repr(علامة))
                for 누름값, _ in محدد.select(0.2):
                    بيانات_حظر = 누름값.fileobj.read(4096)
                    if بيانات_حظر:
                        نسخة_مكتوبة.extend(بيانات_حظر)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', نسخة_مكتوبة):
                    raise AssertionError('kernel failure')
                if عملية.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(عملية.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for علامة in 확인표시들:
                assert علامة in نسخة_مكتوبة, علامة
            # GTK 없는 حديث_عنصر 호스트에서도 VNC로 الفعلي_بيانات GUI를 볼 رقم 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(حجم):
                    نتيجة = b''
                    while len(نتيجة) < حجم:
                        조각 = 화면접속자.recv(حجم - len(نتيجة))
                        if not 조각: raise AssertionError('VNC disconnected')
                        نتيجة += 조각
                    return نتيجة
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                خادم_قيمة = 정확한값(24)
                assert int.from_bytes(خادم_قيمة[:2], 'big') == 640 and int.from_bytes(خادم_قيمة[2:4], 'big') == 480
                정확한값(int.from_bytes(خادم_قيمة[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for أمر_بايت, علامة in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', 'اختبارات.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                إزاحة_قيمة = len(نسخة_مكتوبة)
                عملية.stdin.write(أمر_بايت + b'\n')
                عملية.stdin.flush()
                표시까지받기(b'jkoros-native> ', إزاحة_قيمة)
                assert علامة in نسخة_مكتوبة[إزاحة_قيمة:], علامة
            def 셸(سطر, 예상결과):
                إزاحة_قيمة = len(نسخة_مكتوبة)
                عملية.stdin.write(سطر.encode('utf-8') + b'\n'); عملية.stdin.flush()
                표시까지받기(b'jkoros-native> ', إزاحة_قيمة)
                رد_1262b476 = bytes(نسخة_مكتوبة[إزاحة_قيمة:])
                for نص in 예상결과:
                    assert نص.encode('utf-8') in رد_1262b476, (سطر, نص, رد_1262b476)
                return رد_1262b476
            def يدخل(سطر, طلب_1dd14da4):
                إزاحة_قيمة = len(نسخة_مكتوبة)
                عملية.stdin.write(سطر.encode('utf-8') + b'\n'); عملية.stdin.flush()
                표시까지받기(طلب_1dd14da4, إزاحة_قيمة)
                return bytes(نسخة_مكتوبة[إزاحة_قيمة:])
            def يحرر_قيمة(اسم, محتوى_قيمة, يلغي_تشغيل=False):
                يدخل('edit ' + اسم, b'edit> ')
                for سطر in محتوى_قيمة.splitlines(): يدخل(سطر, b'edit> ')
                if يلغي_تشغيل:
                    إزاحة_قيمة = len(نسخة_مكتوبة)
                    عملية.stdin.write(b'\x03'); عملية.stdin.flush()
                    표시까지받기(b'jkoros-native> ', إزاحة_قيمة)
                    assert b'EDIT CANCELLED' in نسخة_مكتوبة[إزاحة_قيمة:]
                else:
                    assert b'SAVED' in يدخل('.', b'jkoros-native> ')
            def تحميل_الملفات(اسم, بيانات):
                assert len(بيانات) <= 16384
                يدخل('load ' + اسم, b'hex> ')
                for 순번 in range(0, len(بيانات), 64): يدخل(بيانات[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in يدخل('.', b'jkoros-native> ')
            def تنزيل(اسم):
                رد_1262b476 = 셸('hex ' + اسم, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', رد_1262b476, re.S)
                بيانات = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(بيانات) == int(일치.group(1)); return بيانات
            셸('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            셸('java -version', ['not OpenJDK', 'exit 0'])
            셸('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            셸('java Hello "한글 وسائط 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 وسائط 😀', 'exit 0'])
            셸('python --version', ['MicroPython 1.24.1', 'exit 0'])
            셸('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 ملف', 'exit 0'])
            셸('cat python.txt', ['한글 ملف'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = الناتج / 'Hello.class'; 자바클래스.write_bytes(تنزيل('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(الناتج), 'Hello', '한글 وسائط 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 وسائط 😀'], 예상결과
            يحرر_قيمة('인사.java', 'public class 인사 { public static void main(String[] args) { int قيمة = 7; System.out.println("한글=" + قيمة); } }')
            셸('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            셸('java 인사', ['한글=7', 'exit 0'])
            (الناتج / '인사.class').write_bytes(تنزيل('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(الناتج), '인사']).decode().strip() == '한글=7'
            يحرر_قيمة('Hello.java', 'broken', يلغي_تشغيل=True)
            셸('javac Hello.java', ['Compiled:', 'exit 0'])
            يحرر_قيمة('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            셸('javac Broken.java', ['javac error:', 'exit 1'])
            تحميل_الملفات('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            셸('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            셸('rm Broken.java', [])
            들여온파일 = الناتج / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            تحميل_الملفات('Imported.class', (الناتج / 'Imported.class').read_bytes())
            셸('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            셸('rm Imported.class', [])
            يحرر_قيمة('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            셸('javac Loop.java', ['Compiled:', 'exit 0'])
            رد_1262b476 = 셸('java Loop', ['exit '])
            assert b'instruction limit' in رد_1262b476 or b'exit -1004' in رد_1262b476
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
            يحرر_قيمة('checks.py', 파이썬검사)
            셸('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            셸('rm checks.py', [])
            يحرر_قيمة('helper.py', 'value = 321')
            셸("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            셸('rm helper.py', [])
            셸("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            셸("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                셸('python hello.py', ['한글 ملف', 'exit 0'])
                셸('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            تحميل_الملفات('app.elf', (يعرض_جذر / 'build/user/demo.elf').read_bytes())
            assert تنزيل('app.elf') == (يعرض_جذر / 'build/user/demo.elf').read_bytes()
            셸('run app.elf', ['EL0 C++', 'exit 0'])
            تحميل_الملفات('app.elf', b'not an ELF')
            셸('run app.elf', ['exit -8'])
            셸('rm app.elf', [])
            셸('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            رسم_مسار = الناتج / 'java-framebuffer'; رسم_مسار.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(يعرض_جذر / 'dist/jkoros-native-korean.jar'), '-d', str(رسم_مسار), str(يعرض_جذر / 'اختبارات/자바/화면시험.java')])
            تحميل_الملفات('화면시험.class', (رسم_مسار / '화면시험.class').read_bytes())
            셸('java 화면시험', ['화면 يقص يرفض_قيمة', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            셸('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as عميل:
                عميل.settimeout(10)
                عميل.connect(str(모의제어경로))
                with عميل.makefile('rwb') as بث_قيمة:
                    인사 = json.loads(بث_قيمة.readline())
                    def 모의제어접속(تنفيذ, 전달인수=None):
                        شبكة_رسالة = {'execute': تنفيذ}
                        if 전달인수: شبكة_رسالة['arguments'] = 전달인수
                        بث_قيمة.write((json.dumps(شبكة_رسالة) + '\n').encode())
                        بث_قيمة.flush()
                        while True:
                            رد = json.loads(بث_قيمة.readline())
                            if 'error' in رد: raise AssertionError(رد)
                            if 'return' in رد: return رد['return']
                    모의제어접속('qmp_capabilities')
                    لقطة_شاشة = الناتج / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(لقطة_شاشة), 'format': 'ppm'})
                    def 예제들(مسار, 지점들):
                        with مسار.open('rb') as عنصر_صورة_ملف:
                            assert عنصر_صورة_ملف.readline().strip() == b'P6'
                            assert عنصر_صورة_ملف.readline().strip() == b'640 480'
                            assert عنصر_صورة_ملف.readline().strip() == b'255'
                            عنصر_صورة_بيانات = عنصر_صورة_ملف.read()
                        assert len(عنصر_صورة_بيانات) == 640 * 480 * 3
                        return [list(عنصر_صورة_بيانات[(الزر_Y_إحداثيات * 640 + الإحداثي_س) * 3:(الزر_Y_إحداثيات * 640 + الإحداثي_س) * 3 + 3]) for الإحداثي_س, الزر_Y_إحداثيات in 지점들]
                    assert 예제들(لقطة_شاشة, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(لقطة_شاشة, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def يرسل(누름값, علامة):
                        إزاحة_قيمة = len(نسخة_مكتوبة)
                        عملية.stdin.write(누름값); عملية.stdin.flush()
                        표시까지받기(علامة, إزاحة_قيمة)
                    يرسل(b'gui\n', b'GUI READY:')
                    첫화면 = الناتج / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(الناتج / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    يرسل(b'\r', b'GUI ACTION 0 RESULT 0')
                    يرسل(b'\t', b'GUI FOCUS 1')
                    يرسل(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = الناتج / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(الناتج / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    يرسل(b'\t', b'GUI FOCUS 2')
                    يرسل(b'\r', b'GUI ACTION 2 RESULT 0')
                    يرسل(b'\t', b'GUI FOCUS 3')
                    يرسل(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(الناتج / 'gui-python.png'), 'format': 'png'})
                    يرسل(b'q', b'jkoros-native> ')
                    التحقق_من_صحة_إبلاغ['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            عملية.wait(timeout=10)
            # framebuffer 응답뿐 아니라 الفعلي_بيانات scanout 픽셀도 확인한다.
            with لقطة_شاشة.open('rb') as ملف_إدخال_3d0c1245:
                assert ملف_إدخال_3d0c1245.readline().strip() == b'P6'
                치수 = ملف_إدخال_3d0c1245.readline().strip()
                assert 치수 == b'640 480', 치수
                assert ملف_إدخال_3d0c1245.readline().strip() == b'255'
                화소들 = ملف_إدخال_3d0c1245.read()
            assert len(화소들) == 640 * 480 * 3
            def عنصر_صورة(الإحداثي_س, الزر_Y_إحداثيات): return list(화소들[(الزر_Y_إحداثيات * 640 + الإحداثي_س) * 3:(الزر_Y_إحداثيات * 640 + الإحداثي_س) * 3 + 3])
            예제들 = {'background': عنصر_صورة(5, 5), 'panel': عنصر_صورة(45, 85), 'tile': عنصر_صورة(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            التحقق_من_صحة_إبلاغ.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((يعرض_جذر / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if عملية.poll() is None:
                عملية.terminate()
                try: عملية.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    عملية.kill(); عملية.wait(timeout=5)
            محدد.close()
            عملية.stdin.close(); عملية.stdout.close()
            (الناتج / 'serial.log').write_bytes(نسخة_مكتوبة)
            (الناتج / 'report.json').write_text(json.dumps(التحقق_من_صحة_إبلاغ, indent=2) + '\n')


if __name__ == '__main__':
    تشغيل()
