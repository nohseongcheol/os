#!/usr/bin/env python3
"""stvaran_podaci raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from Izvrši_naredba import akcija_korijen, Naredba


def Pokreni():
    출력결과 = akcija_korijen / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    transkript = bytearray()
    provjera_izvješće = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Naredba() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        provjera_izvješće['command'] = 명령인수
        Proces = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        odabirač = selectors.DefaultSelector()
        odabirač.register(Proces.stdout, selectors.EVENT_READ)
        def 표시까지받기(marker, pomak_VALUE=0, 시간제한=45):
            rok_za_dovršetak_TIME = time.monotonic() + 시간제한
            while marker not in transkript[pomak_VALUE:]:
                if time.monotonic() > rok_za_dovršetak_TIME:
                    raise AssertionError('UART timeout: ' + repr(marker))
                for 누름값, _ in odabirač.select(0.2):
                    podatkovni_blok = 누름값.fileobj.read(4096)
                    if podatkovni_blok:
                        transkript.extend(podatkovni_blok)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', transkript):
                    raise AssertionError('kernel failure')
                if Proces.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Proces.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for marker in 확인표시들:
                assert marker in transkript, marker
            # GTK 없는 redovno_artikl 호스트에서도 VNC로 stvaran_podaci GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def EXACT_VALUE(Veličina):
                    REZULTAT = b''
                    while len(REZULTAT) < Veličina:
                        fragment_VALUE = 화면접속자.recv(Veličina - len(REZULTAT))
                        if not fragment_VALUE: raise AssertionError('VNC disconnected')
                        REZULTAT += fragment_VALUE
                    return REZULTAT
                assert EXACT_VALUE(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in EXACT_VALUE(EXACT_VALUE(1)[0]); 화면접속자.sendall(b'\x01')
                assert EXACT_VALUE(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                server_VALUE = EXACT_VALUE(24)
                assert int.from_bytes(server_VALUE[:2], 'big') == 640 and int.from_bytes(server_VALUE[2:4], 'big') == 480
                EXACT_VALUE(int.from_bytes(server_VALUE[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for naredba_bajt, marker in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                pomak_VALUE = len(transkript)
                Proces.stdin.write(naredba_bajt + b'\n')
                Proces.stdin.flush()
                표시까지받기(b'jkoros-native> ', pomak_VALUE)
                assert marker in transkript[pomak_VALUE:], marker
            def ljuska(red, 예상결과):
                pomak_VALUE = len(transkript)
                Proces.stdin.write(red.encode('utf-8') + b'\n'); Proces.stdin.flush()
                표시까지받기(b'jkoros-native> ', pomak_VALUE)
                odgovor_1262b476 = bytes(transkript[pomak_VALUE:])
                for Tekst in 예상결과:
                    assert Tekst.encode('utf-8') in odgovor_1262b476, (red, Tekst, odgovor_1262b476)
                return odgovor_1262b476
            def unijeti(red, upit):
                pomak_VALUE = len(transkript)
                Proces.stdin.write(red.encode('utf-8') + b'\n'); Proces.stdin.flush()
                표시까지받기(upit, pomak_VALUE)
                return bytes(transkript[pomak_VALUE:])
            def Uredi_VALUE(Ime, Sadržaj_VALUE, Odustani_operacija=False):
                unijeti('edit ' + Ime, b'edit> ')
                for red in Sadržaj_VALUE.splitlines(): unijeti(red, b'edit> ')
                if Odustani_operacija:
                    pomak_VALUE = len(transkript)
                    Proces.stdin.write(b'\x03'); Proces.stdin.flush()
                    표시까지받기(b'jkoros-native> ', pomak_VALUE)
                    assert b'EDIT CANCELLED' in transkript[pomak_VALUE:]
                else:
                    assert b'SAVED' in unijeti('.', b'jkoros-native> ')
            def Prijenos_Datoteke(Ime, podaci):
                assert len(podaci) <= 16384
                unijeti('load ' + Ime, b'hex> ')
                for 순번 in range(0, len(podaci), 64): unijeti(podaci[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in unijeti('.', b'jkoros-native> ')
            def preuzmi(Ime):
                odgovor_1262b476 = ljuska('hex ' + Ime, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', odgovor_1262b476, re.S)
                podaci = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(podaci) == int(일치.group(1)); return podaci
            ljuska('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            ljuska('java -version', ['not OpenJDK', 'exit 0'])
            ljuska('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            ljuska('java Hello "한글 Argumenti 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Argumenti 😀', 'exit 0'])
            ljuska('python --version', ['MicroPython 1.24.1', 'exit 0'])
            ljuska('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Datoteka', 'exit 0'])
            ljuska('cat python.txt', ['한글 Datoteka'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(preuzmi('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 Argumenti 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Argumenti 😀'], 예상결과
            Uredi_VALUE('인사.java', 'public class 인사 { public static void main(String[] args) { int VALUE = 7; System.out.println("한글=" + VALUE); } }')
            ljuska('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            ljuska('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(preuzmi('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            Uredi_VALUE('Hello.java', 'broken', Odustani_operacija=True)
            ljuska('javac Hello.java', ['Compiled:', 'exit 0'])
            Uredi_VALUE('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            ljuska('javac Broken.java', ['javac error:', 'exit 1'])
            Prijenos_Datoteke('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            ljuska('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            ljuska('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Prijenos_Datoteke('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            ljuska('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            ljuska('rm Imported.class', [])
            Uredi_VALUE('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            ljuska('javac Loop.java', ['Compiled:', 'exit 0'])
            odgovor_1262b476 = ljuska('java Loop', ['exit '])
            assert b'instruction limit' in odgovor_1262b476 or b'exit -1004' in odgovor_1262b476
            ljuska('rm Loop.java', []); ljuska('rm Loop.class', [])
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
            Uredi_VALUE('checks.py', 파이썬검사)
            ljuska('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            ljuska('rm checks.py', [])
            Uredi_VALUE('helper.py', 'value = 321')
            ljuska("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            ljuska('rm helper.py', [])
            ljuska("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            ljuska("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                ljuska('python hello.py', ['한글 Datoteka', 'exit 0'])
                ljuska('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Prijenos_Datoteke('app.elf', (akcija_korijen / 'build/user/demo.elf').read_bytes())
            assert preuzmi('app.elf') == (akcija_korijen / 'build/user/demo.elf').read_bytes()
            ljuska('run app.elf', ['EL0 C++', 'exit 0'])
            Prijenos_Datoteke('app.elf', b'not an ELF')
            ljuska('run app.elf', ['exit -8'])
            ljuska('rm app.elf', [])
            ljuska('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            crtež_put = 출력결과 / 'java-framebuffer'; crtež_put.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(akcija_korijen / 'dist/jkoros-native-korean.jar'), '-d', str(crtež_put), str(akcija_korijen / '시험/자바/화면시험.java')])
            Prijenos_Datoteke('화면시험.class', (crtež_put / '화면시험.class').read_bytes())
            ljuska('java 화면시험', ['화면 isječak odbiti_VALUE', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            ljuska('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as klijent:
                klijent.settimeout(10)
                klijent.connect(str(모의제어경로))
                with klijent.makefile('rwb') as tok_VALUE:
                    인사 = json.loads(tok_VALUE.readline())
                    def 모의제어접속(Izvrši, 전달인수=None):
                        mreža_poruka = {'execute': Izvrši}
                        if 전달인수: mreža_poruka['arguments'] = 전달인수
                        tok_VALUE.write((json.dumps(mreža_poruka) + '\n').encode())
                        tok_VALUE.flush()
                        while True:
                            odgovor = json.loads(tok_VALUE.readline())
                            if 'error' in odgovor: raise AssertionError(odgovor)
                            if 'return' in odgovor: return odgovor['return']
                    모의제어접속('qmp_capabilities')
                    snimka_zaslona = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(snimka_zaslona), 'format': 'ppm'})
                    def 예제들(PUTANJA, 지점들):
                        with PUTANJA.open('rb') as slikovni_element_Datoteka:
                            assert slikovni_element_Datoteka.readline().strip() == b'P6'
                            assert slikovni_element_Datoteka.readline().strip() == b'640 480'
                            assert slikovni_element_Datoteka.readline().strip() == b'255'
                            slikovni_element_podaci = slikovni_element_Datoteka.read()
                        assert len(slikovni_element_podaci) == 640 * 480 * 3
                        return [list(slikovni_element_podaci[(세로좌표 * 640 + koordinata_x) * 3:(세로좌표 * 640 + koordinata_x) * 3 + 3]) for koordinata_x, 세로좌표 in 지점들]
                    assert 예제들(snimka_zaslona, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(snimka_zaslona, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def slati(누름값, marker):
                        pomak_VALUE = len(transkript)
                        Proces.stdin.write(누름값); Proces.stdin.flush()
                        표시까지받기(marker, pomak_VALUE)
                    slati(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    slati(b'\r', b'GUI ACTION 0 RESULT 0')
                    slati(b'\t', b'GUI FOCUS 1')
                    slati(b'\r', b'GUI ACTION 1 RESULT 0')
                    SECOND_GUI = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SECOND_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SECOND_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    slati(b'\t', b'GUI FOCUS 2')
                    slati(b'\r', b'GUI ACTION 2 RESULT 0')
                    slati(b'\t', b'GUI FOCUS 3')
                    slati(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    slati(b'q', b'jkoros-native> ')
                    provjera_izvješće['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Proces.wait(timeout=10)
            # framebuffer 응답뿐 아니라 stvaran_podaci scanout 픽셀도 확인한다.
            with snimka_zaslona.open('rb') as Datoteka_unos:
                assert Datoteka_unos.readline().strip() == b'P6'
                치수 = Datoteka_unos.readline().strip()
                assert 치수 == b'640 480', 치수
                assert Datoteka_unos.readline().strip() == b'255'
                화소들 = Datoteka_unos.read()
            assert len(화소들) == 640 * 480 * 3
            def slikovni_element(koordinata_x, 세로좌표): return list(화소들[(세로좌표 * 640 + koordinata_x) * 3:(세로좌표 * 640 + koordinata_x) * 3 + 3])
            예제들 = {'background': slikovni_element(5, 5), 'panel': slikovni_element(45, 85), 'tile': slikovni_element(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            provjera_izvješće.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((akcija_korijen / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Proces.poll() is None:
                Proces.terminate()
                try: Proces.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Proces.kill(); Proces.wait(timeout=5)
            odabirač.close()
            Proces.stdin.close(); Proces.stdout.close()
            (출력결과 / 'serial.log').write_bytes(transkript)
            (출력결과 / 'report.json').write_text(json.dumps(provjera_izvješće, indent=2) + '\n')


if __name__ == '__main__':
    Pokreni()
