#!/usr/bin/env python3
"""gangan_détà raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from ṣiṣẹ́_àṣẹ import 기준, Àṣẹ


def Rọ́ọ̀nù():
    출력결과 = 기준 / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    Àfọwọ́sí_ìjábọ̀ = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Àṣẹ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        Àfọwọ́sí_ìjábọ̀['command'] = 명령인수
        Ìlànà = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        olùyàn = selectors.DefaultSelector()
        olùyàn.register(Ìlànà.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, Ìtayọ_iye=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[Ìtayọ_iye:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in olùyàn.select(0.2):
                    détà_sèdíwọ = 누름값.fileobj.read(4096)
                    if détà_sèdíwọ:
                        대화기록.extend(détà_sèdíwọ)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if Ìlànà.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Ìlànà.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 gangan_détà GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(Ìwọ̀n):
                    결과 = b''
                    while len(결과) < Ìwọ̀n:
                        조각 = 화면접속자.recv(Ìwọ̀n - len(결과))
                        if not 조각: raise AssertionError('VNC disconnected')
                        결과 += 조각
                    return 결과
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                apèsè_iye = 정확한값(24)
                assert int.from_bytes(apèsè_iye[:2], 'big') == 640 and int.from_bytes(apèsè_iye[2:4], 'big') == 480
                정확한값(int.from_bytes(apèsè_iye[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for àṣẹ_báìtì, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                Ìtayọ_iye = len(대화기록)
                Ìlànà.stdin.write(àṣẹ_báìtì + b'\n')
                Ìlànà.stdin.flush()
                표시까지받기(b'jkoros-native> ', Ìtayọ_iye)
                assert 확인표시 in 대화기록[Ìtayọ_iye:], 확인표시
            def ṣẹ́ẹ̀lì(ìlà, 예상결과):
                Ìtayọ_iye = len(대화기록)
                Ìlànà.stdin.write(ìlà.encode('utf-8') + b'\n'); Ìlànà.stdin.flush()
                표시까지받기(b'jkoros-native> ', Ìtayọ_iye)
                응답자료 = bytes(대화기록[Ìtayọ_iye:])
                for SMS in 예상결과:
                    assert SMS.encode('utf-8') in 응답자료, (ìlà, SMS, 응답자료)
                return 응답자료
            def ṣàtẹ̀wọlé(ìlà, ìgún_ní_kẹ́ṣẹ́):
                Ìtayọ_iye = len(대화기록)
                Ìlànà.stdin.write(ìlà.encode('utf-8') + b'\n'); Ìlànà.stdin.flush()
                표시까지받기(ìgún_ní_kẹ́ṣẹ́, Ìtayọ_iye)
                return bytes(대화기록[Ìtayọ_iye:])
            def ṣàtúnṣe_iye(Orúkọ, Àkóónú_iye, paá_rẹ́_ìmú_ṣiṣẹ́=False):
                ṣàtẹ̀wọlé('edit ' + Orúkọ, b'edit> ')
                for ìlà in Àkóónú_iye.splitlines(): ṣàtẹ̀wọlé(ìlà, b'edit> ')
                if paá_rẹ́_ìmú_ṣiṣẹ́:
                    Ìtayọ_iye = len(대화기록)
                    Ìlànà.stdin.write(b'\x03'); Ìlànà.stdin.flush()
                    표시까지받기(b'jkoros-native> ', Ìtayọ_iye)
                    assert b'EDIT CANCELLED' in 대화기록[Ìtayọ_iye:]
                else:
                    assert b'SAVED' in ṣàtẹ̀wọlé('.', b'jkoros-native> ')
            def fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì(Orúkọ, détà):
                assert len(détà) <= 16384
                ṣàtẹ̀wọlé('load ' + Orúkọ, b'hex> ')
                for 순번 in range(0, len(détà), 64): ṣàtẹ̀wọlé(détà[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in ṣàtẹ̀wọlé('.', b'jkoros-native> ')
            def gbígbà_ẹ̀dà_fáìlì(Orúkọ):
                응답자료 = ṣẹ́ẹ̀lì('hex ' + Orúkọ, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                détà = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(détà) == int(일치.group(1)); return détà
            ṣẹ́ẹ̀lì('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            ṣẹ́ẹ̀lì('java -version', ['not OpenJDK', 'exit 0'])
            ṣẹ́ẹ̀lì('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            ṣẹ́ẹ̀lì('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            ṣẹ́ẹ̀lì('python --version', ['MicroPython 1.24.1', 'exit 0'])
            ṣẹ́ẹ̀lì('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Fáìlì', 'exit 0'])
            ṣẹ́ẹ̀lì('cat python.txt', ['한글 Fáìlì'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(gbígbà_ẹ̀dà_fáìlì('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            ṣàtúnṣe_iye('인사.java', 'public class 인사 { public static void main(String[] args) { int iye = 7; System.out.println("한글=" + iye); } }')
            ṣẹ́ẹ̀lì('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            ṣẹ́ẹ̀lì('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(gbígbà_ẹ̀dà_fáìlì('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            ṣàtúnṣe_iye('Hello.java', 'broken', paá_rẹ́_ìmú_ṣiṣẹ́=True)
            ṣẹ́ẹ̀lì('javac Hello.java', ['Compiled:', 'exit 0'])
            ṣàtúnṣe_iye('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            ṣẹ́ẹ̀lì('javac Broken.java', ['javac error:', 'exit 1'])
            fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            ṣẹ́ẹ̀lì('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            ṣẹ́ẹ̀lì('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            ṣẹ́ẹ̀lì('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            ṣẹ́ẹ̀lì('rm Imported.class', [])
            ṣàtúnṣe_iye('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            ṣẹ́ẹ̀lì('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = ṣẹ́ẹ̀lì('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            ṣẹ́ẹ̀lì('rm Loop.java', []); ṣẹ́ẹ̀lì('rm Loop.class', [])
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
            ṣàtúnṣe_iye('checks.py', 파이썬검사)
            ṣẹ́ẹ̀lì('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            ṣẹ́ẹ̀lì('rm checks.py', [])
            ṣàtúnṣe_iye('helper.py', 'value = 321')
            ṣẹ́ẹ̀lì("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            ṣẹ́ẹ̀lì('rm helper.py', [])
            ṣẹ́ẹ̀lì("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            ṣẹ́ẹ̀lì("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                ṣẹ́ẹ̀lì('python hello.py', ['한글 Fáìlì', 'exit 0'])
                ṣẹ́ẹ̀lì('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì('app.elf', (기준 / 'build/user/demo.elf').read_bytes())
            assert gbígbà_ẹ̀dà_fáìlì('app.elf') == (기준 / 'build/user/demo.elf').read_bytes()
            ṣẹ́ẹ̀lì('run app.elf', ['EL0 C++', 'exit 0'])
            fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì('app.elf', b'not an ELF')
            ṣẹ́ẹ̀lì('run app.elf', ['exit -8'])
            ṣẹ́ẹ̀lì('rm app.elf', [])
            ṣẹ́ẹ̀lì('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            íyàwòrán_ọ̀nà = 출력결과 / 'java-framebuffer'; íyàwòrán_ọ̀nà.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준 / 'dist/jkoros-native-korean.jar'), '-d', str(íyàwòrán_ọ̀nà), str(기준 / '시험/자바/화면시험.java')])
            fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì('화면시험.class', (íyàwòrán_ọ̀nà / '화면시험.class').read_bytes())
            ṣẹ́ẹ̀lì('java 화면시험', ['화면 ní_ṣókí 거부', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            ṣẹ́ẹ̀lì('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as aṣojú:
                aṣojú.settimeout(10)
                aṣojú.connect(str(모의제어경로))
                with aṣojú.makefile('rwb') as Stream_iye:
                    인사 = json.loads(Stream_iye.readline())
                    def 모의제어접속(ṣiṣẹ́_iṣẹ́, 전달인수=None):
                        Alásopọ̀_iṣé = {'execute': ṣiṣẹ́_iṣẹ́}
                        if 전달인수: Alásopọ̀_iṣé['arguments'] = 전달인수
                        Stream_iye.write((json.dumps(Alásopọ̀_iṣé) + '\n').encode())
                        Stream_iye.flush()
                        while True:
                            Fèsì = json.loads(Stream_iye.readline())
                            if 'error' in Fèsì: raise AssertionError(Fèsì)
                            if 'return' in Fèsì: return Fèsì['return']
                    모의제어접속('qmp_capabilities')
                    aṣòdiwọ̀n_agbàwòrán = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(aṣòdiwọ̀n_agbàwòrán), 'format': 'ppm'})
                    def 예제들(ọ̀nà, 지점들):
                        with ọ̀nà.open('rb') as píkísẹ̀_fáìlì:
                            assert píkísẹ̀_fáìlì.readline().strip() == b'P6'
                            assert píkísẹ̀_fáìlì.readline().strip() == b'640 480'
                            assert píkísẹ̀_fáìlì.readline().strip() == b'255'
                            píkísẹ̀_détà = píkísẹ̀_fáìlì.read()
                        assert len(píkísẹ̀_détà) == 640 * 480 * 3
                        return [list(píkísẹ̀_détà[(세로좌표 * 640 + ibi_ìtọ́kasí_x) * 3:(세로좌표 * 640 + ibi_ìtọ́kasí_x) * 3 + 3]) for ibi_ìtọ́kasí_x, 세로좌표 in 지점들]
                    assert 예제들(aṣòdiwọ̀n_agbàwòrán, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(aṣòdiwọ̀n_agbàwòrán, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def í_meèlì(누름값, 확인표시):
                        Ìtayọ_iye = len(대화기록)
                        Ìlànà.stdin.write(누름값); Ìlànà.stdin.flush()
                        표시까지받기(확인표시, Ìtayọ_iye)
                    í_meèlì(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    í_meèlì(b'\r', b'GUI ACTION 0 RESULT 0')
                    í_meèlì(b'\t', b'GUI FOCUS 1')
                    í_meèlì(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    í_meèlì(b'\t', b'GUI FOCUS 2')
                    í_meèlì(b'\r', b'GUI ACTION 2 RESULT 0')
                    í_meèlì(b'\t', b'GUI FOCUS 3')
                    í_meèlì(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    í_meèlì(b'q', b'jkoros-native> ')
                    Àfọwọ́sí_ìjábọ̀['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Ìlànà.wait(timeout=10)
            # framebuffer 응답뿐 아니라 gangan_détà scanout 픽셀도 확인한다.
            with aṣòdiwọ̀n_agbàwòrán.open('rb') as fáìlì_ìgbéwọlé:
                assert fáìlì_ìgbéwọlé.readline().strip() == b'P6'
                치수 = fáìlì_ìgbéwọlé.readline().strip()
                assert 치수 == b'640 480', 치수
                assert fáìlì_ìgbéwọlé.readline().strip() == b'255'
                화소들 = fáìlì_ìgbéwọlé.read()
            assert len(화소들) == 640 * 480 * 3
            def píkísẹ̀(ibi_ìtọ́kasí_x, 세로좌표): return list(화소들[(세로좌표 * 640 + ibi_ìtọ́kasí_x) * 3:(세로좌표 * 640 + ibi_ìtọ́kasí_x) * 3 + 3])
            예제들 = {'background': píkísẹ̀(5, 5), 'panel': píkísẹ̀(45, 85), 'tile': píkísẹ̀(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            Àfọwọ́sí_ìjábọ̀.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
            if Ìlànà.poll() is None:
                Ìlànà.terminate()
                try: Ìlànà.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Ìlànà.kill(); Ìlànà.wait(timeout=5)
            olùyàn.close()
            Ìlànà.stdin.close(); Ìlànà.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(Àfọwọ́sí_ìjábọ̀, indent=2) + '\n')


if __name__ == '__main__':
    Rọ́ọ̀nù()
