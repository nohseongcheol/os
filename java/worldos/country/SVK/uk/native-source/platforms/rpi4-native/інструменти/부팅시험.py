#!/usr/bin/env python3
"""фактично_дані raspi4b запуск_машини, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from Виконати_команда import Дії_корінь, команда


def запустити():
    출력결과 = Дії_корінь / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    транскрипт = bytearray()
    перевірка_звіт = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = команда() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        перевірка_звіт['command'] = 명령인수
        Процеси = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        селектор = selectors.DefaultSelector()
        селектор.register(Процеси.stdout, selectors.EVENT_READ)
        def 표시까지받기(маркер, Зміщена_копія_значення=0, 시간제한=45):
            крайнiй_термін_час = time.monotonic() + 시간제한
            while маркер not in транскрипт[Зміщена_копія_значення:]:
                if time.monotonic() > крайнiй_термін_час:
                    raise AssertionError('UART timeout: ' + repr(маркер))
                for 누름값, _ in селектор.select(0.2):
                    блок_даних = 누름값.fileobj.read(4096)
                    if блок_даних:
                        транскрипт.extend(блок_даних)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', транскрипт):
                    raise AssertionError('kernel failure')
                if Процеси.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Процеси.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for маркер in 확인표시들:
                assert маркер in транскрипт, маркер
            # GTK 없는 чинний_елемент 호스트에서도 VNC로 фактично_дані GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(Розмір):
                    результат = b''
                    while len(результат) < Розмір:
                        조각 = 화면접속자.recv(Розмір - len(результат))
                        if not 조각: raise AssertionError('VNC disconnected')
                        результат += 조각
                    return результат
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                сервер_значення = 정확한값(24)
                assert int.from_bytes(сервер_значення[:2], 'big') == 640 and int.from_bytes(сервер_значення[2:4], 'big') == 480
                정확한값(int.from_bytes(сервер_значення[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for команда_байт, маркер in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', 'випробування.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                Зміщена_копія_значення = len(транскрипт)
                Процеси.stdin.write(команда_байт + b'\n')
                Процеси.stdin.flush()
                표시까지받기(b'jkoros-native> ', Зміщена_копія_значення)
                assert маркер in транскрипт[Зміщена_копія_значення:], маркер
            def оболонка(рядок_введення, 예상결과):
                Зміщена_копія_значення = len(транскрипт)
                Процеси.stdin.write(рядок_введення.encode('utf-8') + b'\n'); Процеси.stdin.flush()
                표시까지받기(b'jkoros-native> ', Зміщена_копія_значення)
                відгук = bytes(транскрипт[Зміщена_копія_значення:])
                for текст in 예상결과:
                    assert текст.encode('utf-8') in відгук, (рядок_введення, текст, відгук)
                return відгук
            def вводити(рядок_введення, просити):
                Зміщена_копія_значення = len(транскрипт)
                Процеси.stdin.write(рядок_введення.encode('utf-8') + b'\n'); Процеси.stdin.flush()
                표시까지받기(просити, Зміщена_копія_значення)
                return bytes(транскрипт[Зміщена_копія_значення:])
            def правка_значення(Назва, Вміст_значення, Скасувати_операція=False):
                вводити('edit ' + Назва, b'edit> ')
                for рядок_введення in Вміст_значення.splitlines(): вводити(рядок_введення, b'edit> ')
                if Скасувати_операція:
                    Зміщена_копія_значення = len(транскрипт)
                    Процеси.stdin.write(b'\x03'); Процеси.stdin.flush()
                    표시까지받기(b'jkoros-native> ', Зміщена_копія_значення)
                    assert b'EDIT CANCELLED' in транскрипт[Зміщена_копія_значення:]
                else:
                    assert b'SAVED' in вводити('.', b'jkoros-native> ')
            def передавати_Файли(Назва, дані):
                assert len(дані) <= 16384
                вводити('load ' + Назва, b'hex> ')
                for 순번 in range(0, len(дані), 64): вводити(дані[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in вводити('.', b'jkoros-native> ')
            def завантажити(Назва):
                відгук = оболонка('hex ' + Назва, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', відгук, re.S)
                дані = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(дані) == int(일치.group(1)); return дані
            оболонка('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            оболонка('java -version', ['not OpenJDK', 'exit 0'])
            оболонка('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            оболонка('java Hello "한글 аргументи 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 аргументи 😀', 'exit 0'])
            оболонка('python --version', ['MicroPython 1.24.1', 'exit 0'])
            оболонка('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 файл', 'exit 0'])
            оболонка('cat python.txt', ['한글 файл'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(завантажити('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 аргументи 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 аргументи 😀'], 예상결과
            правка_значення('인사.java', 'public class 인사 { public static void main(String[] args) { int значення = 7; System.out.println("한글=" + значення); } }')
            оболонка('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            оболонка('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(завантажити('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            правка_значення('Hello.java', 'broken', Скасувати_операція=True)
            оболонка('javac Hello.java', ['Compiled:', 'exit 0'])
            правка_значення('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            оболонка('javac Broken.java', ['javac error:', 'exit 1'])
            передавати_Файли('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            оболонка('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            оболонка('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            передавати_Файли('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            оболонка('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            оболонка('rm Imported.class', [])
            правка_значення('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            оболонка('javac Loop.java', ['Compiled:', 'exit 0'])
            відгук = оболонка('java Loop', ['exit '])
            assert b'instruction limit' in відгук or b'exit -1004' in відгук
            оболонка('rm Loop.java', []); оболонка('rm Loop.class', [])
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
            правка_значення('checks.py', 파이썬검사)
            оболонка('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            оболонка('rm checks.py', [])
            правка_значення('helper.py', 'value = 321')
            оболонка("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            оболонка('rm helper.py', [])
            оболонка("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            оболонка("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                оболонка('python hello.py', ['한글 файл', 'exit 0'])
                оболонка('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            передавати_Файли('app.elf', (Дії_корінь / 'build/user/demo.elf').read_bytes())
            assert завантажити('app.elf') == (Дії_корінь / 'build/user/demo.elf').read_bytes()
            оболонка('run app.elf', ['EL0 C++', 'exit 0'])
            передавати_Файли('app.elf', b'not an ELF')
            оболонка('run app.elf', ['exit -8'])
            оболонка('rm app.elf', [])
            оболонка('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            малювання_шлях = 출력결과 / 'java-framebuffer'; малювання_шлях.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Дії_корінь / 'dist/jkoros-native-korean.jar'), '-d', str(малювання_шлях), str(Дії_корінь / 'випробування/자바/화면시험.java')])
            передавати_Файли('화면시험.class', (малювання_шлях / '화면시험.class').read_bytes())
            оболонка('java 화면시험', ['화면 кліп відхилити_значення', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            оболонка('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as клієнт:
                клієнт.settimeout(10)
                клієнт.connect(str(모의제어경로))
                with клієнт.makefile('rwb') as потік_значення:
                    인사 = json.loads(потік_значення.readline())
                    def 모의제어접속(Виконати, 전달인수=None):
                        мережа_повідомлення = {'execute': Виконати}
                        if 전달인수: мережа_повідомлення['arguments'] = 전달인수
                        потік_значення.write((json.dumps(мережа_повідомлення) + '\n').encode())
                        потік_значення.flush()
                        while True:
                            відповідь = json.loads(потік_значення.readline())
                            if 'error' in відповідь: raise AssertionError(відповідь)
                            if 'return' in відповідь: return відповідь['return']
                    모의제어접속('qmp_capabilities')
                    знімок_екрана = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(знімок_екрана), 'format': 'ppm'})
                    def 예제들(шлях, 지점들):
                        with шлях.open('rb') as елемент_зображення_Файл:
                            assert елемент_зображення_Файл.readline().strip() == b'P6'
                            assert елемент_зображення_Файл.readline().strip() == b'640 480'
                            assert елемент_зображення_Файл.readline().strip() == b'255'
                            елемент_зображення_дані = елемент_зображення_Файл.read()
                        assert len(елемент_зображення_дані) == 640 * 480 * 3
                        return [list(елемент_зображення_дані[(세로좌표 * 640 + координата_X) * 3:(세로좌표 * 640 + координата_X) * 3 + 3]) for координата_X, 세로좌표 in 지점들]
                    assert 예제들(знімок_екрана, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(знімок_екрана, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def надсилати(누름값, маркер):
                        Зміщена_копія_значення = len(транскрипт)
                        Процеси.stdin.write(누름값); Процеси.stdin.flush()
                        표시까지받기(маркер, Зміщена_копія_значення)
                    надсилати(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    надсилати(b'\r', b'GUI ACTION 0 RESULT 0')
                    надсилати(b'\t', b'GUI FOCUS 1')
                    надсилати(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    надсилати(b'\t', b'GUI FOCUS 2')
                    надсилати(b'\r', b'GUI ACTION 2 RESULT 0')
                    надсилати(b'\t', b'GUI FOCUS 3')
                    надсилати(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    надсилати(b'q', b'jkoros-native> ')
                    перевірка_звіт['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Процеси.wait(timeout=10)
            # framebuffer 응답뿐 아니라 фактично_дані scanout 픽셀도 확인한다.
            with знімок_екрана.open('rb') as Файл_запис:
                assert Файл_запис.readline().strip() == b'P6'
                치수 = Файл_запис.readline().strip()
                assert 치수 == b'640 480', 치수
                assert Файл_запис.readline().strip() == b'255'
                화소들 = Файл_запис.read()
            assert len(화소들) == 640 * 480 * 3
            def елемент_зображення(координата_X, 세로좌표): return list(화소들[(세로좌표 * 640 + координата_X) * 3:(세로좌표 * 640 + координата_X) * 3 + 3])
            예제들 = {'background': елемент_зображення(5, 5), 'panel': елемент_зображення(45, 85), 'tile': елемент_зображення(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            перевірка_звіт.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((Дії_корінь / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Процеси.poll() is None:
                Процеси.terminate()
                try: Процеси.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Процеси.kill(); Процеси.wait(timeout=5)
            селектор.close()
            Процеси.stdin.close(); Процеси.stdout.close()
            (출력결과 / 'serial.log').write_bytes(транскрипт)
            (출력결과 / 'report.json').write_text(json.dumps(перевірка_звіт, indent=2) + '\n')


if __name__ == '__main__':
    запустити()
