#!/usr/bin/env python3
"""aktual_data raspi4b awal_mesin, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from Jalankan_perintah import Tugas_akar, perintah


def jalankan():
    출력결과 = Tugas_akar / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    transkrip = bytearray()
    validasi_lapor = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = perintah() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        validasi_lapor['command'] = 명령인수
        Proses = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        pemilih = selectors.DefaultSelector()
        pemilih.register(Proses.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, OFFSET_VALUE=0, 시간제한=45):
            tenggat_waktu_TIME = time.monotonic() + 시간제한
            while 확인표시 not in transkrip[OFFSET_VALUE:]:
                if time.monotonic() > tenggat_waktu_TIME:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in pemilih.select(0.2):
                    blok_data = 누름값.fileobj.read(4096)
                    if blok_data:
                        transkrip.extend(blok_data)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', transkrip):
                    raise AssertionError('kernel failure')
                if Proses.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Proses.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in transkrip, 확인표시
            # GTK 없는 saat_ini_item 호스트에서도 VNC로 aktual_data GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def EXACT_VALUE(Ukuran):
                    hasil = b''
                    while len(hasil) < Ukuran:
                        조각 = 화면접속자.recv(Ukuran - len(hasil))
                        if not 조각: raise AssertionError('VNC disconnected')
                        hasil += 조각
                    return hasil
                assert EXACT_VALUE(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in EXACT_VALUE(EXACT_VALUE(1)[0]); 화면접속자.sendall(b'\x01')
                assert EXACT_VALUE(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                server_VALUE = EXACT_VALUE(24)
                assert int.from_bytes(server_VALUE[:2], 'big') == 640 and int.from_bytes(server_VALUE[2:4], 'big') == 480
                EXACT_VALUE(int.from_bytes(server_VALUE[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for perintah_byte, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', 'pengujian.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                OFFSET_VALUE = len(transkrip)
                Proses.stdin.write(perintah_byte + b'\n')
                Proses.stdin.flush()
                표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                assert 확인표시 in transkrip[OFFSET_VALUE:], 확인표시
            def shell(baris_masukan, 예상결과):
                OFFSET_VALUE = len(transkrip)
                Proses.stdin.write(baris_masukan.encode('utf-8') + b'\n'); Proses.stdin.flush()
                표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                respons = bytes(transkrip[OFFSET_VALUE:])
                for teks in 예상결과:
                    assert teks.encode('utf-8') in respons, (baris_masukan, teks, respons)
                return respons
            def masukkan(baris_masukan, minta):
                OFFSET_VALUE = len(transkrip)
                Proses.stdin.write(baris_masukan.encode('utf-8') + b'\n'); Proses.stdin.flush()
                표시까지받기(minta, OFFSET_VALUE)
                return bytes(transkrip[OFFSET_VALUE:])
            def Edit_VALUE(Nama_2, Isi_VALUE, Batal_bedah=False):
                masukkan('edit ' + Nama_2, b'edit> ')
                for baris_masukan in Isi_VALUE.splitlines(): masukkan(baris_masukan, b'edit> ')
                if Batal_bedah:
                    OFFSET_VALUE = len(transkrip)
                    Proses.stdin.write(b'\x03'); Proses.stdin.flush()
                    표시까지받기(b'jkoros-native> ', OFFSET_VALUE)
                    assert b'EDIT CANCELLED' in transkrip[OFFSET_VALUE:]
                else:
                    assert b'SAVED' in masukkan('.', b'jkoros-native> ')
            def Upload_File(Nama_2, data):
                assert len(data) <= 16384
                masukkan('load ' + Nama_2, b'hex> ')
                for 순번 in range(0, len(data), 64): masukkan(data[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in masukkan('.', b'jkoros-native> ')
            def unduh(Nama_2):
                respons = shell('hex ' + Nama_2, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', respons, re.S)
                data = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(data) == int(일치.group(1)); return data
            shell('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            shell('java -version', ['not OpenJDK', 'exit 0'])
            shell('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            shell('java Hello "한글 argumen 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 argumen 😀', 'exit 0'])
            shell('python --version', ['MicroPython 1.24.1', 'exit 0'])
            shell('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 berkas', 'exit 0'])
            shell('cat python.txt', ['한글 berkas'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(unduh('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 argumen 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 argumen 😀'], 예상결과
            Edit_VALUE('인사.java', 'public class 인사 { public static void main(String[] args) { int VALUE = 7; System.out.println("한글=" + VALUE); } }')
            shell('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            shell('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(unduh('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            Edit_VALUE('Hello.java', 'broken', Batal_bedah=True)
            shell('javac Hello.java', ['Compiled:', 'exit 0'])
            Edit_VALUE('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            shell('javac Broken.java', ['javac error:', 'exit 1'])
            Upload_File('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            shell('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            shell('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Upload_File('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            shell('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            shell('rm Imported.class', [])
            Edit_VALUE('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            shell('javac Loop.java', ['Compiled:', 'exit 0'])
            respons = shell('java Loop', ['exit '])
            assert b'instruction limit' in respons or b'exit -1004' in respons
            shell('rm Loop.java', []); shell('rm Loop.class', [])
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
            Edit_VALUE('checks.py', 파이썬검사)
            shell('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            shell('rm checks.py', [])
            Edit_VALUE('helper.py', 'value = 321')
            shell("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            shell('rm helper.py', [])
            shell("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            shell("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                shell('python hello.py', ['한글 berkas', 'exit 0'])
                shell('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Upload_File('app.elf', (Tugas_akar / 'build/user/demo.elf').read_bytes())
            assert unduh('app.elf') == (Tugas_akar / 'build/user/demo.elf').read_bytes()
            shell('run app.elf', ['EL0 C++', 'exit 0'])
            Upload_File('app.elf', b'not an ELF')
            shell('run app.elf', ['exit -8'])
            shell('rm app.elf', [])
            shell('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            gambar_jalur = 출력결과 / 'java-framebuffer'; gambar_jalur.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Tugas_akar / 'dist/jkoros-native-korean.jar'), '-d', str(gambar_jalur), str(Tugas_akar / 'pengujian/자바/화면시험.java')])
            Upload_File('화면시험.class', (gambar_jalur / '화면시험.class').read_bytes())
            shell('java 화면시험', ['화면 klip tolak_VALUE', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            shell('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as klien:
                klien.settimeout(10)
                klien.connect(str(모의제어경로))
                with klien.makefile('rwb') as Stream_VALUE:
                    인사 = json.loads(Stream_VALUE.readline())
                    def 모의제어접속(Eksekusi, 전달인수=None):
                        jaringan_email = {'execute': Eksekusi}
                        if 전달인수: jaringan_email['arguments'] = 전달인수
                        Stream_VALUE.write((json.dumps(jaringan_email) + '\n').encode())
                        Stream_VALUE.flush()
                        while True:
                            balas = json.loads(Stream_VALUE.readline())
                            if 'error' in balas: raise AssertionError(balas)
                            if 'return' in balas: return balas['return']
                    모의제어접속('qmp_capabilities')
                    kliping_layar = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(kliping_layar), 'format': 'ppm'})
                    def 예제들(jalur, 지점들):
                        with jalur.open('rb') as elgam_file:
                            assert elgam_file.readline().strip() == b'P6'
                            assert elgam_file.readline().strip() == b'640 480'
                            assert elgam_file.readline().strip() == b'255'
                            elgam_data = elgam_file.read()
                        assert len(elgam_data) == 640 * 480 * 3
                        return [list(elgam_data[(Y_koordinat * 640 + koordinat_x) * 3:(Y_koordinat * 640 + koordinat_x) * 3 + 3]) for koordinat_x, Y_koordinat in 지점들]
                    assert 예제들(kliping_layar, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(kliping_layar, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def kirim(누름값, 확인표시):
                        OFFSET_VALUE = len(transkrip)
                        Proses.stdin.write(누름값); Proses.stdin.flush()
                        표시까지받기(확인표시, OFFSET_VALUE)
                    kirim(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    kirim(b'\r', b'GUI ACTION 0 RESULT 0')
                    kirim(b'\t', b'GUI FOCUS 1')
                    kirim(b'\r', b'GUI ACTION 1 RESULT 0')
                    SECOND_GUI = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SECOND_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SECOND_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    kirim(b'\t', b'GUI FOCUS 2')
                    kirim(b'\r', b'GUI ACTION 2 RESULT 0')
                    kirim(b'\t', b'GUI FOCUS 3')
                    kirim(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    kirim(b'q', b'jkoros-native> ')
                    validasi_lapor['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Proses.wait(timeout=10)
            # framebuffer 응답뿐 아니라 aktual_data scanout 픽셀도 확인한다.
            with kliping_layar.open('rb') as file_entri:
                assert file_entri.readline().strip() == b'P6'
                치수 = file_entri.readline().strip()
                assert 치수 == b'640 480', 치수
                assert file_entri.readline().strip() == b'255'
                화소들 = file_entri.read()
            assert len(화소들) == 640 * 480 * 3
            def elgam(koordinat_x, Y_koordinat): return list(화소들[(Y_koordinat * 640 + koordinat_x) * 3:(Y_koordinat * 640 + koordinat_x) * 3 + 3])
            예제들 = {'background': elgam(5, 5), 'panel': elgam(45, 85), 'tile': elgam(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            validasi_lapor.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((Tugas_akar / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Proses.poll() is None:
                Proses.terminate()
                try: Proses.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Proses.kill(); Proses.wait(timeout=5)
            pemilih.close()
            Proses.stdin.close(); Proses.stdout.close()
            (출력결과 / 'serial.log').write_bytes(transkrip)
            (출력결과 / 'report.json').write_text(json.dumps(validasi_lapor, indent=2) + '\n')


if __name__ == '__main__':
    jalankan()
