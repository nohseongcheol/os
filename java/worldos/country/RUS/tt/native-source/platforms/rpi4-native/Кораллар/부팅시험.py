#!/usr/bin/env python3
"""фактик_мәгълүмат raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from үтәргә_команда import экранга_җибәрү_тамыр, команда


def эшләтү():
    출력결과 = экранга_җибәрү_тамыр / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    раслау_отчет = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = команда() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        раслау_отчет['command'] = 명령인수
        Процесс = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        сайлагыч = selectors.DefaultSelector()
        сайлагыч.register(Процесс.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, OFFSET_VALUE=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[OFFSET_VALUE:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in сайлагыч.select(0.2):
                    мәгълүмат_тыю = 누름값.fileobj.read(4096)
                    if мәгълүмат_тыю:
                        대화기록.extend(мәгълүмат_тыю)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if Процесс.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Процесс.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 фактик_мәгълүмат GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def EXACT_VALUE(үлчәмен_үзгәртү):
                    үлчәм = b''
                    while len(үлчәм) < үлчәмен_үзгәртү:
                        조각 = 화면접속자.recv(үлчәмен_үзгәртү - len(үлчәм))
                        if not 조각: raise AssertionError('VNC disconnected')
                        үлчәм += 조각
                    return үлчәм
                assert EXACT_VALUE(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in EXACT_VALUE(EXACT_VALUE(1)[0]); 화면접속자.sendall(b'\x01')
                assert EXACT_VALUE(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                сервер_VALUE = EXACT_VALUE(24)
                assert int.from_bytes(сервер_VALUE[:2], 'big') == 640 and int.from_bytes(сервер_VALUE[2:4], 'big') == 480
                EXACT_VALUE(int.from_bytes(сервер_VALUE[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for команда_байт, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                OFFSET_VALUE = len(대화기록)
                Процесс.stdin.write(команда_байт + b'\n')
                Процесс.stdin.flush()
                표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                assert 확인표시 in 대화기록[OFFSET_VALUE:], 확인표시
            def тышча(юл, 예상결과):
                OFFSET_VALUE = len(대화기록)
                Процесс.stdin.write(юл.encode('utf-8') + b'\n'); Процесс.stdin.flush()
                표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                응답자료 = bytes(대화기록[OFFSET_VALUE:])
                for Mäten in 예상결과:
                    assert Mäten.encode('utf-8') in 응답자료, (юл, Mäten, 응답자료)
                return 응답자료
            def кертү(юл, тәкъдим):
                OFFSET_VALUE = len(대화기록)
                Процесс.stdin.write(юл.encode('utf-8') + b'\n'); Процесс.stdin.flush()
                표시까지받기(тәкъдим, OFFSET_VALUE)
                return bytes(대화기록[OFFSET_VALUE:])
            def төзәтү_VALUE(исем, Эчтәлек_VALUE, баш_тарту_гамәл=False):
                кертү('edit ' + исем, b'edit> ')
                for юл in Эчтәлек_VALUE.splitlines(): кертү(юл, b'edit> ')
                if баш_тарту_гамәл:
                    OFFSET_VALUE = len(대화기록)
                    Процесс.stdin.write(b'\x03'); Процесс.stdin.flush()
                    표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                    assert b'EDIT CANCELLED' in 대화기록[OFFSET_VALUE:]
                else:
                    assert b'SAVED' in кертү('.', b'jkoros-native> ')
            def йөкләп_җибәрү_Файллар(исем, мәгълүмат):
                assert len(мәгълүмат) <= 16384
                кертү('load ' + исем, b'hex> ')
                for 순번 in range(0, len(мәгълүмат), 64): кертү(мәгълүмат[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in кертү('.', b'jkoros-native> ')
            def йөкләү_496ddb99(исем):
                응답자료 = тышча('hex ' + исем, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                мәгълүмат = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(мәгълүмат) == int(일치.group(1)); return мәгълүмат
            тышча('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            тышча('java -version', ['not OpenJDK', 'exit 0'])
            тышча('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            тышча('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            тышча('python --version', ['MicroPython 1.24.1', 'exit 0'])
            тышча('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Birem', 'exit 0'])
            тышча('cat python.txt', ['한글 Birem'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(йөкләү_496ddb99('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            төзәтү_VALUE('인사.java', 'public class 인사 { public static void main(String[] args) { int VALUE = 7; System.out.println("한글=" + VALUE); } }')
            тышча('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            тышча('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(йөкләү_496ddb99('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            төзәтү_VALUE('Hello.java', 'broken', баш_тарту_гамәл=True)
            тышча('javac Hello.java', ['Compiled:', 'exit 0'])
            төзәтү_VALUE('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            тышча('javac Broken.java', ['javac error:', 'exit 1'])
            йөкләп_җибәрү_Файллар('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            тышча('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            тышча('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            йөкләп_җибәрү_Файллар('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            тышча('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            тышча('rm Imported.class', [])
            төзәтү_VALUE('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            тышча('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = тышча('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            тышча('rm Loop.java', []); тышча('rm Loop.class', [])
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
            төзәтү_VALUE('checks.py', 파이썬검사)
            тышча('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            тышча('rm checks.py', [])
            төзәтү_VALUE('helper.py', 'value = 321')
            тышча("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            тышча('rm helper.py', [])
            тышча("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            тышча("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                тышча('python hello.py', ['한글 Birem', 'exit 0'])
                тышча('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            йөкләп_җибәрү_Файллар('app.elf', (экранга_җибәрү_тамыр / 'build/user/demo.elf').read_bytes())
            assert йөкләү_496ddb99('app.elf') == (экранга_җибәрү_тамыр / 'build/user/demo.elf').read_bytes()
            тышча('run app.elf', ['EL0 C++', 'exit 0'])
            йөкләп_җибәрү_Файллар('app.elf', b'not an ELF')
            тышча('run app.elf', ['exit -8'])
            тышча('rm app.elf', [])
            тышча('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            сызым_юл = 출력결과 / 'java-framebuffer'; сызым_юл.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(экранга_җибәрү_тамыр / 'dist/jkoros-native-korean.jar'), '-d', str(сызым_юл), str(экранга_җибәрү_тамыр / '시험/자바/화면시험.java')])
            йөкләп_җибәрү_Файллар('화면시험.class', (сызым_юл / '화면시험.class').read_bytes())
            тышча('java 화면시험', ['화면 клип 거부', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            тышча('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as клиент:
                клиент.settimeout(10)
                клиент.connect(str(모의제어경로))
                with клиент.makefile('rwb') as агым_VALUE:
                    인사 = json.loads(агым_VALUE.readline())
                    def 모의제어접속(Башкару, 전달인수=None):
                        Челтәр_хәбәр = {'execute': Башкару}
                        if 전달인수: Челтәр_хәбәр['arguments'] = 전달인수
                        агым_VALUE.write((json.dumps(Челтәр_хәбәр) + '\n').encode())
                        агым_VALUE.flush()
                        while True:
                            җавап_бирү = json.loads(агым_VALUE.readline())
                            if 'error' in җавап_бирү: raise AssertionError(җавап_бирү)
                            if 'return' in җавап_бирү: return җавап_бирү['return']
                    모의제어접속('qmp_capabilities')
                    Экран_кисемтәсе = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(Экран_кисемтәсе), 'format': 'ppm'})
                    def 예제들(Yul, 지점들):
                        with Yul.open('rb') as нокта_файл:
                            assert нокта_файл.readline().strip() == b'P6'
                            assert нокта_файл.readline().strip() == b'640 480'
                            assert нокта_файл.readline().strip() == b'255'
                            нокта_мәгълүмат = нокта_файл.read()
                        assert len(нокта_мәгълүмат) == 640 * 480 * 3
                        return [list(нокта_мәгълүмат[(세로좌표 * 640 + X_координатасы) * 3:(세로좌표 * 640 + X_координатасы) * 3 + 3]) for X_координатасы, 세로좌표 in 지점들]
                    assert 예제들(Экран_кисемтәсе, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(Экран_кисемтәсе, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def җибәрү(누름값, 확인표시):
                        OFFSET_VALUE = len(대화기록)
                        Процесс.stdin.write(누름값); Процесс.stdin.flush()
                        표시까지받기(확인표시, OFFSET_VALUE)
                    җибәрү(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    җибәрү(b'\r', b'GUI ACTION 0 RESULT 0')
                    җибәрү(b'\t', b'GUI FOCUS 1')
                    җибәрү(b'\r', b'GUI ACTION 1 RESULT 0')
                    SECOND_GUI = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SECOND_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SECOND_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    җибәрү(b'\t', b'GUI FOCUS 2')
                    җибәрү(b'\r', b'GUI ACTION 2 RESULT 0')
                    җибәрү(b'\t', b'GUI FOCUS 3')
                    җибәрү(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    җибәрү(b'q', b'jkoros-native> ')
                    раслау_отчет['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Процесс.wait(timeout=10)
            # framebuffer 응답뿐 아니라 фактик_мәгълүмат scanout 픽셀도 확인한다.
            with Экран_кисемтәсе.open('rb') as файл_кертү:
                assert файл_кертү.readline().strip() == b'P6'
                치수 = файл_кертү.readline().strip()
                assert 치수 == b'640 480', 치수
                assert файл_кертү.readline().strip() == b'255'
                화소들 = файл_кертү.read()
            assert len(화소들) == 640 * 480 * 3
            def нокта(X_координатасы, 세로좌표): return list(화소들[(세로좌표 * 640 + X_координатасы) * 3:(세로좌표 * 640 + X_координатасы) * 3 + 3])
            예제들 = {'background': нокта(5, 5), 'panel': нокта(45, 85), 'tile': нокта(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            раслау_отчет.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((экранга_җибәрү_тамыр / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Процесс.poll() is None:
                Процесс.terminate()
                try: Процесс.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Процесс.kill(); Процесс.wait(timeout=5)
            сайлагыч.close()
            Процесс.stdin.close(); Процесс.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(раслау_отчет, indent=2) + '\n')


if __name__ == '__main__':
    эшләтү()
