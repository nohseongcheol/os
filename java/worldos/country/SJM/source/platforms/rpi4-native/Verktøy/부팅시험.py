#!/usr/bin/env python3
"""faktisk_data raspi4b 부팅, UART inndata_VERDI, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from Utfør_kommando import speile_rot, Kommando


def Kjør_2():
    produksjon = speile_rot / 'build/verification'
    produksjon.mkdir(parents=True, exist_ok=True)
    utskrift = bytearray()
    validering_rapport = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Kommando() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        validering_rapport['command'] = 명령인수
        Prosess = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        velger = selectors.DefaultSelector()
        velger.register(Prosess.stdout, selectors.EVENT_READ)
        def 표시까지받기(tusj, FORSKYVNING_VERDI=0, kjøring_TIMEOUT=45):
            tidsfrist_TID = time.monotonic() + kjøring_TIMEOUT
            while tusj not in utskrift[FORSKYVNING_VERDI:]:
                if time.monotonic() > tidsfrist_TID:
                    raise AssertionError('UART timeout: ' + repr(tusj))
                for 누름값, _ in velger.select(0.2):
                    data_blokk = 누름값.fileobj.read(4096)
                    if data_blokk:
                        utskrift.extend(data_blokk)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', utskrift):
                    raise AssertionError('kernel failure')
                if Prosess.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Prosess.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for tusj in 확인표시들:
                assert tusj in utskrift, tusj
            # GTK 없는 betalt_vare 호스트에서도 VNC로 faktisk_data GUI를 볼 nummer 있어야 한다.
            with socket.socket(socket.AF_UNIX) as skjermbilde_klient:
                skjermbilde_klient.settimeout(5); skjermbilde_klient.connect(str(Path(작업경로) / 'vnc.sock'))
                def EKSAKT_VERDI(Størrelse):
                    KR = b''
                    while len(KR) < Størrelse:
                        조각 = skjermbilde_klient.recv(Størrelse - len(KR))
                        if not 조각: raise AssertionError('VNC disconnected')
                        KR += 조각
                    return KR
                assert EKSAKT_VERDI(12) == b'RFB 003.008\n'
                skjermbilde_klient.sendall(b'RFB 003.008\n')
                assert 1 in EKSAKT_VERDI(EKSAKT_VERDI(1)[0]); skjermbilde_klient.sendall(b'\x01')
                assert EKSAKT_VERDI(4) == b'\x00\x00\x00\x00'; skjermbilde_klient.sendall(b'\x01')
                server_VERDI = EKSAKT_VERDI(24)
                assert int.from_bytes(server_VERDI[:2], 'big') == 640 and int.from_bytes(server_VERDI[2:4], 'big') == 480
                EKSAKT_VERDI(int.from_bytes(server_VERDI[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for kommando_byte, tusj in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                FORSKYVNING_VERDI = len(utskrift)
                Prosess.stdin.write(kommando_byte + b'\n')
                Prosess.stdin.flush()
                표시까지받기(b'jkoros-native> ', FORSKYVNING_VERDI)
                assert tusj in utskrift[FORSKYVNING_VERDI:], tusj
            def Shell(Linje, 예상결과):
                FORSKYVNING_VERDI = len(utskrift)
                Prosess.stdin.write(Linje.encode('utf-8') + b'\n'); Prosess.stdin.flush()
                표시까지받기(b'jkoros-native> ', FORSKYVNING_VERDI)
                svar_1262b476 = bytes(utskrift[FORSKYVNING_VERDI:])
                for Tekst in 예상결과:
                    assert Tekst.encode('utf-8') in svar_1262b476, (Linje, Tekst, svar_1262b476)
                return svar_1262b476
            def angi(Linje, be_om):
                FORSKYVNING_VERDI = len(utskrift)
                Prosess.stdin.write(Linje.encode('utf-8') + b'\n'); Prosess.stdin.flush()
                표시까지받기(be_om, FORSKYVNING_VERDI)
                return bytes(utskrift[FORSKYVNING_VERDI:])
            def Rediger_VERDI(Navn, Innhold_VERDI, Avbryt_operasjon=False):
                angi('edit ' + Navn, b'edit> ')
                for Linje in Innhold_VERDI.splitlines(): angi(Linje, b'edit> ')
                if Avbryt_operasjon:
                    FORSKYVNING_VERDI = len(utskrift)
                    Prosess.stdin.write(b'\x03'); Prosess.stdin.flush()
                    표시까지받기(b'jkoros-native> ', FORSKYVNING_VERDI)
                    assert b'EDIT CANCELLED' in utskrift[FORSKYVNING_VERDI:]
                else:
                    assert b'SAVED' in angi('.', b'jkoros-native> ')
            def Upload_Filer(Navn, data):
                assert len(data) <= 16384
                angi('load ' + Navn, b'hex> ')
                for 순번 in range(0, len(data), 64): angi(data[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in angi('.', b'jkoros-native> ')
            def last_ned(Navn):
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
            자바클래스 = produksjon / 'Hello.class'; 자바클래스.write_bytes(last_ned('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(produksjon), 'Hello', '한글 Argumenter 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Argumenter 😀'], 예상결과
            Rediger_VERDI('인사.java', 'public class 인사 { public static void main(String[] args) { int VERDI = 7; System.out.println("한글=" + VERDI); } }')
            Shell('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            Shell('java 인사', ['한글=7', 'exit 0'])
            (produksjon / '인사.class').write_bytes(last_ned('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(produksjon), '인사']).decode().strip() == '한글=7'
            Rediger_VERDI('Hello.java', 'broken', Avbryt_operasjon=True)
            Shell('javac Hello.java', ['Compiled:', 'exit 0'])
            Rediger_VERDI('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            Shell('javac Broken.java', ['javac error:', 'exit 1'])
            Upload_Filer('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            Shell('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            Shell('rm Broken.java', [])
            들여온파일 = produksjon / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Upload_Filer('Imported.class', (produksjon / 'Imported.class').read_bytes())
            Shell('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            Shell('rm Imported.class', [])
            Rediger_VERDI('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
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
            Rediger_VERDI('checks.py', 파이썬검사)
            Shell('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            Shell('rm checks.py', [])
            Rediger_VERDI('helper.py', 'value = 321')
            Shell("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            Shell('rm helper.py', [])
            Shell("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            Shell("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                Shell('python hello.py', ['한글 Fil', 'exit 0'])
                Shell('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Upload_Filer('app.elf', (speile_rot / 'build/user/demo.elf').read_bytes())
            assert last_ned('app.elf') == (speile_rot / 'build/user/demo.elf').read_bytes()
            Shell('run app.elf', ['EL0 C++', 'exit 0'])
            Upload_Filer('app.elf', b'not an ELF')
            Shell('run app.elf', ['exit -8'])
            Shell('rm app.elf', [])
            Shell('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            tegning_bane = produksjon / 'java-framebuffer'; tegning_bane.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(speile_rot / 'dist/jkoros-native-korean.jar'), '-d', str(tegning_bane), str(speile_rot / '시험/자바/test_skjermbilde.java')])
            Upload_Filer('test_skjermbilde.class', (tegning_bane / 'test_skjermbilde.class').read_bytes())
            Shell('java test_skjermbilde', ['skjermbilde klippe avvise_VERDI', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            Shell('rm test_skjermbilde.class', [])
            with socket.socket(socket.AF_UNIX) as klient:
                klient.settimeout(10)
                klient.connect(str(모의제어경로))
                with klient.makefile('rwb') as strøm_VERDI:
                    인사 = json.loads(strøm_VERDI.readline())
                    def 모의제어접속(Kjør, 전달인수=None):
                        nettverk_e_post = {'execute': Kjør}
                        if 전달인수: nettverk_e_post['arguments'] = 전달인수
                        strøm_VERDI.write((json.dumps(nettverk_e_post) + '\n').encode())
                        strøm_VERDI.flush()
                        while True:
                            svar = json.loads(strøm_VERDI.readline())
                            if 'error' in svar: raise AssertionError(svar)
                            if 'return' in svar: return svar['return']
                    모의제어접속('qmp_capabilities')
                    skjermbilde_bb19652a = produksjon / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(skjermbilde_bb19652a), 'format': 'ppm'})
                    def 예제들(Sti, 지점들):
                        with Sti.open('rb') as piksel_Fil:
                            assert piksel_Fil.readline().strip() == b'P6'
                            assert piksel_Fil.readline().strip() == b'640 480'
                            assert piksel_Fil.readline().strip() == b'255'
                            piksel_data = piksel_Fil.read()
                        assert len(piksel_data) == 640 * 480 * 3
                        return [list(piksel_data[(Y_koordinat * 640 + x_koordinat) * 3:(Y_koordinat * 640 + x_koordinat) * 3 + 3]) for x_koordinat, Y_koordinat in 지점들]
                    assert 예제들(skjermbilde_bb19652a, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(skjermbilde_bb19652a, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def sende(누름값, tusj):
                        FORSKYVNING_VERDI = len(utskrift)
                        Prosess.stdin.write(누름값); Prosess.stdin.flush()
                        표시까지받기(tusj, FORSKYVNING_VERDI)
                    sende(b'gui\n', b'GUI READY:')
                    첫화면 = produksjon / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(produksjon / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    sende(b'\r', b'GUI ACTION 0 RESULT 0')
                    sende(b'\t', b'GUI FOCUS 1')
                    sende(b'\r', b'GUI ACTION 1 RESULT 0')
                    SEKUND_GUI = produksjon / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SEKUND_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(produksjon / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SEKUND_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    sende(b'\t', b'GUI FOCUS 2')
                    sende(b'\r', b'GUI ACTION 2 RESULT 0')
                    sende(b'\t', b'GUI FOCUS 3')
                    sende(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(produksjon / 'gui-python.png'), 'format': 'png'})
                    sende(b'q', b'jkoros-native> ')
                    validering_rapport['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Prosess.wait(timeout=10)
            # framebuffer 응답뿐 아니라 faktisk_data scanout 픽셀도 확인한다.
            with skjermbilde_bb19652a.open('rb') as Fil_oppføring:
                assert Fil_oppføring.readline().strip() == b'P6'
                치수 = Fil_oppføring.readline().strip()
                assert 치수 == b'640 480', 치수
                assert Fil_oppføring.readline().strip() == b'255'
                화소들 = Fil_oppføring.read()
            assert len(화소들) == 640 * 480 * 3
            def piksel(x_koordinat, Y_koordinat): return list(화소들[(Y_koordinat * 640 + x_koordinat) * 3:(Y_koordinat * 640 + x_koordinat) * 3 + 3])
            예제들 = {'background': piksel(5, 5), 'panel': piksel(45, 85), 'tile': piksel(65, 115)}
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((speile_rot / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Prosess.poll() is None:
                Prosess.terminate()
                try: Prosess.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Prosess.kill(); Prosess.wait(timeout=5)
            velger.close()
            Prosess.stdin.close(); Prosess.stdout.close()
            (produksjon / 'serial.log').write_bytes(utskrift)
            (produksjon / 'report.json').write_text(json.dumps(validering_rapport, indent=2) + '\n')


if __name__ == '__main__':
    Kjør_2()
