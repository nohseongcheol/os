#!/usr/bin/env python3
"""faktisks_dati raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from Izpildīt_komanda import Project_sakne, Komanda


def Palaist():
    ražojums = Project_sakne / 'build/verification'
    ražojums.mkdir(parents=True, exist_ok=True)
    transkripcija = bytearray()
    validācija_ziņot = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Komanda() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        validācija_ziņot['command'] = 명령인수
        Process = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        atlasītājs = selectors.DefaultSelector()
        atlasītājs.register(Process.stdout, selectors.EVENT_READ)
        def 표시까지받기(marķieris, Nobīde_VALUE=0, 시간제한=45):
            izpildes_termiņš_TIME = time.monotonic() + 시간제한
            while marķieris not in transkripcija[Nobīde_VALUE:]:
                if time.monotonic() > izpildes_termiņš_TIME:
                    raise AssertionError('UART timeout: ' + repr(marķieris))
                for 누름값, _ in atlasītājs.select(0.2):
                    datu_bloks = 누름값.fileobj.read(4096)
                    if datu_bloks:
                        transkripcija.extend(datu_bloks)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', transkripcija):
                    raise AssertionError('kernel failure')
                if Process.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Process.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for marķieris in 확인표시들:
                assert marķieris in transkripcija, marķieris
            # GTK 없는 pašreizējais_krājums 호스트에서도 VNC로 faktisks_dati GUI를 볼 numurs 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def EXACT_VALUE(Izmērs):
                    mērs = b''
                    while len(mērs) < Izmērs:
                        조각 = 화면접속자.recv(Izmērs - len(mērs))
                        if not 조각: raise AssertionError('VNC disconnected')
                        mērs += 조각
                    return mērs
                assert EXACT_VALUE(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in EXACT_VALUE(EXACT_VALUE(1)[0]); 화면접속자.sendall(b'\x01')
                assert EXACT_VALUE(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                serveris_VALUE = EXACT_VALUE(24)
                assert int.from_bytes(serveris_VALUE[:2], 'big') == 640 and int.from_bytes(serveris_VALUE[2:4], 'big') == 480
                EXACT_VALUE(int.from_bytes(serveris_VALUE[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for komanda_byte, marķieris in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                Nobīde_VALUE = len(transkripcija)
                Process.stdin.write(komanda_byte + b'\n')
                Process.stdin.flush()
                표시까지받기(b'jkoros-native> ', Nobīde_VALUE)
                assert marķieris in transkripcija[Nobīde_VALUE:], marķieris
            def čaula(Līniju, 예상결과):
                Nobīde_VALUE = len(transkripcija)
                Process.stdin.write(Līniju.encode('utf-8') + b'\n'); Process.stdin.flush()
                표시까지받기(b'jkoros-native> ', Nobīde_VALUE)
                atbilde_1262b476 = bytes(transkripcija[Nobīde_VALUE:])
                for Teksts in 예상결과:
                    assert Teksts.encode('utf-8') in atbilde_1262b476, (Līniju, Teksts, atbilde_1262b476)
                return atbilde_1262b476
            def ievadīt(Līniju, uzvedne):
                Nobīde_VALUE = len(transkripcija)
                Process.stdin.write(Līniju.encode('utf-8') + b'\n'); Process.stdin.flush()
                표시까지받기(uzvedne, Nobīde_VALUE)
                return bytes(transkripcija[Nobīde_VALUE:])
            def Rediģēt_VALUE(Nosaukums, Saturs_VALUE, Atcelt_operācija=False):
                ievadīt('edit ' + Nosaukums, b'edit> ')
                for Līniju in Saturs_VALUE.splitlines(): ievadīt(Līniju, b'edit> ')
                if Atcelt_operācija:
                    Nobīde_VALUE = len(transkripcija)
                    Process.stdin.write(b'\x03'); Process.stdin.flush()
                    표시까지받기(b'jkoros-native> ', Nobīde_VALUE)
                    assert b'EDIT CANCELLED' in transkripcija[Nobīde_VALUE:]
                else:
                    assert b'SAVED' in ievadīt('.', b'jkoros-native> ')
            def Upload_Faili(Nosaukums, dati):
                assert len(dati) <= 16384
                ievadīt('load ' + Nosaukums, b'hex> ')
                for 순번 in range(0, len(dati), 64): ievadīt(dati[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in ievadīt('.', b'jkoros-native> ')
            def lejupielāde(Nosaukums):
                atbilde_1262b476 = čaula('hex ' + Nosaukums, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', atbilde_1262b476, re.S)
                dati = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(dati) == int(일치.group(1)); return dati
            čaula('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            čaula('java -version', ['not OpenJDK', 'exit 0'])
            čaula('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            čaula('java Hello "한글 Parametri 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Parametri 😀', 'exit 0'])
            čaula('python --version', ['MicroPython 1.24.1', 'exit 0'])
            čaula('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Fails', 'exit 0'])
            čaula('cat python.txt', ['한글 Fails'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = ražojums / 'Hello.class'; 자바클래스.write_bytes(lejupielāde('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ražojums), 'Hello', '한글 Parametri 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Parametri 😀'], 예상결과
            Rediģēt_VALUE('인사.java', 'public class 인사 { public static void main(String[] args) { int VALUE = 7; System.out.println("한글=" + VALUE); } }')
            čaula('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            čaula('java 인사', ['한글=7', 'exit 0'])
            (ražojums / '인사.class').write_bytes(lejupielāde('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(ražojums), '인사']).decode().strip() == '한글=7'
            Rediģēt_VALUE('Hello.java', 'broken', Atcelt_operācija=True)
            čaula('javac Hello.java', ['Compiled:', 'exit 0'])
            Rediģēt_VALUE('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            čaula('javac Broken.java', ['javac error:', 'exit 1'])
            Upload_Faili('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            čaula('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            čaula('rm Broken.java', [])
            들여온파일 = ražojums / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Upload_Faili('Imported.class', (ražojums / 'Imported.class').read_bytes())
            čaula('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            čaula('rm Imported.class', [])
            Rediģēt_VALUE('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            čaula('javac Loop.java', ['Compiled:', 'exit 0'])
            atbilde_1262b476 = čaula('java Loop', ['exit '])
            assert b'instruction limit' in atbilde_1262b476 or b'exit -1004' in atbilde_1262b476
            čaula('rm Loop.java', []); čaula('rm Loop.class', [])
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
            Rediģēt_VALUE('checks.py', 파이썬검사)
            čaula('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            čaula('rm checks.py', [])
            Rediģēt_VALUE('helper.py', 'value = 321')
            čaula("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            čaula('rm helper.py', [])
            čaula("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            čaula("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                čaula('python hello.py', ['한글 Fails', 'exit 0'])
                čaula('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Upload_Faili('app.elf', (Project_sakne / 'build/user/demo.elf').read_bytes())
            assert lejupielāde('app.elf') == (Project_sakne / 'build/user/demo.elf').read_bytes()
            čaula('run app.elf', ['EL0 C++', 'exit 0'])
            Upload_Faili('app.elf', b'not an ELF')
            čaula('run app.elf', ['exit -8'])
            čaula('rm app.elf', [])
            čaula('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            zīmējums_ceļš = ražojums / 'java-framebuffer'; zīmējums_ceļš.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_sakne / 'dist/jkoros-native-korean.jar'), '-d', str(zīmējums_ceļš), str(Project_sakne / '시험/자바/화면시험.java')])
            Upload_Faili('화면시험.class', (zīmējums_ceļš / '화면시험.class').read_bytes())
            čaula('java 화면시험', ['화면 klips noraidīt_VALUE', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            čaula('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as klients:
                klients.settimeout(10)
                klients.connect(str(모의제어경로))
                with klients.makefile('rwb') as Stream_VALUE:
                    인사 = json.loads(Stream_VALUE.readline())
                    def 모의제어접속(Izpildīt, 전달인수=None):
                        tīkls_ziņa = {'execute': Izpildīt}
                        if 전달인수: tīkls_ziņa['arguments'] = 전달인수
                        Stream_VALUE.write((json.dumps(tīkls_ziņa) + '\n').encode())
                        Stream_VALUE.flush()
                        while True:
                            atbilde = json.loads(Stream_VALUE.readline())
                            if 'error' in atbilde: raise AssertionError(atbilde)
                            if 'return' in atbilde: return atbilde['return']
                    모의제어접속('qmp_capabilities')
                    ekrānuzņēmums = ražojums / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(ekrānuzņēmums), 'format': 'ppm'})
                    def 예제들(CEĻŠ, 지점들):
                        with CEĻŠ.open('rb') as attēla_elements_Fails:
                            assert attēla_elements_Fails.readline().strip() == b'P6'
                            assert attēla_elements_Fails.readline().strip() == b'640 480'
                            assert attēla_elements_Fails.readline().strip() == b'255'
                            attēla_elements_dati = attēla_elements_Fails.read()
                        assert len(attēla_elements_dati) == 640 * 480 * 3
                        return [list(attēla_elements_dati[(세로좌표 * 640 + x_koordināta) * 3:(세로좌표 * 640 + x_koordināta) * 3 + 3]) for x_koordināta, 세로좌표 in 지점들]
                    assert 예제들(ekrānuzņēmums, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(ekrānuzņēmums, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def sūtīt(누름값, marķieris):
                        Nobīde_VALUE = len(transkripcija)
                        Process.stdin.write(누름값); Process.stdin.flush()
                        표시까지받기(marķieris, Nobīde_VALUE)
                    sūtīt(b'gui\n', b'GUI READY:')
                    첫화면 = ražojums / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(ražojums / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    sūtīt(b'\r', b'GUI ACTION 0 RESULT 0')
                    sūtīt(b'\t', b'GUI FOCUS 1')
                    sūtīt(b'\r', b'GUI ACTION 1 RESULT 0')
                    SECOND_GUI = ražojums / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SECOND_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(ražojums / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SECOND_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    sūtīt(b'\t', b'GUI FOCUS 2')
                    sūtīt(b'\r', b'GUI ACTION 2 RESULT 0')
                    sūtīt(b'\t', b'GUI FOCUS 3')
                    sūtīt(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(ražojums / 'gui-python.png'), 'format': 'png'})
                    sūtīt(b'q', b'jkoros-native> ')
                    validācija_ziņot['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Process.wait(timeout=10)
            # framebuffer 응답뿐 아니라 faktisks_dati scanout 픽셀도 확인한다.
            with ekrānuzņēmums.open('rb') as Fails_ievade:
                assert Fails_ievade.readline().strip() == b'P6'
                치수 = Fails_ievade.readline().strip()
                assert 치수 == b'640 480', 치수
                assert Fails_ievade.readline().strip() == b'255'
                화소들 = Fails_ievade.read()
            assert len(화소들) == 640 * 480 * 3
            def attēla_elements(x_koordināta, 세로좌표): return list(화소들[(세로좌표 * 640 + x_koordināta) * 3:(세로좌표 * 640 + x_koordināta) * 3 + 3])
            예제들 = {'background': attēla_elements(5, 5), 'panel': attēla_elements(45, 85), 'tile': attēla_elements(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            validācija_ziņot.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((Project_sakne / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Process.poll() is None:
                Process.terminate()
                try: Process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Process.kill(); Process.wait(timeout=5)
            atlasītājs.close()
            Process.stdin.close(); Process.stdout.close()
            (ražojums / 'serial.log').write_bytes(transkripcija)
            (ražojums / 'report.json').write_text(json.dumps(validācija_ziņot, indent=2) + '\n')


if __name__ == '__main__':
    Palaist()
