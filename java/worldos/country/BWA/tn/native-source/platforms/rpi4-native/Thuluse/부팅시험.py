#!/usr/bin/env python3
"""tota_tshedimosetso raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from diragatsa_Taelo import 기준, Taelo


def dirisa():
    출력결과 = 기준 / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    netefatso_pego = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Taelo() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        netefatso_pego['command'] = 명령인수
        Thulaganyo = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        setlhophi = selectors.DefaultSelector()
        setlhophi.register(Thulaganyo.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, Baya_ka_Tekatekanyo_Boleng=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[Baya_ka_Tekatekanyo_Boleng:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in setlhophi.select(0.2):
                    tshedimosetso_thibela = 누름값.fileobj.read(4096)
                    if tshedimosetso_thibela:
                        대화기록.extend(tshedimosetso_thibela)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if Thulaganyo.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Thulaganyo.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 ga_jaana_selwana 호스트에서도 VNC로 tota_tshedimosetso GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(lekanya):
                    결과 = b''
                    while len(결과) < lekanya:
                        조각 = 화면접속자.recv(lekanya - len(결과))
                        if not 조각: raise AssertionError('VNC disconnected')
                        결과 += 조각
                    return 결과
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                sefara_Boleng = 정확한값(24)
                assert int.from_bytes(sefara_Boleng[:2], 'big') == 640 and int.from_bytes(sefara_Boleng[2:4], 'big') == 480
                정확한값(int.from_bytes(sefara_Boleng[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for Taelo_baete, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                Baya_ka_Tekatekanyo_Boleng = len(대화기록)
                Thulaganyo.stdin.write(Taelo_baete + b'\n')
                Thulaganyo.stdin.flush()
                표시까지받기(b'jkoros-native> ', Baya_ka_Tekatekanyo_Boleng)
                assert 확인표시 in 대화기록[Baya_ka_Tekatekanyo_Boleng:], 확인표시
            def setlhalosataelo(Mola, 예상결과):
                Baya_ka_Tekatekanyo_Boleng = len(대화기록)
                Thulaganyo.stdin.write(Mola.encode('utf-8') + b'\n'); Thulaganyo.stdin.flush()
                표시까지받기(b'jkoros-native> ', Baya_ka_Tekatekanyo_Boleng)
                응답자료 = bytes(대화기록[Baya_ka_Tekatekanyo_Boleng:])
                for SMS in 예상결과:
                    assert SMS.encode('utf-8') in 응답자료, (Mola, SMS, 응답자료)
                return 응답자료
            def kwadisa(Mola, kgwetlho):
                Baya_ka_Tekatekanyo_Boleng = len(대화기록)
                Thulaganyo.stdin.write(Mola.encode('utf-8') + b'\n'); Thulaganyo.stdin.flush()
                표시까지받기(kgwetlho, Baya_ka_Tekatekanyo_Boleng)
                return bytes(대화기록[Baya_ka_Tekatekanyo_Boleng:])
            def Tseleganya_Boleng(leina, Diteng_Boleng, khansela_tiro=False):
                kwadisa('edit ' + leina, b'edit> ')
                for Mola in Diteng_Boleng.splitlines(): kwadisa(Mola, b'edit> ')
                if khansela_tiro:
                    Baya_ka_Tekatekanyo_Boleng = len(대화기록)
                    Thulaganyo.stdin.write(b'\x03'); Thulaganyo.stdin.flush()
                    표시까지받기(b'jkoros-native> ', Baya_ka_Tekatekanyo_Boleng)
                    assert b'EDIT CANCELLED' in 대화기록[Baya_ka_Tekatekanyo_Boleng:]
                else:
                    assert b'SAVED' in kwadisa('.', b'jkoros-native> ')
            def laisa_Difaele(leina, tshedimosetso):
                assert len(tshedimosetso) <= 16384
                kwadisa('load ' + leina, b'hex> ')
                for 순번 in range(0, len(tshedimosetso), 64): kwadisa(tshedimosetso[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in kwadisa('.', b'jkoros-native> ')
            def laisolola(leina):
                응답자료 = setlhalosataelo('hex ' + leina, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                tshedimosetso = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(tshedimosetso) == int(일치.group(1)); return tshedimosetso
            setlhalosataelo('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            setlhalosataelo('java -version', ['not OpenJDK', 'exit 0'])
            setlhalosataelo('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            setlhalosataelo('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            setlhalosataelo('python --version', ['MicroPython 1.24.1', 'exit 0'])
            setlhalosataelo('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 faele', 'exit 0'])
            setlhalosataelo('cat python.txt', ['한글 faele'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(laisolola('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            Tseleganya_Boleng('인사.java', 'public class 인사 { public static void main(String[] args) { int Boleng = 7; System.out.println("한글=" + Boleng); } }')
            setlhalosataelo('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            setlhalosataelo('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(laisolola('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            Tseleganya_Boleng('Hello.java', 'broken', khansela_tiro=True)
            setlhalosataelo('javac Hello.java', ['Compiled:', 'exit 0'])
            Tseleganya_Boleng('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            setlhalosataelo('javac Broken.java', ['javac error:', 'exit 1'])
            laisa_Difaele('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            setlhalosataelo('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            setlhalosataelo('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            laisa_Difaele('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            setlhalosataelo('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            setlhalosataelo('rm Imported.class', [])
            Tseleganya_Boleng('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            setlhalosataelo('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = setlhalosataelo('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            setlhalosataelo('rm Loop.java', []); setlhalosataelo('rm Loop.class', [])
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
            Tseleganya_Boleng('checks.py', 파이썬검사)
            setlhalosataelo('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            setlhalosataelo('rm checks.py', [])
            Tseleganya_Boleng('helper.py', 'value = 321')
            setlhalosataelo("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            setlhalosataelo('rm helper.py', [])
            setlhalosataelo("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            setlhalosataelo("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                setlhalosataelo('python hello.py', ['한글 faele', 'exit 0'])
                setlhalosataelo('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            laisa_Difaele('app.elf', (기준 / 'build/user/demo.elf').read_bytes())
            assert laisolola('app.elf') == (기준 / 'build/user/demo.elf').read_bytes()
            setlhalosataelo('run app.elf', ['EL0 C++', 'exit 0'])
            laisa_Difaele('app.elf', b'not an ELF')
            setlhalosataelo('run app.elf', ['exit -8'])
            setlhalosataelo('rm app.elf', [])
            setlhalosataelo('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            sethalo_tsela = 출력결과 / 'java-framebuffer'; sethalo_tsela.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준 / 'dist/jkoros-native-korean.jar'), '-d', str(sethalo_tsela), str(기준 / '시험/자바/화면시험.java')])
            laisa_Difaele('화면시험.class', (sethalo_tsela / '화면시험.class').read_bytes())
            setlhalosataelo('java 화면시험', ['화면 faelekhutshwe_ya_media 거부', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            setlhalosataelo('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as sedirelwa:
                sedirelwa.settimeout(10)
                sedirelwa.connect(str(모의제어경로))
                with sedirelwa.makefile('rwb') as moela_Boleng:
                    인사 = json.loads(moela_Boleng.readline())
                    def 모의제어접속(diragatsa_Tiro, 전달인수=None):
                        Neteweke_molaetsa = {'execute': diragatsa_Tiro}
                        if 전달인수: Neteweke_molaetsa['arguments'] = 전달인수
                        moela_Boleng.write((json.dumps(Neteweke_molaetsa) + '\n').encode())
                        moela_Boleng.flush()
                        while True:
                            araba = json.loads(moela_Boleng.readline())
                            if 'error' in araba: raise AssertionError(araba)
                            if 'return' in araba: return araba['return']
                    모의제어접속('qmp_capabilities')
                    pontsho_ya_sekerine = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(pontsho_ya_sekerine), 'format': 'ppm'})
                    def 예제들(tsela, 지점들):
                        with tsela.open('rb') as phele_faele:
                            assert phele_faele.readline().strip() == b'P6'
                            assert phele_faele.readline().strip() == b'640 480'
                            assert phele_faele.readline().strip() == b'255'
                            phele_tshedimosetso = phele_faele.read()
                        assert len(phele_tshedimosetso) == 640 * 480 * 3
                        return [list(phele_tshedimosetso[(세로좌표 * 640 + kgokagano_ya_x) * 3:(세로좌표 * 640 + kgokagano_ya_x) * 3 + 3]) for kgokagano_ya_x, 세로좌표 in 지점들]
                    assert 예제들(pontsho_ya_sekerine, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(pontsho_ya_sekerine, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def romela(누름값, 확인표시):
                        Baya_ka_Tekatekanyo_Boleng = len(대화기록)
                        Thulaganyo.stdin.write(누름값); Thulaganyo.stdin.flush()
                        표시까지받기(확인표시, Baya_ka_Tekatekanyo_Boleng)
                    romela(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    romela(b'\r', b'GUI ACTION 0 RESULT 0')
                    romela(b'\t', b'GUI FOCUS 1')
                    romela(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    romela(b'\t', b'GUI FOCUS 2')
                    romela(b'\r', b'GUI ACTION 2 RESULT 0')
                    romela(b'\t', b'GUI FOCUS 3')
                    romela(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    romela(b'q', b'jkoros-native> ')
                    netefatso_pego['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Thulaganyo.wait(timeout=10)
            # framebuffer 응답뿐 아니라 tota_tshedimosetso scanout 픽셀도 확인한다.
            with pontsho_ya_sekerine.open('rb') as faele_tsenyo:
                assert faele_tsenyo.readline().strip() == b'P6'
                치수 = faele_tsenyo.readline().strip()
                assert 치수 == b'640 480', 치수
                assert faele_tsenyo.readline().strip() == b'255'
                화소들 = faele_tsenyo.read()
            assert len(화소들) == 640 * 480 * 3
            def phele(kgokagano_ya_x, 세로좌표): return list(화소들[(세로좌표 * 640 + kgokagano_ya_x) * 3:(세로좌표 * 640 + kgokagano_ya_x) * 3 + 3])
            예제들 = {'background': phele(5, 5), 'panel': phele(45, 85), 'tile': phele(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            netefatso_pego.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
            if Thulaganyo.poll() is None:
                Thulaganyo.terminate()
                try: Thulaganyo.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Thulaganyo.kill(); Thulaganyo.wait(timeout=5)
            setlhophi.close()
            Thulaganyo.stdin.close(); Thulaganyo.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(netefatso_pego, indent=2) + '\n')


if __name__ == '__main__':
    dirisa()
