#!/usr/bin/env python3
"""dữLiệuThựcTế raspi4b KhởiĐộng, UART giáTrịVào, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from thựcThiLệnh import gốcCâyDựÁn, lệnh


def chạy():
    đầuRa = gốcCâyDựÁn / 'build/verification'
    đầuRa.mkdir(parents=True, exist_ok=True)
    bảnGhiDiễnTiến = bytearray()
    báoCáoViệcThẩmĐịnh = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as đườngDẫnĐangLàmViệc:
        đườngDẫnQMP = Path(đườngDẫnĐangLàmViệc) / 'qmp.sock'
        cácĐốiSốLệnh = lệnh() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(đườngDẫnQMP),
                           '-vnc', 'unix:{}'.format(Path(đườngDẫnĐangLàmViệc) / 'vnc.sock')]
        báoCáoViệcThẩmĐịnh['command'] = cácĐốiSốLệnh
        tiếnTrình = subprocess.Popen(cácĐốiSốLệnh, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        bộChọn = selectors.DefaultSelector()
        bộChọn.register(tiếnTrình.stdout, selectors.EVENT_READ)
        def nhậnĐếnKhi(dấuMốc, giáTrịĐộLệch=0, hếtGiờViệcThựcThi=45):
            thờiGianHạnChót = time.monotonic() + hếtGiờViệcThựcThi
            while dấuMốc not in bảnGhiDiễnTiến[giáTrịĐộLệch:]:
                if time.monotonic() > thờiGianHạnChót:
                    raise AssertionError('UART timeout: ' + repr(dấuMốc))
                for giáTrịĐãNhấn, _ in bộChọn.select(0.2):
                    khốiDữLiệu = giáTrịĐãNhấn.fileobj.read(4096)
                    if khốiDữLiệu:
                        bảnGhiDiễnTiến.extend(khốiDữLiệu)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', bảnGhiDiễnTiến):
                    raise AssertionError('kernel failure')
                if tiếnTrình.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(tiếnTrình.returncode))
        try:
            nhậnĐếnKhi(b'jkoros-native> ')
            cácDấuMốc = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for dấuMốc in cácDấuMốc:
                assert dấuMốc in bảnGhiDiễnTiến, dấuMốc
            # GTK 없는 phầnMụcHiệnTại 호스트에서도 VNC로 dữLiệuThựcTế GUI를 볼 trịSố 있어야 한다.
            with socket.socket(socket.AF_UNIX) as máyKháchMànHình:
                máyKháchMànHình.settimeout(5); máyKháchMànHình.connect(str(Path(đườngDẫnĐangLàmViệc) / 'vnc.sock'))
                def giáTrịChínhXác(cỡ):
                    kếtQuả = b''
                    while len(kếtQuả) < cỡ:
                        giáTrịĐoạn = máyKháchMànHình.recv(cỡ - len(kếtQuả))
                        if not giáTrịĐoạn: raise AssertionError('VNC disconnected')
                        kếtQuả += giáTrịĐoạn
                    return kếtQuả
                assert giáTrịChínhXác(12) == b'RFB 003.008\n'
                máyKháchMànHình.sendall(b'RFB 003.008\n')
                assert 1 in giáTrịChínhXác(giáTrịChínhXác(1)[0]); máyKháchMànHình.sendall(b'\x01')
                assert giáTrịChínhXác(4) == b'\x00\x00\x00\x00'; máyKháchMànHình.sendall(b'\x01')
                giáTrịMáyChủ = giáTrịChínhXác(24)
                assert int.from_bytes(giáTrịMáyChủ[:2], 'big') == 640 and int.from_bytes(giáTrịMáyChủ[2:4], 'big') == 480
                giáTrịChínhXác(int.from_bytes(giáTrịMáyChủ[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for byteLệnh, dấuMốc in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', 'KiểmThử.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                giáTrịĐộLệch = len(bảnGhiDiễnTiến)
                tiếnTrình.stdin.write(byteLệnh + b'\n')
                tiếnTrình.stdin.flush()
                nhậnĐếnKhi(b'jkoros-native> ', giáTrịĐộLệch)
                assert dấuMốc in bảnGhiDiễnTiến[giáTrịĐộLệch:], dấuMốc
            def vỏLệnh(dòng, dựKiến):
                giáTrịĐộLệch = len(bảnGhiDiễnTiến)
                tiếnTrình.stdin.write(dòng.encode('utf-8') + b'\n'); tiếnTrình.stdin.flush()
                nhậnĐếnKhi(b'jkoros-native> ', giáTrịĐộLệch)
                phảnHồi = bytes(bảnGhiDiễnTiến[giáTrịĐộLệch:])
                for vănBản in dựKiến:
                    assert vănBản.encode('utf-8') in phảnHồi, (dòng, vănBản, phảnHồi)
                return phảnHồi
            def vào(dòng, dấuNhắc):
                giáTrịĐộLệch = len(bảnGhiDiễnTiến)
                tiếnTrình.stdin.write(dòng.encode('utf-8') + b'\n'); tiếnTrình.stdin.flush()
                nhậnĐếnKhi(dấuNhắc, giáTrịĐộLệch)
                return bytes(bảnGhiDiễnTiến[giáTrịĐộLệch:])
            def giáTrịSửa(tên, giáTrịNộiDung, thaoTácHủy=False):
                vào('edit ' + tên, b'edit> ')
                for dòng in giáTrịNộiDung.splitlines(): vào(dòng, b'edit> ')
                if thaoTácHủy:
                    giáTrịĐộLệch = len(bảnGhiDiễnTiến)
                    tiếnTrình.stdin.write(b'\x03'); tiếnTrình.stdin.flush()
                    nhậnĐếnKhi(b'jkoros-native> ', giáTrịĐộLệch)
                    assert b'EDIT CANCELLED' in bảnGhiDiễnTiến[giáTrịĐộLệch:]
                else:
                    assert b'SAVED' in vào('.', b'jkoros-native> ')
            def cácTệpTảiLên(tên, DữLiệu):
                assert len(DữLiệu) <= 16384
                vào('load ' + tên, b'hex> ')
                for chỉSốThứBậc in range(0, len(DữLiệu), 64): vào(DữLiệu[chỉSốThứBậc:chỉSốThứBậc+64].hex(), b'hex> ')
                assert b'LOADED' in vào('.', b'jkoros-native> ')
            def tảiXuống(tên):
                phảnHồi = vỏLệnh('hex ' + tên, ['HEX BEGIN', 'HEX END'])
                làBằng = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', phảnHồi, re.S)
                DữLiệu = bytes.fromhex(''.join(làBằng.group(2).decode('ascii').split()))
                assert len(DữLiệu) == int(làBằng.group(1)); return DữLiệu
            vỏLệnh('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            vỏLệnh('java -version', ['not OpenJDK', 'exit 0'])
            vỏLệnh('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            vỏLệnh('java Hello "한글 cácĐốiSố 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 cácĐốiSố 😀', 'exit 0'])
            vỏLệnh('python --version', ['MicroPython 1.24.1', 'exit 0'])
            vỏLệnh('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Tệp', 'exit 0'])
            vỏLệnh('cat python.txt', ['한글 Tệp'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            lớpJava = đầuRa / 'Hello.class'; lớpJava.write_bytes(tảiXuống('Hello.class'))
            dựKiến = subprocess.check_output(['java', '-Xverify:all', '-cp', str(đầuRa), 'Hello', '한글 cácĐốiSố 😀']).decode('utf-8')
            assert dựKiến.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 cácĐốiSố 😀'], dựKiến
            giáTrịSửa('LờiChào.java', 'public class LờiChào { public static void main(String[] args) { int giáTrị = 7; System.out.println("한글=" + giáTrị); } }')
            vỏLệnh('javac LờiChào.java', ['Compiled: LờiChào.class', 'exit 0'])
            vỏLệnh('java LờiChào', ['한글=7', 'exit 0'])
            (đầuRa / 'LờiChào.class').write_bytes(tảiXuống('LờiChào.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(đầuRa), 'LờiChào']).decode().strip() == '한글=7'
            giáTrịSửa('Hello.java', 'broken', thaoTácHủy=True)
            vỏLệnh('javac Hello.java', ['Compiled:', 'exit 0'])
            giáTrịSửa('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            vỏLệnh('javac Broken.java', ['javac error:', 'exit 1'])
            cácTệpTảiLên('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            vỏLệnh('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            vỏLệnh('rm Broken.java', [])
            đãNhập = đầuRa / 'Imported.java'
            đãNhập.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(đãNhập)])
            cácTệpTảiLên('Imported.class', (đầuRa / 'Imported.class').read_bytes())
            vỏLệnh('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            vỏLệnh('rm Imported.class', [])
            giáTrịSửa('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            vỏLệnh('javac Loop.java', ['Compiled:', 'exit 0'])
            phảnHồi = vỏLệnh('java Loop', ['exit '])
            assert b'instruction limit' in phảnHồi or b'exit -1004' in phảnHồi
            vỏLệnh('rm Loop.java', []); vỏLệnh('rm Loop.class', [])
            # CPython-independent Python runtime: Unicode, big integers, closures/classes,
            # GC roots, file imports, exceptions and UDP queues are exercised in the guest.
            cácPhépKiểmTraPython = """import gc, jkoros
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
            giáTrịSửa('checks.py', cácPhépKiểmTraPython)
            vỏLệnh('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            vỏLệnh('rm checks.py', [])
            giáTrịSửa('helper.py', 'value = 321')
            vỏLệnh("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            vỏLệnh('rm helper.py', [])
            vỏLệnh("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            vỏLệnh("python -c 'while True: pass'", ['exit -1004'])
            for chỉSốThứBậc in range(4):
                vỏLệnh('python hello.py', ['한글 Tệp', 'exit 0'])
                vỏLệnh('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            cácTệpTảiLên('app.elf', (gốcCâyDựÁn / 'build/user/demo.elf').read_bytes())
            assert tảiXuống('app.elf') == (gốcCâyDựÁn / 'build/user/demo.elf').read_bytes()
            vỏLệnh('run app.elf', ['EL0 C++', 'exit 0'])
            cácTệpTảiLên('app.elf', b'not an ELF')
            vỏLệnh('run app.elf', ['exit -8'])
            vỏLệnh('rm app.elf', [])
            vỏLệnh('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            đườngDẫnBảnVẽ = đầuRa / 'java-framebuffer'; đườngDẫnBảnVẽ.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(gốcCâyDựÁn / 'dist/jkoros-native-korean.jar'), '-d', str(đườngDẫnBảnVẽ), str(gốcCâyDựÁn / 'KiểmThử/Java/thửMànHình.java')])
            cácTệpTảiLên('thửMànHình.class', (đườngDẫnBảnVẽ / 'thửMànHình.class').read_bytes())
            vỏLệnh('java thửMànHình', ['MànHình cắtXén từChốiGiáTrị', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            vỏLệnh('rm thửMànHình.class', [])
            with socket.socket(socket.AF_UNIX) as máyKhách:
                máyKhách.settimeout(10)
                máyKhách.connect(str(đườngDẫnQMP))
                with máyKhách.makefile('rwb') as giáTrịLuồng:
                    LờiChào = json.loads(giáTrịLuồng.readline())
                    def kếtNốiĐiềuKhiểnGiảLập(thựcThiTácVụ, đốiSốĐãChuyểnTiếp=None):
                        thôngĐiệpMạng = {'execute': thựcThiTácVụ}
                        if đốiSốĐãChuyểnTiếp: thôngĐiệpMạng['arguments'] = đốiSốĐãChuyểnTiếp
                        giáTrịLuồng.write((json.dumps(thôngĐiệpMạng) + '\n').encode())
                        giáTrịLuồng.flush()
                        while True:
                            lờiĐáp = json.loads(giáTrịLuồng.readline())
                            if 'error' in lờiĐáp: raise AssertionError(lờiĐáp)
                            if 'return' in lờiĐáp: return lờiĐáp['return']
                    kếtNốiĐiềuKhiểnGiảLập('qmp_capabilities')
                    ảnhMànHình = đầuRa / 'framebuffer.ppm'
                    kếtNốiĐiềuKhiểnGiảLập('screendump', {'filename': str(ảnhMànHình), 'format': 'ppm'})
                    def cácMụcVíDụ(đườngDẫn, cácĐiểm):
                        with đườngDẫn.open('rb') as tệpĐiểmẢnh:
                            assert tệpĐiểmẢnh.readline().strip() == b'P6'
                            assert tệpĐiểmẢnh.readline().strip() == b'640 480'
                            assert tệpĐiểmẢnh.readline().strip() == b'255'
                            dữLiệuĐiểmẢnh = tệpĐiểmẢnh.read()
                        assert len(dữLiệuĐiểmẢnh) == 640 * 480 * 3
                        return [list(dữLiệuĐiểmẢnh[(tọaĐộY * 640 + tọaĐộX) * 3:(tọaĐộY * 640 + tọaĐộX) * 3 + 3]) for tọaĐộX, tọaĐộY in cácĐiểm]
                    assert cácMụcVíDụ(ảnhMànHình, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert cácMụcVíDụ(ảnhMànHình, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def gửi(giáTrịĐãNhấn, dấuMốc):
                        giáTrịĐộLệch = len(bảnGhiDiễnTiến)
                        tiếnTrình.stdin.write(giáTrịĐãNhấn); tiếnTrình.stdin.flush()
                        nhậnĐếnKhi(dấuMốc, giáTrịĐộLệch)
                    gửi(b'gui\n', b'GUI READY:')
                    giaoDiệnĐồHọaĐầuTiên = đầuRa / 'gui-programs.ppm'
                    kếtNốiĐiềuKhiểnGiảLập('screendump', {'filename': str(giaoDiệnĐồHọaĐầuTiên), 'format': 'ppm'})
                    kếtNốiĐiềuKhiểnGiảLập('screendump', {'filename': str(đầuRa / 'gui-programs.png'), 'format': 'png'})
                    assert cácMụcVíDụ(giaoDiệnĐồHọaĐầuTiên, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    gửi(b'\r', b'GUI ACTION 0 RESULT 0')
                    gửi(b'\t', b'GUI FOCUS 1')
                    gửi(b'\r', b'GUI ACTION 1 RESULT 0')
                    giaoDiệnĐồHọaThứHai = đầuRa / 'gui-network.ppm'
                    kếtNốiĐiềuKhiểnGiảLập('screendump', {'filename': str(giaoDiệnĐồHọaThứHai), 'format': 'ppm'})
                    kếtNốiĐiềuKhiểnGiảLập('screendump', {'filename': str(đầuRa / 'gui-network.png'), 'format': 'png'})
                    assert cácMụcVíDụ(giaoDiệnĐồHọaThứHai, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    gửi(b'\t', b'GUI FOCUS 2')
                    gửi(b'\r', b'GUI ACTION 2 RESULT 0')
                    gửi(b'\t', b'GUI FOCUS 3')
                    gửi(b'\r', b'GUI ACTION 3 RESULT 0')
                    kếtNốiĐiềuKhiểnGiảLập('screendump', {'filename': str(đầuRa / 'gui-python.png'), 'format': 'png'})
                    gửi(b'q', b'jkoros-native> ')
                    báoCáoViệcThẩmĐịnh['qemu'] = LờiChào['QMP']['version']
                    kếtNốiĐiềuKhiểnGiảLập('quit')
            tiếnTrình.wait(timeout=10)
            # framebuffer 응답뿐 아니라 dữLiệuThựcTế scanout 픽셀도 확인한다.
            with ảnhMànHình.open('rb') as mụcTệp:
                assert mụcTệp.readline().strip() == b'P6'
                giáTrịCácChiều = mụcTệp.readline().strip()
                assert giáTrịCácChiều == b'640 480', giáTrịCácChiều
                assert mụcTệp.readline().strip() == b'255'
                danhSáchCácĐiểmẢnh = mụcTệp.read()
            assert len(danhSáchCácĐiểmẢnh) == 640 * 480 * 3
            def điểmẢnh(tọaĐộX, tọaĐộY): return list(danhSáchCácĐiểmẢnh[(tọaĐộY * 640 + tọaĐộX) * 3:(tọaĐộY * 640 + tọaĐộX) * 3 + 3])
            cácMụcVíDụ = {'background': điểmẢnh(5, 5), 'panel': điểmẢnh(45, 85), 'tile': điểmẢnh(65, 115)}
            assert cácMụcVíDụ == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, cácMụcVíDụ
            báoCáoViệcThẩmĐịnh.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=cácMụcVíDụ, kernel_sha256=hashlib.sha256((gốcCâyDựÁn / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if tiếnTrình.poll() is None:
                tiếnTrình.terminate()
                try: tiếnTrình.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    tiếnTrình.kill(); tiếnTrình.wait(timeout=5)
            bộChọn.close()
            tiếnTrình.stdin.close(); tiếnTrình.stdout.close()
            (đầuRa / 'serial.log').write_bytes(bảnGhiDiễnTiến)
            (đầuRa / 'report.json').write_text(json.dumps(báoCáoViệcThẩmĐịnh, indent=2) + '\n')


if __name__ == '__main__':
    chạy()
