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
from Izvrši_komanda import projicirati_koijen, Naredba


def Pokreni():
    출력결과 = projicirati_koijen / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    provjera_izvještaj = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Naredba() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        provjera_izvještaj['command'] = 명령인수
        proces = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        birač = selectors.DefaultSelector()
        birač.register(proces.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, Pomak_VALUE=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[Pomak_VALUE:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in birač.select(0.2):
                    podaci_blokirati = 누름값.fileobj.read(4096)
                    if podaci_blokirati:
                        대화기록.extend(podaci_blokirati)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if proces.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(proces.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 trenutno_stavka 호스트에서도 VNC로 stvaran_podaci GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def EXACT_VALUE(Veličina):
                    mjera = b''
                    while len(mjera) < Veličina:
                        조각 = 화면접속자.recv(Veličina - len(mjera))
                        if not 조각: raise AssertionError('VNC disconnected')
                        mjera += 조각
                    return mjera
                assert EXACT_VALUE(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in EXACT_VALUE(EXACT_VALUE(1)[0]); 화면접속자.sendall(b'\x01')
                assert EXACT_VALUE(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                server_VALUE = EXACT_VALUE(24)
                assert int.from_bytes(server_VALUE[:2], 'big') == 640 and int.from_bytes(server_VALUE[2:4], 'big') == 480
                EXACT_VALUE(int.from_bytes(server_VALUE[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for komanda_bajt, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                Pomak_VALUE = len(대화기록)
                proces.stdin.write(komanda_bajt + b'\n')
                proces.stdin.flush()
                표시까지받기(b'jkoros-native> ', Pomak_VALUE)
                assert 확인표시 in 대화기록[Pomak_VALUE:], 확인표시
            def ljuska(Linija, 예상결과):
                Pomak_VALUE = len(대화기록)
                proces.stdin.write(Linija.encode('utf-8') + b'\n'); proces.stdin.flush()
                표시까지받기(b'jkoros-native> ', Pomak_VALUE)
                응답자료 = bytes(대화기록[Pomak_VALUE:])
                for Tekst in 예상결과:
                    assert Tekst.encode('utf-8') in 응답자료, (Linija, Tekst, 응답자료)
                return 응답자료
            def unijeti(Linija, upit):
                Pomak_VALUE = len(대화기록)
                proces.stdin.write(Linija.encode('utf-8') + b'\n'); proces.stdin.flush()
                표시까지받기(upit, Pomak_VALUE)
                return bytes(대화기록[Pomak_VALUE:])
            def uređivati_VALUE(Naziv, Sadržaj_VALUE, Otkaži_operacija=False):
                unijeti('edit ' + Naziv, b'edit> ')
                for Linija in Sadržaj_VALUE.splitlines(): unijeti(Linija, b'edit> ')
                if Otkaži_operacija:
                    Pomak_VALUE = len(대화기록)
                    proces.stdin.write(b'\x03'); proces.stdin.flush()
                    표시까지받기(b'jkoros-native> ', Pomak_VALUE)
                    assert b'EDIT CANCELLED' in 대화기록[Pomak_VALUE:]
                else:
                    assert b'SAVED' in unijeti('.', b'jkoros-native> ')
            def Upload_Fajlovi(Naziv, podaci):
                assert len(podaci) <= 16384
                unijeti('load ' + Naziv, b'hex> ')
                for 순번 in range(0, len(podaci), 64): unijeti(podaci[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in unijeti('.', b'jkoros-native> ')
            def preuzeti(Naziv):
                응답자료 = ljuska('hex ' + Naziv, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                podaci = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(podaci) == int(일치.group(1)); return podaci
            ljuska('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            ljuska('java -version', ['not OpenJDK', 'exit 0'])
            ljuska('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            ljuska('java Hello "한글 Argumenti 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Argumenti 😀', 'exit 0'])
            ljuska('python --version', ['MicroPython 1.24.1', 'exit 0'])
            ljuska('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Fajl', 'exit 0'])
            ljuska('cat python.txt', ['한글 Fajl'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(preuzeti('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 Argumenti 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Argumenti 😀'], 예상결과
            uređivati_VALUE('인사.java', 'public class 인사 { public static void main(String[] args) { int VALUE = 7; System.out.println("한글=" + VALUE); } }')
            ljuska('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            ljuska('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(preuzeti('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            uređivati_VALUE('Hello.java', 'broken', Otkaži_operacija=True)
            ljuska('javac Hello.java', ['Compiled:', 'exit 0'])
            uređivati_VALUE('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            ljuska('javac Broken.java', ['javac error:', 'exit 1'])
            Upload_Fajlovi('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            ljuska('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            ljuska('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Upload_Fajlovi('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            ljuska('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            ljuska('rm Imported.class', [])
            uređivati_VALUE('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            ljuska('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = ljuska('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
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
            uređivati_VALUE('checks.py', 파이썬검사)
            ljuska('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            ljuska('rm checks.py', [])
            uređivati_VALUE('helper.py', 'value = 321')
            ljuska("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            ljuska('rm helper.py', [])
            ljuska("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            ljuska("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                ljuska('python hello.py', ['한글 Fajl', 'exit 0'])
                ljuska('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Upload_Fajlovi('app.elf', (projicirati_koijen / 'build/user/demo.elf').read_bytes())
            assert preuzeti('app.elf') == (projicirati_koijen / 'build/user/demo.elf').read_bytes()
            ljuska('run app.elf', ['EL0 C++', 'exit 0'])
            Upload_Fajlovi('app.elf', b'not an ELF')
            ljuska('run app.elf', ['exit -8'])
            ljuska('rm app.elf', [])
            ljuska('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            ucrtavanje_put = 출력결과 / 'java-framebuffer'; ucrtavanje_put.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(projicirati_koijen / 'dist/jkoros-native-korean.jar'), '-d', str(ucrtavanje_put), str(projicirati_koijen / '시험/자바/화면시험.java')])
            Upload_Fajlovi('화면시험.class', (ucrtavanje_put / '화면시험.class').read_bytes())
            ljuska('java 화면시험', ['화면 isječak odbiti_VALUE', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            ljuska('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as klijent:
                klijent.settimeout(10)
                klijent.connect(str(모의제어경로))
                with klijent.makefile('rwb') as tok_VALUE:
                    인사 = json.loads(tok_VALUE.readline())
                    def 모의제어접속(Izvrši, 전달인수=None):
                        Mreža_poruka = {'execute': Izvrši}
                        if 전달인수: Mreža_poruka['arguments'] = 전달인수
                        tok_VALUE.write((json.dumps(Mreža_poruka) + '\n').encode())
                        tok_VALUE.flush()
                        while True:
                            odgovoriti = json.loads(tok_VALUE.readline())
                            if 'error' in odgovoriti: raise AssertionError(odgovoriti)
                            if 'return' in odgovoriti: return odgovoriti['return']
                    모의제어접속('qmp_capabilities')
                    snimak_ekrana = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(snimak_ekrana), 'format': 'ppm'})
                    def 예제들(Putanja, 지점들):
                        with Putanja.open('rb') as pel_fajl:
                            assert pel_fajl.readline().strip() == b'P6'
                            assert pel_fajl.readline().strip() == b'640 480'
                            assert pel_fajl.readline().strip() == b'255'
                            pel_podaci = pel_fajl.read()
                        assert len(pel_podaci) == 640 * 480 * 3
                        return [list(pel_podaci[(Y_koordinata * 640 + koordinata_x) * 3:(Y_koordinata * 640 + koordinata_x) * 3 + 3]) for koordinata_x, Y_koordinata in 지점들]
                    assert 예제들(snimak_ekrana, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(snimak_ekrana, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def poslati(누름값, 확인표시):
                        Pomak_VALUE = len(대화기록)
                        proces.stdin.write(누름값); proces.stdin.flush()
                        표시까지받기(확인표시, Pomak_VALUE)
                    poslati(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    poslati(b'\r', b'GUI ACTION 0 RESULT 0')
                    poslati(b'\t', b'GUI FOCUS 1')
                    poslati(b'\r', b'GUI ACTION 1 RESULT 0')
                    SECOND_GUI = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SECOND_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SECOND_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    poslati(b'\t', b'GUI FOCUS 2')
                    poslati(b'\r', b'GUI ACTION 2 RESULT 0')
                    poslati(b'\t', b'GUI FOCUS 3')
                    poslati(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    poslati(b'q', b'jkoros-native> ')
                    provjera_izvještaj['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            proces.wait(timeout=10)
            # framebuffer 응답뿐 아니라 stvaran_podaci scanout 픽셀도 확인한다.
            with snimak_ekrana.open('rb') as fajl_unos:
                assert fajl_unos.readline().strip() == b'P6'
                치수 = fajl_unos.readline().strip()
                assert 치수 == b'640 480', 치수
                assert fajl_unos.readline().strip() == b'255'
                화소들 = fajl_unos.read()
            assert len(화소들) == 640 * 480 * 3
            def pel(koordinata_x, Y_koordinata): return list(화소들[(Y_koordinata * 640 + koordinata_x) * 3:(Y_koordinata * 640 + koordinata_x) * 3 + 3])
            예제들 = {'background': pel(5, 5), 'panel': pel(45, 85), 'tile': pel(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            provjera_izvještaj.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((projicirati_koijen / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if proces.poll() is None:
                proces.terminate()
                try: proces.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proces.kill(); proces.wait(timeout=5)
            birač.close()
            proces.stdin.close(); proces.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(provjera_izvještaj, indent=2) + '\n')


if __name__ == '__main__':
    Pokreni()
