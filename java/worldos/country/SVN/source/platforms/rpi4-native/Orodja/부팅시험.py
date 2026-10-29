#!/usr/bin/env python3
"""dejanski_podatki raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from Izvedi_ukaz import pobuda_koren, Ukaz


def Zaženi():
    출력결과 = pobuda_koren / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    prepis = bytearray()
    preverjanje_veljavnosti_prijavi = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Ukaz() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        preverjanje_veljavnosti_prijavi['command'] = 명령인수
        Opravilo = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        izbirnik = selectors.DefaultSelector()
        izbirnik.register(Opravilo.stdout, selectors.EVENT_READ)
        def 표시까지받기(oznaka, odmik_VALUE=0, 시간제한=45):
            rok_čas = time.monotonic() + 시간제한
            while oznaka not in prepis[odmik_VALUE:]:
                if time.monotonic() > rok_čas:
                    raise AssertionError('UART timeout: ' + repr(oznaka))
                for 누름값, _ in izbirnik.select(0.2):
                    blok_podatkov = 누름값.fileobj.read(4096)
                    if blok_podatkov:
                        prepis.extend(blok_podatkov)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', prepis):
                    raise AssertionError('kernel failure')
                if Opravilo.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Opravilo.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for oznaka in 확인표시들:
                assert oznaka in prepis, oznaka
            # GTK 없는 sprotno_element 호스트에서도 VNC로 dejanski_podatki GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def EXACT_VALUE(Velikost):
                    REZULTAT = b''
                    while len(REZULTAT) < Velikost:
                        조각 = 화면접속자.recv(Velikost - len(REZULTAT))
                        if not 조각: raise AssertionError('VNC disconnected')
                        REZULTAT += 조각
                    return REZULTAT
                assert EXACT_VALUE(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in EXACT_VALUE(EXACT_VALUE(1)[0]); 화면접속자.sendall(b'\x01')
                assert EXACT_VALUE(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                strežnik_VALUE = EXACT_VALUE(24)
                assert int.from_bytes(strežnik_VALUE[:2], 'big') == 640 and int.from_bytes(strežnik_VALUE[2:4], 'big') == 480
                EXACT_VALUE(int.from_bytes(strežnik_VALUE[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for ukaz_bajt, oznaka in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                odmik_VALUE = len(prepis)
                Opravilo.stdin.write(ukaz_bajt + b'\n')
                Opravilo.stdin.flush()
                표시까지받기(b'jkoros-native> ', odmik_VALUE)
                assert oznaka in prepis[odmik_VALUE:], oznaka
            def lupina(Črtni, 예상결과):
                odmik_VALUE = len(prepis)
                Opravilo.stdin.write(Črtni.encode('utf-8') + b'\n'); Opravilo.stdin.flush()
                표시까지받기(b'jkoros-native> ', odmik_VALUE)
                odziv = bytes(prepis[odmik_VALUE:])
                for Besedilo in 예상결과:
                    assert Besedilo.encode('utf-8') in odziv, (Črtni, Besedilo, odziv)
                return odziv
            def vnesti(Črtni, poziv):
                odmik_VALUE = len(prepis)
                Opravilo.stdin.write(Črtni.encode('utf-8') + b'\n'); Opravilo.stdin.flush()
                표시까지받기(poziv, odmik_VALUE)
                return bytes(prepis[odmik_VALUE:])
            def Uredi_VALUE(Ime, vsebina_VALUE, Prekliči_postopek=False):
                vnesti('edit ' + Ime, b'edit> ')
                for Črtni in vsebina_VALUE.splitlines(): vnesti(Črtni, b'edit> ')
                if Prekliči_postopek:
                    odmik_VALUE = len(prepis)
                    Opravilo.stdin.write(b'\x03'); Opravilo.stdin.flush()
                    표시까지받기(b'jkoros-native> ', odmik_VALUE)
                    assert b'EDIT CANCELLED' in prepis[odmik_VALUE:]
                else:
                    assert b'SAVED' in vnesti('.', b'jkoros-native> ')
            def Upload_Datoteke(Ime, podatki):
                assert len(podatki) <= 16384
                vnesti('load ' + Ime, b'hex> ')
                for 순번 in range(0, len(podatki), 64): vnesti(podatki[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in vnesti('.', b'jkoros-native> ')
            def prenos(Ime):
                odziv = lupina('hex ' + Ime, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', odziv, re.S)
                podatki = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(podatki) == int(일치.group(1)); return podatki
            lupina('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            lupina('java -version', ['not OpenJDK', 'exit 0'])
            lupina('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            lupina('java Hello "한글 Argumenti 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Argumenti 😀', 'exit 0'])
            lupina('python --version', ['MicroPython 1.24.1', 'exit 0'])
            lupina('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Datoteka', 'exit 0'])
            lupina('cat python.txt', ['한글 Datoteka'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(prenos('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 Argumenti 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Argumenti 😀'], 예상결과
            Uredi_VALUE('인사.java', 'public class 인사 { public static void main(String[] args) { int VALUE = 7; System.out.println("한글=" + VALUE); } }')
            lupina('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            lupina('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(prenos('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            Uredi_VALUE('Hello.java', 'broken', Prekliči_postopek=True)
            lupina('javac Hello.java', ['Compiled:', 'exit 0'])
            Uredi_VALUE('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            lupina('javac Broken.java', ['javac error:', 'exit 1'])
            Upload_Datoteke('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            lupina('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            lupina('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Upload_Datoteke('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            lupina('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            lupina('rm Imported.class', [])
            Uredi_VALUE('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            lupina('javac Loop.java', ['Compiled:', 'exit 0'])
            odziv = lupina('java Loop', ['exit '])
            assert b'instruction limit' in odziv or b'exit -1004' in odziv
            lupina('rm Loop.java', []); lupina('rm Loop.class', [])
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
            lupina('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            lupina('rm checks.py', [])
            Uredi_VALUE('helper.py', 'value = 321')
            lupina("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            lupina('rm helper.py', [])
            lupina("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            lupina("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                lupina('python hello.py', ['한글 Datoteka', 'exit 0'])
                lupina('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Upload_Datoteke('app.elf', (pobuda_koren / 'build/user/demo.elf').read_bytes())
            assert prenos('app.elf') == (pobuda_koren / 'build/user/demo.elf').read_bytes()
            lupina('run app.elf', ['EL0 C++', 'exit 0'])
            Upload_Datoteke('app.elf', b'not an ELF')
            lupina('run app.elf', ['exit -8'])
            lupina('rm app.elf', [])
            lupina('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            risba_pot = 출력결과 / 'java-framebuffer'; risba_pot.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(pobuda_koren / 'dist/jkoros-native-korean.jar'), '-d', str(risba_pot), str(pobuda_koren / '시험/자바/화면시험.java')])
            Upload_Datoteke('화면시험.class', (risba_pot / '화면시험.class').read_bytes())
            lupina('java 화면시험', ['화면 izrezek zavrniti_VALUE', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            lupina('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as odjemalec:
                odjemalec.settimeout(10)
                odjemalec.connect(str(모의제어경로))
                with odjemalec.makefile('rwb') as tok_VALUE:
                    인사 = json.loads(tok_VALUE.readline())
                    def 모의제어접속(Izvedi, 전달인수=None):
                        mreža_e_pošta = {'execute': Izvedi}
                        if 전달인수: mreža_e_pošta['arguments'] = 전달인수
                        tok_VALUE.write((json.dumps(mreža_e_pošta) + '\n').encode())
                        tok_VALUE.flush()
                        while True:
                            odgovor = json.loads(tok_VALUE.readline())
                            if 'error' in odgovor: raise AssertionError(odgovor)
                            if 'return' in odgovor: return odgovor['return']
                    모의제어접속('qmp_capabilities')
                    izrezek_zaslona = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(izrezek_zaslona), 'format': 'ppm'})
                    def 예제들(POT, 지점들):
                        with POT.open('rb') as slikovna_pika_Datoteka:
                            assert slikovna_pika_Datoteka.readline().strip() == b'P6'
                            assert slikovna_pika_Datoteka.readline().strip() == b'640 480'
                            assert slikovna_pika_Datoteka.readline().strip() == b'255'
                            slikovna_pika_podatki = slikovna_pika_Datoteka.read()
                        assert len(slikovna_pika_podatki) == 640 * 480 * 3
                        return [list(slikovna_pika_podatki[(세로좌표 * 640 + koordinata_x) * 3:(세로좌표 * 640 + koordinata_x) * 3 + 3]) for koordinata_x, 세로좌표 in 지점들]
                    assert 예제들(izrezek_zaslona, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(izrezek_zaslona, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def poslati(누름값, oznaka):
                        odmik_VALUE = len(prepis)
                        Opravilo.stdin.write(누름값); Opravilo.stdin.flush()
                        표시까지받기(oznaka, odmik_VALUE)
                    poslati(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    poslati(b'\r', b'GUI ACTION 0 RESULT 0')
                    poslati(b'\t', b'GUI FOCUS 1')
                    poslati(b'\r', b'GUI ACTION 1 RESULT 0')
                    SECOND_grafični_uporabniški_vmesnik = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SECOND_grafični_uporabniški_vmesnik), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SECOND_grafični_uporabniški_vmesnik, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    poslati(b'\t', b'GUI FOCUS 2')
                    poslati(b'\r', b'GUI ACTION 2 RESULT 0')
                    poslati(b'\t', b'GUI FOCUS 3')
                    poslati(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    poslati(b'q', b'jkoros-native> ')
                    preverjanje_veljavnosti_prijavi['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Opravilo.wait(timeout=10)
            # framebuffer 응답뿐 아니라 dejanski_podatki scanout 픽셀도 확인한다.
            with izrezek_zaslona.open('rb') as Datoteka_vnos:
                assert Datoteka_vnos.readline().strip() == b'P6'
                치수 = Datoteka_vnos.readline().strip()
                assert 치수 == b'640 480', 치수
                assert Datoteka_vnos.readline().strip() == b'255'
                화소들 = Datoteka_vnos.read()
            assert len(화소들) == 640 * 480 * 3
            def slikovna_pika(koordinata_x, 세로좌표): return list(화소들[(세로좌표 * 640 + koordinata_x) * 3:(세로좌표 * 640 + koordinata_x) * 3 + 3])
            예제들 = {'background': slikovna_pika(5, 5), 'panel': slikovna_pika(45, 85), 'tile': slikovna_pika(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            preverjanje_veljavnosti_prijavi.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((pobuda_koren / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Opravilo.poll() is None:
                Opravilo.terminate()
                try: Opravilo.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Opravilo.kill(); Opravilo.wait(timeout=5)
            izbirnik.close()
            Opravilo.stdin.close(); Opravilo.stdout.close()
            (출력결과 / 'serial.log').write_bytes(prepis)
            (출력결과 / 'report.json').write_text(json.dumps(preverjanje_veljavnosti_prijavi, indent=2) + '\n')


if __name__ == '__main__':
    Zaženi()
