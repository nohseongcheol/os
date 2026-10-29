#!/usr/bin/env python3
"""nyakuri_amakurushingiro raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from gukora_ibwiriza import 기준, Icyo_wifuza


def ihuriro():
    출력결과 = 기준 / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    iyemeza_raporo = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Icyo_wifuza() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        iyemeza_raporo['command'] = 명령인수
        Inzira_a7054519 = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        muhitamo = selectors.DefaultSelector()
        muhitamo.register(Inzira_a7054519.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, Ofuseti_agaciro=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[Ofuseti_agaciro:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in muhitamo.select(0.2):
                    amakurushingiro_guheza = 누름값.fileobj.read(4096)
                    if amakurushingiro_guheza:
                        대화기록.extend(amakurushingiro_guheza)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if Inzira_a7054519.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Inzira_a7054519.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 nyakuri_amakurushingiro GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(Ingano):
                    결과 = b''
                    while len(결과) < Ingano:
                        조각 = 화면접속자.recv(Ingano - len(결과))
                        if not 조각: raise AssertionError('VNC disconnected')
                        결과 += 조각
                    return 결과
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                seriveri_agaciro = 정확한값(24)
                assert int.from_bytes(seriveri_agaciro[:2], 'big') == 640 and int.from_bytes(seriveri_agaciro[2:4], 'big') == 480
                정확한값(int.from_bytes(seriveri_agaciro[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for ibwiriza_bayiti, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                Ofuseti_agaciro = len(대화기록)
                Inzira_a7054519.stdin.write(ibwiriza_bayiti + b'\n')
                Inzira_a7054519.stdin.flush()
                표시까지받기(b'jkoros-native> ', Ofuseti_agaciro)
                assert 확인표시 in 대화기록[Ofuseti_agaciro:], 확인표시
            def insomamabwiriza(umurongo, 예상결과):
                Ofuseti_agaciro = len(대화기록)
                Inzira_a7054519.stdin.write(umurongo.encode('utf-8') + b'\n'); Inzira_a7054519.stdin.flush()
                표시까지받기(b'jkoros-native> ', Ofuseti_agaciro)
                응답자료 = bytes(대화기록[Ofuseti_agaciro:])
                for Umwandiko in 예상결과:
                    assert Umwandiko.encode('utf-8') in 응답자료, (umurongo, Umwandiko, 응답자료)
                return 응답자료
            def kwandika_851ea840(umurongo, integuza):
                Ofuseti_agaciro = len(대화기록)
                Inzira_a7054519.stdin.write(umurongo.encode('utf-8') + b'\n'); Inzira_a7054519.stdin.flush()
                표시까지받기(integuza, Ofuseti_agaciro)
                return bytes(대화기록[Ofuseti_agaciro:])
            def guhindura_agaciro(Izina, Ibirimo_agaciro, kureka_igikorwa=False):
                kwandika_851ea840('edit ' + Izina, b'edit> ')
                for umurongo in Ibirimo_agaciro.splitlines(): kwandika_851ea840(umurongo, b'edit> ')
                if kureka_igikorwa:
                    Ofuseti_agaciro = len(대화기록)
                    Inzira_a7054519.stdin.write(b'\x03'); Inzira_a7054519.stdin.flush()
                    표시까지받기(b'jkoros-native> ', Ofuseti_agaciro)
                    assert b'EDIT CANCELLED' in 대화기록[Ofuseti_agaciro:]
                else:
                    assert b'SAVED' in kwandika_851ea840('.', b'jkoros-native> ')
            def gukurura_Dosiye(Izina, amakurushingiro):
                assert len(amakurushingiro) <= 16384
                kwandika_851ea840('load ' + Izina, b'hex> ')
                for 순번 in range(0, len(amakurushingiro), 64): kwandika_851ea840(amakurushingiro[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in kwandika_851ea840('.', b'jkoros-native> ')
            def gukurura(Izina):
                응답자료 = insomamabwiriza('hex ' + Izina, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                amakurushingiro = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(amakurushingiro) == int(일치.group(1)); return amakurushingiro
            insomamabwiriza('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            insomamabwiriza('java -version', ['not OpenJDK', 'exit 0'])
            insomamabwiriza('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            insomamabwiriza('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            insomamabwiriza('python --version', ['MicroPython 1.24.1', 'exit 0'])
            insomamabwiriza('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Idosiye', 'exit 0'])
            insomamabwiriza('cat python.txt', ['한글 Idosiye'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(gukurura('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            guhindura_agaciro('인사.java', 'public class 인사 { public static void main(String[] args) { int agaciro = 7; System.out.println("한글=" + agaciro); } }')
            insomamabwiriza('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            insomamabwiriza('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(gukurura('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            guhindura_agaciro('Hello.java', 'broken', kureka_igikorwa=True)
            insomamabwiriza('javac Hello.java', ['Compiled:', 'exit 0'])
            guhindura_agaciro('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            insomamabwiriza('javac Broken.java', ['javac error:', 'exit 1'])
            gukurura_Dosiye('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            insomamabwiriza('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            insomamabwiriza('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            gukurura_Dosiye('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            insomamabwiriza('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            insomamabwiriza('rm Imported.class', [])
            guhindura_agaciro('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            insomamabwiriza('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = insomamabwiriza('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            insomamabwiriza('rm Loop.java', []); insomamabwiriza('rm Loop.class', [])
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
            guhindura_agaciro('checks.py', 파이썬검사)
            insomamabwiriza('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            insomamabwiriza('rm checks.py', [])
            guhindura_agaciro('helper.py', 'value = 321')
            insomamabwiriza("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            insomamabwiriza('rm helper.py', [])
            insomamabwiriza("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            insomamabwiriza("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                insomamabwiriza('python hello.py', ['한글 Idosiye', 'exit 0'])
                insomamabwiriza('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            gukurura_Dosiye('app.elf', (기준 / 'build/user/demo.elf').read_bytes())
            assert gukurura('app.elf') == (기준 / 'build/user/demo.elf').read_bytes()
            insomamabwiriza('run app.elf', ['EL0 C++', 'exit 0'])
            gukurura_Dosiye('app.elf', b'not an ELF')
            insomamabwiriza('run app.elf', ['exit -8'])
            insomamabwiriza('rm app.elf', [])
            insomamabwiriza('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            igishushanyo_inzira = 출력결과 / 'java-framebuffer'; igishushanyo_inzira.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준 / 'dist/jkoros-native-korean.jar'), '-d', str(igishushanyo_inzira), str(기준 / '시험/자바/화면시험.java')])
            gukurura_Dosiye('화면시험.class', (igishushanyo_inzira / '화면시험.class').read_bytes())
            insomamabwiriza('java 화면시험', ['화면 kiripu 거부', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            insomamabwiriza('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as umukiriya:
                umukiriya.settimeout(10)
                umukiriya.connect(str(모의제어경로))
                with umukiriya.makefile('rwb') as Stream_agaciro:
                    인사 = json.loads(Stream_agaciro.readline())
                    def 모의제어접속(gukora_umukoro, 전달인수=None):
                        Urusobemiyoboro_ubutumwa = {'execute': gukora_umukoro}
                        if 전달인수: Urusobemiyoboro_ubutumwa['arguments'] = 전달인수
                        Stream_agaciro.write((json.dumps(Urusobemiyoboro_ubutumwa) + '\n').encode())
                        Stream_agaciro.flush()
                        while True:
                            gusubiza = json.loads(Stream_agaciro.readline())
                            if 'error' in gusubiza: raise AssertionError(gusubiza)
                            if 'return' in gusubiza: return gusubiza['return']
                    모의제어접속('qmp_capabilities')
                    guhina_mugaragaza = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(guhina_mugaragaza), 'format': 'ppm'})
                    def 예제들(Inzira, 지점들):
                        with Inzira.open('rb') as pel_dosiye:
                            assert pel_dosiye.readline().strip() == b'P6'
                            assert pel_dosiye.readline().strip() == b'640 480'
                            assert pel_dosiye.readline().strip() == b'255'
                            pel_amakurushingiro = pel_dosiye.read()
                        assert len(pel_amakurushingiro) == 640 * 480 * 3
                        return [list(pel_amakurushingiro[(세로좌표 * 640 + Ihuza_rya_x) * 3:(세로좌표 * 640 + Ihuza_rya_x) * 3 + 3]) for Ihuza_rya_x, 세로좌표 in 지점들]
                    assert 예제들(guhina_mugaragaza, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(guhina_mugaragaza, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def kohereza(누름값, 확인표시):
                        Ofuseti_agaciro = len(대화기록)
                        Inzira_a7054519.stdin.write(누름값); Inzira_a7054519.stdin.flush()
                        표시까지받기(확인표시, Ofuseti_agaciro)
                    kohereza(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    kohereza(b'\r', b'GUI ACTION 0 RESULT 0')
                    kohereza(b'\t', b'GUI FOCUS 1')
                    kohereza(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    kohereza(b'\t', b'GUI FOCUS 2')
                    kohereza(b'\r', b'GUI ACTION 2 RESULT 0')
                    kohereza(b'\t', b'GUI FOCUS 3')
                    kohereza(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    kohereza(b'q', b'jkoros-native> ')
                    iyemeza_raporo['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Inzira_a7054519.wait(timeout=10)
            # framebuffer 응답뿐 아니라 nyakuri_amakurushingiro scanout 픽셀도 확인한다.
            with guhina_mugaragaza.open('rb') as dosiye_icyinjizwa:
                assert dosiye_icyinjizwa.readline().strip() == b'P6'
                치수 = dosiye_icyinjizwa.readline().strip()
                assert 치수 == b'640 480', 치수
                assert dosiye_icyinjizwa.readline().strip() == b'255'
                화소들 = dosiye_icyinjizwa.read()
            assert len(화소들) == 640 * 480 * 3
            def pel(Ihuza_rya_x, 세로좌표): return list(화소들[(세로좌표 * 640 + Ihuza_rya_x) * 3:(세로좌표 * 640 + Ihuza_rya_x) * 3 + 3])
            예제들 = {'background': pel(5, 5), 'panel': pel(45, 85), 'tile': pel(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            iyemeza_raporo.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
            if Inzira_a7054519.poll() is None:
                Inzira_a7054519.terminate()
                try: Inzira_a7054519.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Inzira_a7054519.kill(); Inzira_a7054519.wait(timeout=5)
            muhitamo.close()
            Inzira_a7054519.stdin.close(); Inzira_a7054519.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(iyemeza_raporo, indent=2) + '\n')


if __name__ == '__main__':
    ihuriro()
