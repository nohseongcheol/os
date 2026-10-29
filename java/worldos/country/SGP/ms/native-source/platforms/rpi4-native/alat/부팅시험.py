#!/usr/bin/env python3
"""sebenar_data raspi4b permulaan_mesin, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from laksanakan_perintah import projek_akar, Perintah


def Jalan():
    출력결과 = projek_akar / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    pensahihan_lapor = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Perintah() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        pensahihan_lapor['command'] = 명령인수
        Proses = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        준비선택기 = selectors.DefaultSelector()
        준비선택기.register(Proses.stdout, selectors.EVENT_READ)
        def 표시까지받기(penanda, Ofset_VALUE=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while penanda not in 대화기록[Ofset_VALUE:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(penanda))
                for 누름값, _ in 준비선택기.select(0.2):
                    blok_data = 누름값.fileobj.read(4096)
                    if blok_data:
                        대화기록.extend(blok_data)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if Proses.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Proses.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for penanda in 확인표시들:
                assert penanda in 대화기록, penanda
            # GTK 없는 현재 호스트에서도 VNC로 sebenar_data GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def EXACT_VALUE(Saiz):
                    ukuran = b''
                    while len(ukuran) < Saiz:
                        조각 = 화면접속자.recv(Saiz - len(ukuran))
                        if not 조각: raise AssertionError('VNC disconnected')
                        ukuran += 조각
                    return ukuran
                assert EXACT_VALUE(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in EXACT_VALUE(EXACT_VALUE(1)[0]); 화면접속자.sendall(b'\x01')
                assert EXACT_VALUE(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                pelayan_VALUE = EXACT_VALUE(24)
                assert int.from_bytes(pelayan_VALUE[:2], 'big') == 640 and int.from_bytes(pelayan_VALUE[2:4], 'big') == 480
                EXACT_VALUE(int.from_bytes(pelayan_VALUE[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for perintah_bait, penanda in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', 'ujian.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                Ofset_VALUE = len(대화기록)
                Proses.stdin.write(perintah_bait + b'\n')
                Proses.stdin.flush()
                표시까지받기(b'jkoros-native> ', Ofset_VALUE)
                assert penanda in 대화기록[Ofset_VALUE:], penanda
            def cangkerang(baris, 예상결과):
                Ofset_VALUE = len(대화기록)
                Proses.stdin.write(baris.encode('utf-8') + b'\n'); Proses.stdin.flush()
                표시까지받기(b'jkoros-native> ', Ofset_VALUE)
                respons = bytes(대화기록[Ofset_VALUE:])
                for Teks in 예상결과:
                    assert Teks.encode('utf-8') in respons, (baris, Teks, respons)
                return respons
            def masuk(baris, prom):
                Ofset_VALUE = len(대화기록)
                Proses.stdin.write(baris.encode('utf-8') + b'\n'); Proses.stdin.flush()
                표시까지받기(prom, Ofset_VALUE)
                return bytes(대화기록[Ofset_VALUE:])
            def edit_VALUE(Nama, Kandungan_VALUE, Batal_operasi=False):
                masuk('edit ' + Nama, b'edit> ')
                for baris in Kandungan_VALUE.splitlines(): masuk(baris, b'edit> ')
                if Batal_operasi:
                    Ofset_VALUE = len(대화기록)
                    Proses.stdin.write(b'\x03'); Proses.stdin.flush()
                    표시까지받기(b'jkoros-native> ', Ofset_VALUE)
                    assert b'EDIT CANCELLED' in 대화기록[Ofset_VALUE:]
                else:
                    assert b'SAVED' in masuk('.', b'jkoros-native> ')
            def Upload_Fail(Nama, data):
                assert len(data) <= 16384
                masuk('load ' + Nama, b'hex> ')
                for 순번 in range(0, len(data), 64): masuk(data[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in masuk('.', b'jkoros-native> ')
            def muat_turun(Nama):
                respons = cangkerang('hex ' + Nama, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', respons, re.S)
                data = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(data) == int(일치.group(1)); return data
            cangkerang('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            cangkerang('java -version', ['not OpenJDK', 'exit 0'])
            cangkerang('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            cangkerang('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            cangkerang('python --version', ['MicroPython 1.24.1', 'exit 0'])
            cangkerang('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Fail', 'exit 0'])
            cangkerang('cat python.txt', ['한글 Fail'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(muat_turun('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            edit_VALUE('인사.java', 'public class 인사 { public static void main(String[] args) { int VALUE = 7; System.out.println("한글=" + VALUE); } }')
            cangkerang('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            cangkerang('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(muat_turun('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            edit_VALUE('Hello.java', 'broken', Batal_operasi=True)
            cangkerang('javac Hello.java', ['Compiled:', 'exit 0'])
            edit_VALUE('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            cangkerang('javac Broken.java', ['javac error:', 'exit 1'])
            Upload_Fail('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            cangkerang('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            cangkerang('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Upload_Fail('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            cangkerang('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            cangkerang('rm Imported.class', [])
            edit_VALUE('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            cangkerang('javac Loop.java', ['Compiled:', 'exit 0'])
            respons = cangkerang('java Loop', ['exit '])
            assert b'instruction limit' in respons or b'exit -1004' in respons
            cangkerang('rm Loop.java', []); cangkerang('rm Loop.class', [])
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
            edit_VALUE('checks.py', 파이썬검사)
            cangkerang('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            cangkerang('rm checks.py', [])
            edit_VALUE('helper.py', 'value = 321')
            cangkerang("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            cangkerang('rm helper.py', [])
            cangkerang("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            cangkerang("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                cangkerang('python hello.py', ['한글 Fail', 'exit 0'])
                cangkerang('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Upload_Fail('app.elf', (projek_akar / 'build/user/demo.elf').read_bytes())
            assert muat_turun('app.elf') == (projek_akar / 'build/user/demo.elf').read_bytes()
            cangkerang('run app.elf', ['EL0 C++', 'exit 0'])
            Upload_Fail('app.elf', b'not an ELF')
            cangkerang('run app.elf', ['exit -8'])
            cangkerang('rm app.elf', [])
            cangkerang('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            lukisan_laluan = 출력결과 / 'java-framebuffer'; lukisan_laluan.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(projek_akar / 'dist/jkoros-native-korean.jar'), '-d', str(lukisan_laluan), str(projek_akar / 'ujian/자바/화면시험.java')])
            Upload_Fail('화면시험.class', (lukisan_laluan / '화면시험.class').read_bytes())
            cangkerang('java 화면시험', ['화면 klip tolak_VALUE', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            cangkerang('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as klien:
                klien.settimeout(10)
                klien.connect(str(모의제어경로))
                with klien.makefile('rwb') as strim_VALUE:
                    인사 = json.loads(strim_VALUE.readline())
                    def 모의제어접속(Lakukan, 전달인수=None):
                        rangkaian_e_mel = {'execute': Lakukan}
                        if 전달인수: rangkaian_e_mel['arguments'] = 전달인수
                        strim_VALUE.write((json.dumps(rangkaian_e_mel) + '\n').encode())
                        strim_VALUE.flush()
                        while True:
                            balas = json.loads(strim_VALUE.readline())
                            if 'error' in balas: raise AssertionError(balas)
                            if 'return' in balas: return balas['return']
                    모의제어접속('qmp_capabilities')
                    syot_layar = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(syot_layar), 'format': 'ppm'})
                    def 예제들(LALUAN, 지점들):
                        with LALUAN.open('rb') as pel_fail:
                            assert pel_fail.readline().strip() == b'P6'
                            assert pel_fail.readline().strip() == b'640 480'
                            assert pel_fail.readline().strip() == b'255'
                            pel_data = pel_fail.read()
                        assert len(pel_data) == 640 * 480 * 3
                        return [list(pel_data[(Y_koordinat * 640 + koordinat_x) * 3:(Y_koordinat * 640 + koordinat_x) * 3 + 3]) for koordinat_x, Y_koordinat in 지점들]
                    assert 예제들(syot_layar, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(syot_layar, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def e_mel_9aee63bd(누름값, penanda):
                        Ofset_VALUE = len(대화기록)
                        Proses.stdin.write(누름값); Proses.stdin.flush()
                        표시까지받기(penanda, Ofset_VALUE)
                    e_mel_9aee63bd(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    e_mel_9aee63bd(b'\r', b'GUI ACTION 0 RESULT 0')
                    e_mel_9aee63bd(b'\t', b'GUI FOCUS 1')
                    e_mel_9aee63bd(b'\r', b'GUI ACTION 1 RESULT 0')
                    SECOND_GUI = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SECOND_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SECOND_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    e_mel_9aee63bd(b'\t', b'GUI FOCUS 2')
                    e_mel_9aee63bd(b'\r', b'GUI ACTION 2 RESULT 0')
                    e_mel_9aee63bd(b'\t', b'GUI FOCUS 3')
                    e_mel_9aee63bd(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    e_mel_9aee63bd(b'q', b'jkoros-native> ')
                    pensahihan_lapor['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Proses.wait(timeout=10)
            # framebuffer 응답뿐 아니라 sebenar_data scanout 픽셀도 확인한다.
            with syot_layar.open('rb') as fail_pemasukan:
                assert fail_pemasukan.readline().strip() == b'P6'
                치수 = fail_pemasukan.readline().strip()
                assert 치수 == b'640 480', 치수
                assert fail_pemasukan.readline().strip() == b'255'
                화소들 = fail_pemasukan.read()
            assert len(화소들) == 640 * 480 * 3
            def pel(koordinat_x, Y_koordinat): return list(화소들[(Y_koordinat * 640 + koordinat_x) * 3:(Y_koordinat * 640 + koordinat_x) * 3 + 3])
            예제들 = {'background': pel(5, 5), 'panel': pel(45, 85), 'tile': pel(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            pensahihan_lapor.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((projek_akar / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Proses.poll() is None:
                Proses.terminate()
                try: Proses.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Proses.kill(); Proses.wait(timeout=5)
            준비선택기.close()
            Proses.stdin.close(); Proses.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(pensahihan_lapor, indent=2) + '\n')


if __name__ == '__main__':
    Jalan()
