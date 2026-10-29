#!/usr/bin/env python3
"""faktinis_duomenys raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from Vykdyti_komanda import Project_šaknis, Komanda


def Paleisti():
    išeiga = Project_šaknis / 'build/verification'
    išeiga.mkdir(parents=True, exist_ok=True)
    transkribavimas = bytearray()
    tikrinimas_pranešti = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Komanda() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        tikrinimas_pranešti['command'] = 명령인수
        Procesas = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        išrinkiklis = selectors.DefaultSelector()
        išrinkiklis.register(Procesas.stdout, selectors.EVENT_READ)
        def 표시까지받기(žymeklis, OFFSET_VALUE=0, 시간제한=45):
            terminas_TIME = time.monotonic() + 시간제한
            while žymeklis not in transkribavimas[OFFSET_VALUE:]:
                if time.monotonic() > terminas_TIME:
                    raise AssertionError('UART timeout: ' + repr(žymeklis))
                for 누름값, _ in išrinkiklis.select(0.2):
                    duomenų_blokas = 누름값.fileobj.read(4096)
                    if duomenų_blokas:
                        transkribavimas.extend(duomenų_blokas)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', transkribavimas):
                    raise AssertionError('kernel failure')
                if Procesas.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Procesas.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for žymeklis in 확인표시들:
                assert žymeklis in transkribavimas, žymeklis
            # GTK 없는 dabartinis_prekė 호스트에서도 VNC로 faktinis_duomenys GUI를 볼 numeris 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def EXACT_VALUE(Dydis):
                    REZULTATAS = b''
                    while len(REZULTATAS) < Dydis:
                        조각 = 화면접속자.recv(Dydis - len(REZULTATAS))
                        if not 조각: raise AssertionError('VNC disconnected')
                        REZULTATAS += 조각
                    return REZULTATAS
                assert EXACT_VALUE(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in EXACT_VALUE(EXACT_VALUE(1)[0]); 화면접속자.sendall(b'\x01')
                assert EXACT_VALUE(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                serveris_VALUE = EXACT_VALUE(24)
                assert int.from_bytes(serveris_VALUE[:2], 'big') == 640 and int.from_bytes(serveris_VALUE[2:4], 'big') == 480
                EXACT_VALUE(int.from_bytes(serveris_VALUE[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for komanda_baitas, žymeklis in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                OFFSET_VALUE = len(transkribavimas)
                Procesas.stdin.write(komanda_baitas + b'\n')
                Procesas.stdin.flush()
                표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                assert žymeklis in transkribavimas[OFFSET_VALUE:], žymeklis
            def apvalkalas(Eilutė, 예상결과):
                OFFSET_VALUE = len(transkribavimas)
                Procesas.stdin.write(Eilutė.encode('utf-8') + b'\n'); Procesas.stdin.flush()
                표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                atsakas = bytes(transkribavimas[OFFSET_VALUE:])
                for Tekstas in 예상결과:
                    assert Tekstas.encode('utf-8') in atsakas, (Eilutė, Tekstas, atsakas)
                return atsakas
            def įvesti(Eilutė, raginimas):
                OFFSET_VALUE = len(transkribavimas)
                Procesas.stdin.write(Eilutė.encode('utf-8') + b'\n'); Procesas.stdin.flush()
                표시까지받기(raginimas, OFFSET_VALUE)
                return bytes(transkribavimas[OFFSET_VALUE:])
            def redaguoti_VALUE(Pavadinimas_2, Turinys_VALUE, Atšaukti_operacija=False):
                įvesti('edit ' + Pavadinimas_2, b'edit> ')
                for Eilutė in Turinys_VALUE.splitlines(): įvesti(Eilutė, b'edit> ')
                if Atšaukti_operacija:
                    OFFSET_VALUE = len(transkribavimas)
                    Procesas.stdin.write(b'\x03'); Procesas.stdin.flush()
                    표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                    assert b'EDIT CANCELLED' in transkribavimas[OFFSET_VALUE:]
                else:
                    assert b'SAVED' in įvesti('.', b'jkoros-native> ')
            def Upload_Failai(Pavadinimas_2, duomenys):
                assert len(duomenys) <= 16384
                įvesti('load ' + Pavadinimas_2, b'hex> ')
                for 순번 in range(0, len(duomenys), 64): įvesti(duomenys[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in įvesti('.', b'jkoros-native> ')
            def atsisiųsti(Pavadinimas_2):
                atsakas = apvalkalas('hex ' + Pavadinimas_2, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', atsakas, re.S)
                duomenys = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(duomenys) == int(일치.group(1)); return duomenys
            apvalkalas('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            apvalkalas('java -version', ['not OpenJDK', 'exit 0'])
            apvalkalas('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            apvalkalas('java Hello "한글 Argumentai 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Argumentai 😀', 'exit 0'])
            apvalkalas('python --version', ['MicroPython 1.24.1', 'exit 0'])
            apvalkalas('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Failas', 'exit 0'])
            apvalkalas('cat python.txt', ['한글 Failas'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = išeiga / 'Hello.class'; 자바클래스.write_bytes(atsisiųsti('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(išeiga), 'Hello', '한글 Argumentai 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Argumentai 😀'], 예상결과
            redaguoti_VALUE('인사.java', 'public class 인사 { public static void main(String[] args) { int VALUE = 7; System.out.println("한글=" + VALUE); } }')
            apvalkalas('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            apvalkalas('java 인사', ['한글=7', 'exit 0'])
            (išeiga / '인사.class').write_bytes(atsisiųsti('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(išeiga), '인사']).decode().strip() == '한글=7'
            redaguoti_VALUE('Hello.java', 'broken', Atšaukti_operacija=True)
            apvalkalas('javac Hello.java', ['Compiled:', 'exit 0'])
            redaguoti_VALUE('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            apvalkalas('javac Broken.java', ['javac error:', 'exit 1'])
            Upload_Failai('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            apvalkalas('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            apvalkalas('rm Broken.java', [])
            들여온파일 = išeiga / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Upload_Failai('Imported.class', (išeiga / 'Imported.class').read_bytes())
            apvalkalas('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            apvalkalas('rm Imported.class', [])
            redaguoti_VALUE('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            apvalkalas('javac Loop.java', ['Compiled:', 'exit 0'])
            atsakas = apvalkalas('java Loop', ['exit '])
            assert b'instruction limit' in atsakas or b'exit -1004' in atsakas
            apvalkalas('rm Loop.java', []); apvalkalas('rm Loop.class', [])
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
            redaguoti_VALUE('checks.py', 파이썬검사)
            apvalkalas('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            apvalkalas('rm checks.py', [])
            redaguoti_VALUE('helper.py', 'value = 321')
            apvalkalas("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            apvalkalas('rm helper.py', [])
            apvalkalas("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            apvalkalas("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                apvalkalas('python hello.py', ['한글 Failas', 'exit 0'])
                apvalkalas('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Upload_Failai('app.elf', (Project_šaknis / 'build/user/demo.elf').read_bytes())
            assert atsisiųsti('app.elf') == (Project_šaknis / 'build/user/demo.elf').read_bytes()
            apvalkalas('run app.elf', ['EL0 C++', 'exit 0'])
            Upload_Failai('app.elf', b'not an ELF')
            apvalkalas('run app.elf', ['exit -8'])
            apvalkalas('rm app.elf', [])
            apvalkalas('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            piešinys_kelias = išeiga / 'java-framebuffer'; piešinys_kelias.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_šaknis / 'dist/jkoros-native-korean.jar'), '-d', str(piešinys_kelias), str(Project_šaknis / '시험/자바/화면시험.java')])
            Upload_Failai('화면시험.class', (piešinys_kelias / '화면시험.class').read_bytes())
            apvalkalas('java 화면시험', ['화면 klipas atmesti_VALUE', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            apvalkalas('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as klientas:
                klientas.settimeout(10)
                klientas.connect(str(모의제어경로))
                with klientas.makefile('rwb') as Stream_VALUE:
                    인사 = json.loads(Stream_VALUE.readline())
                    def 모의제어접속(Vykdyti, 전달인수=None):
                        tinklas_žinutė = {'execute': Vykdyti}
                        if 전달인수: tinklas_žinutė['arguments'] = 전달인수
                        Stream_VALUE.write((json.dumps(tinklas_žinutė) + '\n').encode())
                        Stream_VALUE.flush()
                        while True:
                            atsakyti = json.loads(Stream_VALUE.readline())
                            if 'error' in atsakyti: raise AssertionError(atsakyti)
                            if 'return' in atsakyti: return atsakyti['return']
                    모의제어접속('qmp_capabilities')
                    ekrano_kopija = išeiga / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(ekrano_kopija), 'format': 'ppm'})
                    def 예제들(KELIAS, 지점들):
                        with KELIAS.open('rb') as pikselis_Failas:
                            assert pikselis_Failas.readline().strip() == b'P6'
                            assert pikselis_Failas.readline().strip() == b'640 480'
                            assert pikselis_Failas.readline().strip() == b'255'
                            pikselis_duomenys = pikselis_Failas.read()
                        assert len(pikselis_duomenys) == 640 * 480 * 3
                        return [list(pikselis_duomenys[(세로좌표 * 640 + x_koordinatė) * 3:(세로좌표 * 640 + x_koordinatė) * 3 + 3]) for x_koordinatė, 세로좌표 in 지점들]
                    assert 예제들(ekrano_kopija, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(ekrano_kopija, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def siųsti(누름값, žymeklis):
                        OFFSET_VALUE = len(transkribavimas)
                        Procesas.stdin.write(누름값); Procesas.stdin.flush()
                        표시까지받기(žymeklis, OFFSET_VALUE)
                    siųsti(b'gui\n', b'GUI READY:')
                    첫화면 = išeiga / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(išeiga / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    siųsti(b'\r', b'GUI ACTION 0 RESULT 0')
                    siųsti(b'\t', b'GUI FOCUS 1')
                    siųsti(b'\r', b'GUI ACTION 1 RESULT 0')
                    SECOND_GUI = išeiga / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SECOND_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(išeiga / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SECOND_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    siųsti(b'\t', b'GUI FOCUS 2')
                    siųsti(b'\r', b'GUI ACTION 2 RESULT 0')
                    siųsti(b'\t', b'GUI FOCUS 3')
                    siųsti(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(išeiga / 'gui-python.png'), 'format': 'png'})
                    siųsti(b'q', b'jkoros-native> ')
                    tikrinimas_pranešti['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Procesas.wait(timeout=10)
            # framebuffer 응답뿐 아니라 faktinis_duomenys scanout 픽셀도 확인한다.
            with ekrano_kopija.open('rb') as Failas_įrašas:
                assert Failas_įrašas.readline().strip() == b'P6'
                치수 = Failas_įrašas.readline().strip()
                assert 치수 == b'640 480', 치수
                assert Failas_įrašas.readline().strip() == b'255'
                화소들 = Failas_įrašas.read()
            assert len(화소들) == 640 * 480 * 3
            def pikselis(x_koordinatė, 세로좌표): return list(화소들[(세로좌표 * 640 + x_koordinatė) * 3:(세로좌표 * 640 + x_koordinatė) * 3 + 3])
            예제들 = {'background': pikselis(5, 5), 'panel': pikselis(45, 85), 'tile': pikselis(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            tikrinimas_pranešti.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((Project_šaknis / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Procesas.poll() is None:
                Procesas.terminate()
                try: Procesas.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Procesas.kill(); Procesas.wait(timeout=5)
            išrinkiklis.close()
            Procesas.stdin.close(); Procesas.stdout.close()
            (išeiga / 'serial.log').write_bytes(transkribavimas)
            (išeiga / 'report.json').write_text(json.dumps(tikrinimas_pranešti, indent=2) + '\n')


if __name__ == '__main__':
    Paleisti()
