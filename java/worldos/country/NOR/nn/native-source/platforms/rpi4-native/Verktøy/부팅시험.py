#!/usr/bin/env python3
"""faktisk_data raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from Utfør_kommando import spegle_rot, Kommando


def Køyr_2():
    출력결과 = spegle_rot / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    validering_rapport = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Kommando() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        validering_rapport['command'] = 명령인수
        Prosess = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        veljar = selectors.DefaultSelector()
        veljar.register(Prosess.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, OFFSET_VALUE=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[OFFSET_VALUE:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in veljar.select(0.2):
                    data_Blokker = 누름값.fileobj.read(4096)
                    if data_Blokker:
                        대화기록.extend(data_Blokker)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if Prosess.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Prosess.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 betalt_vare 호스트에서도 VNC로 faktisk_data GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def EXACT_VALUE(Storleik):
                    forretningsmål = b''
                    while len(forretningsmål) < Storleik:
                        조각 = 화면접속자.recv(Storleik - len(forretningsmål))
                        if not 조각: raise AssertionError('VNC disconnected')
                        forretningsmål += 조각
                    return forretningsmål
                assert EXACT_VALUE(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in EXACT_VALUE(EXACT_VALUE(1)[0]); 화면접속자.sendall(b'\x01')
                assert EXACT_VALUE(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                tenar_VALUE = EXACT_VALUE(24)
                assert int.from_bytes(tenar_VALUE[:2], 'big') == 640 and int.from_bytes(tenar_VALUE[2:4], 'big') == 480
                EXACT_VALUE(int.from_bytes(tenar_VALUE[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for kommando_byte, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                OFFSET_VALUE = len(대화기록)
                Prosess.stdin.write(kommando_byte + b'\n')
                Prosess.stdin.flush()
                표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                assert 확인표시 in 대화기록[OFFSET_VALUE:], 확인표시
            def grensesnitt(linje, 예상결과):
                OFFSET_VALUE = len(대화기록)
                Prosess.stdin.write(linje.encode('utf-8') + b'\n'); Prosess.stdin.flush()
                표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                응답자료 = bytes(대화기록[OFFSET_VALUE:])
                for Tekst in 예상결과:
                    assert Tekst.encode('utf-8') in 응답자료, (linje, Tekst, 응답자료)
                return 응답자료
            def skrive_inn(linje, spørsmål):
                OFFSET_VALUE = len(대화기록)
                Prosess.stdin.write(linje.encode('utf-8') + b'\n'); Prosess.stdin.flush()
                표시까지받기(spørsmål, OFFSET_VALUE)
                return bytes(대화기록[OFFSET_VALUE:])
            def redigere_VALUE(Namn, Innhald_VALUE, Avbryt_operasjon=False):
                skrive_inn('edit ' + Namn, b'edit> ')
                for linje in Innhald_VALUE.splitlines(): skrive_inn(linje, b'edit> ')
                if Avbryt_operasjon:
                    OFFSET_VALUE = len(대화기록)
                    Prosess.stdin.write(b'\x03'); Prosess.stdin.flush()
                    표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                    assert b'EDIT CANCELLED' in 대화기록[OFFSET_VALUE:]
                else:
                    assert b'SAVED' in skrive_inn('.', b'jkoros-native> ')
            def Upload_Filer(Namn, data):
                assert len(data) <= 16384
                skrive_inn('load ' + Namn, b'hex> ')
                for 순번 in range(0, len(data), 64): skrive_inn(data[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in skrive_inn('.', b'jkoros-native> ')
            def laste_ned(Namn):
                응답자료 = grensesnitt('hex ' + Namn, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                data = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(data) == int(일치.group(1)); return data
            grensesnitt('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            grensesnitt('java -version', ['not OpenJDK', 'exit 0'])
            grensesnitt('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            grensesnitt('java Hello "한글 Argument 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Argument 😀', 'exit 0'])
            grensesnitt('python --version', ['MicroPython 1.24.1', 'exit 0'])
            grensesnitt('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Fil', 'exit 0'])
            grensesnitt('cat python.txt', ['한글 Fil'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(laste_ned('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 Argument 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Argument 😀'], 예상결과
            redigere_VALUE('인사.java', 'public class 인사 { public static void main(String[] args) { int VALUE = 7; System.out.println("한글=" + VALUE); } }')
            grensesnitt('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            grensesnitt('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(laste_ned('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            redigere_VALUE('Hello.java', 'broken', Avbryt_operasjon=True)
            grensesnitt('javac Hello.java', ['Compiled:', 'exit 0'])
            redigere_VALUE('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            grensesnitt('javac Broken.java', ['javac error:', 'exit 1'])
            Upload_Filer('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            grensesnitt('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            grensesnitt('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Upload_Filer('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            grensesnitt('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            grensesnitt('rm Imported.class', [])
            redigere_VALUE('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            grensesnitt('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = grensesnitt('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            grensesnitt('rm Loop.java', []); grensesnitt('rm Loop.class', [])
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
            redigere_VALUE('checks.py', 파이썬검사)
            grensesnitt('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            grensesnitt('rm checks.py', [])
            redigere_VALUE('helper.py', 'value = 321')
            grensesnitt("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            grensesnitt('rm helper.py', [])
            grensesnitt("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            grensesnitt("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                grensesnitt('python hello.py', ['한글 Fil', 'exit 0'])
                grensesnitt('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Upload_Filer('app.elf', (spegle_rot / 'build/user/demo.elf').read_bytes())
            assert laste_ned('app.elf') == (spegle_rot / 'build/user/demo.elf').read_bytes()
            grensesnitt('run app.elf', ['EL0 C++', 'exit 0'])
            Upload_Filer('app.elf', b'not an ELF')
            grensesnitt('run app.elf', ['exit -8'])
            grensesnitt('rm app.elf', [])
            grensesnitt('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            teikning_bane = 출력결과 / 'java-framebuffer'; teikning_bane.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(spegle_rot / 'dist/jkoros-native-korean.jar'), '-d', str(teikning_bane), str(spegle_rot / '시험/자바/화면시험.java')])
            Upload_Filer('화면시험.class', (teikning_bane / '화면시험.class').read_bytes())
            grensesnitt('java 화면시험', ['화면 klipp avvise_VALUE', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            grensesnitt('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as klient:
                klient.settimeout(10)
                klient.connect(str(모의제어경로))
                with klient.makefile('rwb') as Stream_VALUE:
                    인사 = json.loads(Stream_VALUE.readline())
                    def 모의제어접속(Køyr, 전달인수=None):
                        Nettverk_melding = {'execute': Køyr}
                        if 전달인수: Nettverk_melding['arguments'] = 전달인수
                        Stream_VALUE.write((json.dumps(Nettverk_melding) + '\n').encode())
                        Stream_VALUE.flush()
                        while True:
                            svare = json.loads(Stream_VALUE.readline())
                            if 'error' in svare: raise AssertionError(svare)
                            if 'return' in svare: return svare['return']
                    모의제어접속('qmp_capabilities')
                    skjermbilete = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(skjermbilete), 'format': 'ppm'})
                    def 예제들(STIGE, 지점들):
                        with STIGE.open('rb') as piksel_fil:
                            assert piksel_fil.readline().strip() == b'P6'
                            assert piksel_fil.readline().strip() == b'640 480'
                            assert piksel_fil.readline().strip() == b'255'
                            piksel_data = piksel_fil.read()
                        assert len(piksel_data) == 640 * 480 * 3
                        return [list(piksel_data[(Y_koordinat * 640 + x_koordinat) * 3:(Y_koordinat * 640 + x_koordinat) * 3 + 3]) for x_koordinat, Y_koordinat in 지점들]
                    assert 예제들(skjermbilete, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(skjermbilete, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def sende(누름값, 확인표시):
                        OFFSET_VALUE = len(대화기록)
                        Prosess.stdin.write(누름값); Prosess.stdin.flush()
                        표시까지받기(확인표시, OFFSET_VALUE)
                    sende(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    sende(b'\r', b'GUI ACTION 0 RESULT 0')
                    sende(b'\t', b'GUI FOCUS 1')
                    sende(b'\r', b'GUI ACTION 1 RESULT 0')
                    SECOND_GUI = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SECOND_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SECOND_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    sende(b'\t', b'GUI FOCUS 2')
                    sende(b'\r', b'GUI ACTION 2 RESULT 0')
                    sende(b'\t', b'GUI FOCUS 3')
                    sende(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    sende(b'q', b'jkoros-native> ')
                    validering_rapport['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Prosess.wait(timeout=10)
            # framebuffer 응답뿐 아니라 faktisk_data scanout 픽셀도 확인한다.
            with skjermbilete.open('rb') as fil_oppføring:
                assert fil_oppføring.readline().strip() == b'P6'
                치수 = fil_oppføring.readline().strip()
                assert 치수 == b'640 480', 치수
                assert fil_oppføring.readline().strip() == b'255'
                화소들 = fil_oppføring.read()
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((spegle_rot / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Prosess.poll() is None:
                Prosess.terminate()
                try: Prosess.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Prosess.kill(); Prosess.wait(timeout=5)
            veljar.close()
            Prosess.stdin.close(); Prosess.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(validering_rapport, indent=2) + '\n')


if __name__ == '__main__':
    Køyr_2()
