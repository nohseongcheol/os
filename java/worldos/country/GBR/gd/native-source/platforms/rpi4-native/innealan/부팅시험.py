#!/usr/bin/env python3
"""dearbh_dàta raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from gnìomhaich_àithne import tilg_freumh, àithne


def ruith():
    출력결과 = tilg_freumh / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    dearbhadh_aithisg = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = àithne() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        dearbhadh_aithisg['command'] = 명령인수
        Pròiseas = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        roghnaichear = selectors.DefaultSelector()
        roghnaichear.register(Pròiseas.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, OFFSET_VALUE=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[OFFSET_VALUE:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in roghnaichear.select(0.2):
                    dàta_bac = 누름값.fileobj.read(4096)
                    if dàta_bac:
                        대화기록.extend(dàta_bac)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if Pròiseas.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Pròiseas.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 dearbh_dàta GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def EXACT_VALUE(atharraich_am_meud):
                    tomhas = b''
                    while len(tomhas) < atharraich_am_meud:
                        조각 = 화면접속자.recv(atharraich_am_meud - len(tomhas))
                        if not 조각: raise AssertionError('VNC disconnected')
                        tomhas += 조각
                    return tomhas
                assert EXACT_VALUE(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in EXACT_VALUE(EXACT_VALUE(1)[0]); 화면접속자.sendall(b'\x01')
                assert EXACT_VALUE(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                frithealaiche_VALUE = EXACT_VALUE(24)
                assert int.from_bytes(frithealaiche_VALUE[:2], 'big') == 640 and int.from_bytes(frithealaiche_VALUE[2:4], 'big') == 480
                EXACT_VALUE(int.from_bytes(frithealaiche_VALUE[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for àithne_baidht, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                OFFSET_VALUE = len(대화기록)
                Pròiseas.stdin.write(àithne_baidht + b'\n')
                Pròiseas.stdin.flush()
                표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                assert 확인표시 in 대화기록[OFFSET_VALUE:], 확인표시
            def slige(loidhne, 예상결과):
                OFFSET_VALUE = len(대화기록)
                Pròiseas.stdin.write(loidhne.encode('utf-8') + b'\n'); Pròiseas.stdin.flush()
                표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                응답자료 = bytes(대화기록[OFFSET_VALUE:])
                for SMS in 예상결과:
                    assert SMS.encode('utf-8') in 응답자료, (loidhne, SMS, 응답자료)
                return 응답자료
            def cuir_a_steach_851ea840(loidhne, brodadh):
                OFFSET_VALUE = len(대화기록)
                Pròiseas.stdin.write(loidhne.encode('utf-8') + b'\n'); Pròiseas.stdin.flush()
                표시까지받기(brodadh, OFFSET_VALUE)
                return bytes(대화기록[OFFSET_VALUE:])
            def deasaich_VALUE(Ainm, susbaint_VALUE, dì_thagh_obrachadh=False):
                cuir_a_steach_851ea840('edit ' + Ainm, b'edit> ')
                for loidhne in susbaint_VALUE.splitlines(): cuir_a_steach_851ea840(loidhne, b'edit> ')
                if dì_thagh_obrachadh:
                    OFFSET_VALUE = len(대화기록)
                    Pròiseas.stdin.write(b'\x03'); Pròiseas.stdin.flush()
                    표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                    assert b'EDIT CANCELLED' in 대화기록[OFFSET_VALUE:]
                else:
                    assert b'SAVED' in cuir_a_steach_851ea840('.', b'jkoros-native> ')
            def luchdaich_suas_faidhlichean(Ainm, dàta):
                assert len(dàta) <= 16384
                cuir_a_steach_851ea840('load ' + Ainm, b'hex> ')
                for 순번 in range(0, len(dàta), 64): cuir_a_steach_851ea840(dàta[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in cuir_a_steach_851ea840('.', b'jkoros-native> ')
            def luchdadh_a_nuas(Ainm):
                응답자료 = slige('hex ' + Ainm, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                dàta = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(dàta) == int(일치.group(1)); return dàta
            slige('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            slige('java -version', ['not OpenJDK', 'exit 0'])
            slige('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            slige('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            slige('python --version', ['MicroPython 1.24.1', 'exit 0'])
            slige('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 faidhle', 'exit 0'])
            slige('cat python.txt', ['한글 faidhle'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(luchdadh_a_nuas('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            deasaich_VALUE('인사.java', 'public class 인사 { public static void main(String[] args) { int VALUE = 7; System.out.println("한글=" + VALUE); } }')
            slige('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            slige('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(luchdadh_a_nuas('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            deasaich_VALUE('Hello.java', 'broken', dì_thagh_obrachadh=True)
            slige('javac Hello.java', ['Compiled:', 'exit 0'])
            deasaich_VALUE('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            slige('javac Broken.java', ['javac error:', 'exit 1'])
            luchdaich_suas_faidhlichean('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            slige('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            slige('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            luchdaich_suas_faidhlichean('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            slige('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            slige('rm Imported.class', [])
            deasaich_VALUE('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            slige('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = slige('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            slige('rm Loop.java', []); slige('rm Loop.class', [])
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
            deasaich_VALUE('checks.py', 파이썬검사)
            slige('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            slige('rm checks.py', [])
            deasaich_VALUE('helper.py', 'value = 321')
            slige("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            slige('rm helper.py', [])
            slige("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            slige("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                slige('python hello.py', ['한글 faidhle', 'exit 0'])
                slige('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            luchdaich_suas_faidhlichean('app.elf', (tilg_freumh / 'build/user/demo.elf').read_bytes())
            assert luchdadh_a_nuas('app.elf') == (tilg_freumh / 'build/user/demo.elf').read_bytes()
            slige('run app.elf', ['EL0 C++', 'exit 0'])
            luchdaich_suas_faidhlichean('app.elf', b'not an ELF')
            slige('run app.elf', ['exit -8'])
            slige('rm app.elf', [])
            slige('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            tarraing_slighe = 출력결과 / 'java-framebuffer'; tarraing_slighe.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(tilg_freumh / 'dist/jkoros-native-korean.jar'), '-d', str(tarraing_slighe), str(tilg_freumh / '시험/자바/화면시험.java')])
            luchdaich_suas_faidhlichean('화면시험.class', (tarraing_slighe / '화면시험.class').read_bytes())
            slige('java 화면시험', ['화면 cliop 거부', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            slige('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as cliant:
                cliant.settimeout(10)
                cliant.connect(str(모의제어경로))
                with cliant.makefile('rwb') as sruth_VALUE:
                    인사 = json.loads(sruth_VALUE.readline())
                    def 모의제어접속(Ruith, 전달인수=None):
                        lìonra_teachdaireachd = {'execute': Ruith}
                        if 전달인수: lìonra_teachdaireachd['arguments'] = 전달인수
                        sruth_VALUE.write((json.dumps(lìonra_teachdaireachd) + '\n').encode())
                        sruth_VALUE.flush()
                        while True:
                            freagair = json.loads(sruth_VALUE.readline())
                            if 'error' in freagair: raise AssertionError(freagair)
                            if 'return' in freagair: return freagair['return']
                    모의제어접속('qmp_capabilities')
                    bearradh_sgrìn = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(bearradh_sgrìn), 'format': 'ppm'})
                    def 예제들(Slighe, 지점들):
                        with Slighe.open('rb') as pel_faidhle:
                            assert pel_faidhle.readline().strip() == b'P6'
                            assert pel_faidhle.readline().strip() == b'640 480'
                            assert pel_faidhle.readline().strip() == b'255'
                            pel_dàta = pel_faidhle.read()
                        assert len(pel_dàta) == 640 * 480 * 3
                        return [list(pel_dàta[(세로좌표 * 640 + co_chomharra_x) * 3:(세로좌표 * 640 + co_chomharra_x) * 3 + 3]) for co_chomharra_x, 세로좌표 in 지점들]
                    assert 예제들(bearradh_sgrìn, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(bearradh_sgrìn, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def cuir(누름값, 확인표시):
                        OFFSET_VALUE = len(대화기록)
                        Pròiseas.stdin.write(누름값); Pròiseas.stdin.flush()
                        표시까지받기(확인표시, OFFSET_VALUE)
                    cuir(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    cuir(b'\r', b'GUI ACTION 0 RESULT 0')
                    cuir(b'\t', b'GUI FOCUS 1')
                    cuir(b'\r', b'GUI ACTION 1 RESULT 0')
                    SECOND_GUI = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SECOND_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SECOND_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    cuir(b'\t', b'GUI FOCUS 2')
                    cuir(b'\r', b'GUI ACTION 2 RESULT 0')
                    cuir(b'\t', b'GUI FOCUS 3')
                    cuir(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    cuir(b'q', b'jkoros-native> ')
                    dearbhadh_aithisg['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Pròiseas.wait(timeout=10)
            # framebuffer 응답뿐 아니라 dearbh_dàta scanout 픽셀도 확인한다.
            with bearradh_sgrìn.open('rb') as faidhle_cur_a_steach:
                assert faidhle_cur_a_steach.readline().strip() == b'P6'
                치수 = faidhle_cur_a_steach.readline().strip()
                assert 치수 == b'640 480', 치수
                assert faidhle_cur_a_steach.readline().strip() == b'255'
                화소들 = faidhle_cur_a_steach.read()
            assert len(화소들) == 640 * 480 * 3
            def pel(co_chomharra_x, 세로좌표): return list(화소들[(세로좌표 * 640 + co_chomharra_x) * 3:(세로좌표 * 640 + co_chomharra_x) * 3 + 3])
            예제들 = {'background': pel(5, 5), 'panel': pel(45, 85), 'tile': pel(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            dearbhadh_aithisg.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((tilg_freumh / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Pròiseas.poll() is None:
                Pròiseas.terminate()
                try: Pròiseas.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Pròiseas.kill(); Pròiseas.wait(timeout=5)
            roghnaichear.close()
            Pròiseas.stdin.close(); Pròiseas.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(dearbhadh_aithisg, indent=2) + '\n')


if __name__ == '__main__':
    ruith()
