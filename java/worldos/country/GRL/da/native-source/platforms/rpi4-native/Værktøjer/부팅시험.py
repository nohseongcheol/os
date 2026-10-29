#!/usr/bin/env python3
"""faktisk_data raspi4b 부팅, UART input_VÆRDI, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from Udfør_kommando import To_do_rod, Kommando


def Kør_2():
    produktoutput = To_do_rod / 'build/verification'
    produktoutput.mkdir(parents=True, exist_ok=True)
    afskrift = bytearray()
    validering_rapport = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Kommando() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        validering_rapport['command'] = 명령인수
        Proces = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        selektor = selectors.DefaultSelector()
        selektor.register(Proces.stdout, selectors.EVENT_READ)
        def 표시까지받기(mærke, FORSKYDNING_VÆRDI=0, udførelse_TIMEOUT=45):
            deadline_TID = time.monotonic() + udførelse_TIMEOUT
            while mærke not in afskrift[FORSKYDNING_VÆRDI:]:
                if time.monotonic() > deadline_TID:
                    raise AssertionError('UART timeout: ' + repr(mærke))
                for 누름값, _ in selektor.select(0.2):
                    datablok = 누름값.fileobj.read(4096)
                    if datablok:
                        afskrift.extend(datablok)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', afskrift):
                    raise AssertionError('kernel failure')
                if Proces.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Proces.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for mærke in 확인표시들:
                assert mærke in afskrift, mærke
            # GTK 없는 aktuel_vare 호스트에서도 VNC로 faktisk_data GUI를 볼 tal 있어야 한다.
            with socket.socket(socket.AF_UNIX) as skærmbillede_klient:
                skærmbillede_klient.settimeout(5); skærmbillede_klient.connect(str(Path(작업경로) / 'vnc.sock'))
                def EKSAKT_VÆRDI(Størrelse):
                    KR = b''
                    while len(KR) < Størrelse:
                        조각 = skærmbillede_klient.recv(Størrelse - len(KR))
                        if not 조각: raise AssertionError('VNC disconnected')
                        KR += 조각
                    return KR
                assert EKSAKT_VÆRDI(12) == b'RFB 003.008\n'
                skærmbillede_klient.sendall(b'RFB 003.008\n')
                assert 1 in EKSAKT_VÆRDI(EKSAKT_VÆRDI(1)[0]); skærmbillede_klient.sendall(b'\x01')
                assert EKSAKT_VÆRDI(4) == b'\x00\x00\x00\x00'; skærmbillede_klient.sendall(b'\x01')
                server_VÆRDI = EKSAKT_VÆRDI(24)
                assert int.from_bytes(server_VÆRDI[:2], 'big') == 640 and int.from_bytes(server_VÆRDI[2:4], 'big') == 480
                EKSAKT_VÆRDI(int.from_bytes(server_VÆRDI[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for kommando_byte, mærke in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                FORSKYDNING_VÆRDI = len(afskrift)
                Proces.stdin.write(kommando_byte + b'\n')
                Proces.stdin.flush()
                표시까지받기(b'jkoros-native> ', FORSKYDNING_VÆRDI)
                assert mærke in afskrift[FORSKYDNING_VÆRDI:], mærke
            def Shell(Linje, 예상결과):
                FORSKYDNING_VÆRDI = len(afskrift)
                Proces.stdin.write(Linje.encode('utf-8') + b'\n'); Proces.stdin.flush()
                표시까지받기(b'jkoros-native> ', FORSKYDNING_VÆRDI)
                svar_1262b476 = bytes(afskrift[FORSKYDNING_VÆRDI:])
                for Tekst in 예상결과:
                    assert Tekst.encode('utf-8') in svar_1262b476, (Linje, Tekst, svar_1262b476)
                return svar_1262b476
            def angive(Linje, prompt):
                FORSKYDNING_VÆRDI = len(afskrift)
                Proces.stdin.write(Linje.encode('utf-8') + b'\n'); Proces.stdin.flush()
                표시까지받기(prompt, FORSKYDNING_VÆRDI)
                return bytes(afskrift[FORSKYDNING_VÆRDI:])
            def Rediger_VÆRDI(Navn, Indhold_VÆRDI, Annuller_kirurgi=False):
                angive('edit ' + Navn, b'edit> ')
                for Linje in Indhold_VÆRDI.splitlines(): angive(Linje, b'edit> ')
                if Annuller_kirurgi:
                    FORSKYDNING_VÆRDI = len(afskrift)
                    Proces.stdin.write(b'\x03'); Proces.stdin.flush()
                    표시까지받기(b'jkoros-native> ', FORSKYDNING_VÆRDI)
                    assert b'EDIT CANCELLED' in afskrift[FORSKYDNING_VÆRDI:]
                else:
                    assert b'SAVED' in angive('.', b'jkoros-native> ')
            def Upload_Filer(Navn, data):
                assert len(data) <= 16384
                angive('load ' + Navn, b'hex> ')
                for 순번 in range(0, len(data), 64): angive(data[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in angive('.', b'jkoros-native> ')
            def hente(Navn):
                svar_1262b476 = Shell('hex ' + Navn, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', svar_1262b476, re.S)
                data = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(data) == int(일치.group(1)); return data
            Shell('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            Shell('java -version', ['not OpenJDK', 'exit 0'])
            Shell('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            Shell('java Hello "한글 Argumenter 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Argumenter 😀', 'exit 0'])
            Shell('python --version', ['MicroPython 1.24.1', 'exit 0'])
            Shell('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Fil', 'exit 0'])
            Shell('cat python.txt', ['한글 Fil'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = produktoutput / 'Hello.class'; 자바클래스.write_bytes(hente('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(produktoutput), 'Hello', '한글 Argumenter 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Argumenter 😀'], 예상결과
            Rediger_VÆRDI('인사.java', 'public class 인사 { public static void main(String[] args) { int VÆRDI = 7; System.out.println("한글=" + VÆRDI); } }')
            Shell('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            Shell('java 인사', ['한글=7', 'exit 0'])
            (produktoutput / '인사.class').write_bytes(hente('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(produktoutput), '인사']).decode().strip() == '한글=7'
            Rediger_VÆRDI('Hello.java', 'broken', Annuller_kirurgi=True)
            Shell('javac Hello.java', ['Compiled:', 'exit 0'])
            Rediger_VÆRDI('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            Shell('javac Broken.java', ['javac error:', 'exit 1'])
            Upload_Filer('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            Shell('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            Shell('rm Broken.java', [])
            들여온파일 = produktoutput / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Upload_Filer('Imported.class', (produktoutput / 'Imported.class').read_bytes())
            Shell('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            Shell('rm Imported.class', [])
            Rediger_VÆRDI('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            Shell('javac Loop.java', ['Compiled:', 'exit 0'])
            svar_1262b476 = Shell('java Loop', ['exit '])
            assert b'instruction limit' in svar_1262b476 or b'exit -1004' in svar_1262b476
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
            Rediger_VÆRDI('checks.py', 파이썬검사)
            Shell('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            Shell('rm checks.py', [])
            Rediger_VÆRDI('helper.py', 'value = 321')
            Shell("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            Shell('rm helper.py', [])
            Shell("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            Shell("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                Shell('python hello.py', ['한글 Fil', 'exit 0'])
                Shell('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Upload_Filer('app.elf', (To_do_rod / 'build/user/demo.elf').read_bytes())
            assert hente('app.elf') == (To_do_rod / 'build/user/demo.elf').read_bytes()
            Shell('run app.elf', ['EL0 C++', 'exit 0'])
            Upload_Filer('app.elf', b'not an ELF')
            Shell('run app.elf', ['exit -8'])
            Shell('rm app.elf', [])
            Shell('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            tegning_sti = produktoutput / 'java-framebuffer'; tegning_sti.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(To_do_rod / 'dist/jkoros-native-korean.jar'), '-d', str(tegning_sti), str(To_do_rod / '시험/자바/test_skærmbillede.java')])
            Upload_Filer('test_skærmbillede.class', (tegning_sti / 'test_skærmbillede.class').read_bytes())
            Shell('java test_skærmbillede', ['skærmbillede klippe afvise_VÆRDI', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            Shell('rm test_skærmbillede.class', [])
            with socket.socket(socket.AF_UNIX) as klient:
                klient.settimeout(10)
                klient.connect(str(모의제어경로))
                with klient.makefile('rwb') as strøm_VÆRDI:
                    인사 = json.loads(strøm_VÆRDI.readline())
                    def 모의제어접속(Kør, 전달인수=None):
                        netværk_mail = {'execute': Kør}
                        if 전달인수: netværk_mail['arguments'] = 전달인수
                        strøm_VÆRDI.write((json.dumps(netværk_mail) + '\n').encode())
                        strøm_VÆRDI.flush()
                        while True:
                            svar = json.loads(strøm_VÆRDI.readline())
                            if 'error' in svar: raise AssertionError(svar)
                            if 'return' in svar: return svar['return']
                    모의제어접속('qmp_capabilities')
                    skærmklip = produktoutput / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(skærmklip), 'format': 'ppm'})
                    def 예제들(Sti, 지점들):
                        with Sti.open('rb') as pixel_fil:
                            assert pixel_fil.readline().strip() == b'P6'
                            assert pixel_fil.readline().strip() == b'640 480'
                            assert pixel_fil.readline().strip() == b'255'
                            pixel_data = pixel_fil.read()
                        assert len(pixel_data) == 640 * 480 * 3
                        return [list(pixel_data[(Y_koordinat * 640 + X_koordinat) * 3:(Y_koordinat * 640 + X_koordinat) * 3 + 3]) for X_koordinat, Y_koordinat in 지점들]
                    assert 예제들(skærmklip, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(skærmklip, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def maile(누름값, mærke):
                        FORSKYDNING_VÆRDI = len(afskrift)
                        Proces.stdin.write(누름값); Proces.stdin.flush()
                        표시까지받기(mærke, FORSKYDNING_VÆRDI)
                    maile(b'gui\n', b'GUI READY:')
                    첫화면 = produktoutput / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(produktoutput / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    maile(b'\r', b'GUI ACTION 0 RESULT 0')
                    maile(b'\t', b'GUI FOCUS 1')
                    maile(b'\r', b'GUI ACTION 1 RESULT 0')
                    SEKUND_GUI = produktoutput / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SEKUND_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(produktoutput / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SEKUND_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    maile(b'\t', b'GUI FOCUS 2')
                    maile(b'\r', b'GUI ACTION 2 RESULT 0')
                    maile(b'\t', b'GUI FOCUS 3')
                    maile(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(produktoutput / 'gui-python.png'), 'format': 'png'})
                    maile(b'q', b'jkoros-native> ')
                    validering_rapport['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Proces.wait(timeout=10)
            # framebuffer 응답뿐 아니라 faktisk_data scanout 픽셀도 확인한다.
            with skærmklip.open('rb') as fil_post:
                assert fil_post.readline().strip() == b'P6'
                치수 = fil_post.readline().strip()
                assert 치수 == b'640 480', 치수
                assert fil_post.readline().strip() == b'255'
                화소들 = fil_post.read()
            assert len(화소들) == 640 * 480 * 3
            def pixel(X_koordinat, Y_koordinat): return list(화소들[(Y_koordinat * 640 + X_koordinat) * 3:(Y_koordinat * 640 + X_koordinat) * 3 + 3])
            예제들 = {'background': pixel(5, 5), 'panel': pixel(45, 85), 'tile': pixel(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            validering_rapport.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((To_do_rod / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Proces.poll() is None:
                Proces.terminate()
                try: Proces.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Proces.kill(); Proces.wait(timeout=5)
            selektor.close()
            Proces.stdin.close(); Proces.stdout.close()
            (produktoutput / 'serial.log').write_bytes(afskrift)
            (produktoutput / 'report.json').write_text(json.dumps(validering_rapport, indent=2) + '\n')


if __name__ == '__main__':
    Kør_2()
