#!/usr/bin/env python3
"""ຕົວ_ຈິງ_ຂໍ້ມູນ raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ import ໂຄງ_ການ_ເລກຮາກ, ຄໍາສັ່ງ_1f12b8e2


def ແລ່ນ():
    출력결과 = ໂຄງ_ການ_ເລກຮາກ / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    ໃຊ້ໄດ້_ລາຍງານ = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = ຄໍາສັ່ງ_1f12b8e2() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        ໃຊ້ໄດ້_ລາຍງານ['command'] = 명령인수
        ຂະ_ບວນ_ການ = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        ຕົວ_ໃຊ້_ເລືອກ = selectors.DefaultSelector()
        ຕົວ_ໃຊ້_ເລືອກ.register(ຂະ_ບວນ_ການ.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, ອອບເຊັດ_ຄ່າ=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[ອອບເຊັດ_ຄ່າ:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in ຕົວ_ໃຊ້_ເລືອກ.select(0.2):
                    ຂໍ້ມູນ_ບລັອກ = 누름값.fileobj.read(4096)
                    if ຂໍ້ມູນ_ບລັອກ:
                        대화기록.extend(ຂໍ້ມູນ_ບລັອກ)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if ຂະ_ບວນ_ການ.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(ຂະ_ບວນ_ການ.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 ຕົວ_ຈິງ_ຂໍ້ມູນ GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(ຂະ_ຫນາດ):
                    ມາດຕະການ = b''
                    while len(ມາດຕະການ) < ຂະ_ຫນາດ:
                        조각 = 화면접속자.recv(ຂະ_ຫນາດ - len(ມາດຕະການ))
                        if not 조각: raise AssertionError('VNC disconnected')
                        ມາດຕະການ += 조각
                    return ມາດຕະການ
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                서버 = 정확한값(24)
                assert int.from_bytes(서버[:2], 'big') == 640 and int.from_bytes(서버[2:4], 'big') == 480
                정확한값(int.from_bytes(서버[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for ຄໍາສັ່ງ_ໄບ, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                ອອບເຊັດ_ຄ່າ = len(대화기록)
                ຂະ_ບວນ_ການ.stdin.write(ຄໍາສັ່ງ_ໄບ + b'\n')
                ຂະ_ບວນ_ການ.stdin.flush()
                표시까지받기(b'jkoros-native> ', ອອບເຊັດ_ຄ່າ)
                assert 확인표시 in 대화기록[ອອບເຊັດ_ຄ່າ:], 확인표시
            def ເຊລ(ສາຍ, 예상결과):
                ອອບເຊັດ_ຄ່າ = len(대화기록)
                ຂະ_ບວນ_ການ.stdin.write(ສາຍ.encode('utf-8') + b'\n'); ຂະ_ບວນ_ການ.stdin.flush()
                표시까지받기(b'jkoros-native> ', ອອບເຊັດ_ຄ່າ)
                응답자료 = bytes(대화기록[ອອບເຊັດ_ຄ່າ:])
                for ຂໍ້ຄວາມ in 예상결과:
                    assert ຂໍ້ຄວາມ.encode('utf-8') in 응답자료, (ສາຍ, ຂໍ້ຄວາມ, 응답자료)
                return 응답자료
            def ປ້ອນ_ເຂົ້າ(ສາຍ, ພຣອມ):
                ອອບເຊັດ_ຄ່າ = len(대화기록)
                ຂະ_ບວນ_ການ.stdin.write(ສາຍ.encode('utf-8') + b'\n'); ຂະ_ບວນ_ການ.stdin.flush()
                표시까지받기(ພຣອມ, ອອບເຊັດ_ຄ່າ)
                return bytes(대화기록[ອອບເຊັດ_ຄ່າ:])
            def ແກ້ໄຂ_ຄ່າ(ຊື່, ເນື້ອໃນ_ຄ່າ_cb0f2404, ຍົກເລີກ_ການຄໍານວນ=False):
                ປ້ອນ_ເຂົ້າ('edit ' + ຊື່, b'edit> ')
                for ສາຍ in ເນື້ອໃນ_ຄ່າ_cb0f2404.splitlines(): ປ້ອນ_ເຂົ້າ(ສາຍ, b'edit> ')
                if ຍົກເລີກ_ການຄໍານວນ:
                    ອອບເຊັດ_ຄ່າ = len(대화기록)
                    ຂະ_ບວນ_ການ.stdin.write(b'\x03'); ຂະ_ບວນ_ການ.stdin.flush()
                    표시까지받기(b'jkoros-native> ', ອອບເຊັດ_ຄ່າ)
                    assert b'EDIT CANCELLED' in 대화기록[ອອບເຊັດ_ຄ່າ:]
                else:
                    assert b'SAVED' in ປ້ອນ_ເຂົ້າ('.', b'jkoros-native> ')
            def ໂອນອອກ_ໄຟລ໌(ຊື່, ຂໍ້ມູນ):
                assert len(ຂໍ້ມູນ) <= 16384
                ປ້ອນ_ເຂົ້າ('load ' + ຊື່, b'hex> ')
                for 순번 in range(0, len(ຂໍ້ມູນ), 64): ປ້ອນ_ເຂົ້າ(ຂໍ້ມູນ[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in ປ້ອນ_ເຂົ້າ('.', b'jkoros-native> ')
            def ດາວໂຫຼດ(ຊື່):
                응답자료 = ເຊລ('hex ' + ຊື່, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                ຂໍ້ມູນ = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(ຂໍ້ມູນ) == int(일치.group(1)); return ຂໍ້ມູນ
            ເຊລ('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            ເຊລ('java -version', ['not OpenJDK', 'exit 0'])
            ເຊລ('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            ເຊລ('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            ເຊລ('python --version', ['MicroPython 1.24.1', 'exit 0'])
            ເຊລ('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 ຟາຍ', 'exit 0'])
            ເຊລ('cat python.txt', ['한글 ຟາຍ'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(ດາວໂຫຼດ('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            ແກ້ໄຂ_ຄ່າ('인사.java', 'public class 인사 { public static void main(String[] args) { int ຄ່າ = 7; System.out.println("한글=" + ຄ່າ); } }')
            ເຊລ('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            ເຊລ('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(ດາວໂຫຼດ('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            ແກ້ໄຂ_ຄ່າ('Hello.java', 'broken', ຍົກເລີກ_ການຄໍານວນ=True)
            ເຊລ('javac Hello.java', ['Compiled:', 'exit 0'])
            ແກ້ໄຂ_ຄ່າ('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            ເຊລ('javac Broken.java', ['javac error:', 'exit 1'])
            ໂອນອອກ_ໄຟລ໌('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            ເຊລ('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            ເຊລ('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            ໂອນອອກ_ໄຟລ໌('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            ເຊລ('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            ເຊລ('rm Imported.class', [])
            ແກ້ໄຂ_ຄ່າ('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            ເຊລ('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = ເຊລ('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            ເຊລ('rm Loop.java', []); ເຊລ('rm Loop.class', [])
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
            ແກ້ໄຂ_ຄ່າ('checks.py', 파이썬검사)
            ເຊລ('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            ເຊລ('rm checks.py', [])
            ແກ້ໄຂ_ຄ່າ('helper.py', 'value = 321')
            ເຊລ("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            ເຊລ('rm helper.py', [])
            ເຊລ("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            ເຊລ("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                ເຊລ('python hello.py', ['한글 ຟາຍ', 'exit 0'])
                ເຊລ('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            ໂອນອອກ_ໄຟລ໌('app.elf', (ໂຄງ_ການ_ເລກຮາກ / 'build/user/demo.elf').read_bytes())
            assert ດາວໂຫຼດ('app.elf') == (ໂຄງ_ການ_ເລກຮາກ / 'build/user/demo.elf').read_bytes()
            ເຊລ('run app.elf', ['EL0 C++', 'exit 0'])
            ໂອນອອກ_ໄຟລ໌('app.elf', b'not an ELF')
            ເຊລ('run app.elf', ['exit -8'])
            ເຊລ('rm app.elf', [])
            ເຊລ('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            ການ_ແຕ້ມ_ທາງໂຄຈອນ = 출력결과 / 'java-framebuffer'; ການ_ແຕ້ມ_ທາງໂຄຈອນ.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(ໂຄງ_ການ_ເລກຮາກ / 'dist/jkoros-native-korean.jar'), '-d', str(ການ_ແຕ້ມ_ທາງໂຄຈອນ), str(ໂຄງ_ການ_ເລກຮາກ / '시험/자바/화면시험.java')])
            ໂອນອອກ_ໄຟລ໌('화면시험.class', (ການ_ແຕ້ມ_ທາງໂຄຈອນ / '화면시험.class').read_bytes())
            ເຊລ('java 화면시험', ['화면 ຄ_ລິບ ປະຕິເສດ_ຄ່າ', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            ເຊລ('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as ລູກຂ່າຍ:
                ລູກຂ່າຍ.settimeout(10)
                ລູກຂ່າຍ.connect(str(모의제어경로))
                with ລູກຂ່າຍ.makefile('rwb') as ສະຕຣີມ_ຄ່າ:
                    인사 = json.loads(ສະຕຣີມ_ຄ່າ.readline())
                    def 모의제어접속(ປະ_ຕິ_ບັດ_ຫນ້າວຽກ, 전달인수=None):
                        ເຄືອຂ່າຍ_ອີເມວ = {'execute': ປະ_ຕິ_ບັດ_ຫນ້າວຽກ}
                        if 전달인수: ເຄືອຂ່າຍ_ອີເມວ['arguments'] = 전달인수
                        ສະຕຣີມ_ຄ່າ.write((json.dumps(ເຄືອຂ່າຍ_ອີເມວ) + '\n').encode())
                        ສະຕຣີມ_ຄ່າ.flush()
                        while True:
                            ຕອບກັບ = json.loads(ສະຕຣີມ_ຄ່າ.readline())
                            if 'error' in ຕອບກັບ: raise AssertionError(ຕອບກັບ)
                            if 'return' in ຕອບກັບ: return ຕອບກັບ['return']
                    모의제어접속('qmp_capabilities')
                    ພາບຫນ້າຈໍ = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(ພາບຫນ້າຈໍ), 'format': 'ppm'})
                    def 예제들(ທາງໂຄຈອນ, 지점들):
                        with ທາງໂຄຈອນ.open('rb') as ເປ_ລ_ຟາຍ:
                            assert ເປ_ລ_ຟາຍ.readline().strip() == b'P6'
                            assert ເປ_ລ_ຟາຍ.readline().strip() == b'640 480'
                            assert ເປ_ລ_ຟາຍ.readline().strip() == b'255'
                            ເປ_ລ_ຂໍ້ມູນ = ເປ_ລ_ຟາຍ.read()
                        assert len(ເປ_ລ_ຂໍ້ມູນ) == 640 * 480 * 3
                        return [list(ເປ_ລ_ຂໍ້ມູນ[(ປຸ່ມ_Y_ຈຸດປະສານ * 640 + ຈຸດ_ພິ_ກັດ_x) * 3:(ປຸ່ມ_Y_ຈຸດປະສານ * 640 + ຈຸດ_ພິ_ກັດ_x) * 3 + 3]) for ຈຸດ_ພິ_ກັດ_x, ປຸ່ມ_Y_ຈຸດປະສານ in 지점들]
                    assert 예제들(ພາບຫນ້າຈໍ, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(ພາບຫນ້າຈໍ, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def ສົ່ງ(누름값, 확인표시):
                        ອອບເຊັດ_ຄ່າ = len(대화기록)
                        ຂະ_ບວນ_ການ.stdin.write(누름값); ຂະ_ບວນ_ການ.stdin.flush()
                        표시까지받기(확인표시, ອອບເຊັດ_ຄ່າ)
                    ສົ່ງ(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    ສົ່ງ(b'\r', b'GUI ACTION 0 RESULT 0')
                    ສົ່ງ(b'\t', b'GUI FOCUS 1')
                    ສົ່ງ(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    ສົ່ງ(b'\t', b'GUI FOCUS 2')
                    ສົ່ງ(b'\r', b'GUI ACTION 2 RESULT 0')
                    ສົ່ງ(b'\t', b'GUI FOCUS 3')
                    ສົ່ງ(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    ສົ່ງ(b'q', b'jkoros-native> ')
                    ໃຊ້ໄດ້_ລາຍງານ['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            ຂະ_ບວນ_ການ.wait(timeout=10)
            # framebuffer 응답뿐 아니라 ຕົວ_ຈິງ_ຂໍ້ມູນ scanout 픽셀도 확인한다.
            with ພາບຫນ້າຈໍ.open('rb') as ຟາຍ_ເຂົ້າໃນ:
                assert ຟາຍ_ເຂົ້າໃນ.readline().strip() == b'P6'
                치수 = ຟາຍ_ເຂົ້າໃນ.readline().strip()
                assert 치수 == b'640 480', 치수
                assert ຟາຍ_ເຂົ້າໃນ.readline().strip() == b'255'
                화소들 = ຟາຍ_ເຂົ້າໃນ.read()
            assert len(화소들) == 640 * 480 * 3
            def ເປ_ລ(ຈຸດ_ພິ_ກັດ_x, ປຸ່ມ_Y_ຈຸດປະສານ): return list(화소들[(ປຸ່ມ_Y_ຈຸດປະສານ * 640 + ຈຸດ_ພິ_ກັດ_x) * 3:(ປຸ່ມ_Y_ຈຸດປະສານ * 640 + ຈຸດ_ພິ_ກັດ_x) * 3 + 3])
            예제들 = {'background': ເປ_ລ(5, 5), 'panel': ເປ_ລ(45, 85), 'tile': ເປ_ລ(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            ໃຊ້ໄດ້_ລາຍງານ.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((ໂຄງ_ການ_ເລກຮາກ / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if ຂະ_ບວນ_ການ.poll() is None:
                ຂະ_ບວນ_ການ.terminate()
                try: ຂະ_ບວນ_ການ.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    ຂະ_ບວນ_ການ.kill(); ຂະ_ບວນ_ການ.wait(timeout=5)
            ຕົວ_ໃຊ້_ເລືອກ.close()
            ຂະ_ບວນ_ການ.stdin.close(); ຂະ_ບວນ_ການ.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(ໃຊ້ໄດ້_ລາຍງານ, indent=2) + '\n')


if __name__ == '__main__':
    ແລ່ນ()
