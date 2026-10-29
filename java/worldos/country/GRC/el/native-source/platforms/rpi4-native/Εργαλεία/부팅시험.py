#!/usr/bin/env python3
"""πραγματικός_δεδομένα raspi4b 부팅, UART είσοδος_τιμή, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from εκτελώ_εντολή import έργο_ρίζα, Εντολή


def Εκτέλεση_2():
    출력결과 = έργο_ρίζα / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    μεταγραφή = bytearray()
    επικύρωση_έκθεση = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Εντολή() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        επικύρωση_έκθεση['command'] = 명령인수
        Διεργασία = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        επιλογέας = selectors.DefaultSelector()
        επιλογέας.register(Διεργασία.stdout, selectors.EVENT_READ)
        def 표시까지받기(δείκτης_8b722c5f, Υπέρθεση_τιμή=0, εκτέλεση_ΤΕΛΟΣ_ΧΡΟΝΟΥ=45):
            προθεσμία_ώρα = time.monotonic() + εκτέλεση_ΤΕΛΟΣ_ΧΡΟΝΟΥ
            while δείκτης_8b722c5f not in μεταγραφή[Υπέρθεση_τιμή:]:
                if time.monotonic() > προθεσμία_ώρα:
                    raise AssertionError('UART timeout: ' + repr(δείκτης_8b722c5f))
                for 누름값, _ in επιλογέας.select(0.2):
                    μπλοκ_δεδομένων = 누름값.fileobj.read(4096)
                    if μπλοκ_δεδομένων:
                        μεταγραφή.extend(μπλοκ_δεδομένων)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', μεταγραφή):
                    raise AssertionError('kernel failure')
                if Διεργασία.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Διεργασία.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for δείκτης_8b722c5f in 확인표시들:
                assert δείκτης_8b722c5f in μεταγραφή, δείκτης_8b722c5f
            # GTK 없는 τρέχων_στοιχείο 호스트에서도 VNC로 πραγματικός_δεδομένα GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(Μέγεθος):
                    μέτρηση = b''
                    while len(μέτρηση) < Μέγεθος:
                        조각 = 화면접속자.recv(Μέγεθος - len(μέτρηση))
                        if not 조각: raise AssertionError('VNC disconnected')
                        μέτρηση += 조각
                    return μέτρηση
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                διακομιστής_τιμή = 정확한값(24)
                assert int.from_bytes(διακομιστής_τιμή[:2], 'big') == 640 and int.from_bytes(διακομιστής_τιμή[2:4], 'big') == 480
                정확한값(int.from_bytes(διακομιστής_τιμή[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for 명령바이트, δείκτης_8b722c5f in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                Υπέρθεση_τιμή = len(μεταγραφή)
                Διεργασία.stdin.write(명령바이트 + b'\n')
                Διεργασία.stdin.flush()
                표시까지받기(b'jkoros-native> ', Υπέρθεση_τιμή)
                assert δείκτης_8b722c5f in μεταγραφή[Υπέρθεση_τιμή:], δείκτης_8b722c5f
            def κέλυφος(Γραμμή, 예상결과):
                Υπέρθεση_τιμή = len(μεταγραφή)
                Διεργασία.stdin.write(Γραμμή.encode('utf-8') + b'\n'); Διεργασία.stdin.flush()
                표시까지받기(b'jkoros-native> ', Υπέρθεση_τιμή)
                απάντηση = bytes(μεταγραφή[Υπέρθεση_τιμή:])
                for Κείμενο in 예상결과:
                    assert Κείμενο.encode('utf-8') in απάντηση, (Γραμμή, Κείμενο, απάντηση)
                return απάντηση
            def εισάγω(Γραμμή, ζητώ):
                Υπέρθεση_τιμή = len(μεταγραφή)
                Διεργασία.stdin.write(Γραμμή.encode('utf-8') + b'\n'); Διεργασία.stdin.flush()
                표시까지받기(ζητώ, Υπέρθεση_τιμή)
                return bytes(μεταγραφή[Υπέρθεση_τιμή:])
            def Τροποποίησε_τιμή(Όνομα, Περιεχόμενο_τιμή, Άκυρο_εγχείρηση=False):
                εισάγω('edit ' + Όνομα, b'edit> ')
                for Γραμμή in Περιεχόμενο_τιμή.splitlines(): εισάγω(Γραμμή, b'edit> ')
                if Άκυρο_εγχείρηση:
                    Υπέρθεση_τιμή = len(μεταγραφή)
                    Διεργασία.stdin.write(b'\x03'); Διεργασία.stdin.flush()
                    표시까지받기(b'jkoros-native> ', Υπέρθεση_τιμή)
                    assert b'EDIT CANCELLED' in μεταγραφή[Υπέρθεση_τιμή:]
                else:
                    assert b'SAVED' in εισάγω('.', b'jkoros-native> ')
            def ανεβάζω_Αρχεία(Όνομα, δεδομένα):
                assert len(δεδομένα) <= 16384
                εισάγω('load ' + Όνομα, b'hex> ')
                for 순번 in range(0, len(δεδομένα), 64): εισάγω(δεδομένα[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in εισάγω('.', b'jkoros-native> ')
            def λήψη(Όνομα):
                απάντηση = κέλυφος('hex ' + Όνομα, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', απάντηση, re.S)
                δεδομένα = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(δεδομένα) == int(일치.group(1)); return δεδομένα
            κέλυφος('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            κέλυφος('java -version', ['not OpenJDK', 'exit 0'])
            κέλυφος('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            κέλυφος('java Hello "한글 Παράμετροι 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Παράμετροι 😀', 'exit 0'])
            κέλυφος('python --version', ['MicroPython 1.24.1', 'exit 0'])
            κέλυφος('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Αρχείο', 'exit 0'])
            κέλυφος('cat python.txt', ['한글 Αρχείο'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(λήψη('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 Παράμετροι 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Παράμετροι 😀'], 예상결과
            Τροποποίησε_τιμή('인사.java', 'public class 인사 { public static void main(String[] args) { int τιμή = 7; System.out.println("한글=" + τιμή); } }')
            κέλυφος('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            κέλυφος('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(λήψη('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            Τροποποίησε_τιμή('Hello.java', 'broken', Άκυρο_εγχείρηση=True)
            κέλυφος('javac Hello.java', ['Compiled:', 'exit 0'])
            Τροποποίησε_τιμή('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            κέλυφος('javac Broken.java', ['javac error:', 'exit 1'])
            ανεβάζω_Αρχεία('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            κέλυφος('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            κέλυφος('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            ανεβάζω_Αρχεία('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            κέλυφος('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            κέλυφος('rm Imported.class', [])
            Τροποποίησε_τιμή('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            κέλυφος('javac Loop.java', ['Compiled:', 'exit 0'])
            απάντηση = κέλυφος('java Loop', ['exit '])
            assert b'instruction limit' in απάντηση or b'exit -1004' in απάντηση
            κέλυφος('rm Loop.java', []); κέλυφος('rm Loop.class', [])
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
            Τροποποίησε_τιμή('checks.py', 파이썬검사)
            κέλυφος('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            κέλυφος('rm checks.py', [])
            Τροποποίησε_τιμή('helper.py', 'value = 321')
            κέλυφος("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            κέλυφος('rm helper.py', [])
            κέλυφος("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            κέλυφος("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                κέλυφος('python hello.py', ['한글 Αρχείο', 'exit 0'])
                κέλυφος('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            ανεβάζω_Αρχεία('app.elf', (έργο_ρίζα / 'build/user/demo.elf').read_bytes())
            assert λήψη('app.elf') == (έργο_ρίζα / 'build/user/demo.elf').read_bytes()
            κέλυφος('run app.elf', ['EL0 C++', 'exit 0'])
            ανεβάζω_Αρχεία('app.elf', b'not an ELF')
            κέλυφος('run app.elf', ['exit -8'])
            κέλυφος('rm app.elf', [])
            κέλυφος('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            σχέδιο_διαδρομή = 출력결과 / 'java-framebuffer'; σχέδιο_διαδρομή.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(έργο_ρίζα / 'dist/jkoros-native-korean.jar'), '-d', str(σχέδιο_διαδρομή), str(έργο_ρίζα / '시험/자바/화면시험.java')])
            ανεβάζω_Αρχεία('화면시험.class', (σχέδιο_διαδρομή / '화면시험.class').read_bytes())
            κέλυφος('java 화면시험', ['화면 απόσπασμα απορρίπτω_τιμή', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            κέλυφος('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as πελάτης:
                πελάτης.settimeout(10)
                πελάτης.connect(str(모의제어경로))
                with πελάτης.makefile('rwb') as ροή_τιμή:
                    인사 = json.loads(ροή_τιμή.readline())
                    def 모의제어접속(Εκτέλεση, 전달인수=None):
                        δίκτυο_μήνυμα = {'execute': Εκτέλεση}
                        if 전달인수: δίκτυο_μήνυμα['arguments'] = 전달인수
                        ροή_τιμή.write((json.dumps(δίκτυο_μήνυμα) + '\n').encode())
                        ροή_τιμή.flush()
                        while True:
                            απαντώ = json.loads(ροή_τιμή.readline())
                            if 'error' in απαντώ: raise AssertionError(απαντώ)
                            if 'return' in απαντώ: return απαντώ['return']
                    모의제어접속('qmp_capabilities')
                    απόσπασμα_οθόνης = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(απόσπασμα_οθόνης), 'format': 'ppm'})
                    def 예제들(ΔΙΑΔΡΟΜΗ, 지점들):
                        with ΔΙΑΔΡΟΜΗ.open('rb') as 화소파일:
                            assert 화소파일.readline().strip() == b'P6'
                            assert 화소파일.readline().strip() == b'640 480'
                            assert 화소파일.readline().strip() == b'255'
                            화소자료 = 화소파일.read()
                        assert len(화소자료) == 640 * 480 * 3
                        return [list(화소자료[(κουμπί_Y_συντονισμός * 640 + συντεταγμένη_x) * 3:(κουμπί_Y_συντονισμός * 640 + συντεταγμένη_x) * 3 + 3]) for συντεταγμένη_x, κουμπί_Y_συντονισμός in 지점들]
                    assert 예제들(απόσπασμα_οθόνης, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(απόσπασμα_οθόνης, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def στέλνω(누름값, δείκτης_8b722c5f):
                        Υπέρθεση_τιμή = len(μεταγραφή)
                        Διεργασία.stdin.write(누름값); Διεργασία.stdin.flush()
                        표시까지받기(δείκτης_8b722c5f, Υπέρθεση_τιμή)
                    στέλνω(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    στέλνω(b'\r', b'GUI ACTION 0 RESULT 0')
                    στέλνω(b'\t', b'GUI FOCUS 1')
                    στέλνω(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    στέλνω(b'\t', b'GUI FOCUS 2')
                    στέλνω(b'\r', b'GUI ACTION 2 RESULT 0')
                    στέλνω(b'\t', b'GUI FOCUS 3')
                    στέλνω(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    στέλνω(b'q', b'jkoros-native> ')
                    επικύρωση_έκθεση['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Διεργασία.wait(timeout=10)
            # framebuffer 응답뿐 아니라 πραγματικός_δεδομένα scanout 픽셀도 확인한다.
            with απόσπασμα_οθόνης.open('rb') as Αρχείο_καταχώρηση:
                assert Αρχείο_καταχώρηση.readline().strip() == b'P6'
                치수 = Αρχείο_καταχώρηση.readline().strip()
                assert 치수 == b'640 480', 치수
                assert Αρχείο_καταχώρηση.readline().strip() == b'255'
                화소들 = Αρχείο_καταχώρηση.read()
            assert len(화소들) == 640 * 480 * 3
            def 화소(συντεταγμένη_x, κουμπί_Y_συντονισμός): return list(화소들[(κουμπί_Y_συντονισμός * 640 + συντεταγμένη_x) * 3:(κουμπί_Y_συντονισμός * 640 + συντεταγμένη_x) * 3 + 3])
            예제들 = {'background': 화소(5, 5), 'panel': 화소(45, 85), 'tile': 화소(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            επικύρωση_έκθεση.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((έργο_ρίζα / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Διεργασία.poll() is None:
                Διεργασία.terminate()
                try: Διεργασία.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Διεργασία.kill(); Διεργασία.wait(timeout=5)
            επιλογέας.close()
            Διεργασία.stdin.close(); Διεργασία.stdout.close()
            (출력결과 / 'serial.log').write_bytes(μεταγραφή)
            (출력결과 / 'report.json').write_text(json.dumps(επικύρωση_έκθεση, indent=2) + '\n')


if __name__ == '__main__':
    Εκτέλεση_2()
