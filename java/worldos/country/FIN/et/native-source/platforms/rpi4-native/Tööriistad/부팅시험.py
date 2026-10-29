#!/usr/bin/env python3
"""tegelik_andmed raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from Täida_käsk import Project_juur, Käsk


def Käivita_2():
    toodang = Project_juur / 'build/verification'
    toodang.mkdir(parents=True, exist_ok=True)
    transkriptsioon = bytearray()
    kinnitamine_aruanne = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Käsk() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        kinnitamine_aruanne['command'] = 명령인수
        Protsess = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        valija = selectors.DefaultSelector()
        valija.register(Protsess.stdout, selectors.EVENT_READ)
        def 표시까지받기(marker, nihe_VALUE=0, 시간제한=45):
            tähtaeg_Aeg = time.monotonic() + 시간제한
            while marker not in transkriptsioon[nihe_VALUE:]:
                if time.monotonic() > tähtaeg_Aeg:
                    raise AssertionError('UART timeout: ' + repr(marker))
                for 누름값, _ in valija.select(0.2):
                    andmeplokk = 누름값.fileobj.read(4096)
                    if andmeplokk:
                        transkriptsioon.extend(andmeplokk)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', transkriptsioon):
                    raise AssertionError('kernel failure')
                if Protsess.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Protsess.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for marker in 확인표시들:
                assert marker in transkriptsioon, marker
            # GTK 없는 tähtaja_piires_kaup 호스트에서도 VNC로 tegelik_andmed GUI를 볼 number 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def EXACT_VALUE(Suurus):
                    TULEMUS = b''
                    while len(TULEMUS) < Suurus:
                        조각 = 화면접속자.recv(Suurus - len(TULEMUS))
                        if not 조각: raise AssertionError('VNC disconnected')
                        TULEMUS += 조각
                    return TULEMUS
                assert EXACT_VALUE(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in EXACT_VALUE(EXACT_VALUE(1)[0]); 화면접속자.sendall(b'\x01')
                assert EXACT_VALUE(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                server_VALUE = EXACT_VALUE(24)
                assert int.from_bytes(server_VALUE[:2], 'big') == 640 and int.from_bytes(server_VALUE[2:4], 'big') == 480
                EXACT_VALUE(int.from_bytes(server_VALUE[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for käsk_bait, marker in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                nihe_VALUE = len(transkriptsioon)
                Protsess.stdin.write(käsk_bait + b'\n')
                Protsess.stdin.flush()
                표시까지받기(b'jkoros-native> ', nihe_VALUE)
                assert marker in transkriptsioon[nihe_VALUE:], marker
            def kest(Joon, 예상결과):
                nihe_VALUE = len(transkriptsioon)
                Protsess.stdin.write(Joon.encode('utf-8') + b'\n'); Protsess.stdin.flush()
                표시까지받기(b'jkoros-native> ', nihe_VALUE)
                vastus_1262b476 = bytes(transkriptsioon[nihe_VALUE:])
                for Tekst in 예상결과:
                    assert Tekst.encode('utf-8') in vastus_1262b476, (Joon, Tekst, vastus_1262b476)
                return vastus_1262b476
            def sisestama(Joon, viip):
                nihe_VALUE = len(transkriptsioon)
                Protsess.stdin.write(Joon.encode('utf-8') + b'\n'); Protsess.stdin.flush()
                표시까지받기(viip, nihe_VALUE)
                return bytes(transkriptsioon[nihe_VALUE:])
            def muudatus_VALUE(Nimi_2, Sisu_VALUE, Loobu_lõikus=False):
                sisestama('edit ' + Nimi_2, b'edit> ')
                for Joon in Sisu_VALUE.splitlines(): sisestama(Joon, b'edit> ')
                if Loobu_lõikus:
                    nihe_VALUE = len(transkriptsioon)
                    Protsess.stdin.write(b'\x03'); Protsess.stdin.flush()
                    표시까지받기(b'jkoros-native> ', nihe_VALUE)
                    assert b'EDIT CANCELLED' in transkriptsioon[nihe_VALUE:]
                else:
                    assert b'SAVED' in sisestama('.', b'jkoros-native> ')
            def Upload_Failid(Nimi_2, andmed):
                assert len(andmed) <= 16384
                sisestama('load ' + Nimi_2, b'hex> ')
                for 순번 in range(0, len(andmed), 64): sisestama(andmed[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in sisestama('.', b'jkoros-native> ')
            def alla_laadima(Nimi_2):
                vastus_1262b476 = kest('hex ' + Nimi_2, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', vastus_1262b476, re.S)
                andmed = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(andmed) == int(일치.group(1)); return andmed
            kest('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            kest('java -version', ['not OpenJDK', 'exit 0'])
            kest('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            kest('java Hello "한글 Argumendid 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Argumendid 😀', 'exit 0'])
            kest('python --version', ['MicroPython 1.24.1', 'exit 0'])
            kest('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Fail', 'exit 0'])
            kest('cat python.txt', ['한글 Fail'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = toodang / 'Hello.class'; 자바클래스.write_bytes(alla_laadima('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(toodang), 'Hello', '한글 Argumendid 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Argumendid 😀'], 예상결과
            muudatus_VALUE('인사.java', 'public class 인사 { public static void main(String[] args) { int VALUE = 7; System.out.println("한글=" + VALUE); } }')
            kest('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            kest('java 인사', ['한글=7', 'exit 0'])
            (toodang / '인사.class').write_bytes(alla_laadima('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(toodang), '인사']).decode().strip() == '한글=7'
            muudatus_VALUE('Hello.java', 'broken', Loobu_lõikus=True)
            kest('javac Hello.java', ['Compiled:', 'exit 0'])
            muudatus_VALUE('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            kest('javac Broken.java', ['javac error:', 'exit 1'])
            Upload_Failid('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            kest('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            kest('rm Broken.java', [])
            들여온파일 = toodang / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Upload_Failid('Imported.class', (toodang / 'Imported.class').read_bytes())
            kest('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            kest('rm Imported.class', [])
            muudatus_VALUE('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            kest('javac Loop.java', ['Compiled:', 'exit 0'])
            vastus_1262b476 = kest('java Loop', ['exit '])
            assert b'instruction limit' in vastus_1262b476 or b'exit -1004' in vastus_1262b476
            kest('rm Loop.java', []); kest('rm Loop.class', [])
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
            muudatus_VALUE('checks.py', 파이썬검사)
            kest('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            kest('rm checks.py', [])
            muudatus_VALUE('helper.py', 'value = 321')
            kest("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            kest('rm helper.py', [])
            kest("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            kest("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                kest('python hello.py', ['한글 Fail', 'exit 0'])
                kest('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Upload_Failid('app.elf', (Project_juur / 'build/user/demo.elf').read_bytes())
            assert alla_laadima('app.elf') == (Project_juur / 'build/user/demo.elf').read_bytes()
            kest('run app.elf', ['EL0 C++', 'exit 0'])
            Upload_Failid('app.elf', b'not an ELF')
            kest('run app.elf', ['exit -8'])
            kest('rm app.elf', [])
            kest('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            joonis_tee = toodang / 'java-framebuffer'; joonis_tee.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_juur / 'dist/jkoros-native-korean.jar'), '-d', str(joonis_tee), str(Project_juur / '시험/자바/화면시험.java')])
            Upload_Failid('화면시험.class', (joonis_tee / '화면시험.class').read_bytes())
            kest('java 화면시험', ['화면 klipp keelduma_VALUE', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            kest('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as klient:
                klient.settimeout(10)
                klient.connect(str(모의제어경로))
                with klient.makefile('rwb') as voog_VALUE:
                    인사 = json.loads(voog_VALUE.readline())
                    def 모의제어접속(Käivita, 전달인수=None):
                        võrk_meil = {'execute': Käivita}
                        if 전달인수: võrk_meil['arguments'] = 전달인수
                        voog_VALUE.write((json.dumps(võrk_meil) + '\n').encode())
                        voog_VALUE.flush()
                        while True:
                            vastus = json.loads(voog_VALUE.readline())
                            if 'error' in vastus: raise AssertionError(vastus)
                            if 'return' in vastus: return vastus['return']
                    모의제어접속('qmp_capabilities')
                    kuvalõige = toodang / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(kuvalõige), 'format': 'ppm'})
                    def 예제들(RADA, 지점들):
                        with RADA.open('rb') as piksel_Fail:
                            assert piksel_Fail.readline().strip() == b'P6'
                            assert piksel_Fail.readline().strip() == b'640 480'
                            assert piksel_Fail.readline().strip() == b'255'
                            piksel_andmed = piksel_Fail.read()
                        assert len(piksel_andmed) == 640 * 480 * 3
                        return [list(piksel_andmed[(세로좌표 * 640 + 가로좌표) * 3:(세로좌표 * 640 + 가로좌표) * 3 + 3]) for 가로좌표, 세로좌표 in 지점들]
                    assert 예제들(kuvalõige, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(kuvalõige, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def saatma(누름값, marker):
                        nihe_VALUE = len(transkriptsioon)
                        Protsess.stdin.write(누름값); Protsess.stdin.flush()
                        표시까지받기(marker, nihe_VALUE)
                    saatma(b'gui\n', b'GUI READY:')
                    첫화면 = toodang / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(toodang / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    saatma(b'\r', b'GUI ACTION 0 RESULT 0')
                    saatma(b'\t', b'GUI FOCUS 1')
                    saatma(b'\r', b'GUI ACTION 1 RESULT 0')
                    SECOND_GUI = toodang / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SECOND_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(toodang / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SECOND_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    saatma(b'\t', b'GUI FOCUS 2')
                    saatma(b'\r', b'GUI ACTION 2 RESULT 0')
                    saatma(b'\t', b'GUI FOCUS 3')
                    saatma(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(toodang / 'gui-python.png'), 'format': 'png'})
                    saatma(b'q', b'jkoros-native> ')
                    kinnitamine_aruanne['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Protsess.wait(timeout=10)
            # framebuffer 응답뿐 아니라 tegelik_andmed scanout 픽셀도 확인한다.
            with kuvalõige.open('rb') as Fail_kirje:
                assert Fail_kirje.readline().strip() == b'P6'
                치수 = Fail_kirje.readline().strip()
                assert 치수 == b'640 480', 치수
                assert Fail_kirje.readline().strip() == b'255'
                화소들 = Fail_kirje.read()
            assert len(화소들) == 640 * 480 * 3
            def piksel(가로좌표, 세로좌표): return list(화소들[(세로좌표 * 640 + 가로좌표) * 3:(세로좌표 * 640 + 가로좌표) * 3 + 3])
            예제들 = {'background': piksel(5, 5), 'panel': piksel(45, 85), 'tile': piksel(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            kinnitamine_aruanne.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((Project_juur / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Protsess.poll() is None:
                Protsess.terminate()
                try: Protsess.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Protsess.kill(); Protsess.wait(timeout=5)
            valija.close()
            Protsess.stdin.close(); Protsess.stdout.close()
            (toodang / 'serial.log').write_bytes(transkriptsioon)
            (toodang / 'report.json').write_text(json.dumps(kinnitamine_aruanne, indent=2) + '\n')


if __name__ == '__main__':
    Käivita_2()
