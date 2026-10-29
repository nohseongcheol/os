#!/usr/bin/env python3
"""verklig_data raspi4b maskinstart, UART indata_värde, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from köra_kommando import åtgärd_rot, kommando


def Kör():
    utleverans = åtgärd_rot / 'build/verification'
    utleverans.mkdir(parents=True, exist_ok=True)
    avskrift = bytearray()
    validering_Rapport = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = kommando() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        validering_Rapport['command'] = 명령인수
        Process = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        väljare = selectors.DefaultSelector()
        väljare.register(Process.stdout, selectors.EVENT_READ)
        def 표시까지받기(markör_8b722c5f, FÖRSKJUTNING_värde=0, körning_TIMEOUT=45):
            måldatum_tid = time.monotonic() + körning_TIMEOUT
            while markör_8b722c5f not in avskrift[FÖRSKJUTNING_värde:]:
                if time.monotonic() > måldatum_tid:
                    raise AssertionError('UART timeout: ' + repr(markör_8b722c5f))
                for 누름값, _ in väljare.select(0.2):
                    datablock = 누름값.fileobj.read(4096)
                    if datablock:
                        avskrift.extend(datablock)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', avskrift):
                    raise AssertionError('kernel failure')
                if Process.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Process.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for markör_8b722c5f in 확인표시들:
                assert markör_8b722c5f in avskrift, markör_8b722c5f
            # GTK 없는 aktuellt_objekt 호스트에서도 VNC로 verklig_data GUI를 볼 nummer 있어야 한다.
            with socket.socket(socket.AF_UNIX) as skärmbild_klient:
                skärmbild_klient.settimeout(5); skärmbild_klient.connect(str(Path(작업경로) / 'vnc.sock'))
                def EXAKT_värde(Storlek):
                    RESULTAT = b''
                    while len(RESULTAT) < Storlek:
                        조각 = skärmbild_klient.recv(Storlek - len(RESULTAT))
                        if not 조각: raise AssertionError('VNC disconnected')
                        RESULTAT += 조각
                    return RESULTAT
                assert EXAKT_värde(12) == b'RFB 003.008\n'
                skärmbild_klient.sendall(b'RFB 003.008\n')
                assert 1 in EXAKT_värde(EXAKT_värde(1)[0]); skärmbild_klient.sendall(b'\x01')
                assert EXAKT_värde(4) == b'\x00\x00\x00\x00'; skärmbild_klient.sendall(b'\x01')
                server_värde = EXAKT_värde(24)
                assert int.from_bytes(server_värde[:2], 'big') == 640 and int.from_bytes(server_värde[2:4], 'big') == 480
                EXAKT_värde(int.from_bytes(server_värde[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for kommando_byte, markör_8b722c5f in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', 'tester.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                FÖRSKJUTNING_värde = len(avskrift)
                Process.stdin.write(kommando_byte + b'\n')
                Process.stdin.flush()
                표시까지받기(b'jkoros-native> ', FÖRSKJUTNING_värde)
                assert markör_8b722c5f in avskrift[FÖRSKJUTNING_värde:], markör_8b722c5f
            def Shell(inmatningsrad, 예상결과):
                FÖRSKJUTNING_värde = len(avskrift)
                Process.stdin.write(inmatningsrad.encode('utf-8') + b'\n'); Process.stdin.flush()
                표시까지받기(b'jkoros-native> ', FÖRSKJUTNING_värde)
                svar = bytes(avskrift[FÖRSKJUTNING_värde:])
                for text in 예상결과:
                    assert text.encode('utf-8') in svar, (inmatningsrad, text, svar)
                return svar
            def ange(inmatningsrad, fråga):
                FÖRSKJUTNING_värde = len(avskrift)
                Process.stdin.write(inmatningsrad.encode('utf-8') + b'\n'); Process.stdin.flush()
                표시까지받기(fråga, FÖRSKJUTNING_värde)
                return bytes(avskrift[FÖRSKJUTNING_värde:])
            def ändring_värde(Namn, Innehåll_värde, Avbryt_åtgärd=False):
                ange('edit ' + Namn, b'edit> ')
                for inmatningsrad in Innehåll_värde.splitlines(): ange(inmatningsrad, b'edit> ')
                if Avbryt_åtgärd:
                    FÖRSKJUTNING_värde = len(avskrift)
                    Process.stdin.write(b'\x03'); Process.stdin.flush()
                    표시까지받기(b'jkoros-native> ', FÖRSKJUTNING_värde)
                    assert b'EDIT CANCELLED' in avskrift[FÖRSKJUTNING_värde:]
                else:
                    assert b'SAVED' in ange('.', b'jkoros-native> ')
            def Upload_Filer(Namn, data):
                assert len(data) <= 16384
                ange('load ' + Namn, b'hex> ')
                for 순번 in range(0, len(data), 64): ange(data[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in ange('.', b'jkoros-native> ')
            def hämtning(Namn):
                svar = Shell('hex ' + Namn, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', svar, re.S)
                data = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(data) == int(일치.group(1)); return data
            Shell('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            Shell('java -version', ['not OpenJDK', 'exit 0'])
            Shell('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            Shell('java Hello "한글 argument 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 argument 😀', 'exit 0'])
            Shell('python --version', ['MicroPython 1.24.1', 'exit 0'])
            Shell('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 filnamn', 'exit 0'])
            Shell('cat python.txt', ['한글 filnamn'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = utleverans / 'Hello.class'; 자바클래스.write_bytes(hämtning('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(utleverans), 'Hello', '한글 argument 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 argument 😀'], 예상결과
            ändring_värde('인사.java', 'public class 인사 { public static void main(String[] args) { int värde = 7; System.out.println("한글=" + värde); } }')
            Shell('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            Shell('java 인사', ['한글=7', 'exit 0'])
            (utleverans / '인사.class').write_bytes(hämtning('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(utleverans), '인사']).decode().strip() == '한글=7'
            ändring_värde('Hello.java', 'broken', Avbryt_åtgärd=True)
            Shell('javac Hello.java', ['Compiled:', 'exit 0'])
            ändring_värde('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            Shell('javac Broken.java', ['javac error:', 'exit 1'])
            Upload_Filer('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            Shell('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            Shell('rm Broken.java', [])
            들여온파일 = utleverans / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Upload_Filer('Imported.class', (utleverans / 'Imported.class').read_bytes())
            Shell('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            Shell('rm Imported.class', [])
            ändring_värde('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            Shell('javac Loop.java', ['Compiled:', 'exit 0'])
            svar = Shell('java Loop', ['exit '])
            assert b'instruction limit' in svar or b'exit -1004' in svar
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
            ändring_värde('checks.py', 파이썬검사)
            Shell('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            Shell('rm checks.py', [])
            ändring_värde('helper.py', 'value = 321')
            Shell("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            Shell('rm helper.py', [])
            Shell("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            Shell("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                Shell('python hello.py', ['한글 filnamn', 'exit 0'])
                Shell('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Upload_Filer('app.elf', (åtgärd_rot / 'build/user/demo.elf').read_bytes())
            assert hämtning('app.elf') == (åtgärd_rot / 'build/user/demo.elf').read_bytes()
            Shell('run app.elf', ['EL0 C++', 'exit 0'])
            Upload_Filer('app.elf', b'not an ELF')
            Shell('run app.elf', ['exit -8'])
            Shell('rm app.elf', [])
            Shell('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            ritning_väg = utleverans / 'java-framebuffer'; ritning_väg.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(åtgärd_rot / 'dist/jkoros-native-korean.jar'), '-d', str(ritning_väg), str(åtgärd_rot / 'tester/자바/test_skärmbild.java')])
            Upload_Filer('test_skärmbild.class', (ritning_väg / 'test_skärmbild.class').read_bytes())
            Shell('java test_skärmbild', ['skärmbild klipp avvisa_värde', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            Shell('rm test_skärmbild.class', [])
            with socket.socket(socket.AF_UNIX) as klient:
                klient.settimeout(10)
                klient.connect(str(모의제어경로))
                with klient.makefile('rwb') as flöde_värde:
                    인사 = json.loads(flöde_värde.readline())
                    def 모의제어접속(Starta, 전달인수=None):
                        nätverk_dokument = {'execute': Starta}
                        if 전달인수: nätverk_dokument['arguments'] = 전달인수
                        flöde_värde.write((json.dumps(nätverk_dokument) + '\n').encode())
                        flöde_värde.flush()
                        while True:
                            svara = json.loads(flöde_värde.readline())
                            if 'error' in svara: raise AssertionError(svara)
                            if 'return' in svara: return svara['return']
                    모의제어접속('qmp_capabilities')
                    skärmbild_bb19652a = utleverans / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(skärmbild_bb19652a), 'format': 'ppm'})
                    def 예제들(sökväg_2, 지점들):
                        with sökväg_2.open('rb') as bildpunkt_fil:
                            assert bildpunkt_fil.readline().strip() == b'P6'
                            assert bildpunkt_fil.readline().strip() == b'640 480'
                            assert bildpunkt_fil.readline().strip() == b'255'
                            bildpunkt_data = bildpunkt_fil.read()
                        assert len(bildpunkt_data) == 640 * 480 * 3
                        return [list(bildpunkt_data[(Y_koordinat * 640 + x_koordinat) * 3:(Y_koordinat * 640 + x_koordinat) * 3 + 3]) for x_koordinat, Y_koordinat in 지점들]
                    assert 예제들(skärmbild_bb19652a, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(skärmbild_bb19652a, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def skicka(누름값, markör_8b722c5f):
                        FÖRSKJUTNING_värde = len(avskrift)
                        Process.stdin.write(누름값); Process.stdin.flush()
                        표시까지받기(markör_8b722c5f, FÖRSKJUTNING_värde)
                    skicka(b'gui\n', b'GUI READY:')
                    첫화면 = utleverans / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(utleverans / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    skicka(b'\r', b'GUI ACTION 0 RESULT 0')
                    skicka(b'\t', b'GUI FOCUS 1')
                    skicka(b'\r', b'GUI ACTION 1 RESULT 0')
                    SEKUND_GUI = utleverans / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SEKUND_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(utleverans / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SEKUND_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    skicka(b'\t', b'GUI FOCUS 2')
                    skicka(b'\r', b'GUI ACTION 2 RESULT 0')
                    skicka(b'\t', b'GUI FOCUS 3')
                    skicka(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(utleverans / 'gui-python.png'), 'format': 'png'})
                    skicka(b'q', b'jkoros-native> ')
                    validering_Rapport['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Process.wait(timeout=10)
            # framebuffer 응답뿐 아니라 verklig_data scanout 픽셀도 확인한다.
            with skärmbild_bb19652a.open('rb') as fil_post:
                assert fil_post.readline().strip() == b'P6'
                치수 = fil_post.readline().strip()
                assert 치수 == b'640 480', 치수
                assert fil_post.readline().strip() == b'255'
                화소들 = fil_post.read()
            assert len(화소들) == 640 * 480 * 3
            def bildpunkt(x_koordinat, Y_koordinat): return list(화소들[(Y_koordinat * 640 + x_koordinat) * 3:(Y_koordinat * 640 + x_koordinat) * 3 + 3])
            예제들 = {'background': bildpunkt(5, 5), 'panel': bildpunkt(45, 85), 'tile': bildpunkt(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            validering_Rapport.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((åtgärd_rot / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Process.poll() is None:
                Process.terminate()
                try: Process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Process.kill(); Process.wait(timeout=5)
            väljare.close()
            Process.stdin.close(); Process.stdout.close()
            (utleverans / 'serial.log').write_bytes(avskrift)
            (utleverans / 'report.json').write_text(json.dumps(validering_Rapport, indent=2) + '\n')


if __name__ == '__main__':
    Kör()
