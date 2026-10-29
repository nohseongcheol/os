#!/usr/bin/env python3
"""իրական_տվյալ raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from կատարել_հրաման import արձակել_արմատ, Հրահանգ


def Գործարկել():
    출력결과 = արձակել_արմատ / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    վավերացում_զեկույց = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Հրահանգ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        վավերացում_զեկույց['command'] = 명령인수
        Գործընթաց = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        ընտրիչ = selectors.DefaultSelector()
        ընտրիչ.register(Գործընթաց.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, Տեղաշարժում_արժեք=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[Տեղաշարժում_արժեք:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in ընտրիչ.select(0.2):
                    տվյալ_արգելափակել = 누름값.fileobj.read(4096)
                    if տվյալ_արգելափակել:
                        대화기록.extend(տվյալ_արգելափակել)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if Գործընթաց.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Գործընթաց.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 իրական_տվյալ GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(Չափս):
                    չափ = b''
                    while len(չափ) < Չափս:
                        조각 = 화면접속자.recv(Չափս - len(չափ))
                        if not 조각: raise AssertionError('VNC disconnected')
                        չափ += 조각
                    return չափ
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                սպասարկիչ_արժեք = 정확한값(24)
                assert int.from_bytes(սպասարկիչ_արժեք[:2], 'big') == 640 and int.from_bytes(սպասարկիչ_արժեք[2:4], 'big') == 480
                정확한값(int.from_bytes(սպասարկիչ_արժեք[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for հրաման_բայթ, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                Տեղաշարժում_արժեք = len(대화기록)
                Գործընթաց.stdin.write(հրաման_բայթ + b'\n')
                Գործընթաց.stdin.flush()
                표시까지받기(b'jkoros-native> ', Տեղաշարժում_արժեք)
                assert 확인표시 in 대화기록[Տեղաշարժում_արժեք:], 확인표시
            def խեցի(կապ, 예상결과):
                Տեղաշարժում_արժեք = len(대화기록)
                Գործընթաց.stdin.write(կապ.encode('utf-8') + b'\n'); Գործընթաց.stdin.flush()
                표시까지받기(b'jkoros-native> ', Տեղաշարժում_արժեք)
                응답자료 = bytes(대화기록[Տեղաշարժում_արժեք:])
                for Տեքստ in 예상결과:
                    assert Տեքստ.encode('utf-8') in 응답자료, (կապ, Տեքստ, 응답자료)
                return 응답자료
            def մուտքագրել(կապ, հուշում):
                Տեղաշարժում_արժեք = len(대화기록)
                Գործընթաց.stdin.write(կապ.encode('utf-8') + b'\n'); Գործընթաց.stdin.flush()
                표시까지받기(հուշում, Տեղաշարժում_արժեք)
                return bytes(대화기록[Տեղաշարժում_արժեք:])
            def խմբագրել_արժեք(Անուն, Բովանդակություն_արժեք, ապընտրել_գործողություն=False):
                մուտքագրել('edit ' + Անուն, b'edit> ')
                for կապ in Բովանդակություն_արժեք.splitlines(): մուտքագրել(կապ, b'edit> ')
                if ապընտրել_գործողություն:
                    Տեղաշարժում_արժեք = len(대화기록)
                    Գործընթաց.stdin.write(b'\x03'); Գործընթաց.stdin.flush()
                    표시까지받기(b'jkoros-native> ', Տեղաշարժում_արժեք)
                    assert b'EDIT CANCELLED' in 대화기록[Տեղաշարժում_արժեք:]
                else:
                    assert b'SAVED' in մուտքագրել('.', b'jkoros-native> ')
            def վերբեռնել_Նիշքեր(Անուն, տվյալ):
                assert len(տվյալ) <= 16384
                մուտքագրել('load ' + Անուն, b'hex> ')
                for 순번 in range(0, len(տվյալ), 64): մուտքագրել(տվյալ[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in մուտքագրել('.', b'jkoros-native> ')
            def ներբեռնել(Անուն):
                응답자료 = խեցի('hex ' + Անուն, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                տվյալ = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(տվյալ) == int(일치.group(1)); return տվյալ
            խեցի('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            խեցի('java -version', ['not OpenJDK', 'exit 0'])
            խեցի('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            խեցի('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            խեցի('python --version', ['MicroPython 1.24.1', 'exit 0'])
            խեցի('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Ֆայլ', 'exit 0'])
            խեցի('cat python.txt', ['한글 Ֆայլ'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(ներբեռնել('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            խմբագրել_արժեք('인사.java', 'public class 인사 { public static void main(String[] args) { int արժեք = 7; System.out.println("한글=" + արժեք); } }')
            խեցի('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            խեցի('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(ներբեռնել('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            խմբագրել_արժեք('Hello.java', 'broken', ապընտրել_գործողություն=True)
            խեցի('javac Hello.java', ['Compiled:', 'exit 0'])
            խմբագրել_արժեք('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            խեցի('javac Broken.java', ['javac error:', 'exit 1'])
            վերբեռնել_Նիշքեր('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            խեցի('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            խեցի('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            վերբեռնել_Նիշքեր('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            խեցի('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            խեցի('rm Imported.class', [])
            խմբագրել_արժեք('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            խեցի('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = խեցի('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            խեցի('rm Loop.java', []); խեցի('rm Loop.class', [])
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
            խմբագրել_արժեք('checks.py', 파이썬검사)
            խեցի('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            խեցի('rm checks.py', [])
            խմբագրել_արժեք('helper.py', 'value = 321')
            խեցի("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            խեցի('rm helper.py', [])
            խեցի("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            խեցի("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                խեցի('python hello.py', ['한글 Ֆայլ', 'exit 0'])
                խեցի('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            վերբեռնել_Նիշքեր('app.elf', (արձակել_արմատ / 'build/user/demo.elf').read_bytes())
            assert ներբեռնել('app.elf') == (արձակել_արմատ / 'build/user/demo.elf').read_bytes()
            խեցի('run app.elf', ['EL0 C++', 'exit 0'])
            վերբեռնել_Նիշքեր('app.elf', b'not an ELF')
            խեցի('run app.elf', ['exit -8'])
            խեցի('rm app.elf', [])
            խեցի('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            նկար_ուղի = 출력결과 / 'java-framebuffer'; նկար_ուղի.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(արձակել_արմատ / 'dist/jkoros-native-korean.jar'), '-d', str(նկար_ուղի), str(արձակել_արմատ / '시험/자바/화면시험.java')])
            վերբեռնել_Նիշքեր('화면시험.class', (նկար_ուղի / '화면시험.class').read_bytes())
            խեցի('java 화면시험', ['화면 հոլովակ 거부', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            խեցի('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as սպասառու:
                սպասառու.settimeout(10)
                սպասառու.connect(str(모의제어경로))
                with սպասառու.makefile('rwb') as հոսք_արժեք:
                    인사 = json.loads(հոսք_արժեք.readline())
                    def 모의제어접속(Կատարել, 전달인수=None):
                        Ցանց_ուղերձ = {'execute': Կատարել}
                        if 전달인수: Ցանց_ուղերձ['arguments'] = 전달인수
                        հոսք_արժեք.write((json.dumps(Ցանց_ուղերձ) + '\n').encode())
                        հոսք_արժեք.flush()
                        while True:
                            պատասխանել = json.loads(հոսք_արժեք.readline())
                            if 'error' in պատասխանել: raise AssertionError(պատասխանել)
                            if 'return' in պատասխանել: return պատասխանել['return']
                    모의제어접속('qmp_capabilities')
                    էկրանի_պատկեր = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(էկրանի_պատկեր), 'format': 'ppm'})
                    def 예제들(Ճանապարհ, 지점들):
                        with Ճանապարհ.open('rb') as փիքսել_նիշք:
                            assert փիքսել_նիշք.readline().strip() == b'P6'
                            assert փիքսել_նիշք.readline().strip() == b'640 480'
                            assert փիքսել_նիշք.readline().strip() == b'255'
                            փիքսել_տվյալ = փիքսել_նիշք.read()
                        assert len(փիքսել_տվյալ) == 640 * 480 * 3
                        return [list(փիքսել_տվյալ[(세로좌표 * 640 + x_կոորդինատ) * 3:(세로좌표 * 640 + x_կոորդինատ) * 3 + 3]) for x_կոորդինատ, 세로좌표 in 지점들]
                    assert 예제들(էկրանի_պատկեր, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(էկրանի_պատկեր, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def ուղարկել(누름값, 확인표시):
                        Տեղաշարժում_արժեք = len(대화기록)
                        Գործընթաց.stdin.write(누름값); Գործընթաց.stdin.flush()
                        표시까지받기(확인표시, Տեղաշարժում_արժեք)
                    ուղարկել(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    ուղարկել(b'\r', b'GUI ACTION 0 RESULT 0')
                    ուղարկել(b'\t', b'GUI FOCUS 1')
                    ուղարկել(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    ուղարկել(b'\t', b'GUI FOCUS 2')
                    ուղարկել(b'\r', b'GUI ACTION 2 RESULT 0')
                    ուղարկել(b'\t', b'GUI FOCUS 3')
                    ուղարկել(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    ուղարկել(b'q', b'jkoros-native> ')
                    վավերացում_զեկույց['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Գործընթաց.wait(timeout=10)
            # framebuffer 응답뿐 아니라 իրական_տվյալ scanout 픽셀도 확인한다.
            with էկրանի_պատկեր.open('rb') as նիշք_մուտքագրում:
                assert նիշք_մուտքագրում.readline().strip() == b'P6'
                치수 = նիշք_մուտքագրում.readline().strip()
                assert 치수 == b'640 480', 치수
                assert նիշք_մուտքագրում.readline().strip() == b'255'
                화소들 = նիշք_մուտքագրում.read()
            assert len(화소들) == 640 * 480 * 3
            def փիքսել(x_կոորդինատ, 세로좌표): return list(화소들[(세로좌표 * 640 + x_կոորդինատ) * 3:(세로좌표 * 640 + x_կոորդինատ) * 3 + 3])
            예제들 = {'background': փիքսել(5, 5), 'panel': փիքսել(45, 85), 'tile': փիքսել(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            վավերացում_զեկույց.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((արձակել_արմատ / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Գործընթաց.poll() is None:
                Գործընթաց.terminate()
                try: Գործընթաց.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Գործընթաց.kill(); Գործընթաց.wait(timeout=5)
            ընտրիչ.close()
            Գործընթաց.stdin.close(); Գործընթաց.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(վավերացում_զեկույց, indent=2) + '\n')


if __name__ == '__main__':
    Գործարկել()
