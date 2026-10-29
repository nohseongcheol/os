#!/usr/bin/env python3
"""werkelijk_gegevens raspi4b machineopstart, UART invoer_WAARDE, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from Uitvoeren_opdracht import Taken_wortel, opdracht


def starten():
    uitvoer = Taken_wortel / 'build/verification'
    uitvoer.mkdir(parents=True, exist_ok=True)
    transcriptie = bytearray()
    validatie_Rapport = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = opdracht() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        validatie_Rapport['command'] = 명령인수
        Proces = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        selector = selectors.DefaultSelector()
        selector.register(Proces.stdout, selectors.EVENT_READ)
        def 표시까지받기(markering, VERSCHUIVING_WAARDE=0, uitvoerbewerking_TIMEOUT=45):
            deadline_TIJD = time.monotonic() + uitvoerbewerking_TIMEOUT
            while markering not in transcriptie[VERSCHUIVING_WAARDE:]:
                if time.monotonic() > deadline_TIJD:
                    raise AssertionError('UART timeout: ' + repr(markering))
                for 누름값, _ in selector.select(0.2):
                    gegevensblok = 누름값.fileobj.read(4096)
                    if gegevensblok:
                        transcriptie.extend(gegevensblok)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', transcriptie):
                    raise AssertionError('kernel failure')
                if Proces.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Proces.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for markering in 확인표시들:
                assert markering in transcriptie, markering
            # GTK 없는 actueel_item 호스트에서도 VNC로 werkelijk_gegevens GUI를 볼 nummer 있어야 한다.
            with socket.socket(socket.AF_UNIX) as scherm_client:
                scherm_client.settimeout(5); scherm_client.connect(str(Path(작업경로) / 'vnc.sock'))
                def GELIJK_WAARDE(Grootte):
                    resultaat = b''
                    while len(resultaat) < Grootte:
                        조각 = scherm_client.recv(Grootte - len(resultaat))
                        if not 조각: raise AssertionError('VNC disconnected')
                        resultaat += 조각
                    return resultaat
                assert GELIJK_WAARDE(12) == b'RFB 003.008\n'
                scherm_client.sendall(b'RFB 003.008\n')
                assert 1 in GELIJK_WAARDE(GELIJK_WAARDE(1)[0]); scherm_client.sendall(b'\x01')
                assert GELIJK_WAARDE(4) == b'\x00\x00\x00\x00'; scherm_client.sendall(b'\x01')
                server_WAARDE = GELIJK_WAARDE(24)
                assert int.from_bytes(server_WAARDE[:2], 'big') == 640 and int.from_bytes(server_WAARDE[2:4], 'big') == 480
                GELIJK_WAARDE(int.from_bytes(server_WAARDE[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for opdracht_byte, markering in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', 'tests.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                VERSCHUIVING_WAARDE = len(transcriptie)
                Proces.stdin.write(opdracht_byte + b'\n')
                Proces.stdin.flush()
                표시까지받기(b'jkoros-native> ', VERSCHUIVING_WAARDE)
                assert markering in transcriptie[VERSCHUIVING_WAARDE:], markering
            def Shell(invoerregel, 예상결과):
                VERSCHUIVING_WAARDE = len(transcriptie)
                Proces.stdin.write(invoerregel.encode('utf-8') + b'\n'); Proces.stdin.flush()
                표시까지받기(b'jkoros-native> ', VERSCHUIVING_WAARDE)
                reactie_1262b476 = bytes(transcriptie[VERSCHUIVING_WAARDE:])
                for tekst in 예상결과:
                    assert tekst.encode('utf-8') in reactie_1262b476, (invoerregel, tekst, reactie_1262b476)
                return reactie_1262b476
            def invoeren(invoerregel, prompt):
                VERSCHUIVING_WAARDE = len(transcriptie)
                Proces.stdin.write(invoerregel.encode('utf-8') + b'\n'); Proces.stdin.flush()
                표시까지받기(prompt, VERSCHUIVING_WAARDE)
                return bytes(transcriptie[VERSCHUIVING_WAARDE:])
            def Bewerk_WAARDE(Naam, Inhoud_WAARDE, Annuleren_operatie=False):
                invoeren('edit ' + Naam, b'edit> ')
                for invoerregel in Inhoud_WAARDE.splitlines(): invoeren(invoerregel, b'edit> ')
                if Annuleren_operatie:
                    VERSCHUIVING_WAARDE = len(transcriptie)
                    Proces.stdin.write(b'\x03'); Proces.stdin.flush()
                    표시까지받기(b'jkoros-native> ', VERSCHUIVING_WAARDE)
                    assert b'EDIT CANCELLED' in transcriptie[VERSCHUIVING_WAARDE:]
                else:
                    assert b'SAVED' in invoeren('.', b'jkoros-native> ')
            def Upload_Files(Naam, gegevens):
                assert len(gegevens) <= 16384
                invoeren('load ' + Naam, b'hex> ')
                for 순번 in range(0, len(gegevens), 64): invoeren(gegevens[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in invoeren('.', b'jkoros-native> ')
            def download(Naam):
                reactie_1262b476 = Shell('hex ' + Naam, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', reactie_1262b476, re.S)
                gegevens = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(gegevens) == int(일치.group(1)); return gegevens
            Shell('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            Shell('java -version', ['not OpenJDK', 'exit 0'])
            Shell('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            Shell('java Hello "한글 argumenten 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 argumenten 😀', 'exit 0'])
            Shell('python --version', ['MicroPython 1.24.1', 'exit 0'])
            Shell('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 bestand', 'exit 0'])
            Shell('cat python.txt', ['한글 bestand'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = uitvoer / 'Hello.class'; 자바클래스.write_bytes(download('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(uitvoer), 'Hello', '한글 argumenten 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 argumenten 😀'], 예상결과
            Bewerk_WAARDE('인사.java', 'public class 인사 { public static void main(String[] args) { int WAARDE = 7; System.out.println("한글=" + WAARDE); } }')
            Shell('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            Shell('java 인사', ['한글=7', 'exit 0'])
            (uitvoer / '인사.class').write_bytes(download('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(uitvoer), '인사']).decode().strip() == '한글=7'
            Bewerk_WAARDE('Hello.java', 'broken', Annuleren_operatie=True)
            Shell('javac Hello.java', ['Compiled:', 'exit 0'])
            Bewerk_WAARDE('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            Shell('javac Broken.java', ['javac error:', 'exit 1'])
            Upload_Files('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            Shell('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            Shell('rm Broken.java', [])
            들여온파일 = uitvoer / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Upload_Files('Imported.class', (uitvoer / 'Imported.class').read_bytes())
            Shell('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            Shell('rm Imported.class', [])
            Bewerk_WAARDE('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            Shell('javac Loop.java', ['Compiled:', 'exit 0'])
            reactie_1262b476 = Shell('java Loop', ['exit '])
            assert b'instruction limit' in reactie_1262b476 or b'exit -1004' in reactie_1262b476
            Shell('rm Loop.java', []); Shell('rm Loop.class', [])
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
            Bewerk_WAARDE('checks.py', 파이썬검사)
            Shell('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            Shell('rm checks.py', [])
            Bewerk_WAARDE('helper.py', 'value = 321')
            Shell("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            Shell('rm helper.py', [])
            Shell("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            Shell("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                Shell('python hello.py', ['한글 bestand', 'exit 0'])
                Shell('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Upload_Files('app.elf', (Taken_wortel / 'build/user/demo.elf').read_bytes())
            assert download('app.elf') == (Taken_wortel / 'build/user/demo.elf').read_bytes()
            Shell('run app.elf', ['EL0 C++', 'exit 0'])
            Upload_Files('app.elf', b'not an ELF')
            Shell('run app.elf', ['exit -8'])
            Shell('rm app.elf', [])
            Shell('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            tekening_pad = uitvoer / 'java-framebuffer'; tekening_pad.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Taken_wortel / 'dist/jkoros-native-korean.jar'), '-d', str(tekening_pad), str(Taken_wortel / 'tests/자바/test_scherm.java')])
            Upload_Files('test_scherm.class', (tekening_pad / 'test_scherm.class').read_bytes())
            Shell('java test_scherm', ['scherm clip weigeren_WAARDE', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            Shell('rm test_scherm.class', [])
            with socket.socket(socket.AF_UNIX) as client:
                client.settimeout(10)
                client.connect(str(모의제어경로))
                with client.makefile('rwb') as Stream_WAARDE:
                    인사 = json.loads(Stream_WAARDE.readline())
                    def 모의제어접속(Uitvoeren, 전달인수=None):
                        net_e_mail = {'execute': Uitvoeren}
                        if 전달인수: net_e_mail['arguments'] = 전달인수
                        Stream_WAARDE.write((json.dumps(net_e_mail) + '\n').encode())
                        Stream_WAARDE.flush()
                        while True:
                            reactie = json.loads(Stream_WAARDE.readline())
                            if 'error' in reactie: raise AssertionError(reactie)
                            if 'return' in reactie: return reactie['return']
                    모의제어접속('qmp_capabilities')
                    schermopname = uitvoer / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(schermopname), 'format': 'ppm'})
                    def 예제들(pad, 지점들):
                        with pad.open('rb') as pixel_Bestand:
                            assert pixel_Bestand.readline().strip() == b'P6'
                            assert pixel_Bestand.readline().strip() == b'640 480'
                            assert pixel_Bestand.readline().strip() == b'255'
                            pixel_gegevens = pixel_Bestand.read()
                        assert len(pixel_gegevens) == 640 * 480 * 3
                        return [list(pixel_gegevens[(Y_coördinaat * 640 + x_coördinaat) * 3:(Y_coördinaat * 640 + x_coördinaat) * 3 + 3]) for x_coördinaat, Y_coördinaat in 지점들]
                    assert 예제들(schermopname, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(schermopname, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def e_mailen(누름값, markering):
                        VERSCHUIVING_WAARDE = len(transcriptie)
                        Proces.stdin.write(누름값); Proces.stdin.flush()
                        표시까지받기(markering, VERSCHUIVING_WAARDE)
                    e_mailen(b'gui\n', b'GUI READY:')
                    첫화면 = uitvoer / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(uitvoer / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    e_mailen(b'\r', b'GUI ACTION 0 RESULT 0')
                    e_mailen(b'\t', b'GUI FOCUS 1')
                    e_mailen(b'\r', b'GUI ACTION 1 RESULT 0')
                    SECONDE_GUI = uitvoer / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SECONDE_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(uitvoer / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SECONDE_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    e_mailen(b'\t', b'GUI FOCUS 2')
                    e_mailen(b'\r', b'GUI ACTION 2 RESULT 0')
                    e_mailen(b'\t', b'GUI FOCUS 3')
                    e_mailen(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(uitvoer / 'gui-python.png'), 'format': 'png'})
                    e_mailen(b'q', b'jkoros-native> ')
                    validatie_Rapport['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Proces.wait(timeout=10)
            # framebuffer 응답뿐 아니라 werkelijk_gegevens scanout 픽셀도 확인한다.
            with schermopname.open('rb') as Bestand_invoer:
                assert Bestand_invoer.readline().strip() == b'P6'
                치수 = Bestand_invoer.readline().strip()
                assert 치수 == b'640 480', 치수
                assert Bestand_invoer.readline().strip() == b'255'
                화소들 = Bestand_invoer.read()
            assert len(화소들) == 640 * 480 * 3
            def pixel(x_coördinaat, Y_coördinaat): return list(화소들[(Y_coördinaat * 640 + x_coördinaat) * 3:(Y_coördinaat * 640 + x_coördinaat) * 3 + 3])
            예제들 = {'background': pixel(5, 5), 'panel': pixel(45, 85), 'tile': pixel(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            validatie_Rapport.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((Taken_wortel / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Proces.poll() is None:
                Proces.terminate()
                try: Proces.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Proces.kill(); Proces.wait(timeout=5)
            selector.close()
            Proces.stdin.close(); Proces.stdout.close()
            (uitvoer / 'serial.log').write_bytes(transcriptie)
            (uitvoer / 'report.json').write_text(json.dumps(validatie_Rapport, indent=2) + '\n')


if __name__ == '__main__':
    starten()
