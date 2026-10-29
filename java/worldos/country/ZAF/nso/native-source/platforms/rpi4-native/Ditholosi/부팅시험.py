#!/usr/bin/env python3
"""kgonthe_data raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from phethagatša_taelo import 기준, Taelo


def Diriša():
    출력결과 = 기준 / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    tiišetšo_pego = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Taelo() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        tiišetšo_pego['command'] = 명령인수
        tiragalo_a7054519 = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        sekgethi = selectors.DefaultSelector()
        sekgethi.register(tiragalo_a7054519.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, E_Šetšego_boleng=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[E_Šetšego_boleng:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in sekgethi.select(0.2):
                    data_thibela = 누름값.fileobj.read(4096)
                    if data_thibela:
                        대화기록.extend(data_thibela)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if tiragalo_a7054519.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(tiragalo_a7054519.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 kgonthe_data GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(Bogolo):
                    결과 = b''
                    while len(결과) < Bogolo:
                        조각 = 화면접속자.recv(Bogolo - len(결과))
                        if not 조각: raise AssertionError('VNC disconnected')
                        결과 += 조각
                    return 결과
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                seba_boleng = 정확한값(24)
                assert int.from_bytes(seba_boleng[:2], 'big') == 640 and int.from_bytes(seba_boleng[2:4], 'big') == 480
                정확한값(int.from_bytes(seba_boleng[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for taelo_paete, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                E_Šetšego_boleng = len(대화기록)
                tiragalo_a7054519.stdin.write(taelo_paete + b'\n')
                tiragalo_a7054519.stdin.flush()
                표시까지받기(b'jkoros-native> ', E_Šetšego_boleng)
                assert 확인표시 in 대화기록[E_Šetšego_boleng:], 확인표시
            def šele(mothaladi, 예상결과):
                E_Šetšego_boleng = len(대화기록)
                tiragalo_a7054519.stdin.write(mothaladi.encode('utf-8') + b'\n'); tiragalo_a7054519.stdin.flush()
                표시까지받기(b'jkoros-native> ', E_Šetšego_boleng)
                응답자료 = bytes(대화기록[E_Šetšego_boleng:])
                for Sengwalwa in 예상결과:
                    assert Sengwalwa.encode('utf-8') in 응답자료, (mothaladi, Sengwalwa, 응답자료)
                return 응답자료
            def tsenya_851ea840(mothaladi, temoši):
                E_Šetšego_boleng = len(대화기록)
                tiragalo_a7054519.stdin.write(mothaladi.encode('utf-8') + b'\n'); tiragalo_a7054519.stdin.flush()
                표시까지받기(temoši, E_Šetšego_boleng)
                return bytes(대화기록[E_Šetšego_boleng:])
            def rulaganya_boleng(Leina, Diteng_boleng, Khansela_tiro=False):
                tsenya_851ea840('edit ' + Leina, b'edit> ')
                for mothaladi in Diteng_boleng.splitlines(): tsenya_851ea840(mothaladi, b'edit> ')
                if Khansela_tiro:
                    E_Šetšego_boleng = len(대화기록)
                    tiragalo_a7054519.stdin.write(b'\x03'); tiragalo_a7054519.stdin.flush()
                    표시까지받기(b'jkoros-native> ', E_Šetšego_boleng)
                    assert b'EDIT CANCELLED' in 대화기록[E_Šetšego_boleng:]
                else:
                    assert b'SAVED' in tsenya_851ea840('.', b'jkoros-native> ')
            def apolouto_Difaele(Leina, data):
                assert len(data) <= 16384
                tsenya_851ea840('load ' + Leina, b'hex> ')
                for 순번 in range(0, len(data), 64): tsenya_851ea840(data[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in tsenya_851ea840('.', b'jkoros-native> ')
            def tanelouto(Leina):
                응답자료 = šele('hex ' + Leina, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                data = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(data) == int(일치.group(1)); return data
            šele('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            šele('java -version', ['not OpenJDK', 'exit 0'])
            šele('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            šele('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            šele('python --version', ['MicroPython 1.24.1', 'exit 0'])
            šele('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Faele', 'exit 0'])
            šele('cat python.txt', ['한글 Faele'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(tanelouto('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            rulaganya_boleng('인사.java', 'public class 인사 { public static void main(String[] args) { int boleng = 7; System.out.println("한글=" + boleng); } }')
            šele('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            šele('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(tanelouto('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            rulaganya_boleng('Hello.java', 'broken', Khansela_tiro=True)
            šele('javac Hello.java', ['Compiled:', 'exit 0'])
            rulaganya_boleng('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            šele('javac Broken.java', ['javac error:', 'exit 1'])
            apolouto_Difaele('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            šele('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            šele('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            apolouto_Difaele('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            šele('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            šele('rm Imported.class', [])
            rulaganya_boleng('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            šele('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = šele('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            šele('rm Loop.java', []); šele('rm Loop.class', [])
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
            rulaganya_boleng('checks.py', 파이썬검사)
            šele('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            šele('rm checks.py', [])
            rulaganya_boleng('helper.py', 'value = 321')
            šele("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            šele('rm helper.py', [])
            šele("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            šele("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                šele('python hello.py', ['한글 Faele', 'exit 0'])
                šele('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            apolouto_Difaele('app.elf', (기준 / 'build/user/demo.elf').read_bytes())
            assert tanelouto('app.elf') == (기준 / 'build/user/demo.elf').read_bytes()
            šele('run app.elf', ['EL0 C++', 'exit 0'])
            apolouto_Difaele('app.elf', b'not an ELF')
            šele('run app.elf', ['exit -8'])
            šele('rm app.elf', [])
            šele('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            sethalwa_tsela = 출력결과 / 'java-framebuffer'; sethalwa_tsela.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준 / 'dist/jkoros-native-korean.jar'), '-d', str(sethalwa_tsela), str(기준 / '시험/자바/화면시험.java')])
            apolouto_Difaele('화면시험.class', (sethalwa_tsela / '화면시험.class').read_bytes())
            šele('java 화면시험', ['화면 setsopolwa 거부', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            šele('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as klaente:
                klaente.settimeout(10)
                klaente.connect(str(모의제어경로))
                with klaente.makefile('rwb') as Stream_boleng:
                    인사 = json.loads(Stream_boleng.readline())
                    def 모의제어접속(phethagatša_mošomo, 전달인수=None):
                        Netweke_molaetša = {'execute': phethagatša_mošomo}
                        if 전달인수: Netweke_molaetša['arguments'] = 전달인수
                        Stream_boleng.write((json.dumps(Netweke_molaetša) + '\n').encode())
                        Stream_boleng.flush()
                        while True:
                            fetola = json.loads(Stream_boleng.readline())
                            if 'error' in fetola: raise AssertionError(fetola)
                            if 'return' in fetola: return fetola['return']
                    모의제어접속('qmp_capabilities')
                    pontšhosekerini = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(pontšhosekerini), 'format': 'ppm'})
                    def 예제들(Tsejana, 지점들):
                        with Tsejana.open('rb') as phele_faele:
                            assert phele_faele.readline().strip() == b'P6'
                            assert phele_faele.readline().strip() == b'640 480'
                            assert phele_faele.readline().strip() == b'255'
                            phele_data = phele_faele.read()
                        assert len(phele_data) == 640 * 480 * 3
                        return [list(phele_data[(세로좌표 * 640 + kamano_ya_x) * 3:(세로좌표 * 640 + kamano_ya_x) * 3 + 3]) for kamano_ya_x, 세로좌표 in 지점들]
                    assert 예제들(pontšhosekerini, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(pontšhosekerini, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def Romela(누름값, 확인표시):
                        E_Šetšego_boleng = len(대화기록)
                        tiragalo_a7054519.stdin.write(누름값); tiragalo_a7054519.stdin.flush()
                        표시까지받기(확인표시, E_Šetšego_boleng)
                    Romela(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    Romela(b'\r', b'GUI ACTION 0 RESULT 0')
                    Romela(b'\t', b'GUI FOCUS 1')
                    Romela(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    Romela(b'\t', b'GUI FOCUS 2')
                    Romela(b'\r', b'GUI ACTION 2 RESULT 0')
                    Romela(b'\t', b'GUI FOCUS 3')
                    Romela(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    Romela(b'q', b'jkoros-native> ')
                    tiišetšo_pego['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            tiragalo_a7054519.wait(timeout=10)
            # framebuffer 응답뿐 아니라 kgonthe_data scanout 픽셀도 확인한다.
            with pontšhosekerini.open('rb') as faele_go_tsenya_tshedimošo:
                assert faele_go_tsenya_tshedimošo.readline().strip() == b'P6'
                치수 = faele_go_tsenya_tshedimošo.readline().strip()
                assert 치수 == b'640 480', 치수
                assert faele_go_tsenya_tshedimošo.readline().strip() == b'255'
                화소들 = faele_go_tsenya_tshedimošo.read()
            assert len(화소들) == 640 * 480 * 3
            def phele(kamano_ya_x, 세로좌표): return list(화소들[(세로좌표 * 640 + kamano_ya_x) * 3:(세로좌표 * 640 + kamano_ya_x) * 3 + 3])
            예제들 = {'background': phele(5, 5), 'panel': phele(45, 85), 'tile': phele(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            tiišetšo_pego.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if tiragalo_a7054519.poll() is None:
                tiragalo_a7054519.terminate()
                try: tiragalo_a7054519.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    tiragalo_a7054519.kill(); tiragalo_a7054519.wait(timeout=5)
            sekgethi.close()
            tiragalo_a7054519.stdin.close(); tiragalo_a7054519.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(tiišetšo_pego, indent=2) + '\n')


if __name__ == '__main__':
    Diriša()
