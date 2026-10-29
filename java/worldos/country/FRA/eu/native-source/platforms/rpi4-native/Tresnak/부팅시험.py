#!/usr/bin/env python3
"""benetako_datuak raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from exekutatu_komando import Project_erro, Komandoa


def Exekutatu_2():
    출력결과 = Project_erro / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    balidazio_txosten = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Komandoa() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        balidazio_txosten['command'] = 명령인수
        Prozesua = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        준비선택기 = selectors.DefaultSelector()
        준비선택기.register(Prozesua.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, Geruzak_balio=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[Geruzak_balio:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in 준비선택기.select(0.2):
                    datuak_blokeatu = 누름값.fileobj.read(4096)
                    if datuak_blokeatu:
                        대화기록.extend(datuak_blokeatu)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if Prozesua.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Prozesua.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 benetako_datuak GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def BERDIN_balio(Tamaina):
                    EMAITZA = b''
                    while len(EMAITZA) < Tamaina:
                        조각 = 화면접속자.recv(Tamaina - len(EMAITZA))
                        if not 조각: raise AssertionError('VNC disconnected')
                        EMAITZA += 조각
                    return EMAITZA
                assert BERDIN_balio(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in BERDIN_balio(BERDIN_balio(1)[0]); 화면접속자.sendall(b'\x01')
                assert BERDIN_balio(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                zerbitzari_balio = BERDIN_balio(24)
                assert int.from_bytes(zerbitzari_balio[:2], 'big') == 640 and int.from_bytes(zerbitzari_balio[2:4], 'big') == 480
                BERDIN_balio(int.from_bytes(zerbitzari_balio[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for komando_byte, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                Geruzak_balio = len(대화기록)
                Prozesua.stdin.write(komando_byte + b'\n')
                Prozesua.stdin.flush()
                표시까지받기(b'jkoros-native> ', Geruzak_balio)
                assert 확인표시 in 대화기록[Geruzak_balio:], 확인표시
            def shell(Marra, 예상결과):
                Geruzak_balio = len(대화기록)
                Prozesua.stdin.write(Marra.encode('utf-8') + b'\n'); Prozesua.stdin.flush()
                표시까지받기(b'jkoros-native> ', Geruzak_balio)
                erantzun_1262b476 = bytes(대화기록[Geruzak_balio:])
                for Testua in 예상결과:
                    assert Testua.encode('utf-8') in erantzun_1262b476, (Marra, Testua, erantzun_1262b476)
                return erantzun_1262b476
            def sartu(Marra, eskatu):
                Geruzak_balio = len(대화기록)
                Prozesua.stdin.write(Marra.encode('utf-8') + b'\n'); Prozesua.stdin.flush()
                표시까지받기(eskatu, Geruzak_balio)
                return bytes(대화기록[Geruzak_balio:])
            def edizio_balio(Izena, eduki_balio, Utzi_kirurgia=False):
                sartu('edit ' + Izena, b'edit> ')
                for Marra in eduki_balio.splitlines(): sartu(Marra, b'edit> ')
                if Utzi_kirurgia:
                    Geruzak_balio = len(대화기록)
                    Prozesua.stdin.write(b'\x03'); Prozesua.stdin.flush()
                    표시까지받기(b'jkoros-native> ', Geruzak_balio)
                    assert b'EDIT CANCELLED' in 대화기록[Geruzak_balio:]
                else:
                    assert b'SAVED' in sartu('.', b'jkoros-native> ')
            def Upload_Fitxategiak(Izena, datuak):
                assert len(datuak) <= 16384
                sartu('load ' + Izena, b'hex> ')
                for 순번 in range(0, len(datuak), 64): sartu(datuak[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in sartu('.', b'jkoros-native> ')
            def deskarga(Izena):
                erantzun_1262b476 = shell('hex ' + Izena, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', erantzun_1262b476, re.S)
                datuak = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(datuak) == int(일치.group(1)); return datuak
            shell('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            shell('java -version', ['not OpenJDK', 'exit 0'])
            shell('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            shell('java Hello "한글 Argumentuak 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Argumentuak 😀', 'exit 0'])
            shell('python --version', ['MicroPython 1.24.1', 'exit 0'])
            shell('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Fitxategia', 'exit 0'])
            shell('cat python.txt', ['한글 Fitxategia'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(deskarga('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 Argumentuak 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Argumentuak 😀'], 예상결과
            edizio_balio('인사.java', 'public class 인사 { public static void main(String[] args) { int balio = 7; System.out.println("한글=" + balio); } }')
            shell('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            shell('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(deskarga('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            edizio_balio('Hello.java', 'broken', Utzi_kirurgia=True)
            shell('javac Hello.java', ['Compiled:', 'exit 0'])
            edizio_balio('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            shell('javac Broken.java', ['javac error:', 'exit 1'])
            Upload_Fitxategiak('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            shell('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            shell('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Upload_Fitxategiak('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            shell('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            shell('rm Imported.class', [])
            edizio_balio('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            shell('javac Loop.java', ['Compiled:', 'exit 0'])
            erantzun_1262b476 = shell('java Loop', ['exit '])
            assert b'instruction limit' in erantzun_1262b476 or b'exit -1004' in erantzun_1262b476
            shell('rm Loop.java', []); shell('rm Loop.class', [])
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
            edizio_balio('checks.py', 파이썬검사)
            shell('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            shell('rm checks.py', [])
            edizio_balio('helper.py', 'value = 321')
            shell("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            shell('rm helper.py', [])
            shell("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            shell("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                shell('python hello.py', ['한글 Fitxategia', 'exit 0'])
                shell('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Upload_Fitxategiak('app.elf', (Project_erro / 'build/user/demo.elf').read_bytes())
            assert deskarga('app.elf') == (Project_erro / 'build/user/demo.elf').read_bytes()
            shell('run app.elf', ['EL0 C++', 'exit 0'])
            Upload_Fitxategiak('app.elf', b'not an ELF')
            shell('run app.elf', ['exit -8'])
            shell('rm app.elf', [])
            shell('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            그림경로 = 출력결과 / 'java-framebuffer'; 그림경로.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_erro / 'dist/jkoros-native-korean.jar'), '-d', str(그림경로), str(Project_erro / '시험/자바/화면시험.java')])
            Upload_Fitxategiak('화면시험.class', (그림경로 / '화면시험.class').read_bytes())
            shell('java 화면시험', ['화면 klip baztertu_balio', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            shell('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as bezero:
                bezero.settimeout(10)
                bezero.connect(str(모의제어경로))
                with bezero.makefile('rwb') as Stream_balio:
                    인사 = json.loads(Stream_balio.readline())
                    def 모의제어접속(Exekutatu, 전달인수=None):
                        sare_mezu = {'execute': Exekutatu}
                        if 전달인수: sare_mezu['arguments'] = 전달인수
                        Stream_balio.write((json.dumps(sare_mezu) + '\n').encode())
                        Stream_balio.flush()
                        while True:
                            erantzun = json.loads(Stream_balio.readline())
                            if 'error' in erantzun: raise AssertionError(erantzun)
                            if 'return' in erantzun: return erantzun['return']
                    모의제어접속('qmp_capabilities')
                    pantaila_mozketa = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(pantaila_mozketa), 'format': 'ppm'})
                    def 예제들(Bide_izena, 지점들):
                        with Bide_izena.open('rb') as pixel_fitxategi:
                            assert pixel_fitxategi.readline().strip() == b'P6'
                            assert pixel_fitxategi.readline().strip() == b'640 480'
                            assert pixel_fitxategi.readline().strip() == b'255'
                            pixel_datuak = pixel_fitxategi.read()
                        assert len(pixel_datuak) == 640 * 480 * 3
                        return [list(pixel_datuak[(Y_koordenatu * 640 + X_koordenatu) * 3:(Y_koordenatu * 640 + X_koordenatu) * 3 + 3]) for X_koordenatu, Y_koordenatu in 지점들]
                    assert 예제들(pantaila_mozketa, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(pantaila_mozketa, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def bidali(누름값, 확인표시):
                        Geruzak_balio = len(대화기록)
                        Prozesua.stdin.write(누름값); Prozesua.stdin.flush()
                        표시까지받기(확인표시, Geruzak_balio)
                    bidali(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    bidali(b'\r', b'GUI ACTION 0 RESULT 0')
                    bidali(b'\t', b'GUI FOCUS 1')
                    bidali(b'\r', b'GUI ACTION 1 RESULT 0')
                    SEGUNDOA_GUI = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SEGUNDOA_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SEGUNDOA_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    bidali(b'\t', b'GUI FOCUS 2')
                    bidali(b'\r', b'GUI ACTION 2 RESULT 0')
                    bidali(b'\t', b'GUI FOCUS 3')
                    bidali(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    bidali(b'q', b'jkoros-native> ')
                    balidazio_txosten['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Prozesua.wait(timeout=10)
            # framebuffer 응답뿐 아니라 benetako_datuak scanout 픽셀도 확인한다.
            with pantaila_mozketa.open('rb') as fitxategi_sarrera:
                assert fitxategi_sarrera.readline().strip() == b'P6'
                치수 = fitxategi_sarrera.readline().strip()
                assert 치수 == b'640 480', 치수
                assert fitxategi_sarrera.readline().strip() == b'255'
                화소들 = fitxategi_sarrera.read()
            assert len(화소들) == 640 * 480 * 3
            def pixel(X_koordenatu, Y_koordenatu): return list(화소들[(Y_koordenatu * 640 + X_koordenatu) * 3:(Y_koordenatu * 640 + X_koordenatu) * 3 + 3])
            예제들 = {'background': pixel(5, 5), 'panel': pixel(45, 85), 'tile': pixel(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            balidazio_txosten.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((Project_erro / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Prozesua.poll() is None:
                Prozesua.terminate()
                try: Prozesua.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Prozesua.kill(); Prozesua.wait(timeout=5)
            준비선택기.close()
            Prozesua.stdin.close(); Prozesua.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(balidazio_txosten, indent=2) + '\n')


if __name__ == '__main__':
    Exekutatu_2()
