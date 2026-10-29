#!/usr/bin/env python3
"""rzeczywisty_dane raspi4b rozruch_maszyny, UART wejście_WARTOŚĆ, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from Wykonaj_polecenie import Project_korzeń, polecenie


def Uruchom_2():
    produkt_wyjściowy = Project_korzeń / 'build/verification'
    produkt_wyjściowy.mkdir(parents=True, exist_ok=True)
    transkrypcja = bytearray()
    walidacja_Raport = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = polecenie() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        walidacja_Raport['command'] = 명령인수
        Proces = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        selektor = selectors.DefaultSelector()
        selektor.register(Proces.stdout, selectors.EVENT_READ)
        def 표시까지받기(pisak, przesunąć_WARTOŚĆ_450fc799=0, wykonanie_TIMEOUT=45):
            termin_ostateczny_CZAS = time.monotonic() + wykonanie_TIMEOUT
            while pisak not in transkrypcja[przesunąć_WARTOŚĆ_450fc799:]:
                if time.monotonic() > termin_ostateczny_CZAS:
                    raise AssertionError('UART timeout: ' + repr(pisak))
                for 누름값, _ in selektor.select(0.2):
                    blok_danych = 누름값.fileobj.read(4096)
                    if blok_danych:
                        transkrypcja.extend(blok_danych)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', transkrypcja):
                    raise AssertionError('kernel failure')
                if Proces.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Proces.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for pisak in 확인표시들:
                assert pisak in transkrypcja, pisak
            # GTK 없는 bieżący_towar 호스트에서도 VNC로 rzeczywisty_dane GUI를 볼 identyfikator 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def PORÓWNAJ_WARTOŚĆ(Rozmiar):
                    WYNIK = b''
                    while len(WYNIK) < Rozmiar:
                        fragment_WARTOŚĆ_652d4b53 = 화면접속자.recv(Rozmiar - len(WYNIK))
                        if not fragment_WARTOŚĆ_652d4b53: raise AssertionError('VNC disconnected')
                        WYNIK += fragment_WARTOŚĆ_652d4b53
                    return WYNIK
                assert PORÓWNAJ_WARTOŚĆ(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in PORÓWNAJ_WARTOŚĆ(PORÓWNAJ_WARTOŚĆ(1)[0]); 화면접속자.sendall(b'\x01')
                assert PORÓWNAJ_WARTOŚĆ(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                serwer_WARTOŚĆ = PORÓWNAJ_WARTOŚĆ(24)
                assert int.from_bytes(serwer_WARTOŚĆ[:2], 'big') == 640 and int.from_bytes(serwer_WARTOŚĆ[2:4], 'big') == 480
                PORÓWNAJ_WARTOŚĆ(int.from_bytes(serwer_WARTOŚĆ[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for polecenie_bajt, pisak in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', 'testy.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                przesunąć_WARTOŚĆ_450fc799 = len(transkrypcja)
                Proces.stdin.write(polecenie_bajt + b'\n')
                Proces.stdin.flush()
                표시까지받기(b'jkoros-native> ', przesunąć_WARTOŚĆ_450fc799)
                assert pisak in transkrypcja[przesunąć_WARTOŚĆ_450fc799:], pisak
            def powłoka(wiersz_wejścia, 예상결과):
                przesunąć_WARTOŚĆ_450fc799 = len(transkrypcja)
                Proces.stdin.write(wiersz_wejścia.encode('utf-8') + b'\n'); Proces.stdin.flush()
                표시까지받기(b'jkoros-native> ', przesunąć_WARTOŚĆ_450fc799)
                odpowiedź_1262b476 = bytes(transkrypcja[przesunąć_WARTOŚĆ_450fc799:])
                for tekst in 예상결과:
                    assert tekst.encode('utf-8') in odpowiedź_1262b476, (wiersz_wejścia, tekst, odpowiedź_1262b476)
                return odpowiedź_1262b476
            def wprowadzić(wiersz_wejścia, monit):
                przesunąć_WARTOŚĆ_450fc799 = len(transkrypcja)
                Proces.stdin.write(wiersz_wejścia.encode('utf-8') + b'\n'); Proces.stdin.flush()
                표시까지받기(monit, przesunąć_WARTOŚĆ_450fc799)
                return bytes(transkrypcja[przesunąć_WARTOŚĆ_450fc799:])
            def Edytuj_WARTOŚĆ(Nazwa, treść_WARTOŚĆ_cb0f2404, Anuluj_zabieg=False):
                wprowadzić('edit ' + Nazwa, b'edit> ')
                for wiersz_wejścia in treść_WARTOŚĆ_cb0f2404.splitlines(): wprowadzić(wiersz_wejścia, b'edit> ')
                if Anuluj_zabieg:
                    przesunąć_WARTOŚĆ_450fc799 = len(transkrypcja)
                    Proces.stdin.write(b'\x03'); Proces.stdin.flush()
                    표시까지받기(b'jkoros-native> ', przesunąć_WARTOŚĆ_450fc799)
                    assert b'EDIT CANCELLED' in transkrypcja[przesunąć_WARTOŚĆ_450fc799:]
                else:
                    assert b'SAVED' in wprowadzić('.', b'jkoros-native> ')
            def Upload_Files(Nazwa, dane):
                assert len(dane) <= 16384
                wprowadzić('load ' + Nazwa, b'hex> ')
                for 순번 in range(0, len(dane), 64): wprowadzić(dane[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in wprowadzić('.', b'jkoros-native> ')
            def pobrać(Nazwa):
                odpowiedź_1262b476 = powłoka('hex ' + Nazwa, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', odpowiedź_1262b476, re.S)
                dane = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(dane) == int(일치.group(1)); return dane
            powłoka('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            powłoka('java -version', ['not OpenJDK', 'exit 0'])
            powłoka('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            powłoka('java Hello "한글 argumenty 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 argumenty 😀', 'exit 0'])
            powłoka('python --version', ['MicroPython 1.24.1', 'exit 0'])
            powłoka('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 nazwa_pliku', 'exit 0'])
            powłoka('cat python.txt', ['한글 nazwa_pliku'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = produkt_wyjściowy / 'Hello.class'; 자바클래스.write_bytes(pobrać('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(produkt_wyjściowy), 'Hello', '한글 argumenty 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 argumenty 😀'], 예상결과
            Edytuj_WARTOŚĆ('인사.java', 'public class 인사 { public static void main(String[] args) { int WARTOŚĆ = 7; System.out.println("한글=" + WARTOŚĆ); } }')
            powłoka('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            powłoka('java 인사', ['한글=7', 'exit 0'])
            (produkt_wyjściowy / '인사.class').write_bytes(pobrać('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(produkt_wyjściowy), '인사']).decode().strip() == '한글=7'
            Edytuj_WARTOŚĆ('Hello.java', 'broken', Anuluj_zabieg=True)
            powłoka('javac Hello.java', ['Compiled:', 'exit 0'])
            Edytuj_WARTOŚĆ('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            powłoka('javac Broken.java', ['javac error:', 'exit 1'])
            Upload_Files('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            powłoka('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            powłoka('rm Broken.java', [])
            들여온파일 = produkt_wyjściowy / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Upload_Files('Imported.class', (produkt_wyjściowy / 'Imported.class').read_bytes())
            powłoka('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            powłoka('rm Imported.class', [])
            Edytuj_WARTOŚĆ('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            powłoka('javac Loop.java', ['Compiled:', 'exit 0'])
            odpowiedź_1262b476 = powłoka('java Loop', ['exit '])
            assert b'instruction limit' in odpowiedź_1262b476 or b'exit -1004' in odpowiedź_1262b476
            powłoka('rm Loop.java', []); powłoka('rm Loop.class', [])
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
            Edytuj_WARTOŚĆ('checks.py', 파이썬검사)
            powłoka('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            powłoka('rm checks.py', [])
            Edytuj_WARTOŚĆ('helper.py', 'value = 321')
            powłoka("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            powłoka('rm helper.py', [])
            powłoka("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            powłoka("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                powłoka('python hello.py', ['한글 nazwa_pliku', 'exit 0'])
                powłoka('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Upload_Files('app.elf', (Project_korzeń / 'build/user/demo.elf').read_bytes())
            assert pobrać('app.elf') == (Project_korzeń / 'build/user/demo.elf').read_bytes()
            powłoka('run app.elf', ['EL0 C++', 'exit 0'])
            Upload_Files('app.elf', b'not an ELF')
            powłoka('run app.elf', ['exit -8'])
            powłoka('rm app.elf', [])
            powłoka('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            rysunek_ścieżka = produkt_wyjściowy / 'java-framebuffer'; rysunek_ścieżka.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_korzeń / 'dist/jkoros-native-korean.jar'), '-d', str(rysunek_ścieżka), str(Project_korzeń / 'testy/자바/화면시험.java')])
            Upload_Files('화면시험.class', (rysunek_ścieżka / '화면시험.class').read_bytes())
            powłoka('java 화면시험', ['화면 obcinać odrzucić_WARTOŚĆ', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            powłoka('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as klient:
                klient.settimeout(10)
                klient.connect(str(모의제어경로))
                with klient.makefile('rwb') as Stream_WARTOŚĆ:
                    인사 = json.loads(Stream_WARTOŚĆ.readline())
                    def 모의제어접속(Uruchom, 전달인수=None):
                        sieć_e_mail = {'execute': Uruchom}
                        if 전달인수: sieć_e_mail['arguments'] = 전달인수
                        Stream_WARTOŚĆ.write((json.dumps(sieć_e_mail) + '\n').encode())
                        Stream_WARTOŚĆ.flush()
                        while True:
                            odpowiedź = json.loads(Stream_WARTOŚĆ.readline())
                            if 'error' in odpowiedź: raise AssertionError(odpowiedź)
                            if 'return' in odpowiedź: return odpowiedź['return']
                    모의제어접속('qmp_capabilities')
                    zrzut_ekranu = produkt_wyjściowy / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(zrzut_ekranu), 'format': 'ppm'})
                    def 예제들(ścieżka_2, 지점들):
                        with ścieżka_2.open('rb') as piksel_Plik:
                            assert piksel_Plik.readline().strip() == b'P6'
                            assert piksel_Plik.readline().strip() == b'640 480'
                            assert piksel_Plik.readline().strip() == b'255'
                            piksel_dane = piksel_Plik.read()
                        assert len(piksel_dane) == 640 * 480 * 3
                        return [list(piksel_dane[(Y_współrzędna * 640 + współrzędna_X) * 3:(Y_współrzędna * 640 + współrzędna_X) * 3 + 3]) for współrzędna_X, Y_współrzędna in 지점들]
                    assert 예제들(zrzut_ekranu, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(zrzut_ekranu, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def wysłać(누름값, pisak):
                        przesunąć_WARTOŚĆ_450fc799 = len(transkrypcja)
                        Proces.stdin.write(누름값); Proces.stdin.flush()
                        표시까지받기(pisak, przesunąć_WARTOŚĆ_450fc799)
                    wysłać(b'gui\n', b'GUI READY:')
                    첫화면 = produkt_wyjściowy / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(produkt_wyjściowy / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    wysłać(b'\r', b'GUI ACTION 0 RESULT 0')
                    wysłać(b'\t', b'GUI FOCUS 1')
                    wysłać(b'\r', b'GUI ACTION 1 RESULT 0')
                    SEKUNDA_GUI = produkt_wyjściowy / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SEKUNDA_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(produkt_wyjściowy / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SEKUNDA_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    wysłać(b'\t', b'GUI FOCUS 2')
                    wysłać(b'\r', b'GUI ACTION 2 RESULT 0')
                    wysłać(b'\t', b'GUI FOCUS 3')
                    wysłać(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(produkt_wyjściowy / 'gui-python.png'), 'format': 'png'})
                    wysłać(b'q', b'jkoros-native> ')
                    walidacja_Raport['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Proces.wait(timeout=10)
            # framebuffer 응답뿐 아니라 rzeczywisty_dane scanout 픽셀도 확인한다.
            with zrzut_ekranu.open('rb') as Plik_wpis:
                assert Plik_wpis.readline().strip() == b'P6'
                치수 = Plik_wpis.readline().strip()
                assert 치수 == b'640 480', 치수
                assert Plik_wpis.readline().strip() == b'255'
                화소들 = Plik_wpis.read()
            assert len(화소들) == 640 * 480 * 3
            def piksel(współrzędna_X, Y_współrzędna): return list(화소들[(Y_współrzędna * 640 + współrzędna_X) * 3:(Y_współrzędna * 640 + współrzędna_X) * 3 + 3])
            예제들 = {'background': piksel(5, 5), 'panel': piksel(45, 85), 'tile': piksel(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            walidacja_Raport.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((Project_korzeń / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Proces.poll() is None:
                Proces.terminate()
                try: Proces.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Proces.kill(); Proces.wait(timeout=5)
            selektor.close()
            Proces.stdin.close(); Proces.stdout.close()
            (produkt_wyjściowy / 'serial.log').write_bytes(transkrypcja)
            (produkt_wyjściowy / 'report.json').write_text(json.dumps(walidacja_Raport, indent=2) + '\n')


if __name__ == '__main__':
    Uruchom_2()
