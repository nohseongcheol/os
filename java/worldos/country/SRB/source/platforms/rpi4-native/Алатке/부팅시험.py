#!/usr/bin/env python3
"""стваран_подаци raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from Изврши_команда import пројектовати_корен, Наредба


def Покрени():
    출력결과 = пројектовати_корен / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    транскрипт = bytearray()
    провјера_извештај = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Наредба() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        провјера_извештај['command'] = 명령인수
        Процес = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        бирач = selectors.DefaultSelector()
        бирач.register(Процес.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, Помак_вриједност=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in транскрипт[Помак_вриједност:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in бирач.select(0.2):
                    подаци_блокирај = 누름값.fileobj.read(4096)
                    if подаци_блокирај:
                        транскрипт.extend(подаци_блокирај)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', транскрипт):
                    raise AssertionError('kernel failure')
                if Процес.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Процес.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in транскрипт, 확인표시
            # GTK 없는 актуелно_ставка 호스트에서도 VNC로 стваран_подаци GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(Величина):
                    ИСХОД = b''
                    while len(ИСХОД) < Величина:
                        조각 = 화면접속자.recv(Величина - len(ИСХОД))
                        if not 조각: raise AssertionError('VNC disconnected')
                        ИСХОД += 조각
                    return ИСХОД
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                сервер_вриједност = 정확한값(24)
                assert int.from_bytes(сервер_вриједност[:2], 'big') == 640 and int.from_bytes(сервер_вриједност[2:4], 'big') == 480
                정확한값(int.from_bytes(сервер_вриједност[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for команда_бајт, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                Помак_вриједност = len(транскрипт)
                Процес.stdin.write(команда_бајт + b'\n')
                Процес.stdin.flush()
                표시까지받기(b'jkoros-native> ', Помак_вриједност)
                assert 확인표시 in транскрипт[Помак_вриједност:], 확인표시
            def љуска(Ред, 예상결과):
                Помак_вриједност = len(транскрипт)
                Процес.stdin.write(Ред.encode('utf-8') + b'\n'); Процес.stdin.flush()
                표시까지받기(b'jkoros-native> ', Помак_вриједност)
                одговор_1262b476 = bytes(транскрипт[Помак_вриједност:])
                for Текст in 예상결과:
                    assert Текст.encode('utf-8') in одговор_1262b476, (Ред, Текст, одговор_1262b476)
                return одговор_1262b476
            def унети(Ред, одзив):
                Помак_вриједност = len(транскрипт)
                Процес.stdin.write(Ред.encode('utf-8') + b'\n'); Процес.stdin.flush()
                표시까지받기(одзив, Помак_вриједност)
                return bytes(транскрипт[Помак_вриједност:])
            def Уреди_вриједност(Назив, Садржај_вриједност, Откажи_операција=False):
                унети('edit ' + Назив, b'edit> ')
                for Ред in Садржај_вриједност.splitlines(): унети(Ред, b'edit> ')
                if Откажи_операција:
                    Помак_вриједност = len(транскрипт)
                    Процес.stdin.write(b'\x03'); Процес.stdin.flush()
                    표시까지받기(b'jkoros-native> ', Помак_вриједност)
                    assert b'EDIT CANCELLED' in транскрипт[Помак_вриједност:]
                else:
                    assert b'SAVED' in унети('.', b'jkoros-native> ')
            def Отпрема_Фајлови(Назив, подаци):
                assert len(подаци) <= 16384
                унети('load ' + Назив, b'hex> ')
                for 순번 in range(0, len(подаци), 64): унети(подаци[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in унети('.', b'jkoros-native> ')
            def преузми(Назив):
                одговор_1262b476 = љуска('hex ' + Назив, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', одговор_1262b476, re.S)
                подаци = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(подаци) == int(일치.group(1)); return подаци
            љуска('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            љуска('java -version', ['not OpenJDK', 'exit 0'])
            љуска('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            љуска('java Hello "한글 Аргументи 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Аргументи 😀', 'exit 0'])
            љуска('python --version', ['MicroPython 1.24.1', 'exit 0'])
            љуска('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Датотека', 'exit 0'])
            љуска('cat python.txt', ['한글 Датотека'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(преузми('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 Аргументи 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Аргументи 😀'], 예상결과
            Уреди_вриједност('인사.java', 'public class 인사 { public static void main(String[] args) { int вриједност = 7; System.out.println("한글=" + вриједност); } }')
            љуска('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            љуска('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(преузми('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            Уреди_вриједност('Hello.java', 'broken', Откажи_операција=True)
            љуска('javac Hello.java', ['Compiled:', 'exit 0'])
            Уреди_вриједност('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            љуска('javac Broken.java', ['javac error:', 'exit 1'])
            Отпрема_Фајлови('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            љуска('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            љуска('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Отпрема_Фајлови('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            љуска('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            љуска('rm Imported.class', [])
            Уреди_вриједност('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            љуска('javac Loop.java', ['Compiled:', 'exit 0'])
            одговор_1262b476 = љуска('java Loop', ['exit '])
            assert b'instruction limit' in одговор_1262b476 or b'exit -1004' in одговор_1262b476
            љуска('rm Loop.java', []); љуска('rm Loop.class', [])
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
            Уреди_вриједност('checks.py', 파이썬검사)
            љуска('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            љуска('rm checks.py', [])
            Уреди_вриједност('helper.py', 'value = 321')
            љуска("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            љуска('rm helper.py', [])
            љуска("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            љуска("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                љуска('python hello.py', ['한글 Датотека', 'exit 0'])
                љуска('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Отпрема_Фајлови('app.elf', (пројектовати_корен / 'build/user/demo.elf').read_bytes())
            assert преузми('app.elf') == (пројектовати_корен / 'build/user/demo.elf').read_bytes()
            љуска('run app.elf', ['EL0 C++', 'exit 0'])
            Отпрема_Фајлови('app.elf', b'not an ELF')
            љуска('run app.elf', ['exit -8'])
            љуска('rm app.elf', [])
            љуска('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            цртеж_пут = 출력결과 / 'java-framebuffer'; цртеж_пут.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(пројектовати_корен / 'dist/jkoros-native-korean.jar'), '-d', str(цртеж_пут), str(пројектовати_корен / '시험/자바/화면시험.java')])
            Отпрема_Фајлови('화면시험.class', (цртеж_пут / '화면시험.class').read_bytes())
            љуска('java 화면시험', ['화면 клип одбацити_вриједност_e3ecc00b', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            љуска('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as клијент:
                клијент.settimeout(10)
                клијент.connect(str(모의제어경로))
                with клијент.makefile('rwb') as ток_вриједност:
                    인사 = json.loads(ток_вриједност.readline())
                    def 모의제어접속(Изврши, 전달인수=None):
                        Мрежа_порука = {'execute': Изврши}
                        if 전달인수: Мрежа_порука['arguments'] = 전달인수
                        ток_вриједност.write((json.dumps(Мрежа_порука) + '\n').encode())
                        ток_вриједност.flush()
                        while True:
                            одговор = json.loads(ток_вриједност.readline())
                            if 'error' in одговор: raise AssertionError(одговор)
                            if 'return' in одговор: return одговор['return']
                    모의제어접속('qmp_capabilities')
                    исечак_екрана = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(исечак_екрана), 'format': 'ppm'})
                    def 예제들(ПУТАЊА, 지점들):
                        with ПУТАЊА.open('rb') as пиксел_фајл:
                            assert пиксел_фајл.readline().strip() == b'P6'
                            assert пиксел_фајл.readline().strip() == b'640 480'
                            assert пиксел_фајл.readline().strip() == b'255'
                            пиксел_подаци = пиксел_фајл.read()
                        assert len(пиксел_подаци) == 640 * 480 * 3
                        return [list(пиксел_подаци[(дугме_Y_координата * 640 + x_координата) * 3:(дугме_Y_координата * 640 + x_координата) * 3 + 3]) for x_координата, дугме_Y_координата in 지점들]
                    assert 예제들(исечак_екрана, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(исечак_екрана, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def послати(누름값, 확인표시):
                        Помак_вриједност = len(транскрипт)
                        Процес.stdin.write(누름값); Процес.stdin.flush()
                        표시까지받기(확인표시, Помак_вриједност)
                    послати(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    послати(b'\r', b'GUI ACTION 0 RESULT 0')
                    послати(b'\t', b'GUI FOCUS 1')
                    послати(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    послати(b'\t', b'GUI FOCUS 2')
                    послати(b'\r', b'GUI ACTION 2 RESULT 0')
                    послати(b'\t', b'GUI FOCUS 3')
                    послати(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    послати(b'q', b'jkoros-native> ')
                    провјера_извештај['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Процес.wait(timeout=10)
            # framebuffer 응답뿐 아니라 стваран_подаци scanout 픽셀도 확인한다.
            with исечак_екрана.open('rb') as фајл_унос:
                assert фајл_унос.readline().strip() == b'P6'
                치수 = фајл_унос.readline().strip()
                assert 치수 == b'640 480', 치수
                assert фајл_унос.readline().strip() == b'255'
                화소들 = фајл_унос.read()
            assert len(화소들) == 640 * 480 * 3
            def пиксел(x_координата, дугме_Y_координата): return list(화소들[(дугме_Y_координата * 640 + x_координата) * 3:(дугме_Y_координата * 640 + x_координата) * 3 + 3])
            예제들 = {'background': пиксел(5, 5), 'panel': пиксел(45, 85), 'tile': пиксел(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            провјера_извештај.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((пројектовати_корен / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Процес.poll() is None:
                Процес.terminate()
                try: Процес.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Процес.kill(); Процес.wait(timeout=5)
            бирач.close()
            Процес.stdin.close(); Процес.stdout.close()
            (출력결과 / 'serial.log').write_bytes(транскрипт)
            (출력결과 / 'report.json').write_text(json.dumps(провјера_извештај, indent=2) + '\n')


if __name__ == '__main__':
    Покрени()
