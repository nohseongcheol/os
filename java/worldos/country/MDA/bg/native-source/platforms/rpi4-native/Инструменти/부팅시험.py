#!/usr/bin/env python3
"""действителен_данни raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from изпълнявам_команда import проект_корен, Команда


def Стартиране():
    출력결과 = проект_корен / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    препис = bytearray()
    проверка_отчет = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Команда() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        проверка_отчет['command'] = 명령인수
        Процес = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        свързан_елемент_за_избор = selectors.DefaultSelector()
        свързан_елемент_за_избор.register(Процес.stdout, selectors.EVENT_READ)
        def 표시까지받기(маркер, Изместване_стойност=0, 시간제한=45):
            краен_срок_час = time.monotonic() + 시간제한
            while маркер not in препис[Изместване_стойност:]:
                if time.monotonic() > краен_срок_час:
                    raise AssertionError('UART timeout: ' + repr(маркер))
                for 누름값, _ in свързан_елемент_за_избор.select(0.2):
                    блок_с_данни = 누름값.fileobj.read(4096)
                    if блок_с_данни:
                        препис.extend(блок_с_данни)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', препис):
                    raise AssertionError('kernel failure')
                if Процес.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Процес.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for маркер in 확인표시들:
                assert маркер in препис, маркер
            # GTK 없는 в_срок_артикул 호스트에서도 VNC로 действителен_данни GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(Размер):
                    РЕЗУЛТАТ = b''
                    while len(РЕЗУЛТАТ) < Размер:
                        조각 = 화면접속자.recv(Размер - len(РЕЗУЛТАТ))
                        if not 조각: raise AssertionError('VNC disconnected')
                        РЕЗУЛТАТ += 조각
                    return РЕЗУЛТАТ
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                сървър_стойност = 정확한값(24)
                assert int.from_bytes(сървър_стойност[:2], 'big') == 640 and int.from_bytes(сървър_стойност[2:4], 'big') == 480
                정확한값(int.from_bytes(сървър_стойност[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for команда_байт, маркер in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                Изместване_стойност = len(препис)
                Процес.stdin.write(команда_байт + b'\n')
                Процес.stdin.flush()
                표시까지받기(b'jkoros-native> ', Изместване_стойност)
                assert маркер in препис[Изместване_стойност:], маркер
            def обвивка(ред, 예상결과):
                Изместване_стойност = len(препис)
                Процес.stdin.write(ред.encode('utf-8') + b'\n'); Процес.stdin.flush()
                표시까지받기(b'jkoros-native> ', Изместване_стойност)
                отговор_1262b476 = bytes(препис[Изместване_стойност:])
                for Текст in 예상결과:
                    assert Текст.encode('utf-8') in отговор_1262b476, (ред, Текст, отговор_1262b476)
                return отговор_1262b476
            def въвеждам(ред, подкана):
                Изместване_стойност = len(препис)
                Процес.stdin.write(ред.encode('utf-8') + b'\n'); Процес.stdin.flush()
                표시까지받기(подкана, Изместване_стойност)
                return bytes(препис[Изместване_стойност:])
            def редакция_стойност(Име, Съдържание_стойност, Отказ_операция=False):
                въвеждам('edit ' + Име, b'edit> ')
                for ред in Съдържание_стойност.splitlines(): въвеждам(ред, b'edit> ')
                if Отказ_операция:
                    Изместване_стойност = len(препис)
                    Процес.stdin.write(b'\x03'); Процес.stdin.flush()
                    표시까지받기(b'jkoros-native> ', Изместване_стойност)
                    assert b'EDIT CANCELLED' in препис[Изместване_стойност:]
                else:
                    assert b'SAVED' in въвеждам('.', b'jkoros-native> ')
            def качвам_Файлове(Име, данни):
                assert len(данни) <= 16384
                въвеждам('load ' + Име, b'hex> ')
                for 순번 in range(0, len(данни), 64): въвеждам(данни[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in въвеждам('.', b'jkoros-native> ')
            def изтеглям(Име):
                отговор_1262b476 = обвивка('hex ' + Име, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', отговор_1262b476, re.S)
                данни = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(данни) == int(일치.group(1)); return данни
            обвивка('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            обвивка('java -version', ['not OpenJDK', 'exit 0'])
            обвивка('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            обвивка('java Hello "한글 Параметри 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Параметри 😀', 'exit 0'])
            обвивка('python --version', ['MicroPython 1.24.1', 'exit 0'])
            обвивка('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Файл', 'exit 0'])
            обвивка('cat python.txt', ['한글 Файл'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(изтеглям('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 Параметри 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Параметри 😀'], 예상결과
            редакция_стойност('인사.java', 'public class 인사 { public static void main(String[] args) { int стойност = 7; System.out.println("한글=" + стойност); } }')
            обвивка('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            обвивка('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(изтеглям('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            редакция_стойност('Hello.java', 'broken', Отказ_операция=True)
            обвивка('javac Hello.java', ['Compiled:', 'exit 0'])
            редакция_стойност('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            обвивка('javac Broken.java', ['javac error:', 'exit 1'])
            качвам_Файлове('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            обвивка('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            обвивка('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            качвам_Файлове('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            обвивка('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            обвивка('rm Imported.class', [])
            редакция_стойност('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            обвивка('javac Loop.java', ['Compiled:', 'exit 0'])
            отговор_1262b476 = обвивка('java Loop', ['exit '])
            assert b'instruction limit' in отговор_1262b476 or b'exit -1004' in отговор_1262b476
            обвивка('rm Loop.java', []); обвивка('rm Loop.class', [])
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
            редакция_стойност('checks.py', 파이썬검사)
            обвивка('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            обвивка('rm checks.py', [])
            редакция_стойност('helper.py', 'value = 321')
            обвивка("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            обвивка('rm helper.py', [])
            обвивка("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            обвивка("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                обвивка('python hello.py', ['한글 Файл', 'exit 0'])
                обвивка('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            качвам_Файлове('app.elf', (проект_корен / 'build/user/demo.elf').read_bytes())
            assert изтеглям('app.elf') == (проект_корен / 'build/user/demo.elf').read_bytes()
            обвивка('run app.elf', ['EL0 C++', 'exit 0'])
            качвам_Файлове('app.elf', b'not an ELF')
            обвивка('run app.elf', ['exit -8'])
            обвивка('rm app.elf', [])
            обвивка('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            чертеж_път = 출력결과 / 'java-framebuffer'; чертеж_път.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(проект_корен / 'dist/jkoros-native-korean.jar'), '-d', str(чертеж_път), str(проект_корен / '시험/자바/화면시험.java')])
            качвам_Файлове('화면시험.class', (чертеж_път / '화면시험.class').read_bytes())
            обвивка('java 화면시험', ['화면 клип отхвърлям_стойност_e3ecc00b', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            обвивка('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as клиент:
                клиент.settimeout(10)
                клиент.connect(str(모의제어경로))
                with клиент.makefile('rwb') as поток_стойност:
                    인사 = json.loads(поток_стойност.readline())
                    def 모의제어접속(Изпълнение, 전달인수=None):
                        мрежа_имейл = {'execute': Изпълнение}
                        if 전달인수: мрежа_имейл['arguments'] = 전달인수
                        поток_стойност.write((json.dumps(мрежа_имейл) + '\n').encode())
                        поток_стойност.flush()
                        while True:
                            отговор = json.loads(поток_стойност.readline())
                            if 'error' in отговор: raise AssertionError(отговор)
                            if 'return' in отговор: return отговор['return']
                    모의제어접속('qmp_capabilities')
                    екранна_снимка = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(екранна_снимка), 'format': 'ppm'})
                    def 예제들(ПЪТ, 지점들):
                        with ПЪТ.open('rb') as пиксел_Файл:
                            assert пиксел_Файл.readline().strip() == b'P6'
                            assert пиксел_Файл.readline().strip() == b'640 480'
                            assert пиксел_Файл.readline().strip() == b'255'
                            пиксел_данни = пиксел_Файл.read()
                        assert len(пиксел_данни) == 640 * 480 * 3
                        return [list(пиксел_данни[(세로좌표 * 640 + x_координата) * 3:(세로좌표 * 640 + x_координата) * 3 + 3]) for x_координата, 세로좌표 in 지점들]
                    assert 예제들(екранна_снимка, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(екранна_снимка, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def изпращам(누름값, маркер):
                        Изместване_стойност = len(препис)
                        Процес.stdin.write(누름값); Процес.stdin.flush()
                        표시까지받기(маркер, Изместване_стойност)
                    изпращам(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    изпращам(b'\r', b'GUI ACTION 0 RESULT 0')
                    изпращам(b'\t', b'GUI FOCUS 1')
                    изпращам(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    изпращам(b'\t', b'GUI FOCUS 2')
                    изпращам(b'\r', b'GUI ACTION 2 RESULT 0')
                    изпращам(b'\t', b'GUI FOCUS 3')
                    изпращам(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    изпращам(b'q', b'jkoros-native> ')
                    проверка_отчет['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Процес.wait(timeout=10)
            # framebuffer 응답뿐 아니라 действителен_данни scanout 픽셀도 확인한다.
            with екранна_снимка.open('rb') as Файл_запис:
                assert Файл_запис.readline().strip() == b'P6'
                치수 = Файл_запис.readline().strip()
                assert 치수 == b'640 480', 치수
                assert Файл_запис.readline().strip() == b'255'
                화소들 = Файл_запис.read()
            assert len(화소들) == 640 * 480 * 3
            def пиксел(x_координата, 세로좌표): return list(화소들[(세로좌표 * 640 + x_координата) * 3:(세로좌표 * 640 + x_координата) * 3 + 3])
            예제들 = {'background': пиксел(5, 5), 'panel': пиксел(45, 85), 'tile': пиксел(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            проверка_отчет.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((проект_корен / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Процес.poll() is None:
                Процес.terminate()
                try: Процес.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Процес.kill(); Процес.wait(timeout=5)
            свързан_елемент_за_избор.close()
            Процес.stdin.close(); Процес.stdout.close()
            (출력결과 / 'serial.log').write_bytes(препис)
            (출력결과 / 'report.json').write_text(json.dumps(проверка_отчет, indent=2) + '\n')


if __name__ == '__main__':
    Стартиране()
