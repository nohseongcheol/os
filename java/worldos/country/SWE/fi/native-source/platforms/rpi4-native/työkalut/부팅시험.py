#!/usr/bin/env python3
"""todellinen_data raspi4b koneen_käynnistys, UART syöte_ARVO, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from Suorita_komento import aloite_juuri, komento


def Suorita_2():
    tulos = aloite_juuri / 'build/verification'
    tulos.mkdir(parents=True, exist_ok=True)
    transkriptio = bytearray()
    vahvistus_raportti = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = komento() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        vahvistus_raportti['command'] = 명령인수
        Prosessi = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        valitsin = selectors.DefaultSelector()
        valitsin.register(Prosessi.stdout, selectors.EVENT_READ)
        def 표시까지받기(merkintä, SIIRTYMÄ_ARVO=0, suoritus_AIKAKATKAISU=45):
            määräaika_AIKA = time.monotonic() + suoritus_AIKAKATKAISU
            while merkintä not in transkriptio[SIIRTYMÄ_ARVO:]:
                if time.monotonic() > määräaika_AIKA:
                    raise AssertionError('UART timeout: ' + repr(merkintä))
                for 누름값, _ in valitsin.select(0.2):
                    tietolohko = 누름값.fileobj.read(4096)
                    if tietolohko:
                        transkriptio.extend(tietolohko)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', transkriptio):
                    raise AssertionError('kernel failure')
                if Prosessi.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Prosessi.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for merkintä in 확인표시들:
                assert merkintä in transkriptio, merkintä
            # GTK 없는 nykyinen_kohde 호스트에서도 VNC로 todellinen_data GUI를 볼 numero 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def VERTAA_ARVO(Koko):
                    TULOS = b''
                    while len(TULOS) < Koko:
                        조각 = 화면접속자.recv(Koko - len(TULOS))
                        if not 조각: raise AssertionError('VNC disconnected')
                        TULOS += 조각
                    return TULOS
                assert VERTAA_ARVO(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in VERTAA_ARVO(VERTAA_ARVO(1)[0]); 화면접속자.sendall(b'\x01')
                assert VERTAA_ARVO(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                palvelin_ARVO = VERTAA_ARVO(24)
                assert int.from_bytes(palvelin_ARVO[:2], 'big') == 640 and int.from_bytes(palvelin_ARVO[2:4], 'big') == 480
                VERTAA_ARVO(int.from_bytes(palvelin_ARVO[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for komento_tavu, merkintä in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', 'testit.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                SIIRTYMÄ_ARVO = len(transkriptio)
                Prosessi.stdin.write(komento_tavu + b'\n')
                Prosessi.stdin.flush()
                표시까지받기(b'jkoros-native> ', SIIRTYMÄ_ARVO)
                assert merkintä in transkriptio[SIIRTYMÄ_ARVO:], merkintä
            def liittymä(syöterivi, 예상결과):
                SIIRTYMÄ_ARVO = len(transkriptio)
                Prosessi.stdin.write(syöterivi.encode('utf-8') + b'\n'); Prosessi.stdin.flush()
                표시까지받기(b'jkoros-native> ', SIIRTYMÄ_ARVO)
                vastaus = bytes(transkriptio[SIIRTYMÄ_ARVO:])
                for teksti in 예상결과:
                    assert teksti.encode('utf-8') in vastaus, (syöterivi, teksti, vastaus)
                return vastaus
            def anna(syöterivi, kehote):
                SIIRTYMÄ_ARVO = len(transkriptio)
                Prosessi.stdin.write(syöterivi.encode('utf-8') + b'\n'); Prosessi.stdin.flush()
                표시까지받기(kehote, SIIRTYMÄ_ARVO)
                return bytes(transkriptio[SIIRTYMÄ_ARVO:])
            def muutos_ARVO(Nimi, Sisältö_ARVO, kumota_leikkaus=False):
                anna('edit ' + Nimi, b'edit> ')
                for syöterivi in Sisältö_ARVO.splitlines(): anna(syöterivi, b'edit> ')
                if kumota_leikkaus:
                    SIIRTYMÄ_ARVO = len(transkriptio)
                    Prosessi.stdin.write(b'\x03'); Prosessi.stdin.flush()
                    표시까지받기(b'jkoros-native> ', SIIRTYMÄ_ARVO)
                    assert b'EDIT CANCELLED' in transkriptio[SIIRTYMÄ_ARVO:]
                else:
                    assert b'SAVED' in anna('.', b'jkoros-native> ')
            def Upload_Files(Nimi, data):
                assert len(data) <= 16384
                anna('load ' + Nimi, b'hex> ')
                for 순번 in range(0, len(data), 64): anna(data[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in anna('.', b'jkoros-native> ')
            def ladata(Nimi):
                vastaus = liittymä('hex ' + Nimi, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', vastaus, re.S)
                data = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(data) == int(일치.group(1)); return data
            liittymä('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            liittymä('java -version', ['not OpenJDK', 'exit 0'])
            liittymä('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            liittymä('java Hello "한글 argumentit 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 argumentit 😀', 'exit 0'])
            liittymä('python --version', ['MicroPython 1.24.1', 'exit 0'])
            liittymä('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 tiedoston_nimi', 'exit 0'])
            liittymä('cat python.txt', ['한글 tiedoston_nimi'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = tulos / 'Hello.class'; 자바클래스.write_bytes(ladata('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(tulos), 'Hello', '한글 argumentit 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 argumentit 😀'], 예상결과
            muutos_ARVO('인사.java', 'public class 인사 { public static void main(String[] args) { int ARVO = 7; System.out.println("한글=" + ARVO); } }')
            liittymä('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            liittymä('java 인사', ['한글=7', 'exit 0'])
            (tulos / '인사.class').write_bytes(ladata('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(tulos), '인사']).decode().strip() == '한글=7'
            muutos_ARVO('Hello.java', 'broken', kumota_leikkaus=True)
            liittymä('javac Hello.java', ['Compiled:', 'exit 0'])
            muutos_ARVO('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            liittymä('javac Broken.java', ['javac error:', 'exit 1'])
            Upload_Files('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            liittymä('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            liittymä('rm Broken.java', [])
            들여온파일 = tulos / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Upload_Files('Imported.class', (tulos / 'Imported.class').read_bytes())
            liittymä('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            liittymä('rm Imported.class', [])
            muutos_ARVO('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            liittymä('javac Loop.java', ['Compiled:', 'exit 0'])
            vastaus = liittymä('java Loop', ['exit '])
            assert b'instruction limit' in vastaus or b'exit -1004' in vastaus
            liittymä('rm Loop.java', []); liittymä('rm Loop.class', [])
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
            muutos_ARVO('checks.py', 파이썬검사)
            liittymä('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            liittymä('rm checks.py', [])
            muutos_ARVO('helper.py', 'value = 321')
            liittymä("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            liittymä('rm helper.py', [])
            liittymä("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            liittymä("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                liittymä('python hello.py', ['한글 tiedoston_nimi', 'exit 0'])
                liittymä('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Upload_Files('app.elf', (aloite_juuri / 'build/user/demo.elf').read_bytes())
            assert ladata('app.elf') == (aloite_juuri / 'build/user/demo.elf').read_bytes()
            liittymä('run app.elf', ['EL0 C++', 'exit 0'])
            Upload_Files('app.elf', b'not an ELF')
            liittymä('run app.elf', ['exit -8'])
            liittymä('rm app.elf', [])
            liittymä('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            piirustus_polku = tulos / 'java-framebuffer'; piirustus_polku.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(aloite_juuri / 'dist/jkoros-native-korean.jar'), '-d', str(piirustus_polku), str(aloite_juuri / 'testit/자바/화면시험.java')])
            Upload_Files('화면시험.class', (piirustus_polku / '화면시험.class').read_bytes())
            liittymä('java 화면시험', ['화면 leikata hylkää_ARVO_e3ecc00b', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            liittymä('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as asiakas:
                asiakas.settimeout(10)
                asiakas.connect(str(모의제어경로))
                with asiakas.makefile('rwb') as virta_ARVO:
                    인사 = json.loads(virta_ARVO.readline())
                    def 모의제어접속(Suorita, 전달인수=None):
                        verkko_sanoma = {'execute': Suorita}
                        if 전달인수: verkko_sanoma['arguments'] = 전달인수
                        virta_ARVO.write((json.dumps(verkko_sanoma) + '\n').encode())
                        virta_ARVO.flush()
                        while True:
                            palaute = json.loads(virta_ARVO.readline())
                            if 'error' in palaute: raise AssertionError(palaute)
                            if 'return' in palaute: return palaute['return']
                    모의제어접속('qmp_capabilities')
                    näyttökuva = tulos / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(näyttökuva), 'format': 'ppm'})
                    def 예제들(polku_2, 지점들):
                        with polku_2.open('rb') as kuvapiste_Tiedosto:
                            assert kuvapiste_Tiedosto.readline().strip() == b'P6'
                            assert kuvapiste_Tiedosto.readline().strip() == b'640 480'
                            assert kuvapiste_Tiedosto.readline().strip() == b'255'
                            kuvapiste_data = kuvapiste_Tiedosto.read()
                        assert len(kuvapiste_data) == 640 * 480 * 3
                        return [list(kuvapiste_data[(Y_koordinaatti * 640 + x_koordinaatti) * 3:(Y_koordinaatti * 640 + x_koordinaatti) * 3 + 3]) for x_koordinaatti, Y_koordinaatti in 지점들]
                    assert 예제들(näyttökuva, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(näyttökuva, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def lähettää(누름값, merkintä):
                        SIIRTYMÄ_ARVO = len(transkriptio)
                        Prosessi.stdin.write(누름값); Prosessi.stdin.flush()
                        표시까지받기(merkintä, SIIRTYMÄ_ARVO)
                    lähettää(b'gui\n', b'GUI READY:')
                    첫화면 = tulos / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(tulos / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    lähettää(b'\r', b'GUI ACTION 0 RESULT 0')
                    lähettää(b'\t', b'GUI FOCUS 1')
                    lähettää(b'\r', b'GUI ACTION 1 RESULT 0')
                    SEKUNNIT_GUI = tulos / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SEKUNNIT_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(tulos / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SEKUNNIT_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    lähettää(b'\t', b'GUI FOCUS 2')
                    lähettää(b'\r', b'GUI ACTION 2 RESULT 0')
                    lähettää(b'\t', b'GUI FOCUS 3')
                    lähettää(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(tulos / 'gui-python.png'), 'format': 'png'})
                    lähettää(b'q', b'jkoros-native> ')
                    vahvistus_raportti['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Prosessi.wait(timeout=10)
            # framebuffer 응답뿐 아니라 todellinen_data scanout 픽셀도 확인한다.
            with näyttökuva.open('rb') as Tiedosto_merkintä:
                assert Tiedosto_merkintä.readline().strip() == b'P6'
                치수 = Tiedosto_merkintä.readline().strip()
                assert 치수 == b'640 480', 치수
                assert Tiedosto_merkintä.readline().strip() == b'255'
                화소들 = Tiedosto_merkintä.read()
            assert len(화소들) == 640 * 480 * 3
            def kuvapiste(x_koordinaatti, Y_koordinaatti): return list(화소들[(Y_koordinaatti * 640 + x_koordinaatti) * 3:(Y_koordinaatti * 640 + x_koordinaatti) * 3 + 3])
            예제들 = {'background': kuvapiste(5, 5), 'panel': kuvapiste(45, 85), 'tile': kuvapiste(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            vahvistus_raportti.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((aloite_juuri / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Prosessi.poll() is None:
                Prosessi.terminate()
                try: Prosessi.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Prosessi.kill(); Prosessi.wait(timeout=5)
            valitsin.close()
            Prosessi.stdin.close(); Prosessi.stdout.close()
            (tulos / 'serial.log').write_bytes(transkriptio)
            (tulos / 'report.json').write_text(json.dumps(vahvistus_raportti, indent=2) + '\n')


if __name__ == '__main__':
    Suorita_2()
