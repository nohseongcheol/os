#!/usr/bin/env python3
"""Na_hakika_Tarin_bayani raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from gudanar_Umarni import 기준, Umarni


def Tafiyar_da():
    출력결과 = 기준 / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    amincewa_Rahoto = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Umarni() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        amincewa_Rahoto['command'] = 명령인수
        haryar_aikin_na_ura = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        mai_zabe = selectors.DefaultSelector()
        mai_zabe.register(haryar_aikin_na_ura.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, Sassautawa_Daraja=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[Sassautawa_Daraja:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in mai_zabe.select(0.2):
                    Tarin_bayani_bulo = 누름값.fileobj.read(4096)
                    if Tarin_bayani_bulo:
                        대화기록.extend(Tarin_bayani_bulo)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if haryar_aikin_na_ura.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(haryar_aikin_na_ura.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 Na_hakika_Tarin_bayani GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(Girma):
                    결과 = b''
                    while len(결과) < Girma:
                        조각 = 화면접속자.recv(Girma - len(결과))
                        if not 조각: raise AssertionError('VNC disconnected')
                        결과 += 조각
                    return 결과
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                Saba_Daraja = 정확한값(24)
                assert int.from_bytes(Saba_Daraja[:2], 'big') == 640 and int.from_bytes(Saba_Daraja[2:4], 'big') == 480
                정확한값(int.from_bytes(Saba_Daraja[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for Umarni_bayit, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                Sassautawa_Daraja = len(대화기록)
                haryar_aikin_na_ura.stdin.write(Umarni_bayit + b'\n')
                haryar_aikin_na_ura.stdin.flush()
                표시까지받기(b'jkoros-native> ', Sassautawa_Daraja)
                assert 확인표시 in 대화기록[Sassautawa_Daraja:], 확인표시
            def Mai_fayyace_umani(Layi, 예상결과):
                Sassautawa_Daraja = len(대화기록)
                haryar_aikin_na_ura.stdin.write(Layi.encode('utf-8') + b'\n'); haryar_aikin_na_ura.stdin.flush()
                표시까지받기(b'jkoros-native> ', Sassautawa_Daraja)
                응답자료 = bytes(대화기록[Sassautawa_Daraja:])
                for SMS in 예상결과:
                    assert SMS.encode('utf-8') in 응답자료, (Layi, SMS, 응답자료)
                return 응답자료
            def Shiga(Layi, promt):
                Sassautawa_Daraja = len(대화기록)
                haryar_aikin_na_ura.stdin.write(Layi.encode('utf-8') + b'\n'); haryar_aikin_na_ura.stdin.flush()
                표시까지받기(promt, Sassautawa_Daraja)
                return bytes(대화기록[Sassautawa_Daraja:])
            def gyaran_Daraja(Suna, kunshiya_Daraja, Soke_aiki=False):
                Shiga('edit ' + Suna, b'edit> ')
                for Layi in kunshiya_Daraja.splitlines(): Shiga(Layi, b'edit> ')
                if Soke_aiki:
                    Sassautawa_Daraja = len(대화기록)
                    haryar_aikin_na_ura.stdin.write(b'\x03'); haryar_aikin_na_ura.stdin.flush()
                    표시까지받기(b'jkoros-native> ', Sassautawa_Daraja)
                    assert b'EDIT CANCELLED' in 대화기록[Sassautawa_Daraja:]
                else:
                    assert b'SAVED' in Shiga('.', b'jkoros-native> ')
            def lodawa_Fayiloli(Suna, Tarin_bayani):
                assert len(Tarin_bayani) <= 16384
                Shiga('load ' + Suna, b'hex> ')
                for 순번 in range(0, len(Tarin_bayani), 64): Shiga(Tarin_bayani[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in Shiga('.', b'jkoros-native> ')
            def zazzage(Suna):
                응답자료 = Mai_fayyace_umani('hex ' + Suna, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                Tarin_bayani = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(Tarin_bayani) == int(일치.group(1)); return Tarin_bayani
            Mai_fayyace_umani('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            Mai_fayyace_umani('java -version', ['not OpenJDK', 'exit 0'])
            Mai_fayyace_umani('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            Mai_fayyace_umani('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            Mai_fayyace_umani('python --version', ['MicroPython 1.24.1', 'exit 0'])
            Mai_fayyace_umani('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Fayil', 'exit 0'])
            Mai_fayyace_umani('cat python.txt', ['한글 Fayil'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(zazzage('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            gyaran_Daraja('인사.java', 'public class 인사 { public static void main(String[] args) { int Daraja = 7; System.out.println("한글=" + Daraja); } }')
            Mai_fayyace_umani('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            Mai_fayyace_umani('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(zazzage('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            gyaran_Daraja('Hello.java', 'broken', Soke_aiki=True)
            Mai_fayyace_umani('javac Hello.java', ['Compiled:', 'exit 0'])
            gyaran_Daraja('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            Mai_fayyace_umani('javac Broken.java', ['javac error:', 'exit 1'])
            lodawa_Fayiloli('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            Mai_fayyace_umani('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            Mai_fayyace_umani('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            lodawa_Fayiloli('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            Mai_fayyace_umani('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            Mai_fayyace_umani('rm Imported.class', [])
            gyaran_Daraja('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            Mai_fayyace_umani('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = Mai_fayyace_umani('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            Mai_fayyace_umani('rm Loop.java', []); Mai_fayyace_umani('rm Loop.class', [])
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
            gyaran_Daraja('checks.py', 파이썬검사)
            Mai_fayyace_umani('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            Mai_fayyace_umani('rm checks.py', [])
            gyaran_Daraja('helper.py', 'value = 321')
            Mai_fayyace_umani("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            Mai_fayyace_umani('rm helper.py', [])
            Mai_fayyace_umani("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            Mai_fayyace_umani("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                Mai_fayyace_umani('python hello.py', ['한글 Fayil', 'exit 0'])
                Mai_fayyace_umani('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            lodawa_Fayiloli('app.elf', (기준 / 'build/user/demo.elf').read_bytes())
            assert zazzage('app.elf') == (기준 / 'build/user/demo.elf').read_bytes()
            Mai_fayyace_umani('run app.elf', ['EL0 C++', 'exit 0'])
            lodawa_Fayiloli('app.elf', b'not an ELF')
            Mai_fayyace_umani('run app.elf', ['exit -8'])
            Mai_fayyace_umani('rm app.elf', [])
            Mai_fayyace_umani('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            zane_Hanyar_shiga = 출력결과 / 'java-framebuffer'; zane_Hanyar_shiga.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준 / 'dist/jkoros-native-korean.jar'), '-d', str(zane_Hanyar_shiga), str(기준 / '시험/자바/화면시험.java')])
            lodawa_Fayiloli('화면시험.class', (zane_Hanyar_shiga / '화면시험.class').read_bytes())
            Mai_fayyace_umani('java 화면시험', ['화면 darfi kore_Daraja', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            Mai_fayyace_umani('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as abokin_hulda:
                abokin_hulda.settimeout(10)
                abokin_hulda.connect(str(모의제어경로))
                with abokin_hulda.makefile('rwb') as watsuwa_Daraja:
                    인사 = json.loads(watsuwa_Daraja.readline())
                    def 모의제어접속(gudanar_aiki, 전달인수=None):
                        Hanyar_sadarwa_imel = {'execute': gudanar_aiki}
                        if 전달인수: Hanyar_sadarwa_imel['arguments'] = 전달인수
                        watsuwa_Daraja.write((json.dumps(Hanyar_sadarwa_imel) + '\n').encode())
                        watsuwa_Daraja.flush()
                        while True:
                            mayar_da_martani = json.loads(watsuwa_Daraja.readline())
                            if 'error' in mayar_da_martani: raise AssertionError(mayar_da_martani)
                            if 'return' in mayar_da_martani: return mayar_da_martani['return']
                    모의제어접속('qmp_capabilities')
                    hoton_allo = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(hoton_allo), 'format': 'ppm'})
                    def 예제들(Hanyar_shiga, 지점들):
                        with Hanyar_shiga.open('rb') as pel_Fayil:
                            assert pel_Fayil.readline().strip() == b'P6'
                            assert pel_Fayil.readline().strip() == b'640 480'
                            assert pel_Fayil.readline().strip() == b'255'
                            pel_Tarin_bayani = pel_Fayil.read()
                        assert len(pel_Tarin_bayani) == 640 * 480 * 3
                        return [list(pel_Tarin_bayani[(Maɓallin_Y_Mai_tsarawa * 640 + gamayyar_x) * 3:(Maɓallin_Y_Mai_tsarawa * 640 + gamayyar_x) * 3 + 3]) for gamayyar_x, Maɓallin_Y_Mai_tsarawa in 지점들]
                    assert 예제들(hoton_allo, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(hoton_allo, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def Aika(누름값, 확인표시):
                        Sassautawa_Daraja = len(대화기록)
                        haryar_aikin_na_ura.stdin.write(누름값); haryar_aikin_na_ura.stdin.flush()
                        표시까지받기(확인표시, Sassautawa_Daraja)
                    Aika(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    Aika(b'\r', b'GUI ACTION 0 RESULT 0')
                    Aika(b'\t', b'GUI FOCUS 1')
                    Aika(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    Aika(b'\t', b'GUI FOCUS 2')
                    Aika(b'\r', b'GUI ACTION 2 RESULT 0')
                    Aika(b'\t', b'GUI FOCUS 3')
                    Aika(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    Aika(b'q', b'jkoros-native> ')
                    amincewa_Rahoto['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            haryar_aikin_na_ura.wait(timeout=10)
            # framebuffer 응답뿐 아니라 Na_hakika_Tarin_bayani scanout 픽셀도 확인한다.
            with hoton_allo.open('rb') as Fayil_Mashigar_bayanai:
                assert Fayil_Mashigar_bayanai.readline().strip() == b'P6'
                치수 = Fayil_Mashigar_bayanai.readline().strip()
                assert 치수 == b'640 480', 치수
                assert Fayil_Mashigar_bayanai.readline().strip() == b'255'
                화소들 = Fayil_Mashigar_bayanai.read()
            assert len(화소들) == 640 * 480 * 3
            def pel(gamayyar_x, Maɓallin_Y_Mai_tsarawa): return list(화소들[(Maɓallin_Y_Mai_tsarawa * 640 + gamayyar_x) * 3:(Maɓallin_Y_Mai_tsarawa * 640 + gamayyar_x) * 3 + 3])
            예제들 = {'background': pel(5, 5), 'panel': pel(45, 85), 'tile': pel(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            amincewa_Rahoto.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
            if haryar_aikin_na_ura.poll() is None:
                haryar_aikin_na_ura.terminate()
                try: haryar_aikin_na_ura.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    haryar_aikin_na_ura.kill(); haryar_aikin_na_ura.wait(timeout=5)
            mai_zabe.close()
            haryar_aikin_na_ura.stdin.close(); haryar_aikin_na_ura.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(amincewa_Rahoto, indent=2) + '\n')


if __name__ == '__main__':
    Tafiyar_da()
