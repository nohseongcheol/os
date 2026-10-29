#!/usr/bin/env python3
"""нақты_деректер raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from орындау_пәрмен import жоба_түбір, Команда


def Орындау_2():
    출력결과 = жоба_түбір / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    тексерім_есеп = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Команда() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        тексерім_есеп['command'] = 명령인수
        Үрдіс = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        селектор = selectors.DefaultSelector()
        селектор.register(Үрдіс.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, жылжыту_мән_450fc799=0, 시간제한=45):
            ең_соңғы_мерзім_уақыт = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[жылжыту_мән_450fc799:]:
                if time.monotonic() > ең_соңғы_мерзім_уақыт:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in селектор.select(0.2):
                    деректер_блогы = 누름값.fileobj.read(4096)
                    if деректер_блогы:
                        대화기록.extend(деректер_блогы)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if Үрдіс.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Үрдіс.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 ток_элемент 호스트에서도 VNC로 нақты_деректер GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(Өлшемі):
                    НӘТИЖЕ = b''
                    while len(НӘТИЖЕ) < Өлшемі:
                        조각 = 화면접속자.recv(Өлшемі - len(НӘТИЖЕ))
                        if not 조각: raise AssertionError('VNC disconnected')
                        НӘТИЖЕ += 조각
                    return НӘТИЖЕ
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                сервер_мән = 정확한값(24)
                assert int.from_bytes(сервер_мән[:2], 'big') == 640 and int.from_bytes(сервер_мән[2:4], 'big') == 480
                정확한값(int.from_bytes(сервер_мән[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for пәрмен_байт, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                жылжыту_мән_450fc799 = len(대화기록)
                Үрдіс.stdin.write(пәрмен_байт + b'\n')
                Үрдіс.stdin.flush()
                표시까지받기(b'jkoros-native> ', жылжыту_мән_450fc799)
                assert 확인표시 in 대화기록[жылжыту_мән_450fc799:], 확인표시
            def қоршам(Жол, 예상결과):
                жылжыту_мән_450fc799 = len(대화기록)
                Үрдіс.stdin.write(Жол.encode('utf-8') + b'\n'); Үрдіс.stdin.flush()
                표시까지받기(b'jkoros-native> ', жылжыту_мән_450fc799)
                жауап_1262b476 = bytes(대화기록[жылжыту_мән_450fc799:])
                for Мәтін in 예상결과:
                    assert Мәтін.encode('utf-8') in жауап_1262b476, (Жол, Мәтін, жауап_1262b476)
                return жауап_1262b476
            def енгізу(Жол, сұрау):
                жылжыту_мән_450fc799 = len(대화기록)
                Үрдіс.stdin.write(Жол.encode('utf-8') + b'\n'); Үрдіс.stdin.flush()
                표시까지받기(сұрау, жылжыту_мән_450fc799)
                return bytes(대화기록[жылжыту_мән_450fc799:])
            def өңдеу_мән(Аты, мазмұн_мән, бас_тарту_ота=False):
                енгізу('edit ' + Аты, b'edit> ')
                for Жол in мазмұн_мән.splitlines(): енгізу(Жол, b'edit> ')
                if бас_тарту_ота:
                    жылжыту_мән_450fc799 = len(대화기록)
                    Үрдіс.stdin.write(b'\x03'); Үрдіс.stdin.flush()
                    표시까지받기(b'jkoros-native> ', жылжыту_мән_450fc799)
                    assert b'EDIT CANCELLED' in 대화기록[жылжыту_мән_450fc799:]
                else:
                    assert b'SAVED' in енгізу('.', b'jkoros-native> ')
            def Жүктеп_салу_Файлдар(Аты, деректер):
                assert len(деректер) <= 16384
                енгізу('load ' + Аты, b'hex> ')
                for 순번 in range(0, len(деректер), 64): енгізу(деректер[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in енгізу('.', b'jkoros-native> ')
            def жүктеме(Аты):
                жауап_1262b476 = қоршам('hex ' + Аты, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', жауап_1262b476, re.S)
                деректер = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(деректер) == int(일치.group(1)); return деректер
            қоршам('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            қоршам('java -version', ['not OpenJDK', 'exit 0'])
            қоршам('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            қоршам('java Hello "한글 Аргументтер 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Аргументтер 😀', 'exit 0'])
            қоршам('python --version', ['MicroPython 1.24.1', 'exit 0'])
            қоршам('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Файл', 'exit 0'])
            қоршам('cat python.txt', ['한글 Файл'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(жүктеме('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 Аргументтер 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Аргументтер 😀'], 예상결과
            өңдеу_мән('인사.java', 'public class 인사 { public static void main(String[] args) { int мән = 7; System.out.println("한글=" + мән); } }')
            қоршам('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            қоршам('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(жүктеме('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            өңдеу_мән('Hello.java', 'broken', бас_тарту_ота=True)
            қоршам('javac Hello.java', ['Compiled:', 'exit 0'])
            өңдеу_мән('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            қоршам('javac Broken.java', ['javac error:', 'exit 1'])
            Жүктеп_салу_Файлдар('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            қоршам('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            қоршам('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Жүктеп_салу_Файлдар('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            қоршам('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            қоршам('rm Imported.class', [])
            өңдеу_мән('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            қоршам('javac Loop.java', ['Compiled:', 'exit 0'])
            жауап_1262b476 = қоршам('java Loop', ['exit '])
            assert b'instruction limit' in жауап_1262b476 or b'exit -1004' in жауап_1262b476
            қоршам('rm Loop.java', []); қоршам('rm Loop.class', [])
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
            өңдеу_мән('checks.py', 파이썬검사)
            қоршам('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            қоршам('rm checks.py', [])
            өңдеу_мән('helper.py', 'value = 321')
            қоршам("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            қоршам('rm helper.py', [])
            қоршам("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            қоршам("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                қоршам('python hello.py', ['한글 Файл', 'exit 0'])
                қоршам('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Жүктеп_салу_Файлдар('app.elf', (жоба_түбір / 'build/user/demo.elf').read_bytes())
            assert жүктеме('app.elf') == (жоба_түбір / 'build/user/demo.elf').read_bytes()
            қоршам('run app.elf', ['EL0 C++', 'exit 0'])
            Жүктеп_салу_Файлдар('app.elf', b'not an ELF')
            қоршам('run app.elf', ['exit -8'])
            қоршам('rm app.elf', [])
            қоршам('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            сызба_жол = 출력결과 / 'java-framebuffer'; сызба_жол.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(жоба_түбір / 'dist/jkoros-native-korean.jar'), '-d', str(сызба_жол), str(жоба_түбір / '시험/자바/화면시험.java')])
            Жүктеп_салу_Файлдар('화면시험.class', (сызба_жол / '화면시험.class').read_bytes())
            қоршам('java 화면시험', ['화면 клип қабылдамау_мән', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            қоршам('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as клиент:
                клиент.settimeout(10)
                клиент.connect(str(모의제어경로))
                with клиент.makefile('rwb') as ағым_мән:
                    인사 = json.loads(ағым_мән.readline())
                    def 모의제어접속(Орындау, 전달인수=None):
                        желі_хабар = {'execute': Орындау}
                        if 전달인수: желі_хабар['arguments'] = 전달인수
                        ағым_мән.write((json.dumps(желі_хабар) + '\n').encode())
                        ағым_мән.flush()
                        while True:
                            жауап = json.loads(ағым_мән.readline())
                            if 'error' in жауап: raise AssertionError(жауап)
                            if 'return' in жауап: return жауап['return']
                    모의제어접속('qmp_capabilities')
                    скриншот = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(скриншот), 'format': 'ppm'})
                    def 예제들(Жол_2, 지점들):
                        with Жол_2.open('rb') as нүкте_файл:
                            assert нүкте_файл.readline().strip() == b'P6'
                            assert нүкте_файл.readline().strip() == b'640 480'
                            assert нүкте_файл.readline().strip() == b'255'
                            нүкте_деректер = нүкте_файл.read()
                        assert len(нүкте_деректер) == 640 * 480 * 3
                        return [list(нүкте_деректер[(Y_түймешігі_координата * 640 + x_координатасы) * 3:(Y_түймешігі_координата * 640 + x_координатасы) * 3 + 3]) for x_координатасы, Y_түймешігі_координата in 지점들]
                    assert 예제들(скриншот, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(скриншот, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def жіберу(누름값, 확인표시):
                        жылжыту_мән_450fc799 = len(대화기록)
                        Үрдіс.stdin.write(누름값); Үрдіс.stdin.flush()
                        표시까지받기(확인표시, жылжыту_мән_450fc799)
                    жіберу(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    жіберу(b'\r', b'GUI ACTION 0 RESULT 0')
                    жіберу(b'\t', b'GUI FOCUS 1')
                    жіберу(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    жіберу(b'\t', b'GUI FOCUS 2')
                    жіберу(b'\r', b'GUI ACTION 2 RESULT 0')
                    жіберу(b'\t', b'GUI FOCUS 3')
                    жіберу(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    жіберу(b'q', b'jkoros-native> ')
                    тексерім_есеп['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Үрдіс.wait(timeout=10)
            # framebuffer 응답뿐 아니라 нақты_деректер scanout 픽셀도 확인한다.
            with скриншот.open('rb') as файл_енгізу:
                assert файл_енгізу.readline().strip() == b'P6'
                치수 = файл_енгізу.readline().strip()
                assert 치수 == b'640 480', 치수
                assert файл_енгізу.readline().strip() == b'255'
                화소들 = файл_енгізу.read()
            assert len(화소들) == 640 * 480 * 3
            def нүкте(x_координатасы, Y_түймешігі_координата): return list(화소들[(Y_түймешігі_координата * 640 + x_координатасы) * 3:(Y_түймешігі_координата * 640 + x_координатасы) * 3 + 3])
            예제들 = {'background': нүкте(5, 5), 'panel': нүкте(45, 85), 'tile': нүкте(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            тексерім_есеп.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((жоба_түбір / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Үрдіс.poll() is None:
                Үрдіс.terminate()
                try: Үрдіс.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Үрдіс.kill(); Үрдіс.wait(timeout=5)
            селектор.close()
            Үрдіс.stdin.close(); Үрдіс.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(тексерім_есеп, indent=2) + '\n')


if __name__ == '__main__':
    Орындау_2()
