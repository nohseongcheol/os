#!/usr/bin/env python3
"""фактический_данные raspi4b запуск_машины, UART входные_данные_ЗНАЧЕН, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from 실행 import задача_корень, команда


def запустить():
    выход = задача_корень / 'build/verification'
    выход.mkdir(parents=True, exist_ok=True)
    расшифровка = bytearray()
    проверка_Отчет = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = команда() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        проверка_Отчет['command'] = 명령인수
        Процесс = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        селектор = selectors.DefaultSelector()
        селектор.register(Процесс.stdout, selectors.EVENT_READ)
        def 표시까지받기(метка, СМЕЩ_ЗНАЧЕН=0, выполнение_ТАЙМАУТ=45):
            крайний_срок_ВРЕМЯ = time.monotonic() + выполнение_ТАЙМАУТ
            while метка not in расшифровка[СМЕЩ_ЗНАЧЕН:]:
                if time.monotonic() > крайний_срок_ВРЕМЯ:
                    raise AssertionError('UART timeout: ' + repr(метка))
                for 누름값, _ in селектор.select(0.2):
                    блок_данных = 누름값.fileobj.read(4096)
                    if блок_данных:
                        расшифровка.extend(блок_данных)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', расшифровка):
                    raise AssertionError('kernel failure')
                if Процесс.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Процесс.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for метка in 확인표시들:
                assert метка in расшифровка, метка
            # GTK 없는 текущий_товар 호스트에서도 VNC로 фактический_данные GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as экран_клиент:
                экран_клиент.settimeout(5); экран_клиент.connect(str(Path(작업경로) / 'vnc.sock'))
                def СОВПАД_ЗНАЧЕН(Размер):
                    результат = b''
                    while len(результат) < Размер:
                        блок_ЗНАЧЕН_652d4b53 = экран_клиент.recv(Размер - len(результат))
                        if not блок_ЗНАЧЕН_652d4b53: raise AssertionError('VNC disconnected')
                        результат += блок_ЗНАЧЕН_652d4b53
                    return результат
                assert СОВПАД_ЗНАЧЕН(12) == b'RFB 003.008\n'
                экран_клиент.sendall(b'RFB 003.008\n')
                assert 1 in СОВПАД_ЗНАЧЕН(СОВПАД_ЗНАЧЕН(1)[0]); экран_клиент.sendall(b'\x01')
                assert СОВПАД_ЗНАЧЕН(4) == b'\x00\x00\x00\x00'; экран_клиент.sendall(b'\x01')
                сервер_ЗНАЧЕН = СОВПАД_ЗНАЧЕН(24)
                assert int.from_bytes(сервер_ЗНАЧЕН[:2], 'big') == 640 and int.from_bytes(сервер_ЗНАЧЕН[2:4], 'big') == 480
                СОВПАД_ЗНАЧЕН(int.from_bytes(сервер_ЗНАЧЕН[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for 명령바이트, метка in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', 'испытания.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                СМЕЩ_ЗНАЧЕН = len(расшифровка)
                Процесс.stdin.write(명령바이트 + b'\n')
                Процесс.stdin.flush()
                표시까지받기(b'jkoros-native> ', СМЕЩ_ЗНАЧЕН)
                assert метка in расшифровка[СМЕЩ_ЗНАЧЕН:], метка
            def оболочка(строка_ввода, 예상결과):
                СМЕЩ_ЗНАЧЕН = len(расшифровка)
                Процесс.stdin.write(строка_ввода.encode('utf-8') + b'\n'); Процесс.stdin.flush()
                표시까지받기(b'jkoros-native> ', СМЕЩ_ЗНАЧЕН)
                ответ_1262b476 = bytes(расшифровка[СМЕЩ_ЗНАЧЕН:])
                for текст in 예상결과:
                    assert текст.encode('utf-8') in ответ_1262b476, (строка_ввода, текст, ответ_1262b476)
                return ответ_1262b476
            def ввести(строка_ввода, запрос_1dd14da4):
                СМЕЩ_ЗНАЧЕН = len(расшифровка)
                Процесс.stdin.write(строка_ввода.encode('utf-8') + b'\n'); Процесс.stdin.flush()
                표시까지받기(запрос_1dd14da4, СМЕЩ_ЗНАЧЕН)
                return bytes(расшифровка[СМЕЩ_ЗНАЧЕН:])
            def правка_ЗНАЧЕН(Название, контент_ЗНАЧЕН, Close_операция=False):
                ввести('edit ' + Название, b'edit> ')
                for строка_ввода in контент_ЗНАЧЕН.splitlines(): ввести(строка_ввода, b'edit> ')
                if Close_операция:
                    СМЕЩ_ЗНАЧЕН = len(расшифровка)
                    Процесс.stdin.write(b'\x03'); Процесс.stdin.flush()
                    표시까지받기(b'jkoros-native> ', СМЕЩ_ЗНАЧЕН)
                    assert b'EDIT CANCELLED' in расшифровка[СМЕЩ_ЗНАЧЕН:]
                else:
                    assert b'SAVED' in ввести('.', b'jkoros-native> ')
            def Upload_Файлы(Название, данные):
                assert len(данные) <= 16384
                ввести('load ' + Название, b'hex> ')
                for 순번 in range(0, len(данные), 64): ввести(данные[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in ввести('.', b'jkoros-native> ')
            def скачать(Название):
                ответ_1262b476 = оболочка('hex ' + Название, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', ответ_1262b476, re.S)
                данные = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(данные) == int(일치.group(1)); return данные
            оболочка('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            оболочка('java -version', ['not OpenJDK', 'exit 0'])
            оболочка('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            оболочка('java Hello "한글 аргументы 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 аргументы 😀', 'exit 0'])
            оболочка('python --version', ['MicroPython 1.24.1', 'exit 0'])
            оболочка('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 файл', 'exit 0'])
            оболочка('cat python.txt', ['한글 файл'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = выход / 'Hello.class'; 자바클래스.write_bytes(скачать('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(выход), 'Hello', '한글 аргументы 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 аргументы 😀'], 예상결과
            правка_ЗНАЧЕН('приветствие_ae353e94.java', 'public class приветствие_ae353e94 { public static void main(String[] args) { int ЗНАЧЕН = 7; System.out.println("한글=" + ЗНАЧЕН); } }')
            оболочка('javac приветствие_ae353e94.java', ['Compiled: приветствие_ae353e94.class', 'exit 0'])
            оболочка('java приветствие_ae353e94', ['한글=7', 'exit 0'])
            (выход / 'приветствие_ae353e94.class').write_bytes(скачать('приветствие_ae353e94.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(выход), 'приветствие_ae353e94']).decode().strip() == '한글=7'
            правка_ЗНАЧЕН('Hello.java', 'broken', Close_операция=True)
            оболочка('javac Hello.java', ['Compiled:', 'exit 0'])
            правка_ЗНАЧЕН('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            оболочка('javac Broken.java', ['javac error:', 'exit 1'])
            Upload_Файлы('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            оболочка('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            оболочка('rm Broken.java', [])
            들여온파일 = выход / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Upload_Файлы('Imported.class', (выход / 'Imported.class').read_bytes())
            оболочка('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            оболочка('rm Imported.class', [])
            правка_ЗНАЧЕН('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            оболочка('javac Loop.java', ['Compiled:', 'exit 0'])
            ответ_1262b476 = оболочка('java Loop', ['exit '])
            assert b'instruction limit' in ответ_1262b476 or b'exit -1004' in ответ_1262b476
            оболочка('rm Loop.java', []); оболочка('rm Loop.class', [])
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
            правка_ЗНАЧЕН('checks.py', 파이썬검사)
            оболочка('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            оболочка('rm checks.py', [])
            правка_ЗНАЧЕН('helper.py', 'value = 321')
            оболочка("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            оболочка('rm helper.py', [])
            оболочка("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            оболочка("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                оболочка('python hello.py', ['한글 файл', 'exit 0'])
                оболочка('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Upload_Файлы('app.elf', (задача_корень / 'build/user/demo.elf').read_bytes())
            assert скачать('app.elf') == (задача_корень / 'build/user/demo.elf').read_bytes()
            оболочка('run app.elf', ['EL0 C++', 'exit 0'])
            Upload_Файлы('app.elf', b'not an ELF')
            оболочка('run app.elf', ['exit -8'])
            оболочка('rm app.elf', [])
            оболочка('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            рисунок_путь = выход / 'java-framebuffer'; рисунок_путь.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(задача_корень / 'dist/jkoros-native-korean.jar'), '-d', str(рисунок_путь), str(задача_корень / 'испытания/자바/тест_экран.java')])
            Upload_Файлы('тест_экран.class', (рисунок_путь / 'тест_экран.class').read_bytes())
            оболочка('java тест_экран', ['экран клип отклонить_ЗНАЧЕН', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            оболочка('rm тест_экран.class', [])
            with socket.socket(socket.AF_UNIX) as клиент:
                клиент.settimeout(10)
                клиент.connect(str(모의제어경로))
                with клиент.makefile('rwb') as поток_ЗНАЧЕН:
                    приветствие_ae353e94 = json.loads(поток_ЗНАЧЕН.readline())
                    def 모의제어접속(Выполнить, 전달인수=None):
                        сеть_письмо = {'execute': Выполнить}
                        if 전달인수: сеть_письмо['arguments'] = 전달인수
                        поток_ЗНАЧЕН.write((json.dumps(сеть_письмо) + '\n').encode())
                        поток_ЗНАЧЕН.flush()
                        while True:
                            ответ = json.loads(поток_ЗНАЧЕН.readline())
                            if 'error' in ответ: raise AssertionError(ответ)
                            if 'return' in ответ: return ответ['return']
                    모의제어접속('qmp_capabilities')
                    снимок_экрана = выход / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(снимок_экрана), 'format': 'ppm'})
                    def 예제들(путь, 지점들):
                        with путь.open('rb') as пиксель_файл:
                            assert пиксель_файл.readline().strip() == b'P6'
                            assert пиксель_файл.readline().strip() == b'640 480'
                            assert пиксель_файл.readline().strip() == b'255'
                            пиксель_данные = пиксель_файл.read()
                        assert len(пиксель_данные) == 640 * 480 * 3
                        return [list(пиксель_данные[(Y_координата * 640 + координата_X) * 3:(Y_координата * 640 + координата_X) * 3 + 3]) for координата_X, Y_координата in 지점들]
                    assert 예제들(снимок_экрана, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(снимок_экрана, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def написать(누름값, метка):
                        СМЕЩ_ЗНАЧЕН = len(расшифровка)
                        Процесс.stdin.write(누름값); Процесс.stdin.flush()
                        표시까지받기(метка, СМЕЩ_ЗНАЧЕН)
                    написать(b'gui\n', b'GUI READY:')
                    첫화면 = выход / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(выход / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    написать(b'\r', b'GUI ACTION 0 RESULT 0')
                    написать(b'\t', b'GUI FOCUS 1')
                    написать(b'\r', b'GUI ACTION 1 RESULT 0')
                    СЕКУНДЫ_графический_пользовательский_интерфейс = выход / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(СЕКУНДЫ_графический_пользовательский_интерфейс), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(выход / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(СЕКУНДЫ_графический_пользовательский_интерфейс, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    написать(b'\t', b'GUI FOCUS 2')
                    написать(b'\r', b'GUI ACTION 2 RESULT 0')
                    написать(b'\t', b'GUI FOCUS 3')
                    написать(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(выход / 'gui-python.png'), 'format': 'png'})
                    написать(b'q', b'jkoros-native> ')
                    проверка_Отчет['qemu'] = приветствие_ae353e94['QMP']['version']
                    모의제어접속('quit')
            Процесс.wait(timeout=10)
            # framebuffer 응답뿐 아니라 фактический_данные scanout 픽셀도 확인한다.
            with снимок_экрана.open('rb') as файл_ввод:
                assert файл_ввод.readline().strip() == b'P6'
                치수 = файл_ввод.readline().strip()
                assert 치수 == b'640 480', 치수
                assert файл_ввод.readline().strip() == b'255'
                화소들 = файл_ввод.read()
            assert len(화소들) == 640 * 480 * 3
            def пиксель(координата_X, Y_координата): return list(화소들[(Y_координата * 640 + координата_X) * 3:(Y_координата * 640 + координата_X) * 3 + 3])
            예제들 = {'background': пиксель(5, 5), 'panel': пиксель(45, 85), 'tile': пиксель(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            проверка_Отчет.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((задача_корень / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Процесс.poll() is None:
                Процесс.terminate()
                try: Процесс.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Процесс.kill(); Процесс.wait(timeout=5)
            селектор.close()
            Процесс.stdin.close(); Процесс.stdout.close()
            (выход / 'serial.log').write_bytes(расшифровка)
            (выход / 'report.json').write_text(json.dumps(проверка_Отчет, indent=2) + '\n')


if __name__ == '__main__':
    запустить()
