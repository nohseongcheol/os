#!/usr/bin/env python3
"""real_date raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from executa_comandă import Project_rădăcină, Comandă


def Pornește():
    출력결과 = Project_rădăcină / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    transcriere = bytearray()
    validare_raport = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Comandă() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        validare_raport['command'] = 명령인수
        Proces = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        selector = selectors.DefaultSelector()
        selector.register(Proces.stdout, selectors.EVENT_READ)
        def 표시까지받기(marcaj, OFFSET_VALUE=0, executare_TIMEOUT=45):
            dată_limită_oră = time.monotonic() + executare_TIMEOUT
            while marcaj not in transcriere[OFFSET_VALUE:]:
                if time.monotonic() > dată_limită_oră:
                    raise AssertionError('UART timeout: ' + repr(marcaj))
                for 누름값, _ in selector.select(0.2):
                    bloc_de_date = 누름값.fileobj.read(4096)
                    if bloc_de_date:
                        transcriere.extend(bloc_de_date)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', transcriere):
                    raise AssertionError('kernel failure')
                if Proces.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Proces.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for marcaj in 확인표시들:
                assert marcaj in transcriere, marcaj
            # GTK 없는 curent_element 호스트에서도 VNC로 real_date GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def EXACT_VALUE(Mărime):
                    KR = b''
                    while len(KR) < Mărime:
                        조각 = 화면접속자.recv(Mărime - len(KR))
                        if not 조각: raise AssertionError('VNC disconnected')
                        KR += 조각
                    return KR
                assert EXACT_VALUE(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in EXACT_VALUE(EXACT_VALUE(1)[0]); 화면접속자.sendall(b'\x01')
                assert EXACT_VALUE(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                server_VALUE = EXACT_VALUE(24)
                assert int.from_bytes(server_VALUE[:2], 'big') == 640 and int.from_bytes(server_VALUE[2:4], 'big') == 480
                EXACT_VALUE(int.from_bytes(server_VALUE[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for comandă_byte, marcaj in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                OFFSET_VALUE = len(transcriere)
                Proces.stdin.write(comandă_byte + b'\n')
                Proces.stdin.flush()
                표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                assert marcaj in transcriere[OFFSET_VALUE:], marcaj
            def shell(Linie, 예상결과):
                OFFSET_VALUE = len(transcriere)
                Proces.stdin.write(Linie.encode('utf-8') + b'\n'); Proces.stdin.flush()
                표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                răspuns = bytes(transcriere[OFFSET_VALUE:])
                for SMS in 예상결과:
                    assert SMS.encode('utf-8') in răspuns, (Linie, SMS, răspuns)
                return răspuns
            def introduce(Linie, solicita):
                OFFSET_VALUE = len(transcriere)
                Proces.stdin.write(Linie.encode('utf-8') + b'\n'); Proces.stdin.flush()
                표시까지받기(solicita, OFFSET_VALUE)
                return bytes(transcriere[OFFSET_VALUE:])
            def edita_VALUE(Nume, Conținut_VALUE, anula_operație=False):
                introduce('edit ' + Nume, b'edit> ')
                for Linie in Conținut_VALUE.splitlines(): introduce(Linie, b'edit> ')
                if anula_operație:
                    OFFSET_VALUE = len(transcriere)
                    Proces.stdin.write(b'\x03'); Proces.stdin.flush()
                    표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                    assert b'EDIT CANCELLED' in transcriere[OFFSET_VALUE:]
                else:
                    assert b'SAVED' in introduce('.', b'jkoros-native> ')
            def Upload_Fișiere(Nume, date):
                assert len(date) <= 16384
                introduce('load ' + Nume, b'hex> ')
                for 순번 in range(0, len(date), 64): introduce(date[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in introduce('.', b'jkoros-native> ')
            def descărca(Nume):
                răspuns = shell('hex ' + Nume, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', răspuns, re.S)
                date = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(date) == int(일치.group(1)); return date
            shell('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            shell('java -version', ['not OpenJDK', 'exit 0'])
            shell('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            shell('java Hello "한글 Argumente 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Argumente 😀', 'exit 0'])
            shell('python --version', ['MicroPython 1.24.1', 'exit 0'])
            shell('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Fișier', 'exit 0'])
            shell('cat python.txt', ['한글 Fișier'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(descărca('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 Argumente 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Argumente 😀'], 예상결과
            edita_VALUE('인사.java', 'public class 인사 { public static void main(String[] args) { int VALUE = 7; System.out.println("한글=" + VALUE); } }')
            shell('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            shell('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(descărca('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            edita_VALUE('Hello.java', 'broken', anula_operație=True)
            shell('javac Hello.java', ['Compiled:', 'exit 0'])
            edita_VALUE('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            shell('javac Broken.java', ['javac error:', 'exit 1'])
            Upload_Fișiere('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            shell('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            shell('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Upload_Fișiere('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            shell('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            shell('rm Imported.class', [])
            edita_VALUE('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            shell('javac Loop.java', ['Compiled:', 'exit 0'])
            răspuns = shell('java Loop', ['exit '])
            assert b'instruction limit' in răspuns or b'exit -1004' in răspuns
            shell('rm Loop.java', []); shell('rm Loop.class', [])
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
            edita_VALUE('checks.py', 파이썬검사)
            shell('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            shell('rm checks.py', [])
            edita_VALUE('helper.py', 'value = 321')
            shell("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            shell('rm helper.py', [])
            shell("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            shell("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                shell('python hello.py', ['한글 Fișier', 'exit 0'])
                shell('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Upload_Fișiere('app.elf', (Project_rădăcină / 'build/user/demo.elf').read_bytes())
            assert descărca('app.elf') == (Project_rădăcină / 'build/user/demo.elf').read_bytes()
            shell('run app.elf', ['EL0 C++', 'exit 0'])
            Upload_Fișiere('app.elf', b'not an ELF')
            shell('run app.elf', ['exit -8'])
            shell('rm app.elf', [])
            shell('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            desen_cale = 출력결과 / 'java-framebuffer'; desen_cale.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_rădăcină / 'dist/jkoros-native-korean.jar'), '-d', str(desen_cale), str(Project_rădăcină / '시험/자바/화면시험.java')])
            Upload_Fișiere('화면시험.class', (desen_cale / '화면시험.class').read_bytes())
            shell('java 화면시험', ['화면 clip respinge_VALUE', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            shell('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as client:
                client.settimeout(10)
                client.connect(str(모의제어경로))
                with client.makefile('rwb') as flux_VALUE:
                    인사 = json.loads(flux_VALUE.readline())
                    def 모의제어접속(Execută, 전달인수=None):
                        rețea_mesaj = {'execute': Execută}
                        if 전달인수: rețea_mesaj['arguments'] = 전달인수
                        flux_VALUE.write((json.dumps(rețea_mesaj) + '\n').encode())
                        flux_VALUE.flush()
                        while True:
                            replică = json.loads(flux_VALUE.readline())
                            if 'error' in replică: raise AssertionError(replică)
                            if 'return' in replică: return replică['return']
                    모의제어접속('qmp_capabilities')
                    captură_de_ecran = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(captură_de_ecran), 'format': 'ppm'})
                    def 예제들(Cale, 지점들):
                        with Cale.open('rb') as element_imagine_Fișier:
                            assert element_imagine_Fișier.readline().strip() == b'P6'
                            assert element_imagine_Fișier.readline().strip() == b'640 480'
                            assert element_imagine_Fișier.readline().strip() == b'255'
                            element_imagine_date = element_imagine_Fișier.read()
                        assert len(element_imagine_date) == 640 * 480 * 3
                        return [list(element_imagine_date[(세로좌표 * 640 + coordonata_X) * 3:(세로좌표 * 640 + coordonata_X) * 3 + 3]) for coordonata_X, 세로좌표 in 지점들]
                    assert 예제들(captură_de_ecran, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(captură_de_ecran, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def trimite(누름값, marcaj):
                        OFFSET_VALUE = len(transcriere)
                        Proces.stdin.write(누름값); Proces.stdin.flush()
                        표시까지받기(marcaj, OFFSET_VALUE)
                    trimite(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    trimite(b'\r', b'GUI ACTION 0 RESULT 0')
                    trimite(b'\t', b'GUI FOCUS 1')
                    trimite(b'\r', b'GUI ACTION 1 RESULT 0')
                    SECOND_GUI = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SECOND_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SECOND_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    trimite(b'\t', b'GUI FOCUS 2')
                    trimite(b'\r', b'GUI ACTION 2 RESULT 0')
                    trimite(b'\t', b'GUI FOCUS 3')
                    trimite(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    trimite(b'q', b'jkoros-native> ')
                    validare_raport['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Proces.wait(timeout=10)
            # framebuffer 응답뿐 아니라 real_date scanout 픽셀도 확인한다.
            with captură_de_ecran.open('rb') as Fișier_intrare:
                assert Fișier_intrare.readline().strip() == b'P6'
                치수 = Fișier_intrare.readline().strip()
                assert 치수 == b'640 480', 치수
                assert Fișier_intrare.readline().strip() == b'255'
                화소들 = Fișier_intrare.read()
            assert len(화소들) == 640 * 480 * 3
            def element_imagine(coordonata_X, 세로좌표): return list(화소들[(세로좌표 * 640 + coordonata_X) * 3:(세로좌표 * 640 + coordonata_X) * 3 + 3])
            예제들 = {'background': element_imagine(5, 5), 'panel': element_imagine(45, 85), 'tile': element_imagine(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            validare_raport.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((Project_rădăcină / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Proces.poll() is None:
                Proces.terminate()
                try: Proces.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Proces.kill(); Proces.wait(timeout=5)
            selector.close()
            Proces.stdin.close(); Proces.stdout.close()
            (출력결과 / 'serial.log').write_bytes(transcriere)
            (출력결과 / 'report.json').write_text(json.dumps(validare_raport, indent=2) + '\n')


if __name__ == '__main__':
    Pornește()
