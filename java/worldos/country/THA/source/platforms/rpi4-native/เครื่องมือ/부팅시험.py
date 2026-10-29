#!/usr/bin/env python3
"""ค่าจริง_ข้อมูล raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from ดําเนินการ_คําสั่ง import แสดง_ราก, คําสั่ง


def เรียกใช้งาน():
    ผลผลิต = แสดง_ราก / 'build/verification'
    ผลผลิต.mkdir(parents=True, exist_ok=True)
    การถอดความ = bytearray()
    การตรวจสอบความถูกต้อง_รายงาน = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = คําสั่ง() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        การตรวจสอบความถูกต้อง_รายงาน['command'] = 명령인수
        โพรเซส = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        ตัวเลือก_582fe3b9 = selectors.DefaultSelector()
        ตัวเลือก_582fe3b9.register(โพรเซส.stdout, selectors.EVENT_READ)
        def 표시까지받기(มาร์กเกอร์, ออฟเซต_ค่า=0, 시간제한=45):
            วันครบกําหนด_เวลา = time.monotonic() + 시간제한
            while มาร์กเกอร์ not in การถอดความ[ออฟเซต_ค่า:]:
                if time.monotonic() > วันครบกําหนด_เวลา:
                    raise AssertionError('UART timeout: ' + repr(มาร์กเกอร์))
                for 누름값, _ in ตัวเลือก_582fe3b9.select(0.2):
                    ข้อมูล_บล็อก = 누름값.fileobj.read(4096)
                    if ข้อมูล_บล็อก:
                        การถอดความ.extend(ข้อมูล_บล็อก)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', การถอดความ):
                    raise AssertionError('kernel failure')
                if โพรเซส.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(โพรเซส.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for มาร์กเกอร์ in 확인표시들:
                assert มาร์กเกอร์ in การถอดความ, มาร์กเกอร์
            # GTK 없는 ปัจจุบัน_รายการ 호스트에서도 VNC로 ค่าจริง_ข้อมูล GUI를 볼 หมายเลข 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def 정확한값(ขนาด):
                    ผลลัพธ์ = b''
                    while len(ผลลัพธ์) < ขนาด:
                        조각 = 화면접속자.recv(ขนาด - len(ผลลัพธ์))
                        if not 조각: raise AssertionError('VNC disconnected')
                        ผลลัพธ์ += 조각
                    return ผลลัพธ์
                assert 정확한값(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in 정확한값(정확한값(1)[0]); 화면접속자.sendall(b'\x01')
                assert 정확한값(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                เซิร์ฟเวอร์_ค่า = 정확한값(24)
                assert int.from_bytes(เซิร์ฟเวอร์_ค่า[:2], 'big') == 640 and int.from_bytes(เซิร์ฟเวอร์_ค่า[2:4], 'big') == 480
                정확한값(int.from_bytes(เซิร์ฟเวอร์_ค่า[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for คําสั่ง_ไบต์, มาร์กเกอร์ in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                ออฟเซต_ค่า = len(การถอดความ)
                โพรเซส.stdin.write(คําสั่ง_ไบต์ + b'\n')
                โพรเซส.stdin.flush()
                표시까지받기(b'jkoros-native> ', ออฟเซต_ค่า)
                assert มาร์กเกอร์ in การถอดความ[ออฟเซต_ค่า:], มาร์กเกอร์
            def เชลล์(บรรทัด, 예상결과):
                ออฟเซต_ค่า = len(การถอดความ)
                โพรเซส.stdin.write(บรรทัด.encode('utf-8') + b'\n'); โพรเซส.stdin.flush()
                표시까지받기(b'jkoros-native> ', ออฟเซต_ค่า)
                การตอบ = bytes(การถอดความ[ออฟเซต_ค่า:])
                for ข้อความ in 예상결과:
                    assert ข้อความ.encode('utf-8') in การตอบ, (บรรทัด, ข้อความ, การตอบ)
                return การตอบ
            def ใส่(บรรทัด, พร้อมท์):
                ออฟเซต_ค่า = len(การถอดความ)
                โพรเซส.stdin.write(บรรทัด.encode('utf-8') + b'\n'); โพรเซส.stdin.flush()
                표시까지받기(พร้อมท์, ออฟเซต_ค่า)
                return bytes(การถอดความ[ออฟเซต_ค่า:])
            def แก้ไข_ค่า(ชื่อ, เนื้อหา_ค่า, ยกเลิก_ศัลยกรรม=False):
                ใส่('edit ' + ชื่อ, b'edit> ')
                for บรรทัด in เนื้อหา_ค่า.splitlines(): ใส่(บรรทัด, b'edit> ')
                if ยกเลิก_ศัลยกรรม:
                    ออฟเซต_ค่า = len(การถอดความ)
                    โพรเซส.stdin.write(b'\x03'); โพรเซส.stdin.flush()
                    표시까지받기(b'jkoros-native> ', ออฟเซต_ค่า)
                    assert b'EDIT CANCELLED' in การถอดความ[ออฟเซต_ค่า:]
                else:
                    assert b'SAVED' in ใส่('.', b'jkoros-native> ')
            def อัปโหลด_ไฟล์(ชื่อ, ข้อมูล):
                assert len(ข้อมูล) <= 16384
                ใส่('load ' + ชื่อ, b'hex> ')
                for 순번 in range(0, len(ข้อมูล), 64): ใส่(ข้อมูล[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in ใส่('.', b'jkoros-native> ')
            def ดาวน์โหลด(ชื่อ):
                การตอบ = เชลล์('hex ' + ชื่อ, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', การตอบ, re.S)
                ข้อมูล = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(ข้อมูล) == int(일치.group(1)); return ข้อมูล
            เชลล์('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            เชลล์('java -version', ['not OpenJDK', 'exit 0'])
            เชลล์('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            เชลล์('java Hello "한글 อาร์กิวเมนต์ 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 อาร์กิวเมนต์ 😀', 'exit 0'])
            เชลล์('python --version', ['MicroPython 1.24.1', 'exit 0'])
            เชลล์('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 แฟ้ม', 'exit 0'])
            เชลล์('cat python.txt', ['한글 แฟ้ม'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = ผลผลิต / 'Hello.class'; 자바클래스.write_bytes(ดาวน์โหลด('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ผลผลิต), 'Hello', '한글 อาร์กิวเมนต์ 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 อาร์กิวเมนต์ 😀'], 예상결과
            แก้ไข_ค่า('인사.java', 'public class 인사 { public static void main(String[] args) { int ค่า = 7; System.out.println("한글=" + ค่า); } }')
            เชลล์('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            เชลล์('java 인사', ['한글=7', 'exit 0'])
            (ผลผลิต / '인사.class').write_bytes(ดาวน์โหลด('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(ผลผลิต), '인사']).decode().strip() == '한글=7'
            แก้ไข_ค่า('Hello.java', 'broken', ยกเลิก_ศัลยกรรม=True)
            เชลล์('javac Hello.java', ['Compiled:', 'exit 0'])
            แก้ไข_ค่า('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            เชลล์('javac Broken.java', ['javac error:', 'exit 1'])
            อัปโหลด_ไฟล์('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            เชลล์('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            เชลล์('rm Broken.java', [])
            들여온파일 = ผลผลิต / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            อัปโหลด_ไฟล์('Imported.class', (ผลผลิต / 'Imported.class').read_bytes())
            เชลล์('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            เชลล์('rm Imported.class', [])
            แก้ไข_ค่า('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            เชลล์('javac Loop.java', ['Compiled:', 'exit 0'])
            การตอบ = เชลล์('java Loop', ['exit '])
            assert b'instruction limit' in การตอบ or b'exit -1004' in การตอบ
            เชลล์('rm Loop.java', []); เชลล์('rm Loop.class', [])
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
            แก้ไข_ค่า('checks.py', 파이썬검사)
            เชลล์('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            เชลล์('rm checks.py', [])
            แก้ไข_ค่า('helper.py', 'value = 321')
            เชลล์("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            เชลล์('rm helper.py', [])
            เชลล์("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            เชลล์("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                เชลล์('python hello.py', ['한글 แฟ้ม', 'exit 0'])
                เชลล์('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            อัปโหลด_ไฟล์('app.elf', (แสดง_ราก / 'build/user/demo.elf').read_bytes())
            assert ดาวน์โหลด('app.elf') == (แสดง_ราก / 'build/user/demo.elf').read_bytes()
            เชลล์('run app.elf', ['EL0 C++', 'exit 0'])
            อัปโหลด_ไฟล์('app.elf', b'not an ELF')
            เชลล์('run app.elf', ['exit -8'])
            เชลล์('rm app.elf', [])
            เชลล์('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            รูปวาด_พาธ = ผลผลิต / 'java-framebuffer'; รูปวาด_พาธ.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(แสดง_ราก / 'dist/jkoros-native-korean.jar'), '-d', str(รูปวาด_พาธ), str(แสดง_ราก / '시험/자바/화면시험.java')])
            อัปโหลด_ไฟล์('화면시험.class', (รูปวาด_พาธ / '화면시험.class').read_bytes())
            เชลล์('java 화면시험', ['화면 คลิป ปฏิเสธ_ค่า', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            เชลล์('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as ไคลเอ็นต์:
                ไคลเอ็นต์.settimeout(10)
                ไคลเอ็นต์.connect(str(모의제어경로))
                with ไคลเอ็นต์.makefile('rwb') as สตรีม_ค่า:
                    인사 = json.loads(สตรีม_ค่า.readline())
                    def 모의제어접속(เรียกทํางาน, 전달인수=None):
                        เครือข่าย_อีเมล = {'execute': เรียกทํางาน}
                        if 전달인수: เครือข่าย_อีเมล['arguments'] = 전달인수
                        สตรีม_ค่า.write((json.dumps(เครือข่าย_อีเมล) + '\n').encode())
                        สตรีม_ค่า.flush()
                        while True:
                            ตอบกลับ = json.loads(สตรีม_ค่า.readline())
                            if 'error' in ตอบกลับ: raise AssertionError(ตอบกลับ)
                            if 'return' in ตอบกลับ: return ตอบกลับ['return']
                    모의제어접속('qmp_capabilities')
                    สกรีนช็อต = ผลผลิต / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(สกรีนช็อต), 'format': 'ppm'})
                    def 예제들(เส้นทาง, 지점들):
                        with เส้นทาง.open('rb') as พิกเซล_แฟ้ม:
                            assert พิกเซล_แฟ้ม.readline().strip() == b'P6'
                            assert พิกเซล_แฟ้ม.readline().strip() == b'640 480'
                            assert พิกเซล_แฟ้ม.readline().strip() == b'255'
                            พิกเซล_ข้อมูล = พิกเซล_แฟ้ม.read()
                        assert len(พิกเซล_ข้อมูล) == 640 * 480 * 3
                        return [list(พิกเซล_ข้อมูล[(세로좌표 * 640 + พิกัดแกน_x) * 3:(세로좌표 * 640 + พิกัดแกน_x) * 3 + 3]) for พิกัดแกน_x, 세로좌표 in 지점들]
                    assert 예제들(สกรีนช็อต, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(สกรีนช็อต, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def ส่ง(누름값, มาร์กเกอร์):
                        ออฟเซต_ค่า = len(การถอดความ)
                        โพรเซส.stdin.write(누름값); โพรเซส.stdin.flush()
                        표시까지받기(มาร์กเกอร์, ออฟเซต_ค่า)
                    ส่ง(b'gui\n', b'GUI READY:')
                    첫화면 = ผลผลิต / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(ผลผลิต / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    ส่ง(b'\r', b'GUI ACTION 0 RESULT 0')
                    ส่ง(b'\t', b'GUI FOCUS 1')
                    ส่ง(b'\r', b'GUI ACTION 1 RESULT 0')
                    둘째화면 = ผลผลิต / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(둘째화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(ผลผลิต / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(둘째화면, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    ส่ง(b'\t', b'GUI FOCUS 2')
                    ส่ง(b'\r', b'GUI ACTION 2 RESULT 0')
                    ส่ง(b'\t', b'GUI FOCUS 3')
                    ส่ง(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(ผลผลิต / 'gui-python.png'), 'format': 'png'})
                    ส่ง(b'q', b'jkoros-native> ')
                    การตรวจสอบความถูกต้อง_รายงาน['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            โพรเซส.wait(timeout=10)
            # framebuffer 응답뿐 아니라 ค่าจริง_ข้อมูล scanout 픽셀도 확인한다.
            with สกรีนช็อต.open('rb') as แฟ้ม_รายการ_3d0c1245:
                assert แฟ้ม_รายการ_3d0c1245.readline().strip() == b'P6'
                치수 = แฟ้ม_รายการ_3d0c1245.readline().strip()
                assert 치수 == b'640 480', 치수
                assert แฟ้ม_รายการ_3d0c1245.readline().strip() == b'255'
                화소들 = แฟ้ม_รายการ_3d0c1245.read()
            assert len(화소들) == 640 * 480 * 3
            def พิกเซล(พิกัดแกน_x, 세로좌표): return list(화소들[(세로좌표 * 640 + พิกัดแกน_x) * 3:(세로좌표 * 640 + พิกัดแกน_x) * 3 + 3])
            예제들 = {'background': พิกเซล(5, 5), 'panel': พิกเซล(45, 85), 'tile': พิกเซล(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            การตรวจสอบความถูกต้อง_รายงาน.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((แสดง_ราก / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if โพรเซส.poll() is None:
                โพรเซส.terminate()
                try: โพรเซส.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    โพรเซส.kill(); โพรเซส.wait(timeout=5)
            ตัวเลือก_582fe3b9.close()
            โพรเซส.stdin.close(); โพรเซส.stdout.close()
            (ผลผลิต / 'serial.log').write_bytes(การถอดความ)
            (ผลผลิต / 'report.json').write_text(json.dumps(การตรวจสอบความถูกต้อง_รายงาน, indent=2) + '\n')


if __name__ == '__main__':
    เรียกใช้งาน()
