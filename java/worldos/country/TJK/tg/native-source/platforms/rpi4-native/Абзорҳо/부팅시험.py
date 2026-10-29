#!/usr/bin/env python3
"""воқеӣ_иттилоот raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from иҷро_кардан_фармон import 기준, фармон


def порча():
    출력결과 = 기준 / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    санҷиши_эътибор_гузориш = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = фармон() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        санҷиши_эътибор_гузориш['command'] = 명령인수
        Раванд = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        интихобкунанда = selectors.DefaultSelector()
        интихобкунанда.register(Раванд.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, Интиқолшавӣ_қимат=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[Интиқолшавӣ_қимат:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in интихобкунанда.select(0.2):
                    иттилоот_манъ_кардан = 누름값.fileobj.read(4096)
                    if иттилоот_манъ_кардан:
                        대화기록.extend(иттилоот_манъ_кардан)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if Раванд.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Раванд.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 воқеӣ_иттилоот GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(андоза_кардан):
                    결과 = b''
                    while len(결과) < андоза_кардан:
                        조각 = 화면접속자.recv(андоза_кардан - len(결과))
                        if not 조각: raise AssertionError('VNC disconnected')
                        결과 += 조각
                    return 결과
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                сервер_қимат = 정확한값(24)
                assert int.from_bytes(сервер_қимат[:2], 'big') == 640 and int.from_bytes(сервер_қимат[2:4], 'big') == 480
                정확한값(int.from_bytes(сервер_қимат[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for фармон_байт, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                Интиқолшавӣ_қимат = len(대화기록)
                Раванд.stdin.write(фармон_байт + b'\n')
                Раванд.stdin.flush()
                표시까지받기(b'jkoros-native> ', Интиқолшавӣ_қимат)
                assert 확인표시 in 대화기록[Интиқолшавӣ_қимат:], 확인표시
            def восит(хат, 예상결과):
                Интиқолшавӣ_қимат = len(대화기록)
                Раванд.stdin.write(хат.encode('utf-8') + b'\n'); Раванд.stdin.flush()
                표시까지받기(b'jkoros-native> ', Интиқолшавӣ_қимат)
                응답자료 = bytes(대화기록[Интиқолшавӣ_қимат:])
                for Матн in 예상결과:
                    assert Матн.encode('utf-8') in 응답자료, (хат, Матн, 응답자료)
                return 응답자료
            def ворид_кардан(хат, сатри_фармон):
                Интиқолшавӣ_қимат = len(대화기록)
                Раванд.stdin.write(хат.encode('utf-8') + b'\n'); Раванд.stdin.flush()
                표시까지받기(сатри_фармон, Интиқолшавӣ_қимат)
                return bytes(대화기록[Интиқолшавӣ_қимат:])
            def таҳрир_қимат(Ном, Мӯҳтаво_қимат, бекор_кардан_кор=False):
                ворид_кардан('edit ' + Ном, b'edit> ')
                for хат in Мӯҳтаво_қимат.splitlines(): ворид_кардан(хат, b'edit> ')
                if бекор_кардан_кор:
                    Интиқолшавӣ_қимат = len(대화기록)
                    Раванд.stdin.write(b'\x03'); Раванд.stdin.flush()
                    표시까지받기(b'jkoros-native> ', Интиқолшавӣ_қимат)
                    assert b'EDIT CANCELLED' in 대화기록[Интиқолшавӣ_қимат:]
                else:
                    assert b'SAVED' in ворид_кардан('.', b'jkoros-native> ')
            def бор_кардан_Файлҳо(Ном, иттилоот):
                assert len(иттилоот) <= 16384
                ворид_кардан('load ' + Ном, b'hex> ')
                for 순번 in range(0, len(иттилоот), 64): ворид_кардан(иттилоот[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in ворид_кардан('.', b'jkoros-native> ')
            def боргирӣ(Ном):
                응답자료 = восит('hex ' + Ном, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                иттилоот = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(иттилоот) == int(일치.group(1)); return иттилоот
            восит('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            восит('java -version', ['not OpenJDK', 'exit 0'])
            восит('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            восит('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            восит('python --version', ['MicroPython 1.24.1', 'exit 0'])
            восит('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Файл', 'exit 0'])
            восит('cat python.txt', ['한글 Файл'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(боргирӣ('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            таҳрир_қимат('인사.java', 'public class 인사 { public static void main(String[] args) { int қимат = 7; System.out.println("한글=" + қимат); } }')
            восит('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            восит('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(боргирӣ('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            таҳрир_қимат('Hello.java', 'broken', бекор_кардан_кор=True)
            восит('javac Hello.java', ['Compiled:', 'exit 0'])
            таҳрир_қимат('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            восит('javac Broken.java', ['javac error:', 'exit 1'])
            бор_кардан_Файлҳо('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            восит('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            восит('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            бор_кардан_Файлҳо('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            восит('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            восит('rm Imported.class', [])
            таҳрир_қимат('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            восит('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = восит('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            восит('rm Loop.java', []); восит('rm Loop.class', [])
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
            таҳрир_қимат('checks.py', 파이썬검사)
            восит('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            восит('rm checks.py', [])
            таҳрир_қимат('helper.py', 'value = 321')
            восит("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            восит('rm helper.py', [])
            восит("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            восит("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                восит('python hello.py', ['한글 Файл', 'exit 0'])
                восит('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            бор_кардан_Файлҳо('app.elf', (기준 / 'build/user/demo.elf').read_bytes())
            assert боргирӣ('app.elf') == (기준 / 'build/user/demo.elf').read_bytes()
            восит('run app.elf', ['EL0 C++', 'exit 0'])
            бор_кардан_Файлҳо('app.elf', b'not an ELF')
            восит('run app.elf', ['exit -8'])
            восит('rm app.elf', [])
            восит('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            нақша_масир = 출력결과 / 'java-framebuffer'; нақша_масир.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준 / 'dist/jkoros-native-korean.jar'), '-d', str(нақша_масир), str(기준 / '시험/자바/화면시험.java')])
            бор_кардан_Файлҳо('화면시험.class', (нақша_масир / '화면시험.class').read_bytes())
            восит('java 화면시험', ['화면 клип 거부', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            восит('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as муштарӣ:
                муштарӣ.settimeout(10)
                муштарӣ.connect(str(모의제어경로))
                with муштарӣ.makefile('rwb') as ҷараён_қимат:
                    인사 = json.loads(ҷараён_қимат.readline())
                    def 모의제어접속(Иҷро_кардан, 전달인수=None):
                        Шабака_паём = {'execute': Иҷро_кардан}
                        if 전달인수: Шабака_паём['arguments'] = 전달인수
                        ҷараён_қимат.write((json.dumps(Шабака_паём) + '\n').encode())
                        ҷараён_қимат.flush()
                        while True:
                            ҷавоб_додан = json.loads(ҷараён_қимат.readline())
                            if 'error' in ҷавоб_додан: raise AssertionError(ҷавоб_додан)
                            if 'return' in ҷавоб_додан: return ҷавоб_додан['return']
                    모의제어접속('qmp_capabilities')
                    буридаи_экран = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(буридаи_экран), 'format': 'ppm'})
                    def 예제들(масир, 지점들):
                        with масир.open('rb') as пиксел_файл:
                            assert пиксел_файл.readline().strip() == b'P6'
                            assert пиксел_файл.readline().strip() == b'640 480'
                            assert пиксел_файл.readline().strip() == b'255'
                            пиксел_иттилоот = пиксел_файл.read()
                        assert len(пиксел_иттилоот) == 640 * 480 * 3
                        return [list(пиксел_иттилоот[(세로좌표 * 640 + координатаи_х) * 3:(세로좌표 * 640 + координатаи_х) * 3 + 3]) for координатаи_х, 세로좌표 in 지점들]
                    assert 예제들(буридаи_экран, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(буридаи_экран, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def фиристодан(누름값, 확인표시):
                        Интиқолшавӣ_қимат = len(대화기록)
                        Раванд.stdin.write(누름값); Раванд.stdin.flush()
                        표시까지받기(확인표시, Интиқолшавӣ_қимат)
                    фиристодан(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    фиристодан(b'\r', b'GUI ACTION 0 RESULT 0')
                    фиристодан(b'\t', b'GUI FOCUS 1')
                    фиристодан(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    фиристодан(b'\t', b'GUI FOCUS 2')
                    фиристодан(b'\r', b'GUI ACTION 2 RESULT 0')
                    фиристодан(b'\t', b'GUI FOCUS 3')
                    фиристодан(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    фиристодан(b'q', b'jkoros-native> ')
                    санҷиши_эътибор_гузориш['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Раванд.wait(timeout=10)
            # framebuffer 응답뿐 아니라 воқеӣ_иттилоот scanout 픽셀도 확인한다.
            with буридаи_экран.open('rb') as файл_ворида:
                assert файл_ворида.readline().strip() == b'P6'
                치수 = файл_ворида.readline().strip()
                assert 치수 == b'640 480', 치수
                assert файл_ворида.readline().strip() == b'255'
                화소들 = файл_ворида.read()
            assert len(화소들) == 640 * 480 * 3
            def пиксел(координатаи_х, 세로좌표): return list(화소들[(세로좌표 * 640 + координатаи_х) * 3:(세로좌표 * 640 + координатаи_х) * 3 + 3])
            예제들 = {'background': пиксел(5, 5), 'panel': пиксел(45, 85), 'tile': пиксел(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            санҷиши_эътибор_гузориш.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
            if Раванд.poll() is None:
                Раванд.terminate()
                try: Раванд.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Раванд.kill(); Раванд.wait(timeout=5)
            интихобкунанда.close()
            Раванд.stdin.close(); Раванд.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(санҷиши_эътибор_гузориш, indent=2) + '\n')


if __name__ == '__main__':
    порча()
