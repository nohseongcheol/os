#!/usr/bin/env python3
"""ڕاستەکی_دەیتا raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from جێبەجێکردن_فەرمان import 기준, فەرمان


def ڕادان():
    출력결과 = 기준 / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    ڕەواکردن_ڕاپۆرت = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = فەرمان() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        ڕەواکردن_ڕاپۆرت['command'] = 명령인수
        پرۆسە = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        هەڵبژێرەر = selectors.DefaultSelector()
        هەڵبژێرەر.register(پرۆسە.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, ئۆفسێت_نرخ=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[ئۆفسێت_نرخ:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in هەڵبژێرەر.select(0.2):
                    دەیتا_بلۆک_کردن = 누름값.fileobj.read(4096)
                    if دەیتا_بلۆک_کردن:
                        대화기록.extend(دەیتا_بلۆک_کردن)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if پرۆسە.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(پرۆسە.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 ڕاستەکی_دەیتا GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(گۆڕینی_ئەندازە):
                    결과 = b''
                    while len(결과) < گۆڕینی_ئەندازە:
                        조각 = 화면접속자.recv(گۆڕینی_ئەندازە - len(결과))
                        if not 조각: raise AssertionError('VNC disconnected')
                        결과 += 조각
                    return 결과
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                ڕاژەکار_نرخ = 정확한값(24)
                assert int.from_bytes(ڕاژەکار_نرخ[:2], 'big') == 640 and int.from_bytes(ڕاژەکار_نرخ[2:4], 'big') == 480
                정확한값(int.from_bytes(ڕاژەکار_نرخ[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for فەرمان_بایت, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                ئۆفسێت_نرخ = len(대화기록)
                پرۆسە.stdin.write(فەرمان_بایت + b'\n')
                پرۆسە.stdin.flush()
                표시까지받기(b'jkoros-native> ', ئۆفسێت_نرخ)
                assert 확인표시 in 대화기록[ئۆفسێت_نرخ:], 확인표시
            def توێکڵ(دێڕ, 예상결과):
                ئۆفسێت_نرخ = len(대화기록)
                پرۆسە.stdin.write(دێڕ.encode('utf-8') + b'\n'); پرۆسە.stdin.flush()
                표시까지받기(b'jkoros-native> ', ئۆفسێت_نرخ)
                응답자료 = bytes(대화기록[ئۆفسێت_نرخ:])
                for دەق in 예상결과:
                    assert دەق.encode('utf-8') in 응답자료, (دێڕ, دەق, 응답자료)
                return 응답자료
            def تێنووسین(دێڕ, برووسکە):
                ئۆفسێت_نرخ = len(대화기록)
                پرۆسە.stdin.write(دێڕ.encode('utf-8') + b'\n'); پرۆسە.stdin.flush()
                표시까지받기(برووسکە, ئۆفسێت_نرخ)
                return bytes(대화기록[ئۆفسێت_نرخ:])
            def بژار_نرخ(ناو, ناوەرۆک_نرخ, بەتاڵ_کردنەوە_کار=False):
                تێنووسین('edit ' + ناو, b'edit> ')
                for دێڕ in ناوەرۆک_نرخ.splitlines(): تێنووسین(دێڕ, b'edit> ')
                if بەتاڵ_کردنەوە_کار:
                    ئۆفسێت_نرخ = len(대화기록)
                    پرۆسە.stdin.write(b'\x03'); پرۆسە.stdin.flush()
                    표시까지받기(b'jkoros-native> ', ئۆفسێت_نرخ)
                    assert b'EDIT CANCELLED' in 대화기록[ئۆفسێت_نرخ:]
                else:
                    assert b'SAVED' in تێنووسین('.', b'jkoros-native> ')
            def بار_کردن_فایله_کان(ناو, دەیتا):
                assert len(دەیتا) <= 16384
                تێنووسین('load ' + ناو, b'hex> ')
                for 순번 in range(0, len(دەیتا), 64): تێنووسین(دەیتا[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in تێنووسین('.', b'jkoros-native> ')
            def داگرتن(ناو):
                응답자료 = توێکڵ('hex ' + ناو, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                دەیتا = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(دەیتا) == int(일치.group(1)); return دەیتا
            توێکڵ('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            توێکڵ('java -version', ['not OpenJDK', 'exit 0'])
            توێکڵ('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            توێکڵ('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            توێکڵ('python --version', ['MicroPython 1.24.1', 'exit 0'])
            توێکڵ('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 فایل', 'exit 0'])
            توێکڵ('cat python.txt', ['한글 فایل'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(داگرتن('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            بژار_نرخ('인사.java', 'public class 인사 { public static void main(String[] args) { int نرخ = 7; System.out.println("한글=" + نرخ); } }')
            توێکڵ('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            توێکڵ('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(داگرتن('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            بژار_نرخ('Hello.java', 'broken', بەتاڵ_کردنەوە_کار=True)
            توێکڵ('javac Hello.java', ['Compiled:', 'exit 0'])
            بژار_نرخ('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            توێکڵ('javac Broken.java', ['javac error:', 'exit 1'])
            بار_کردن_فایله_کان('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            توێکڵ('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            توێکڵ('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            بار_کردن_فایله_کان('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            توێکڵ('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            توێکڵ('rm Imported.class', [])
            بژار_نرخ('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            توێکڵ('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = توێکڵ('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            توێکڵ('rm Loop.java', []); توێکڵ('rm Loop.class', [])
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
            بژار_نرخ('checks.py', 파이썬검사)
            توێکڵ('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            توێکڵ('rm checks.py', [])
            بژار_نرخ('helper.py', 'value = 321')
            توێکڵ("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            توێکڵ('rm helper.py', [])
            توێکڵ("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            توێکڵ("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                توێکڵ('python hello.py', ['한글 فایل', 'exit 0'])
                توێکڵ('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            بار_کردن_فایله_کان('app.elf', (기준 / 'build/user/demo.elf').read_bytes())
            assert داگرتن('app.elf') == (기준 / 'build/user/demo.elf').read_bytes()
            توێکڵ('run app.elf', ['EL0 C++', 'exit 0'])
            بار_کردن_فایله_کان('app.elf', b'not an ELF')
            توێکڵ('run app.elf', ['exit -8'])
            توێکڵ('rm app.elf', [])
            توێکڵ('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            نگار_گوزەر = 출력결과 / 'java-framebuffer'; نگار_گوزەر.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준 / 'dist/jkoros-native-korean.jar'), '-d', str(نگار_گوزەر), str(기준 / '시험/자바/화면시험.java')])
            بار_کردن_فایله_کان('화면시험.class', (نگار_گوزەر / '화면시험.class').read_bytes())
            توێکڵ('java 화면시험', ['화면 کلیپ 거부', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            توێکڵ('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as کلایەنت:
                کلایەنت.settimeout(10)
                کلایەنت.connect(str(모의제어경로))
                with کلایەنت.makefile('rwb') as Stream_نرخ:
                    인사 = json.loads(Stream_نرخ.readline())
                    def 모의제어접속(جێبەجێکردن_ئەرک, 전달인수=None):
                        تۆڕ_پەیام = {'execute': جێبەجێکردن_ئەرک}
                        if 전달인수: تۆڕ_پەیام['arguments'] = 전달인수
                        Stream_نرخ.write((json.dumps(تۆڕ_پەیام) + '\n').encode())
                        Stream_نرخ.flush()
                        while True:
                            وەڵامدانەوه = json.loads(Stream_نرخ.readline())
                            if 'error' in وەڵامدانەوه: raise AssertionError(وەڵامدانەوه)
                            if 'return' in وەڵامدانەوه: return وەڵامدانەوه['return']
                    모의제어접속('qmp_capabilities')
                    وێنەی_شاشە = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(وێنەی_شاشە), 'format': 'ppm'})
                    def 예제들(گوزەر, 지점들):
                        with گوزەر.open('rb') as پێڵ_فایل:
                            assert پێڵ_فایل.readline().strip() == b'P6'
                            assert پێڵ_فایل.readline().strip() == b'640 480'
                            assert پێڵ_فایل.readline().strip() == b'255'
                            پێڵ_دەیتا = پێڵ_فایل.read()
                        assert len(پێڵ_دەیتا) == 640 * 480 * 3
                        return [list(پێڵ_دەیتا[(세로좌표 * 640 + پۆوتانی_x) * 3:(세로좌표 * 640 + پۆوتانی_x) * 3 + 3]) for پۆوتانی_x, 세로좌표 in 지점들]
                    assert 예제들(وێنەی_شاشە, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(وێنەی_شاشە, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def ناردن(누름값, 확인표시):
                        ئۆفسێت_نرخ = len(대화기록)
                        پرۆسە.stdin.write(누름값); پرۆسە.stdin.flush()
                        표시까지받기(확인표시, ئۆفسێت_نرخ)
                    ناردن(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    ناردن(b'\r', b'GUI ACTION 0 RESULT 0')
                    ناردن(b'\t', b'GUI FOCUS 1')
                    ناردن(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    ناردن(b'\t', b'GUI FOCUS 2')
                    ناردن(b'\r', b'GUI ACTION 2 RESULT 0')
                    ناردن(b'\t', b'GUI FOCUS 3')
                    ناردن(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    ناردن(b'q', b'jkoros-native> ')
                    ڕەواکردن_ڕاپۆرت['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            پرۆسە.wait(timeout=10)
            # framebuffer 응답뿐 아니라 ڕاستەکی_دەیتا scanout 픽셀도 확인한다.
            with وێنەی_شاشە.open('rb') as فایل_تێنووسین:
                assert فایل_تێنووسین.readline().strip() == b'P6'
                치수 = فایل_تێنووسین.readline().strip()
                assert 치수 == b'640 480', 치수
                assert فایل_تێنووسین.readline().strip() == b'255'
                화소들 = فایل_تێنووسین.read()
            assert len(화소들) == 640 * 480 * 3
            def پێڵ(پۆوتانی_x, 세로좌표): return list(화소들[(세로좌표 * 640 + پۆوتانی_x) * 3:(세로좌표 * 640 + پۆوتانی_x) * 3 + 3])
            예제들 = {'background': پێڵ(5, 5), 'panel': پێڵ(45, 85), 'tile': پێڵ(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            ڕەواکردن_ڕاپۆرت.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
            if پرۆسە.poll() is None:
                پرۆسە.terminate()
                try: پرۆسە.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    پرۆسە.kill(); پرۆسە.wait(timeout=5)
            هەڵبژێرەر.close()
            پرۆسە.stdin.close(); پرۆسە.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(ڕەواکردن_ڕاپۆرت, indent=2) + '\n')


if __name__ == '__main__':
    ڕادان()
