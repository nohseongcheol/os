#!/usr/bin/env python3
"""raun_gögn raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from keyra_skipun import verk_rót, Skipun


def Keyra_2():
    úttak_54cd5e1d = verk_rót / 'build/verification'
    úttak_54cd5e1d.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    prófun_skrá = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Skipun() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        prófun_skrá['command'] = 명령인수
        Ferli = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        val = selectors.DefaultSelector()
        val.register(Ferli.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, OFFSET_VALUE=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[OFFSET_VALUE:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in val.select(0.2):
                    gögn_útiloka = 누름값.fileobj.read(4096)
                    if gögn_útiloka:
                        대화기록.extend(gögn_útiloka)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if Ferli.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Ferli.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 raun_gögn GUI를 볼 númer 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def EXACT_VALUE(Stærð):
                    NIÐURSTAÐA = b''
                    while len(NIÐURSTAÐA) < Stærð:
                        조각 = 화면접속자.recv(Stærð - len(NIÐURSTAÐA))
                        if not 조각: raise AssertionError('VNC disconnected')
                        NIÐURSTAÐA += 조각
                    return NIÐURSTAÐA
                assert EXACT_VALUE(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in EXACT_VALUE(EXACT_VALUE(1)[0]); 화면접속자.sendall(b'\x01')
                assert EXACT_VALUE(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                þjónn_VALUE = EXACT_VALUE(24)
                assert int.from_bytes(þjónn_VALUE[:2], 'big') == 640 and int.from_bytes(þjónn_VALUE[2:4], 'big') == 480
                EXACT_VALUE(int.from_bytes(þjónn_VALUE[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for skipun_bæti, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                OFFSET_VALUE = len(대화기록)
                Ferli.stdin.write(skipun_bæti + b'\n')
                Ferli.stdin.flush()
                표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                assert 확인표시 in 대화기록[OFFSET_VALUE:], 확인표시
            def skel(Lína, 예상결과):
                OFFSET_VALUE = len(대화기록)
                Ferli.stdin.write(Lína.encode('utf-8') + b'\n'); Ferli.stdin.flush()
                표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                응답자료 = bytes(대화기록[OFFSET_VALUE:])
                for Texti in 예상결과:
                    assert Texti.encode('utf-8') in 응답자료, (Lína, Texti, 응답자료)
                return 응답자료
            def slá_inn(Lína, biðja):
                OFFSET_VALUE = len(대화기록)
                Ferli.stdin.write(Lína.encode('utf-8') + b'\n'); Ferli.stdin.flush()
                표시까지받기(biðja, OFFSET_VALUE)
                return bytes(대화기록[OFFSET_VALUE:])
            def breyta_VALUE(Heiti, Efni_VALUE, Hætta_við_aðgerð=False):
                slá_inn('edit ' + Heiti, b'edit> ')
                for Lína in Efni_VALUE.splitlines(): slá_inn(Lína, b'edit> ')
                if Hætta_við_aðgerð:
                    OFFSET_VALUE = len(대화기록)
                    Ferli.stdin.write(b'\x03'); Ferli.stdin.flush()
                    표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                    assert b'EDIT CANCELLED' in 대화기록[OFFSET_VALUE:]
                else:
                    assert b'SAVED' in slá_inn('.', b'jkoros-native> ')
            def hlaða_upp_Skrár(Heiti, gögn):
                assert len(gögn) <= 16384
                slá_inn('load ' + Heiti, b'hex> ')
                for 순번 in range(0, len(gögn), 64): slá_inn(gögn[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in slá_inn('.', b'jkoros-native> ')
            def sækja(Heiti):
                응답자료 = skel('hex ' + Heiti, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                gögn = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(gögn) == int(일치.group(1)); return gögn
            skel('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            skel('java -version', ['not OpenJDK', 'exit 0'])
            skel('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            skel('java Hello "한글 Viðföng 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Viðföng 😀', 'exit 0'])
            skel('python --version', ['MicroPython 1.24.1', 'exit 0'])
            skel('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Skrá', 'exit 0'])
            skel('cat python.txt', ['한글 Skrá'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = úttak_54cd5e1d / 'Hello.class'; 자바클래스.write_bytes(sækja('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(úttak_54cd5e1d), 'Hello', '한글 Viðföng 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Viðföng 😀'], 예상결과
            breyta_VALUE('인사.java', 'public class 인사 { public static void main(String[] args) { int VALUE = 7; System.out.println("한글=" + VALUE); } }')
            skel('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            skel('java 인사', ['한글=7', 'exit 0'])
            (úttak_54cd5e1d / '인사.class').write_bytes(sækja('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(úttak_54cd5e1d), '인사']).decode().strip() == '한글=7'
            breyta_VALUE('Hello.java', 'broken', Hætta_við_aðgerð=True)
            skel('javac Hello.java', ['Compiled:', 'exit 0'])
            breyta_VALUE('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            skel('javac Broken.java', ['javac error:', 'exit 1'])
            hlaða_upp_Skrár('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            skel('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            skel('rm Broken.java', [])
            들여온파일 = úttak_54cd5e1d / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            hlaða_upp_Skrár('Imported.class', (úttak_54cd5e1d / 'Imported.class').read_bytes())
            skel('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            skel('rm Imported.class', [])
            breyta_VALUE('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            skel('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = skel('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            skel('rm Loop.java', []); skel('rm Loop.class', [])
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
            breyta_VALUE('checks.py', 파이썬검사)
            skel('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            skel('rm checks.py', [])
            breyta_VALUE('helper.py', 'value = 321')
            skel("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            skel('rm helper.py', [])
            skel("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            skel("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                skel('python hello.py', ['한글 Skrá', 'exit 0'])
                skel('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            hlaða_upp_Skrár('app.elf', (verk_rót / 'build/user/demo.elf').read_bytes())
            assert sækja('app.elf') == (verk_rót / 'build/user/demo.elf').read_bytes()
            skel('run app.elf', ['EL0 C++', 'exit 0'])
            hlaða_upp_Skrár('app.elf', b'not an ELF')
            skel('run app.elf', ['exit -8'])
            skel('rm app.elf', [])
            skel('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            teikning_slóð = úttak_54cd5e1d / 'java-framebuffer'; teikning_slóð.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(verk_rót / 'dist/jkoros-native-korean.jar'), '-d', str(teikning_slóð), str(verk_rót / '시험/자바/화면시험.java')])
            hlaða_upp_Skrár('화면시험.class', (teikning_slóð / '화면시험.class').read_bytes())
            skel('java 화면시험', ['화면 miðlaskrá hafna_VALUE', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            skel('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as biðlari:
                biðlari.settimeout(10)
                biðlari.connect(str(모의제어경로))
                with biðlari.makefile('rwb') as Stream_VALUE:
                    인사 = json.loads(Stream_VALUE.readline())
                    def 모의제어접속(Keyra, 전달인수=None):
                        Net_skeyti = {'execute': Keyra}
                        if 전달인수: Net_skeyti['arguments'] = 전달인수
                        Stream_VALUE.write((json.dumps(Net_skeyti) + '\n').encode())
                        Stream_VALUE.flush()
                        while True:
                            svara = json.loads(Stream_VALUE.readline())
                            if 'error' in svara: raise AssertionError(svara)
                            if 'return' in svara: return svara['return']
                    모의제어접속('qmp_capabilities')
                    skjámynd = úttak_54cd5e1d / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(skjámynd), 'format': 'ppm'})
                    def 예제들(SLÓÐ, 지점들):
                        with SLÓÐ.open('rb') as díll_skrá:
                            assert díll_skrá.readline().strip() == b'P6'
                            assert díll_skrá.readline().strip() == b'640 480'
                            assert díll_skrá.readline().strip() == b'255'
                            díll_gögn = díll_skrá.read()
                        assert len(díll_gögn) == 640 * 480 * 3
                        return [list(díll_gögn[(Y_hnit * 640 + x_hnit) * 3:(Y_hnit * 640 + x_hnit) * 3 + 3]) for x_hnit, Y_hnit in 지점들]
                    assert 예제들(skjámynd, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(skjámynd, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def senda(누름값, 확인표시):
                        OFFSET_VALUE = len(대화기록)
                        Ferli.stdin.write(누름값); Ferli.stdin.flush()
                        표시까지받기(확인표시, OFFSET_VALUE)
                    senda(b'gui\n', b'GUI READY:')
                    첫화면 = úttak_54cd5e1d / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(úttak_54cd5e1d / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    senda(b'\r', b'GUI ACTION 0 RESULT 0')
                    senda(b'\t', b'GUI FOCUS 1')
                    senda(b'\r', b'GUI ACTION 1 RESULT 0')
                    SECOND_GUI = úttak_54cd5e1d / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SECOND_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(úttak_54cd5e1d / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SECOND_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    senda(b'\t', b'GUI FOCUS 2')
                    senda(b'\r', b'GUI ACTION 2 RESULT 0')
                    senda(b'\t', b'GUI FOCUS 3')
                    senda(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(úttak_54cd5e1d / 'gui-python.png'), 'format': 'png'})
                    senda(b'q', b'jkoros-native> ')
                    prófun_skrá['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Ferli.wait(timeout=10)
            # framebuffer 응답뿐 아니라 raun_gögn scanout 픽셀도 확인한다.
            with skjámynd.open('rb') as skrá_færsla_3d0c1245:
                assert skrá_færsla_3d0c1245.readline().strip() == b'P6'
                치수 = skrá_færsla_3d0c1245.readline().strip()
                assert 치수 == b'640 480', 치수
                assert skrá_færsla_3d0c1245.readline().strip() == b'255'
                화소들 = skrá_færsla_3d0c1245.read()
            assert len(화소들) == 640 * 480 * 3
            def díll(x_hnit, Y_hnit): return list(화소들[(Y_hnit * 640 + x_hnit) * 3:(Y_hnit * 640 + x_hnit) * 3 + 3])
            예제들 = {'background': díll(5, 5), 'panel': díll(45, 85), 'tile': díll(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            prófun_skrá.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((verk_rót / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Ferli.poll() is None:
                Ferli.terminate()
                try: Ferli.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Ferli.kill(); Ferli.wait(timeout=5)
            val.close()
            Ferli.stdin.close(); Ferli.stdout.close()
            (úttak_54cd5e1d / 'serial.log').write_bytes(대화기록)
            (úttak_54cd5e1d / 'report.json').write_text(json.dumps(prófun_skrá, indent=2) + '\n')


if __name__ == '__main__':
    Keyra_2()
