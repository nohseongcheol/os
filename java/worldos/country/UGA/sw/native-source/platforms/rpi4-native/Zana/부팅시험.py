#!/usr/bin/env python3
"""halisi_data raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from tekeleza_amri import 기준, amri


def endesha():
    출력결과 = 기준 / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    uhakikishi_ripoti = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = amri() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        uhakikishi_ripoti['command'] = 명령인수
        Mchakato = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        kiteuzi = selectors.DefaultSelector()
        kiteuzi.register(Mchakato.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, Chipua_thamani=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[Chipua_thamani:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in kiteuzi.select(0.2):
                    data_zuia = 누름값.fileobj.read(4096)
                    if data_zuia:
                        대화기록.extend(data_zuia)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if Mchakato.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Mchakato.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 halisi_data GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(panga_ukubwa):
                    결과 = b''
                    while len(결과) < panga_ukubwa:
                        조각 = 화면접속자.recv(panga_ukubwa - len(결과))
                        if not 조각: raise AssertionError('VNC disconnected')
                        결과 += 조각
                    return 결과
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                seva_thamani = 정확한값(24)
                assert int.from_bytes(seva_thamani[:2], 'big') == 640 and int.from_bytes(seva_thamani[2:4], 'big') == 480
                정확한값(int.from_bytes(seva_thamani[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for amri_baiti, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                Chipua_thamani = len(대화기록)
                Mchakato.stdin.write(amri_baiti + b'\n')
                Mchakato.stdin.flush()
                표시까지받기(b'jkoros-native> ', Chipua_thamani)
                assert 확인표시 in 대화기록[Chipua_thamani:], 확인표시
            def sheli(laini, 예상결과):
                Chipua_thamani = len(대화기록)
                Mchakato.stdin.write(laini.encode('utf-8') + b'\n'); Mchakato.stdin.flush()
                표시까지받기(b'jkoros-native> ', Chipua_thamani)
                응답자료 = bytes(대화기록[Chipua_thamani:])
                for SMS in 예상결과:
                    assert SMS.encode('utf-8') in 응답자료, (laini, SMS, 응답자료)
                return 응답자료
            def ingiza(laini, kisituo):
                Chipua_thamani = len(대화기록)
                Mchakato.stdin.write(laini.encode('utf-8') + b'\n'); Mchakato.stdin.flush()
                표시까지받기(kisituo, Chipua_thamani)
                return bytes(대화기록[Chipua_thamani:])
            def hariri_thamani(Jina, maudhui_thamani, ghairi_upasuaji=False):
                ingiza('edit ' + Jina, b'edit> ')
                for laini in maudhui_thamani.splitlines(): ingiza(laini, b'edit> ')
                if ghairi_upasuaji:
                    Chipua_thamani = len(대화기록)
                    Mchakato.stdin.write(b'\x03'); Mchakato.stdin.flush()
                    표시까지받기(b'jkoros-native> ', Chipua_thamani)
                    assert b'EDIT CANCELLED' in 대화기록[Chipua_thamani:]
                else:
                    assert b'SAVED' in ingiza('.', b'jkoros-native> ')
            def pakia_Faili(Jina, data):
                assert len(data) <= 16384
                ingiza('load ' + Jina, b'hex> ')
                for 순번 in range(0, len(data), 64): ingiza(data[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in ingiza('.', b'jkoros-native> ')
            def pakua(Jina):
                응답자료 = sheli('hex ' + Jina, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                data = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(data) == int(일치.group(1)); return data
            sheli('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            sheli('java -version', ['not OpenJDK', 'exit 0'])
            sheli('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            sheli('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            sheli('python --version', ['MicroPython 1.24.1', 'exit 0'])
            sheli('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 faili', 'exit 0'])
            sheli('cat python.txt', ['한글 faili'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(pakua('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            hariri_thamani('인사.java', 'public class 인사 { public static void main(String[] args) { int thamani = 7; System.out.println("한글=" + thamani); } }')
            sheli('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            sheli('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(pakua('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            hariri_thamani('Hello.java', 'broken', ghairi_upasuaji=True)
            sheli('javac Hello.java', ['Compiled:', 'exit 0'])
            hariri_thamani('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            sheli('javac Broken.java', ['javac error:', 'exit 1'])
            pakia_Faili('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            sheli('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            sheli('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            pakia_Faili('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            sheli('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            sheli('rm Imported.class', [])
            hariri_thamani('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            sheli('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = sheli('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            sheli('rm Loop.java', []); sheli('rm Loop.class', [])
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
            hariri_thamani('checks.py', 파이썬검사)
            sheli('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            sheli('rm checks.py', [])
            hariri_thamani('helper.py', 'value = 321')
            sheli("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            sheli('rm helper.py', [])
            sheli("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            sheli("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                sheli('python hello.py', ['한글 faili', 'exit 0'])
                sheli('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            pakia_Faili('app.elf', (기준 / 'build/user/demo.elf').read_bytes())
            assert pakua('app.elf') == (기준 / 'build/user/demo.elf').read_bytes()
            sheli('run app.elf', ['EL0 C++', 'exit 0'])
            pakia_Faili('app.elf', b'not an ELF')
            sheli('run app.elf', ['exit -8'])
            sheli('rm app.elf', [])
            sheli('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            mchoro_njia = 출력결과 / 'java-framebuffer'; mchoro_njia.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준 / 'dist/jkoros-native-korean.jar'), '-d', str(mchoro_njia), str(기준 / '시험/자바/화면시험.java')])
            pakia_Faili('화면시험.class', (mchoro_njia / '화면시험.class').read_bytes())
            sheli('java 화면시험', ['화면 dondoo kataa_thamani', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            sheli('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as teja:
                teja.settimeout(10)
                teja.connect(str(모의제어경로))
                with teja.makefile('rwb') as Stream_thamani:
                    인사 = json.loads(Stream_thamani.readline())
                    def 모의제어접속(tekeleza_kazi, 전달인수=None):
                        Mtandao_ujumbe = {'execute': tekeleza_kazi}
                        if 전달인수: Mtandao_ujumbe['arguments'] = 전달인수
                        Stream_thamani.write((json.dumps(Mtandao_ujumbe) + '\n').encode())
                        Stream_thamani.flush()
                        while True:
                            jibu = json.loads(Stream_thamani.readline())
                            if 'error' in jibu: raise AssertionError(jibu)
                            if 'return' in jibu: return jibu['return']
                    모의제어접속('qmp_capabilities')
                    picha_ya_skrini = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(picha_ya_skrini), 'format': 'ppm'})
                    def 예제들(njia, 지점들):
                        with njia.open('rb') as elepi_faili:
                            assert elepi_faili.readline().strip() == b'P6'
                            assert elepi_faili.readline().strip() == b'640 480'
                            assert elepi_faili.readline().strip() == b'255'
                            elepi_data = elepi_faili.read()
                        assert len(elepi_data) == 640 * 480 * 3
                        return [list(elepi_data[(Kitufe_cha_Y_kiratibu * 640 + jira_x) * 3:(Kitufe_cha_Y_kiratibu * 640 + jira_x) * 3 + 3]) for jira_x, Kitufe_cha_Y_kiratibu in 지점들]
                    assert 예제들(picha_ya_skrini, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(picha_ya_skrini, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def tuma(누름값, 확인표시):
                        Chipua_thamani = len(대화기록)
                        Mchakato.stdin.write(누름값); Mchakato.stdin.flush()
                        표시까지받기(확인표시, Chipua_thamani)
                    tuma(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    tuma(b'\r', b'GUI ACTION 0 RESULT 0')
                    tuma(b'\t', b'GUI FOCUS 1')
                    tuma(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    tuma(b'\t', b'GUI FOCUS 2')
                    tuma(b'\r', b'GUI ACTION 2 RESULT 0')
                    tuma(b'\t', b'GUI FOCUS 3')
                    tuma(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    tuma(b'q', b'jkoros-native> ')
                    uhakikishi_ripoti['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Mchakato.wait(timeout=10)
            # framebuffer 응답뿐 아니라 halisi_data scanout 픽셀도 확인한다.
            with picha_ya_skrini.open('rb') as faili_ingizo:
                assert faili_ingizo.readline().strip() == b'P6'
                치수 = faili_ingizo.readline().strip()
                assert 치수 == b'640 480', 치수
                assert faili_ingizo.readline().strip() == b'255'
                화소들 = faili_ingizo.read()
            assert len(화소들) == 640 * 480 * 3
            def elepi(jira_x, Kitufe_cha_Y_kiratibu): return list(화소들[(Kitufe_cha_Y_kiratibu * 640 + jira_x) * 3:(Kitufe_cha_Y_kiratibu * 640 + jira_x) * 3 + 3])
            예제들 = {'background': elepi(5, 5), 'panel': elepi(45, 85), 'tile': elepi(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            uhakikishi_ripoti.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
            if Mchakato.poll() is None:
                Mchakato.terminate()
                try: Mchakato.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Mchakato.kill(); Mchakato.wait(timeout=5)
            kiteuzi.close()
            Mchakato.stdin.close(); Mchakato.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(uhakikishi_ripoti, indent=2) + '\n')


if __name__ == '__main__':
    endesha()
