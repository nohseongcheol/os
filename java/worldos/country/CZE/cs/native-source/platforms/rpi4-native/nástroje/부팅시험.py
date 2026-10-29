#!/usr/bin/env python3
"""skutečný_data raspi4b spuštění_stroje, UART vstup_HODNOTA, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from Provést_příkaz import akce_kořen, příkaz


def Spustit_2():
    výstup = akce_kořen / 'build/verification'
    výstup.mkdir(parents=True, exist_ok=True)
    přepis = bytearray()
    ověření_Zpráva = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = příkaz() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        ověření_Zpráva['command'] = 명령인수
        Proces = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        selektor = selectors.DefaultSelector()
        selektor.register(Proces.stdout, selectors.EVENT_READ)
        def 표시까지받기(značka, POSUN_HODNOTA=0, spuštění_TIMEOUT=45):
            konečný_termín_ČAS = time.monotonic() + spuštění_TIMEOUT
            while značka not in přepis[POSUN_HODNOTA:]:
                if time.monotonic() > konečný_termín_ČAS:
                    raise AssertionError('UART timeout: ' + repr(značka))
                for 누름값, _ in selektor.select(0.2):
                    datový_blok = 누름값.fileobj.read(4096)
                    if datový_blok:
                        přepis.extend(datový_blok)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', přepis):
                    raise AssertionError('kernel failure')
                if Proces.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Proces.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for značka in 확인표시들:
                assert značka in přepis, značka
            # GTK 없는 dobrá_zboží 호스트에서도 VNC로 skutečný_data GUI를 볼 číslo 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def STEJNÉ_HODNOTA(Velikost):
                    VÝSLEDEK = b''
                    while len(VÝSLEDEK) < Velikost:
                        조각 = 화면접속자.recv(Velikost - len(VÝSLEDEK))
                        if not 조각: raise AssertionError('VNC disconnected')
                        VÝSLEDEK += 조각
                    return VÝSLEDEK
                assert STEJNÉ_HODNOTA(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in STEJNÉ_HODNOTA(STEJNÉ_HODNOTA(1)[0]); 화면접속자.sendall(b'\x01')
                assert STEJNÉ_HODNOTA(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                server_HODNOTA = STEJNÉ_HODNOTA(24)
                assert int.from_bytes(server_HODNOTA[:2], 'big') == 640 and int.from_bytes(server_HODNOTA[2:4], 'big') == 480
                STEJNÉ_HODNOTA(int.from_bytes(server_HODNOTA[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for příkaz_bajt, značka in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', 'zkoušky.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                POSUN_HODNOTA = len(přepis)
                Proces.stdin.write(příkaz_bajt + b'\n')
                Proces.stdin.flush()
                표시까지받기(b'jkoros-native> ', POSUN_HODNOTA)
                assert značka in přepis[POSUN_HODNOTA:], značka
            def prostředí(vstupní_řádek, 예상결과):
                POSUN_HODNOTA = len(přepis)
                Proces.stdin.write(vstupní_řádek.encode('utf-8') + b'\n'); Proces.stdin.flush()
                표시까지받기(b'jkoros-native> ', POSUN_HODNOTA)
                odpověď = bytes(přepis[POSUN_HODNOTA:])
                for text in 예상결과:
                    assert text.encode('utf-8') in odpověď, (vstupní_řádek, text, odpověď)
                return odpověď
            def zadat(vstupní_řádek, výzva):
                POSUN_HODNOTA = len(přepis)
                Proces.stdin.write(vstupní_řádek.encode('utf-8') + b'\n'); Proces.stdin.flush()
                표시까지받기(výzva, POSUN_HODNOTA)
                return bytes(přepis[POSUN_HODNOTA:])
            def úprava_HODNOTA(Název, Obsah_HODNOTA, Zrušit_operace=False):
                zadat('edit ' + Název, b'edit> ')
                for vstupní_řádek in Obsah_HODNOTA.splitlines(): zadat(vstupní_řádek, b'edit> ')
                if Zrušit_operace:
                    POSUN_HODNOTA = len(přepis)
                    Proces.stdin.write(b'\x03'); Proces.stdin.flush()
                    표시까지받기(b'jkoros-native> ', POSUN_HODNOTA)
                    assert b'EDIT CANCELLED' in přepis[POSUN_HODNOTA:]
                else:
                    assert b'SAVED' in zadat('.', b'jkoros-native> ')
            def Upload_Files(Název, data):
                assert len(data) <= 16384
                zadat('load ' + Název, b'hex> ')
                for 순번 in range(0, len(data), 64): zadat(data[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in zadat('.', b'jkoros-native> ')
            def stažení(Název):
                odpověď = prostředí('hex ' + Název, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', odpověď, re.S)
                data = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(data) == int(일치.group(1)); return data
            prostředí('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            prostředí('java -version', ['not OpenJDK', 'exit 0'])
            prostředí('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            prostředí('java Hello "한글 argumenty 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 argumenty 😀', 'exit 0'])
            prostředí('python --version', ['MicroPython 1.24.1', 'exit 0'])
            prostředí('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 název_souboru', 'exit 0'])
            prostředí('cat python.txt', ['한글 název_souboru'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = výstup / 'Hello.class'; 자바클래스.write_bytes(stažení('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(výstup), 'Hello', '한글 argumenty 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 argumenty 😀'], 예상결과
            úprava_HODNOTA('인사.java', 'public class 인사 { public static void main(String[] args) { int HODNOTA = 7; System.out.println("한글=" + HODNOTA); } }')
            prostředí('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            prostředí('java 인사', ['한글=7', 'exit 0'])
            (výstup / '인사.class').write_bytes(stažení('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(výstup), '인사']).decode().strip() == '한글=7'
            úprava_HODNOTA('Hello.java', 'broken', Zrušit_operace=True)
            prostředí('javac Hello.java', ['Compiled:', 'exit 0'])
            úprava_HODNOTA('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            prostředí('javac Broken.java', ['javac error:', 'exit 1'])
            Upload_Files('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            prostředí('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            prostředí('rm Broken.java', [])
            들여온파일 = výstup / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Upload_Files('Imported.class', (výstup / 'Imported.class').read_bytes())
            prostředí('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            prostředí('rm Imported.class', [])
            úprava_HODNOTA('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            prostředí('javac Loop.java', ['Compiled:', 'exit 0'])
            odpověď = prostředí('java Loop', ['exit '])
            assert b'instruction limit' in odpověď or b'exit -1004' in odpověď
            prostředí('rm Loop.java', []); prostředí('rm Loop.class', [])
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
            úprava_HODNOTA('checks.py', 파이썬검사)
            prostředí('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            prostředí('rm checks.py', [])
            úprava_HODNOTA('helper.py', 'value = 321')
            prostředí("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            prostředí('rm helper.py', [])
            prostředí("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            prostředí("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                prostředí('python hello.py', ['한글 název_souboru', 'exit 0'])
                prostředí('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Upload_Files('app.elf', (akce_kořen / 'build/user/demo.elf').read_bytes())
            assert stažení('app.elf') == (akce_kořen / 'build/user/demo.elf').read_bytes()
            prostředí('run app.elf', ['EL0 C++', 'exit 0'])
            Upload_Files('app.elf', b'not an ELF')
            prostředí('run app.elf', ['exit -8'])
            prostředí('rm app.elf', [])
            prostředí('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            kreslení_cesta = výstup / 'java-framebuffer'; kreslení_cesta.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(akce_kořen / 'dist/jkoros-native-korean.jar'), '-d', str(kreslení_cesta), str(akce_kořen / 'zkoušky/자바/화면시험.java')])
            Upload_Files('화면시험.class', (kreslení_cesta / '화면시험.class').read_bytes())
            prostředí('java 화면시험', ['화면 oříznout odmítnout_HODNOTA', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            prostředí('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as klient:
                klient.settimeout(10)
                klient.connect(str(모의제어경로))
                with klient.makefile('rwb') as tok_HODNOTA:
                    인사 = json.loads(tok_HODNOTA.readline())
                    def 모의제어접속(Spustit, 전달인수=None):
                        síť_e_mail = {'execute': Spustit}
                        if 전달인수: síť_e_mail['arguments'] = 전달인수
                        tok_HODNOTA.write((json.dumps(síť_e_mail) + '\n').encode())
                        tok_HODNOTA.flush()
                        while True:
                            odezva = json.loads(tok_HODNOTA.readline())
                            if 'error' in odezva: raise AssertionError(odezva)
                            if 'return' in odezva: return odezva['return']
                    모의제어접속('qmp_capabilities')
                    screenshot = výstup / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(screenshot), 'format': 'ppm'})
                    def 예제들(cesta_2, 지점들):
                        with cesta_2.open('rb') as pixel_Soubor:
                            assert pixel_Soubor.readline().strip() == b'P6'
                            assert pixel_Soubor.readline().strip() == b'640 480'
                            assert pixel_Soubor.readline().strip() == b'255'
                            pixel_data = pixel_Soubor.read()
                        assert len(pixel_data) == 640 * 480 * 3
                        return [list(pixel_data[(Y_souřadnice * 640 + souřadnice_x) * 3:(Y_souřadnice * 640 + souřadnice_x) * 3 + 3]) for souřadnice_x, Y_souřadnice in 지점들]
                    assert 예제들(screenshot, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(screenshot, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def poslat(누름값, značka):
                        POSUN_HODNOTA = len(přepis)
                        Proces.stdin.write(누름값); Proces.stdin.flush()
                        표시까지받기(značka, POSUN_HODNOTA)
                    poslat(b'gui\n', b'GUI READY:')
                    첫화면 = výstup / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(výstup / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    poslat(b'\r', b'GUI ACTION 0 RESULT 0')
                    poslat(b'\t', b'GUI FOCUS 1')
                    poslat(b'\r', b'GUI ACTION 1 RESULT 0')
                    SEKUNDA_grafické_rozhraní_GUI = výstup / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SEKUNDA_grafické_rozhraní_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(výstup / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SEKUNDA_grafické_rozhraní_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    poslat(b'\t', b'GUI FOCUS 2')
                    poslat(b'\r', b'GUI ACTION 2 RESULT 0')
                    poslat(b'\t', b'GUI FOCUS 3')
                    poslat(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(výstup / 'gui-python.png'), 'format': 'png'})
                    poslat(b'q', b'jkoros-native> ')
                    ověření_Zpráva['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Proces.wait(timeout=10)
            # framebuffer 응답뿐 아니라 skutečný_data scanout 픽셀도 확인한다.
            with screenshot.open('rb') as Soubor_položka:
                assert Soubor_položka.readline().strip() == b'P6'
                치수 = Soubor_položka.readline().strip()
                assert 치수 == b'640 480', 치수
                assert Soubor_položka.readline().strip() == b'255'
                화소들 = Soubor_položka.read()
            assert len(화소들) == 640 * 480 * 3
            def pixel(souřadnice_x, Y_souřadnice): return list(화소들[(Y_souřadnice * 640 + souřadnice_x) * 3:(Y_souřadnice * 640 + souřadnice_x) * 3 + 3])
            예제들 = {'background': pixel(5, 5), 'panel': pixel(45, 85), 'tile': pixel(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            ověření_Zpráva.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((akce_kořen / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Proces.poll() is None:
                Proces.terminate()
                try: Proces.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Proces.kill(); Proces.wait(timeout=5)
            selektor.close()
            Proces.stdin.close(); Proces.stdout.close()
            (výstup / 'serial.log').write_bytes(přepis)
            (výstup / 'report.json').write_text(json.dumps(ověření_Zpráva, indent=2) + '\n')


if __name__ == '__main__':
    Spustit_2()
