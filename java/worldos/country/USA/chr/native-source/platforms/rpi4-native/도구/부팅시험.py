#!/usr/bin/env python3
"""ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ import 기준, ᎤᏁᏤᎸᎩ


def ᎠᎢᏎᏍᏗ():
    출력결과 = 기준 / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = ᎤᏁᏤᎸᎩ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['command'] = 명령인수
        ᎢᏯᏛᏁᎵᏓᏍᏗ = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        ᎠᏑᏰᏍᎩ = selectors.DefaultSelector()
        ᎠᏑᏰᏍᎩ.register(ᎢᏯᏛᏁᎵᏓᏍᏗ.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, 변위=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[변위:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in ᎠᏑᏰᏍᎩ.select(0.2):
                    ᎦᏟᏌᏅᎯ_ᎦᏐᎾᎸᏗᏍᏗᎢ = 누름값.fileobj.read(4096)
                    if ᎦᏟᏌᏅᎯ_ᎦᏐᎾᎸᏗᏍᏗᎢ:
                        대화기록.extend(ᎦᏟᏌᏅᎯ_ᎦᏐᎾᎸᏗᏍᏗᎢ)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if ᎢᏯᏛᏁᎵᏓᏍᏗ.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(ᎢᏯᏛᏁᎵᏓᏍᏗ.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(ᎢᎩᏓ):
                    결과 = b''
                    while len(결과) < ᎢᎩᏓ:
                        조각 = 화면접속자.recv(ᎢᎩᏓ - len(결과))
                        if not 조각: raise AssertionError('VNC disconnected')
                        결과 += 조각
                    return 결과
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ = 정확한값(24)
                assert int.from_bytes(ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ[:2], 'big') == 640 and int.from_bytes(ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ[2:4], 'big') == 480
                정확한값(int.from_bytes(ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for ᎤᏁᏤᎸᎩ_byte, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                변위 = len(대화기록)
                ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.write(ᎤᏁᏤᎸᎩ_byte + b'\n')
                ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.flush()
                표시까지받기(b'jkoros-native> ', 변위)
                assert 확인표시 in 대화기록[변위:], 확인표시
            def ᎤᏯᏍᎦ(ᏚᏓᏅᏅᎢ, 예상결과):
                변위 = len(대화기록)
                ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.write(ᏚᏓᏅᏅᎢ.encode('utf-8') + b'\n'); ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.flush()
                표시까지받기(b'jkoros-native> ', 변위)
                응답자료 = bytes(대화기록[변위:])
                for ᎠᎪᎵᏰᏗ in 예상결과:
                    assert ᎠᎪᎵᏰᏗ.encode('utf-8') in 응답자료, (ᏚᏓᏅᏅᎢ, ᎠᎪᎵᏰᏗ, 응답자료)
                return 응답자료
            def ᎥᎧᏁᏉᏍᎬᎢ(ᏚᏓᏅᏅᎢ, ᎦᏅᏫᏍᏗᏍᎩ):
                변위 = len(대화기록)
                ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.write(ᏚᏓᏅᏅᎢ.encode('utf-8') + b'\n'); ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.flush()
                표시까지받기(ᎦᏅᏫᏍᏗᏍᎩ, 변위)
                return bytes(대화기록[변위:])
            def ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ(ᏚᏙᎥᎢ, ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ, ᎠᏎᏒᏗ_ᎠᎢᏒᎢ=False):
                ᎥᎧᏁᏉᏍᎬᎢ('edit ' + ᏚᏙᎥᎢ, b'edit> ')
                for ᏚᏓᏅᏅᎢ in ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ.splitlines(): ᎥᎧᏁᏉᏍᎬᎢ(ᏚᏓᏅᏅᎢ, b'edit> ')
                if ᎠᏎᏒᏗ_ᎠᎢᏒᎢ:
                    변위 = len(대화기록)
                    ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.write(b'\x03'); ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.flush()
                    표시까지받기(b'jkoros-native> ', 변위)
                    assert b'EDIT CANCELLED' in 대화기록[변위:]
                else:
                    assert b'SAVED' in ᎥᎧᏁᏉᏍᎬᎢ('.', b'jkoros-native> ')
            def 올리기(ᏚᏙᎥᎢ, ᎦᏟᏌᏅᎯ):
                assert len(ᎦᏟᏌᏅᎯ) <= 16384
                ᎥᎧᏁᏉᏍᎬᎢ('load ' + ᏚᏙᎥᎢ, b'hex> ')
                for 순번 in range(0, len(ᎦᏟᏌᏅᎯ), 64): ᎥᎧᏁᏉᏍᎬᎢ(ᎦᏟᏌᏅᎯ[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in ᎥᎧᏁᏉᏍᎬᎢ('.', b'jkoros-native> ')
            def ᎡᎳᏓᎪᏘ_ᎦᏢᏍᎬᎢ(ᏚᏙᎥᎢ):
                응답자료 = ᎤᏯᏍᎦ('hex ' + ᏚᏙᎥᎢ, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                ᎦᏟᏌᏅᎯ = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(ᎦᏟᏌᏅᎯ) == int(일치.group(1)); return ᎦᏟᏌᏅᎯ
            ᎤᏯᏍᎦ('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            ᎤᏯᏍᎦ('java -version', ['not OpenJDK', 'exit 0'])
            ᎤᏯᏍᎦ('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            ᎤᏯᏍᎦ('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            ᎤᏯᏍᎦ('python --version', ['MicroPython 1.24.1', 'exit 0'])
            ᎤᏯᏍᎦ('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 ᎠᏍᏆᏂᎪᏙᏗ', 'exit 0'])
            ᎤᏯᏍᎦ('cat python.txt', ['한글 ᎠᏍᏆᏂᎪᏙᏗ'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(ᎡᎳᏓᎪᏘ_ᎦᏢᏍᎬᎢ('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ('인사.java', 'public class 인사 { public static void main(String[] args) { int ᏧᎬᏩᎶᏗᏯ = 7; System.out.println("한글=" + ᏧᎬᏩᎶᏗᏯ); } }')
            ᎤᏯᏍᎦ('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            ᎤᏯᏍᎦ('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(ᎡᎳᏓᎪᏘ_ᎦᏢᏍᎬᎢ('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ('Hello.java', 'broken', ᎠᏎᏒᏗ_ᎠᎢᏒᎢ=True)
            ᎤᏯᏍᎦ('javac Hello.java', ['Compiled:', 'exit 0'])
            ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            ᎤᏯᏍᎦ('javac Broken.java', ['javac error:', 'exit 1'])
            올리기('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            ᎤᏯᏍᎦ('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            ᎤᏯᏍᎦ('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            올리기('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            ᎤᏯᏍᎦ('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            ᎤᏯᏍᎦ('rm Imported.class', [])
            ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            ᎤᏯᏍᎦ('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = ᎤᏯᏍᎦ('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            ᎤᏯᏍᎦ('rm Loop.java', []); ᎤᏯᏍᎦ('rm Loop.class', [])
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
            ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ('checks.py', 파이썬검사)
            ᎤᏯᏍᎦ('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            ᎤᏯᏍᎦ('rm checks.py', [])
            ᎦᏁᏟᏴᏓ_ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ('helper.py', 'value = 321')
            ᎤᏯᏍᎦ("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            ᎤᏯᏍᎦ('rm helper.py', [])
            ᎤᏯᏍᎦ("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            ᎤᏯᏍᎦ("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                ᎤᏯᏍᎦ('python hello.py', ['한글 ᎠᏍᏆᏂᎪᏙᏗ', 'exit 0'])
                ᎤᏯᏍᎦ('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            올리기('app.elf', (기준 / 'build/user/demo.elf').read_bytes())
            assert ᎡᎳᏓᎪᏘ_ᎦᏢᏍᎬᎢ('app.elf') == (기준 / 'build/user/demo.elf').read_bytes()
            ᎤᏯᏍᎦ('run app.elf', ['EL0 C++', 'exit 0'])
            올리기('app.elf', b'not an ELF')
            ᎤᏯᏍᎦ('run app.elf', ['exit -8'])
            ᎤᏯᏍᎦ('rm app.elf', [])
            ᎤᏯᏍᎦ('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            ᎠᏍᏓᏅᎿᏂᏙᎸ_ᎠᏍᏓᏩᏛᏍᏗ = 출력결과 / 'java-framebuffer'; ᎠᏍᏓᏅᎿᏂᏙᎸ_ᎠᏍᏓᏩᏛᏍᏗ.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준 / 'dist/jkoros-native-korean.jar'), '-d', str(ᎠᏍᏓᏅᎿᏂᏙᎸ_ᎠᏍᏓᏩᏛᏍᏗ), str(기준 / '시험/자바/화면시험.java')])
            올리기('화면시험.class', (ᎠᏍᏓᏅᎿᏂᏙᎸ_ᎠᏍᏓᏩᏛᏍᏗ / '화면시험.class').read_bytes())
            ᎤᏯᏍᎦ('java 화면시험', ['화면 ᎠᎬᎭᎸᏓ_ᏗᏓᏴᎳᏛᏙᏗ 거부', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            ᎤᏯᏍᎦ('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as ᎠᏥᏍᏕᎵᏍᎩ:
                ᎠᏥᏍᏕᎵᏍᎩ.settimeout(10)
                ᎠᏥᏍᏕᎵᏍᎩ.connect(str(모의제어경로))
                with ᎠᏥᏍᏕᎵᏍᎩ.makefile('rwb') as ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ:
                    인사 = json.loads(ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.readline())
                    def 모의제어접속(ᎠᎴᏅᏗᏱ_ᏯᏛᏁᏗ, 전달인수=None):
                        ᏧᎾᏚᏓᎵ_ᎠᎪᎵᏰᏗ = {'execute': ᎠᎴᏅᏗᏱ_ᏯᏛᏁᏗ}
                        if 전달인수: ᏧᎾᏚᏓᎵ_ᎠᎪᎵᏰᏗ['arguments'] = 전달인수
                        ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.write((json.dumps(ᏧᎾᏚᏓᎵ_ᎠᎪᎵᏰᏗ) + '\n').encode())
                        ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.flush()
                        while True:
                            응답 = json.loads(ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.readline())
                            if 'error' in 응답: raise AssertionError(응답)
                            if 'return' in 응답: return 응답['return']
                    모의제어접속('qmp_capabilities')
                    화면갈무리 = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(화면갈무리), 'format': 'ppm'})
                    def 예제들(ᎠᏍᏓᏩᏛᏍᏗ, 지점들):
                        with ᎠᏍᏓᏩᏛᏍᏗ.open('rb') as pel_ᎠᏍᏆᏂᎪᏙᏗ:
                            assert pel_ᎠᏍᏆᏂᎪᏙᏗ.readline().strip() == b'P6'
                            assert pel_ᎠᏍᏆᏂᎪᏙᏗ.readline().strip() == b'640 480'
                            assert pel_ᎠᏍᏆᏂᎪᏙᏗ.readline().strip() == b'255'
                            pel_ᎦᏟᏌᏅᎯ = pel_ᎠᏍᏆᏂᎪᏙᏗ.read()
                        assert len(pel_ᎦᏟᏌᏅᎯ) == 640 * 480 * 3
                        return [list(pel_ᎦᏟᏌᏅᎯ[(세로좌표 * 640 + 가로좌표) * 3:(세로좌표 * 640 + 가로좌표) * 3 + 3]) for 가로좌표, 세로좌표 in 지점들]
                    assert 예제들(화면갈무리, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(화면갈무리, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def ᏫᎦᏅᏗ(누름값, 확인표시):
                        변위 = len(대화기록)
                        ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.write(누름값); ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.flush()
                        표시까지받기(확인표시, 변위)
                    ᏫᎦᏅᏗ(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    ᏫᎦᏅᏗ(b'\r', b'GUI ACTION 0 RESULT 0')
                    ᏫᎦᏅᏗ(b'\t', b'GUI FOCUS 1')
                    ᏫᎦᏅᏗ(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    ᏫᎦᏅᏗ(b'\t', b'GUI FOCUS 2')
                    ᏫᎦᏅᏗ(b'\r', b'GUI ACTION 2 RESULT 0')
                    ᏫᎦᏅᏗ(b'\t', b'GUI FOCUS 3')
                    ᏫᎦᏅᏗ(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    ᏫᎦᏅᏗ(b'q', b'jkoros-native> ')
                    ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            ᎢᏯᏛᏁᎵᏓᏍᏗ.wait(timeout=10)
            # framebuffer 응답뿐 아니라 ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ scanout 픽셀도 확인한다.
            with 화면갈무리.open('rb') as ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ:
                assert ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ.readline().strip() == b'P6'
                치수 = ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ.readline().strip()
                assert 치수 == b'640 480', 치수
                assert ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ.readline().strip() == b'255'
                화소들 = ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ.read()
            assert len(화소들) == 640 * 480 * 3
            def pel(가로좌표, 세로좌표): return list(화소들[(세로좌표 * 640 + 가로좌표) * 3:(세로좌표 * 640 + 가로좌표) * 3 + 3])
            예제들 = {'background': pel(5, 5), 'panel': pel(45, 85), 'tile': pel(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
            if ᎢᏯᏛᏁᎵᏓᏍᏗ.poll() is None:
                ᎢᏯᏛᏁᎵᏓᏍᏗ.terminate()
                try: ᎢᏯᏛᏁᎵᏓᏍᏗ.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    ᎢᏯᏛᏁᎵᏓᏍᏗ.kill(); ᎢᏯᏛᏁᎵᏓᏍᏗ.wait(timeout=5)
            ᎠᏑᏰᏍᎩ.close()
            ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.close(); ᎢᏯᏛᏁᎵᏓᏍᏗ.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ, indent=2) + '\n')


if __name__ == '__main__':
    ᎠᎢᏎᏍᏗ()
