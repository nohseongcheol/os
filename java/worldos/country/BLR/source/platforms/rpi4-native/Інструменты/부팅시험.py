#!/usr/bin/env python3
"""фактычны_дадзеныя raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from выканаць_каманда import 기준, Загад


def Выканаць():
    출력결과 = 기준 / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    праверка_справаздача = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Загад() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        праверка_справаздача['command'] = 명령인수
        Працэс = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        селектар = selectors.DefaultSelector()
        селектар.register(Працэс.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, Зрух_значэнне=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[Зрух_значэнне:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in селектар.select(0.2):
                    дадзеныя_блакіраваць = 누름값.fileobj.read(4096)
                    if дадзеныя_блакіраваць:
                        대화기록.extend(дадзеныя_блакіраваць)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if Працэс.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Працэс.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 фактычны_дадзеныя GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(Памер):
                    결과 = b''
                    while len(결과) < Памер:
                        조각 = 화면접속자.recv(Памер - len(결과))
                        if not 조각: raise AssertionError('VNC disconnected')
                        결과 += 조각
                    return 결과
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                сервер_значэнне = 정확한값(24)
                assert int.from_bytes(сервер_значэнне[:2], 'big') == 640 and int.from_bytes(сервер_значэнне[2:4], 'big') == 480
                정확한값(int.from_bytes(сервер_значэнне[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for каманда_байт, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                Зрух_значэнне = len(대화기록)
                Працэс.stdin.write(каманда_байт + b'\n')
                Працэс.stdin.flush()
                표시까지받기(b'jkoros-native> ', Зрух_значэнне)
                assert 확인표시 in 대화기록[Зрух_значэнне:], 확인표시
            def абалонка(лінія, 예상결과):
                Зрух_значэнне = len(대화기록)
                Працэс.stdin.write(лінія.encode('utf-8') + b'\n'); Працэс.stdin.flush()
                표시까지받기(b'jkoros-native> ', Зрух_значэнне)
                응답자료 = bytes(대화기록[Зрух_значэнне:])
                for Тэкст in 예상결과:
                    assert Тэкст.encode('utf-8') in 응답자료, (лінія, Тэкст, 응답자료)
                return 응답자료
            def увесці(лінія, запыт):
                Зрух_значэнне = len(대화기록)
                Працэс.stdin.write(лінія.encode('utf-8') + b'\n'); Працэс.stdin.flush()
                표시까지받기(запыт, Зрух_значэнне)
                return bytes(대화기록[Зрух_значэнне:])
            def рэдагаваць_значэнне(Назва, кантэнт_значэнне, Адмена_аперацыя=False):
                увесці('edit ' + Назва, b'edit> ')
                for лінія in кантэнт_значэнне.splitlines(): увесці(лінія, b'edit> ')
                if Адмена_аперацыя:
                    Зрух_значэнне = len(대화기록)
                    Працэс.stdin.write(b'\x03'); Працэс.stdin.flush()
                    표시까지받기(b'jkoros-native> ', Зрух_значэнне)
                    assert b'EDIT CANCELLED' in 대화기록[Зрух_значэнне:]
                else:
                    assert b'SAVED' in увесці('.', b'jkoros-native> ')
            def запампоўка_Файлы(Назва, дадзеныя):
                assert len(дадзеныя) <= 16384
                увесці('load ' + Назва, b'hex> ')
                for 순번 in range(0, len(дадзеныя), 64): увесці(дадзеныя[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in увесці('.', b'jkoros-native> ')
            def спампоўка(Назва):
                응답자료 = абалонка('hex ' + Назва, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                дадзеныя = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(дадзеныя) == int(일치.group(1)); return дадзеныя
            абалонка('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            абалонка('java -version', ['not OpenJDK', 'exit 0'])
            абалонка('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            абалонка('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            абалонка('python --version', ['MicroPython 1.24.1', 'exit 0'])
            абалонка('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Файл', 'exit 0'])
            абалонка('cat python.txt', ['한글 Файл'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(спампоўка('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            рэдагаваць_значэнне('인사.java', 'public class 인사 { public static void main(String[] args) { int значэнне = 7; System.out.println("한글=" + значэнне); } }')
            абалонка('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            абалонка('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(спампоўка('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            рэдагаваць_значэнне('Hello.java', 'broken', Адмена_аперацыя=True)
            абалонка('javac Hello.java', ['Compiled:', 'exit 0'])
            рэдагаваць_значэнне('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            абалонка('javac Broken.java', ['javac error:', 'exit 1'])
            запампоўка_Файлы('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            абалонка('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            абалонка('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            запампоўка_Файлы('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            абалонка('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            абалонка('rm Imported.class', [])
            рэдагаваць_значэнне('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            абалонка('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = абалонка('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            абалонка('rm Loop.java', []); абалонка('rm Loop.class', [])
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
            рэдагаваць_значэнне('checks.py', 파이썬검사)
            абалонка('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            абалонка('rm checks.py', [])
            рэдагаваць_значэнне('helper.py', 'value = 321')
            абалонка("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            абалонка('rm helper.py', [])
            абалонка("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            абалонка("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                абалонка('python hello.py', ['한글 Файл', 'exit 0'])
                абалонка('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            запампоўка_Файлы('app.elf', (기준 / 'build/user/demo.elf').read_bytes())
            assert спампоўка('app.elf') == (기준 / 'build/user/demo.elf').read_bytes()
            абалонка('run app.elf', ['EL0 C++', 'exit 0'])
            запампоўка_Файлы('app.elf', b'not an ELF')
            абалонка('run app.elf', ['exit -8'])
            абалонка('rm app.elf', [])
            абалонка('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            рукапісная_графіка_шлях = 출력결과 / 'java-framebuffer'; рукапісная_графіка_шлях.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준 / 'dist/jkoros-native-korean.jar'), '-d', str(рукапісная_графіка_шлях), str(기준 / '시험/자바/화면시험.java')])
            запампоўка_Файлы('화면시험.class', (рукапісная_графіка_шлях / '화면시험.class').read_bytes())
            абалонка('java 화면시험', ['화면 кліп адхіліць_значэнне', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            абалонка('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as кліент:
                кліент.settimeout(10)
                кліент.connect(str(모의제어경로))
                with кліент.makefile('rwb') as паток_значэнне:
                    인사 = json.loads(паток_значэнне.readline())
                    def 모의제어접속(Выкананне, 전달인수=None):
                        Сетка_ліст = {'execute': Выкананне}
                        if 전달인수: Сетка_ліст['arguments'] = 전달인수
                        паток_значэнне.write((json.dumps(Сетка_ліст) + '\n').encode())
                        паток_значэнне.flush()
                        while True:
                            адказаць = json.loads(паток_значэнне.readline())
                            if 'error' in адказаць: raise AssertionError(адказаць)
                            if 'return' in адказаць: return адказаць['return']
                    모의제어접속('qmp_capabilities')
                    здымак_экрана = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(здымак_экрана), 'format': 'ppm'})
                    def 예제들(ШЛЯХ, 지점들):
                        with ШЛЯХ.open('rb') as пэл_файл:
                            assert пэл_файл.readline().strip() == b'P6'
                            assert пэл_файл.readline().strip() == b'640 480'
                            assert пэл_файл.readline().strip() == b'255'
                            пэл_дадзеныя = пэл_файл.read()
                        assert len(пэл_дадзеныя) == 640 * 480 * 3
                        return [list(пэл_дадзеныя[(세로좌표 * 640 + каардыната_x) * 3:(세로좌표 * 640 + каардыната_x) * 3 + 3]) for каардыната_x, 세로좌표 in 지점들]
                    assert 예제들(здымак_экрана, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(здымак_экрана, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def адправіць(누름값, 확인표시):
                        Зрух_значэнне = len(대화기록)
                        Працэс.stdin.write(누름값); Працэс.stdin.flush()
                        표시까지받기(확인표시, Зрух_значэнне)
                    адправіць(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    адправіць(b'\r', b'GUI ACTION 0 RESULT 0')
                    адправіць(b'\t', b'GUI FOCUS 1')
                    адправіць(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    адправіць(b'\t', b'GUI FOCUS 2')
                    адправіць(b'\r', b'GUI ACTION 2 RESULT 0')
                    адправіць(b'\t', b'GUI FOCUS 3')
                    адправіць(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    адправіць(b'q', b'jkoros-native> ')
                    праверка_справаздача['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Працэс.wait(timeout=10)
            # framebuffer 응답뿐 아니라 фактычны_дадзеныя scanout 픽셀도 확인한다.
            with здымак_экрана.open('rb') as файл_увядзенне:
                assert файл_увядзенне.readline().strip() == b'P6'
                치수 = файл_увядзенне.readline().strip()
                assert 치수 == b'640 480', 치수
                assert файл_увядзенне.readline().strip() == b'255'
                화소들 = файл_увядзенне.read()
            assert len(화소들) == 640 * 480 * 3
            def пэл(каардыната_x, 세로좌표): return list(화소들[(세로좌표 * 640 + каардыната_x) * 3:(세로좌표 * 640 + каардыната_x) * 3 + 3])
            예제들 = {'background': пэл(5, 5), 'panel': пэл(45, 85), 'tile': пэл(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            праверка_справаздача.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
            if Працэс.poll() is None:
                Працэс.terminate()
                try: Працэс.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Працэс.kill(); Працэс.wait(timeout=5)
            селектар.close()
            Працэс.stdin.close(); Працэс.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(праверка_справаздача, indent=2) + '\n')


if __name__ == '__main__':
    Выканаць()
