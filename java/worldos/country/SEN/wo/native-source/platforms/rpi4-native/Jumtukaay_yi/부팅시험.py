#!/usr/bin/env python3
"""liteew_mbir raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from def_ndigel import 기준, ndigel


def daw():
    출력결과 = 기준 / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    wéral_tënk = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = ndigel() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        wéral_tënk['command'] = 명령인수
        yokkute = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        tànnkat = selectors.DefaultSelector()
        tànnkat.register(yokkute.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, Randal_xëyma=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[Randal_xëyma:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in tànnkat.select(0.2):
                    mbir_gatandu = 누름값.fileobj.read(4096)
                    if mbir_gatandu:
                        대화기록.extend(mbir_gatandu)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if yokkute.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(yokkute.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 liteew_mbir GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(tolluwaay):
                    결과 = b''
                    while len(결과) < tolluwaay:
                        조각 = 화면접속자.recv(tolluwaay - len(결과))
                        if not 조각: raise AssertionError('VNC disconnected')
                        결과 += 조각
                    return 결과
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                dëggu_xëyma = 정확한값(24)
                assert int.from_bytes(dëggu_xëyma[:2], 'big') == 640 and int.from_bytes(dëggu_xëyma[2:4], 'big') == 480
                정확한값(int.from_bytes(dëggu_xëyma[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for ndigel_okte, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                Randal_xëyma = len(대화기록)
                yokkute.stdin.write(ndigel_okte + b'\n')
                yokkute.stdin.flush()
                표시까지받기(b'jkoros-native> ', Randal_xëyma)
                assert 확인표시 in 대화기록[Randal_xëyma:], 확인표시
            def Wëreef(buum, 예상결과):
                Randal_xëyma = len(대화기록)
                yokkute.stdin.write(buum.encode('utf-8') + b'\n'); yokkute.stdin.flush()
                표시까지받기(b'jkoros-native> ', Randal_xëyma)
                응답자료 = bytes(대화기록[Randal_xëyma:])
                for Tekst in 예상결과:
                    assert Tekst.encode('utf-8') in 응답자료, (buum, Tekst, 응답자료)
                return 응답자료
            def dugal_851ea840(buum, xaar_jëf):
                Randal_xëyma = len(대화기록)
                yokkute.stdin.write(buum.encode('utf-8') + b'\n'); yokkute.stdin.flush()
                표시까지받기(xaar_jëf, Randal_xëyma)
                return bytes(대화기록[Randal_xëyma:])
            def soppi_xëyma(tur_253d1510, Këmb_xëyma, Bayyi_sëfu_xayma=False):
                dugal_851ea840('edit ' + tur_253d1510, b'edit> ')
                for buum in Këmb_xëyma.splitlines(): dugal_851ea840(buum, b'edit> ')
                if Bayyi_sëfu_xayma:
                    Randal_xëyma = len(대화기록)
                    yokkute.stdin.write(b'\x03'); yokkute.stdin.flush()
                    표시까지받기(b'jkoros-native> ', Randal_xëyma)
                    assert b'EDIT CANCELLED' in 대화기록[Randal_xëyma:]
                else:
                    assert b'SAVED' in dugal_851ea840('.', b'jkoros-native> ')
            def toxalsi_Fisiye_yi(tur_253d1510, mbir):
                assert len(mbir) <= 16384
                dugal_851ea840('load ' + tur_253d1510, b'hex> ')
                for 순번 in range(0, len(mbir), 64): dugal_851ea840(mbir[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in dugal_851ea840('.', b'jkoros-native> ')
            def yebbi(tur_253d1510):
                응답자료 = Wëreef('hex ' + tur_253d1510, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 응답자료, re.S)
                mbir = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(mbir) == int(일치.group(1)); return mbir
            Wëreef('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            Wëreef('java -version', ['not OpenJDK', 'exit 0'])
            Wëreef('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            Wëreef('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            Wëreef('python --version', ['MicroPython 1.24.1', 'exit 0'])
            Wëreef('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 bara_denc', 'exit 0'])
            Wëreef('cat python.txt', ['한글 bara_denc'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(yebbi('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            soppi_xëyma('인사.java', 'public class 인사 { public static void main(String[] args) { int xëyma = 7; System.out.println("한글=" + xëyma); } }')
            Wëreef('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            Wëreef('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(yebbi('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            soppi_xëyma('Hello.java', 'broken', Bayyi_sëfu_xayma=True)
            Wëreef('javac Hello.java', ['Compiled:', 'exit 0'])
            soppi_xëyma('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            Wëreef('javac Broken.java', ['javac error:', 'exit 1'])
            toxalsi_Fisiye_yi('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            Wëreef('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            Wëreef('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            toxalsi_Fisiye_yi('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            Wëreef('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            Wëreef('rm Imported.class', [])
            soppi_xëyma('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            Wëreef('javac Loop.java', ['Compiled:', 'exit 0'])
            응답자료 = Wëreef('java Loop', ['exit '])
            assert b'instruction limit' in 응답자료 or b'exit -1004' in 응답자료
            Wëreef('rm Loop.java', []); Wëreef('rm Loop.class', [])
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
            soppi_xëyma('checks.py', 파이썬검사)
            Wëreef('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            Wëreef('rm checks.py', [])
            soppi_xëyma('helper.py', 'value = 321')
            Wëreef("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            Wëreef('rm helper.py', [])
            Wëreef("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            Wëreef("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                Wëreef('python hello.py', ['한글 bara_denc', 'exit 0'])
                Wëreef('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            toxalsi_Fisiye_yi('app.elf', (기준 / 'build/user/demo.elf').read_bytes())
            assert yebbi('app.elf') == (기준 / 'build/user/demo.elf').read_bytes()
            Wëreef('run app.elf', ['EL0 C++', 'exit 0'])
            toxalsi_Fisiye_yi('app.elf', b'not an ELF')
            Wëreef('run app.elf', ['exit -8'])
            Wëreef('rm app.elf', [])
            Wëreef('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            deseñ_Yoonu_jëmale = 출력결과 / 'java-framebuffer'; deseñ_Yoonu_jëmale.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준 / 'dist/jkoros-native-korean.jar'), '-d', str(deseñ_Yoonu_jëmale), str(기준 / '시험/자바/화면시험.java')])
            toxalsi_Fisiye_yi('화면시험.class', (deseñ_Yoonu_jëmale / '화면시험.class').read_bytes())
            Wëreef('java 화면시험', ['화면 kilip 거부', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            Wëreef('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as lëkkalekat:
                lëkkalekat.settimeout(10)
                lëkkalekat.connect(str(모의제어경로))
                with lëkkalekat.makefile('rwb') as dawal_xëyma:
                    인사 = json.loads(dawal_xëyma.readline())
                    def 모의제어접속(def_ligeey, 전달인수=None):
                        mbaal_bataaxal = {'execute': def_ligeey}
                        if 전달인수: mbaal_bataaxal['arguments'] = 전달인수
                        dawal_xëyma.write((json.dumps(mbaal_bataaxal) + '\n').encode())
                        dawal_xëyma.flush()
                        while True:
                            tontu = json.loads(dawal_xëyma.readline())
                            if 'error' in tontu: raise AssertionError(tontu)
                            if 'return' in tontu: return tontu['return']
                    모의제어접속('qmp_capabilities')
                    Jàppug_nataalu_ekaraŋ_bi = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(Jàppug_nataalu_ekaraŋ_bi), 'format': 'ppm'})
                    def 예제들(Yoonu_jëmale, 지점들):
                        with Yoonu_jëmale.open('rb') as piksel_bara_denc:
                            assert piksel_bara_denc.readline().strip() == b'P6'
                            assert piksel_bara_denc.readline().strip() == b'640 480'
                            assert piksel_bara_denc.readline().strip() == b'255'
                            piksel_mbir = piksel_bara_denc.read()
                        assert len(piksel_mbir) == 640 * 480 * 3
                        return [list(piksel_mbir[(세로좌표 * 640 + rëddu_iks_yi) * 3:(세로좌표 * 640 + rëddu_iks_yi) * 3 + 3]) for rëddu_iks_yi, 세로좌표 in 지점들]
                    assert 예제들(Jàppug_nataalu_ekaraŋ_bi, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(Jàppug_nataalu_ekaraŋ_bi, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def Yónnee(누름값, 확인표시):
                        Randal_xëyma = len(대화기록)
                        yokkute.stdin.write(누름값); yokkute.stdin.flush()
                        표시까지받기(확인표시, Randal_xëyma)
                    Yónnee(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    Yónnee(b'\r', b'GUI ACTION 0 RESULT 0')
                    Yónnee(b'\t', b'GUI FOCUS 1')
                    Yónnee(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    Yónnee(b'\t', b'GUI FOCUS 2')
                    Yónnee(b'\r', b'GUI ACTION 2 RESULT 0')
                    Yónnee(b'\t', b'GUI FOCUS 3')
                    Yónnee(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    Yónnee(b'q', b'jkoros-native> ')
                    wéral_tënk['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            yokkute.wait(timeout=10)
            # framebuffer 응답뿐 아니라 liteew_mbir scanout 픽셀도 확인한다.
            with Jàppug_nataalu_ekaraŋ_bi.open('rb') as bara_denc_dugal_xabaar:
                assert bara_denc_dugal_xabaar.readline().strip() == b'P6'
                치수 = bara_denc_dugal_xabaar.readline().strip()
                assert 치수 == b'640 480', 치수
                assert bara_denc_dugal_xabaar.readline().strip() == b'255'
                화소들 = bara_denc_dugal_xabaar.read()
            assert len(화소들) == 640 * 480 * 3
            def piksel(rëddu_iks_yi, 세로좌표): return list(화소들[(세로좌표 * 640 + rëddu_iks_yi) * 3:(세로좌표 * 640 + rëddu_iks_yi) * 3 + 3])
            예제들 = {'background': piksel(5, 5), 'panel': piksel(45, 85), 'tile': piksel(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            wéral_tënk.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
            if yokkute.poll() is None:
                yokkute.terminate()
                try: yokkute.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    yokkute.kill(); yokkute.wait(timeout=5)
            tànnkat.close()
            yokkute.stdin.close(); yokkute.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(wéral_tënk, indent=2) + '\n')


if __name__ == '__main__':
    daw()
