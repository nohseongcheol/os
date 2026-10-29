#!/usr/bin/env python3
"""tūturu_raraunga raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from kawe_tono import whakaatu_pūtake, tono


def whakahaere():
    출력결과 = whakaatu_pūtake / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    whakamana_pūrongo = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = tono() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        whakamana_pūrongo['command'] = 명령인수
        Hātepe = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        pūtīpako = selectors.DefaultSelector()
        pūtīpako.register(Hātepe.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, OFFSET_uara=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[OFFSET_uara:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in pūtīpako.select(0.2):
                    raraunga_aukati = 누름값.fileobj.read(4096)
                    if raraunga_aukati:
                        대화기록.extend(raraunga_aukati)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if Hātepe.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Hātepe.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 tūturu_raraunga GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def EXACT_uara(rahi):
                    mēhua = b''
                    while len(mēhua) < rahi:
                        조각 = 화면접속자.recv(rahi - len(mēhua))
                        if not 조각: raise AssertionError('VNC disconnected')
                        mēhua += 조각
                    return mēhua
                assert EXACT_uara(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in EXACT_uara(EXACT_uara(1)[0]); 화면접속자.sendall(b'\x01')
                assert EXACT_uara(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                tūmau_uara = EXACT_uara(24)
                assert int.from_bytes(tūmau_uara[:2], 'big') == 640 and int.from_bytes(tūmau_uara[2:4], 'big') == 480
                EXACT_uara(int.from_bytes(tūmau_uara[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for tono_paita, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                OFFSET_uara = len(대화기록)
                Hātepe.stdin.write(tono_paita + b'\n')
                Hātepe.stdin.flush()
                표시까지받기(b'jkoros-native> ', OFFSET_uara)
                assert 확인표시 in 대화기록[OFFSET_uara:], 확인표시
            def anga(hononga, 예상결과):
                OFFSET_uara = len(대화기록)
                Hātepe.stdin.write(hononga.encode('utf-8') + b'\n'); Hātepe.stdin.flush()
                표시까지받기(b'jkoros-native> ', OFFSET_uara)
                응답자료 = bytes(대화기록[OFFSET_uara:])
                for Ngā_kupu in 예상결과:
                    assert Ngā_kupu.encode('utf-8') in 응답자료, (hononga, Ngā_kupu, 응답자료)
                return 응답자료
            def tāuru(hononga, tohuaki):
                OFFSET_uara = len(대화기록)
                Hātepe.stdin.write(hononga.encode('utf-8') + b'\n'); Hātepe.stdin.flush()
                표시까지받기(tohuaki, OFFSET_uara)
                return bytes(대화기록[OFFSET_uara:])
            def whakatika_uara(Ingoa, Ihirangi_uara, whakakore_mahi=False):
                tāuru('edit ' + Ingoa, b'edit> ')
                for hononga in Ihirangi_uara.splitlines(): tāuru(hononga, b'edit> ')
                if whakakore_mahi:
                    OFFSET_uara = len(대화기록)
                    Hātepe.stdin.write(b'\x03'); Hātepe.stdin.flush()
                    표시까지받기(b'jkoros-native> ', OFFSET_uara)
                    assert b'EDIT CANCELLED' in 대화기록[OFFSET_uara:]
                else:
                    assert b'SAVED' in tāuru('.', b'jkoros-native> ')
            def tukuatu_Ngā_Kōnae(Ingoa, raraunga):
                assert len(raraunga) <= 16384
                tāuru('load ' + Ingoa, b'hex> ')
                for 순번 in range(0, len(raraunga), 64): tāuru(raraunga[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in tāuru('.', b'jkoros-native> ')
            def tikiake(Ingoa):
                응답자료 = anga('hex ' + Ingoa, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                raraunga = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(raraunga) == int(일치.group(1)); return raraunga
            anga('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            anga('java -version', ['not OpenJDK', 'exit 0'])
            anga('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            anga('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            anga('python --version', ['MicroPython 1.24.1', 'exit 0'])
            anga('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Kōnae', 'exit 0'])
            anga('cat python.txt', ['한글 Kōnae'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(tikiake('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            whakatika_uara('인사.java', 'public class 인사 { public static void main(String[] args) { int uara = 7; System.out.println("한글=" + uara); } }')
            anga('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            anga('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(tikiake('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            whakatika_uara('Hello.java', 'broken', whakakore_mahi=True)
            anga('javac Hello.java', ['Compiled:', 'exit 0'])
            whakatika_uara('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            anga('javac Broken.java', ['javac error:', 'exit 1'])
            tukuatu_Ngā_Kōnae('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            anga('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            anga('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            tukuatu_Ngā_Kōnae('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            anga('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            anga('rm Imported.class', [])
            whakatika_uara('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            anga('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = anga('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            anga('rm Loop.java', []); anga('rm Loop.class', [])
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
            whakatika_uara('checks.py', 파이썬검사)
            anga('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            anga('rm checks.py', [])
            whakatika_uara('helper.py', 'value = 321')
            anga("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            anga('rm helper.py', [])
            anga("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            anga("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                anga('python hello.py', ['한글 Kōnae', 'exit 0'])
                anga('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            tukuatu_Ngā_Kōnae('app.elf', (whakaatu_pūtake / 'build/user/demo.elf').read_bytes())
            assert tikiake('app.elf') == (whakaatu_pūtake / 'build/user/demo.elf').read_bytes()
            anga('run app.elf', ['EL0 C++', 'exit 0'])
            tukuatu_Ngā_Kōnae('app.elf', b'not an ELF')
            anga('run app.elf', ['exit -8'])
            anga('rm app.elf', [])
            anga('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            tātuhi_ara = 출력결과 / 'java-framebuffer'; tātuhi_ara.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(whakaatu_pūtake / 'dist/jkoros-native-korean.jar'), '-d', str(tātuhi_ara), str(whakaatu_pūtake / '시험/자바/화면시험.java')])
            tukuatu_Ngā_Kōnae('화면시험.class', (tātuhi_ara / '화면시험.class').read_bytes())
            anga('java 화면시험', ['화면 topenga 거부', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            anga('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as kiritaki:
                kiritaki.settimeout(10)
                kiritaki.connect(str(모의제어경로))
                with kiritaki.makefile('rwb') as roma_uara:
                    인사 = json.loads(roma_uara.readline())
                    def 모의제어접속(kawe_tūmahi, 전달인수=None):
                        whatunga_karere = {'execute': kawe_tūmahi}
                        if 전달인수: whatunga_karere['arguments'] = 전달인수
                        roma_uara.write((json.dumps(whatunga_karere) + '\n').encode())
                        roma_uara.flush()
                        while True:
                            whakautu = json.loads(roma_uara.readline())
                            if 'error' in whakautu: raise AssertionError(whakautu)
                            if 'return' in whakautu: return whakautu['return']
                    모의제어접속('qmp_capabilities')
                    topenga_mata = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(topenga_mata), 'format': 'ppm'})
                    def 예제들(ara, 지점들):
                        with ara.open('rb') as pika_kōnae:
                            assert pika_kōnae.readline().strip() == b'P6'
                            assert pika_kōnae.readline().strip() == b'640 480'
                            assert pika_kōnae.readline().strip() == b'255'
                            pika_raraunga = pika_kōnae.read()
                        assert len(pika_raraunga) == 640 * 480 * 3
                        return [list(pika_raraunga[(세로좌표 * 640 + taunga_x) * 3:(세로좌표 * 640 + taunga_x) * 3 + 3]) for taunga_x, 세로좌표 in 지점들]
                    assert 예제들(topenga_mata, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(topenga_mata, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def tuku(누름값, 확인표시):
                        OFFSET_uara = len(대화기록)
                        Hātepe.stdin.write(누름값); Hātepe.stdin.flush()
                        표시까지받기(확인표시, OFFSET_uara)
                    tuku(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    tuku(b'\r', b'GUI ACTION 0 RESULT 0')
                    tuku(b'\t', b'GUI FOCUS 1')
                    tuku(b'\r', b'GUI ACTION 1 RESULT 0')
                    SECOND_AKW = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SECOND_AKW), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SECOND_AKW, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    tuku(b'\t', b'GUI FOCUS 2')
                    tuku(b'\r', b'GUI ACTION 2 RESULT 0')
                    tuku(b'\t', b'GUI FOCUS 3')
                    tuku(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    tuku(b'q', b'jkoros-native> ')
                    whakamana_pūrongo['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Hātepe.wait(timeout=10)
            # framebuffer 응답뿐 아니라 tūturu_raraunga scanout 픽셀도 확인한다.
            with topenga_mata.open('rb') as kōnae_tāurunga:
                assert kōnae_tāurunga.readline().strip() == b'P6'
                치수 = kōnae_tāurunga.readline().strip()
                assert 치수 == b'640 480', 치수
                assert kōnae_tāurunga.readline().strip() == b'255'
                화소들 = kōnae_tāurunga.read()
            assert len(화소들) == 640 * 480 * 3
            def pika(taunga_x, 세로좌표): return list(화소들[(세로좌표 * 640 + taunga_x) * 3:(세로좌표 * 640 + taunga_x) * 3 + 3])
            예제들 = {'background': pika(5, 5), 'panel': pika(45, 85), 'tile': pika(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            whakamana_pūrongo.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((whakaatu_pūtake / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Hātepe.poll() is None:
                Hātepe.terminate()
                try: Hātepe.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Hātepe.kill(); Hātepe.wait(timeout=5)
            pūtīpako.close()
            Hātepe.stdin.close(); Hātepe.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(whakamana_pūrongo, indent=2) + '\n')


if __name__ == '__main__':
    whakahaere()
