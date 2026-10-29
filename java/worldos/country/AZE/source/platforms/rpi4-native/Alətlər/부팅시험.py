#!/usr/bin/env python3
"""faktiki_verilənlər raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from icra_etmək_əmr import Project_kök, Əmr


def İcra_Et():
    출력결과 = Project_kök / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    yoxlama_hesabat = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Əmr() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        yoxlama_hesabat['command'] = 명령인수
        Proses = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        seçici = selectors.DefaultSelector()
        seçici.register(Proses.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, OFFSET_VALUE=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[OFFSET_VALUE:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in seçici.select(0.2):
                    verilənlər_blokla = 누름값.fileobj.read(4096)
                    if verilənlər_blokla:
                        대화기록.extend(verilənlər_blokla)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if Proses.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Proses.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 faktiki_verilənlər GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def EXACT_VALUE(Böyüklük):
                    ölçü = b''
                    while len(ölçü) < Böyüklük:
                        조각 = 화면접속자.recv(Böyüklük - len(ölçü))
                        if not 조각: raise AssertionError('VNC disconnected')
                        ölçü += 조각
                    return ölçü
                assert EXACT_VALUE(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in EXACT_VALUE(EXACT_VALUE(1)[0]); 화면접속자.sendall(b'\x01')
                assert EXACT_VALUE(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                server_VALUE = EXACT_VALUE(24)
                assert int.from_bytes(server_VALUE[:2], 'big') == 640 and int.from_bytes(server_VALUE[2:4], 'big') == 480
                EXACT_VALUE(int.from_bytes(server_VALUE[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for əmr_bayt, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                OFFSET_VALUE = len(대화기록)
                Proses.stdin.write(əmr_bayt + b'\n')
                Proses.stdin.flush()
                표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                assert 확인표시 in 대화기록[OFFSET_VALUE:], 확인표시
            def örtük(Giriş, 예상결과):
                OFFSET_VALUE = len(대화기록)
                Proses.stdin.write(Giriş.encode('utf-8') + b'\n'); Proses.stdin.flush()
                표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                video_münasibət = bytes(대화기록[OFFSET_VALUE:])
                for Mətn in 예상결과:
                    assert Mətn.encode('utf-8') in video_münasibət, (Giriş, Mətn, video_münasibət)
                return video_münasibət
            def daxil_etmək(Giriş, dəvət):
                OFFSET_VALUE = len(대화기록)
                Proses.stdin.write(Giriş.encode('utf-8') + b'\n'); Proses.stdin.flush()
                표시까지받기(dəvət, OFFSET_VALUE)
                return bytes(대화기록[OFFSET_VALUE:])
            def redaktə_VALUE(Ad, Məzmun_VALUE, imtina_etmək_əməliyyat=False):
                daxil_etmək('edit ' + Ad, b'edit> ')
                for Giriş in Məzmun_VALUE.splitlines(): daxil_etmək(Giriş, b'edit> ')
                if imtina_etmək_əməliyyat:
                    OFFSET_VALUE = len(대화기록)
                    Proses.stdin.write(b'\x03'); Proses.stdin.flush()
                    표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                    assert b'EDIT CANCELLED' in 대화기록[OFFSET_VALUE:]
                else:
                    assert b'SAVED' in daxil_etmək('.', b'jkoros-native> ')
            def Upload_Fayllar(Ad, verilənlər):
                assert len(verilənlər) <= 16384
                daxil_etmək('load ' + Ad, b'hex> ')
                for 순번 in range(0, len(verilənlər), 64): daxil_etmək(verilənlər[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in daxil_etmək('.', b'jkoros-native> ')
            def yüklə(Ad):
                video_münasibət = örtük('hex ' + Ad, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', video_münasibət, re.S)
                verilənlər = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(verilənlər) == int(일치.group(1)); return verilənlər
            örtük('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            örtük('java -version', ['not OpenJDK', 'exit 0'])
            örtük('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            örtük('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            örtük('python --version', ['MicroPython 1.24.1', 'exit 0'])
            örtük('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 FAYL', 'exit 0'])
            örtük('cat python.txt', ['한글 FAYL'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(yüklə('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            redaktə_VALUE('인사.java', 'public class 인사 { public static void main(String[] args) { int VALUE = 7; System.out.println("한글=" + VALUE); } }')
            örtük('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            örtük('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(yüklə('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            redaktə_VALUE('Hello.java', 'broken', imtina_etmək_əməliyyat=True)
            örtük('javac Hello.java', ['Compiled:', 'exit 0'])
            redaktə_VALUE('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            örtük('javac Broken.java', ['javac error:', 'exit 1'])
            Upload_Fayllar('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            örtük('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            örtük('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Upload_Fayllar('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            örtük('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            örtük('rm Imported.class', [])
            redaktə_VALUE('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            örtük('javac Loop.java', ['Compiled:', 'exit 0'])
            video_münasibət = örtük('java Loop', ['exit '])
            assert b'instruction limit' in video_münasibət or b'exit -1004' in video_münasibət
            örtük('rm Loop.java', []); örtük('rm Loop.class', [])
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
            redaktə_VALUE('checks.py', 파이썬검사)
            örtük('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            örtük('rm checks.py', [])
            redaktə_VALUE('helper.py', 'value = 321')
            örtük("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            örtük('rm helper.py', [])
            örtük("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            örtük("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                örtük('python hello.py', ['한글 FAYL', 'exit 0'])
                örtük('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Upload_Fayllar('app.elf', (Project_kök / 'build/user/demo.elf').read_bytes())
            assert yüklə('app.elf') == (Project_kök / 'build/user/demo.elf').read_bytes()
            örtük('run app.elf', ['EL0 C++', 'exit 0'])
            Upload_Fayllar('app.elf', b'not an ELF')
            örtük('run app.elf', ['exit -8'])
            örtük('rm app.elf', [])
            örtük('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            rəsm_yol = 출력결과 / 'java-framebuffer'; rəsm_yol.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_kök / 'dist/jkoros-native-korean.jar'), '-d', str(rəsm_yol), str(Project_kök / '시험/자바/화면시험.java')])
            Upload_Fayllar('화면시험.class', (rəsm_yol / '화면시험.class').read_bytes())
            örtük('java 화면시험', ['화면 klip 거부', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            örtük('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as müştəri:
                müştəri.settimeout(10)
                müştəri.connect(str(모의제어경로))
                with müştəri.makefile('rwb') as axın_VALUE:
                    인사 = json.loads(axın_VALUE.readline())
                    def 모의제어접속(icra_etmək_tapşırıq, 전달인수=None):
                        Şəbəkə_mesaj = {'execute': icra_etmək_tapşırıq}
                        if 전달인수: Şəbəkə_mesaj['arguments'] = 전달인수
                        axın_VALUE.write((json.dumps(Şəbəkə_mesaj) + '\n').encode())
                        axın_VALUE.flush()
                        while True:
                            cavab = json.loads(axın_VALUE.readline())
                            if 'error' in cavab: raise AssertionError(cavab)
                            if 'return' in cavab: return cavab['return']
                    모의제어접속('qmp_capabilities')
                    ekran_şəkli = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(ekran_şəkli), 'format': 'ppm'})
                    def 예제들(Cığır, 지점들):
                        with Cığır.open('rb') as piksel_fayl:
                            assert piksel_fayl.readline().strip() == b'P6'
                            assert piksel_fayl.readline().strip() == b'640 480'
                            assert piksel_fayl.readline().strip() == b'255'
                            piksel_verilənlər = piksel_fayl.read()
                        assert len(piksel_verilənlər) == 640 * 480 * 3
                        return [list(piksel_verilənlər[(Y_koordinat * 640 + x_koordinatı) * 3:(Y_koordinat * 640 + x_koordinatı) * 3 + 3]) for x_koordinatı, Y_koordinat in 지점들]
                    assert 예제들(ekran_şəkli, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(ekran_şəkli, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def göndərmək(누름값, 확인표시):
                        OFFSET_VALUE = len(대화기록)
                        Proses.stdin.write(누름값); Proses.stdin.flush()
                        표시까지받기(확인표시, OFFSET_VALUE)
                    göndərmək(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    göndərmək(b'\r', b'GUI ACTION 0 RESULT 0')
                    göndərmək(b'\t', b'GUI FOCUS 1')
                    göndərmək(b'\r', b'GUI ACTION 1 RESULT 0')
                    SECOND_GUI = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SECOND_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SECOND_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    göndərmək(b'\t', b'GUI FOCUS 2')
                    göndərmək(b'\r', b'GUI ACTION 2 RESULT 0')
                    göndərmək(b'\t', b'GUI FOCUS 3')
                    göndərmək(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    göndərmək(b'q', b'jkoros-native> ')
                    yoxlama_hesabat['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Proses.wait(timeout=10)
            # framebuffer 응답뿐 아니라 faktiki_verilənlər scanout 픽셀도 확인한다.
            with ekran_şəkli.open('rb') as fayl_daxiletmə:
                assert fayl_daxiletmə.readline().strip() == b'P6'
                치수 = fayl_daxiletmə.readline().strip()
                assert 치수 == b'640 480', 치수
                assert fayl_daxiletmə.readline().strip() == b'255'
                화소들 = fayl_daxiletmə.read()
            assert len(화소들) == 640 * 480 * 3
            def piksel(x_koordinatı, Y_koordinat): return list(화소들[(Y_koordinat * 640 + x_koordinatı) * 3:(Y_koordinat * 640 + x_koordinatı) * 3 + 3])
            예제들 = {'background': piksel(5, 5), 'panel': piksel(45, 85), 'tile': piksel(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            yoxlama_hesabat.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((Project_kök / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Proses.poll() is None:
                Proses.terminate()
                try: Proses.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Proses.kill(); Proses.wait(timeout=5)
            seçici.close()
            Proses.stdin.close(); Proses.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(yoxlama_hesabat, indent=2) + '\n')


if __name__ == '__main__':
    İcra_Et()
