#!/usr/bin/env python3
"""fiili_veri raspi4b makine_başlatma, UART artış_değer, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from yürütmek_komut import işlem_kök, komut


def çalıştır():
    çıktı = işlem_kök / 'build/verification'
    çıktı.mkdir(parents=True, exist_ok=True)
    döküm = bytearray()
    doğrulama_Rapor = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = komut() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        doğrulama_Rapor['command'] = 명령인수
        Süreç = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        seçici = selectors.DefaultSelector()
        seçici.register(Süreç.stdout, selectors.EVENT_READ)
        def 표시까지받기(işaret, Ofset_değer=0, yürütme_ZAMANAŞIMI=45):
            son_tarih_saat = time.monotonic() + yürütme_ZAMANAŞIMI
            while işaret not in döküm[Ofset_değer:]:
                if time.monotonic() > son_tarih_saat:
                    raise AssertionError('UART timeout: ' + repr(işaret))
                for 누름값, _ in seçici.select(0.2):
                    veri_bloğu = 누름값.fileobj.read(4096)
                    if veri_bloğu:
                        döküm.extend(veri_bloğu)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', döküm):
                    raise AssertionError('kernel failure')
                if Süreç.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Süreç.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for işaret in 확인표시들:
                assert işaret in döküm, işaret
            # GTK 없는 geçerli_öğe 호스트에서도 VNC로 fiili_veri GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def ÖZDEŞ_değer(Boyut):
                    sonuç = b''
                    while len(sonuç) < Boyut:
                        parça_değer = 화면접속자.recv(Boyut - len(sonuç))
                        if not parça_değer: raise AssertionError('VNC disconnected')
                        sonuç += parça_değer
                    return sonuç
                assert ÖZDEŞ_değer(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in ÖZDEŞ_değer(ÖZDEŞ_değer(1)[0]); 화면접속자.sendall(b'\x01')
                assert ÖZDEŞ_değer(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                sunucu_değer = ÖZDEŞ_değer(24)
                assert int.from_bytes(sunucu_değer[:2], 'big') == 640 and int.from_bytes(sunucu_değer[2:4], 'big') == 480
                ÖZDEŞ_değer(int.from_bytes(sunucu_değer[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for komut_bayt, işaret in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', 'sınamalar.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                Ofset_değer = len(döküm)
                Süreç.stdin.write(komut_bayt + b'\n')
                Süreç.stdin.flush()
                표시까지받기(b'jkoros-native> ', Ofset_değer)
                assert işaret in döküm[Ofset_değer:], işaret
            def kabuk(girdi_satırı, 예상결과):
                Ofset_değer = len(döküm)
                Süreç.stdin.write(girdi_satırı.encode('utf-8') + b'\n'); Süreç.stdin.flush()
                표시까지받기(b'jkoros-native> ', Ofset_değer)
                cevap = bytes(döküm[Ofset_değer:])
                for metin in 예상결과:
                    assert metin.encode('utf-8') in cevap, (girdi_satırı, metin, cevap)
                return cevap
            def girmek(girdi_satırı, istem):
                Ofset_değer = len(döküm)
                Süreç.stdin.write(girdi_satırı.encode('utf-8') + b'\n'); Süreç.stdin.flush()
                표시까지받기(istem, Ofset_değer)
                return bytes(döküm[Ofset_değer:])
            def Düzenle_değer(İsim, içerik_değer, İptal_işlem=False):
                girmek('edit ' + İsim, b'edit> ')
                for girdi_satırı in içerik_değer.splitlines(): girmek(girdi_satırı, b'edit> ')
                if İptal_işlem:
                    Ofset_değer = len(döküm)
                    Süreç.stdin.write(b'\x03'); Süreç.stdin.flush()
                    표시까지받기(b'jkoros-native> ', Ofset_değer)
                    assert b'EDIT CANCELLED' in döküm[Ofset_değer:]
                else:
                    assert b'SAVED' in girmek('.', b'jkoros-native> ')
            def yükle_Dosyalar(İsim, veri):
                assert len(veri) <= 16384
                girmek('load ' + İsim, b'hex> ')
                for 순번 in range(0, len(veri), 64): girmek(veri[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in girmek('.', b'jkoros-native> ')
            def indir(İsim):
                cevap = kabuk('hex ' + İsim, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', cevap, re.S)
                veri = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(veri) == int(일치.group(1)); return veri
            kabuk('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            kabuk('java -version', ['not OpenJDK', 'exit 0'])
            kabuk('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            kabuk('java Hello "한글 bağımsız_değişkenler 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 bağımsız_değişkenler 😀', 'exit 0'])
            kabuk('python --version', ['MicroPython 1.24.1', 'exit 0'])
            kabuk('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 dosya', 'exit 0'])
            kabuk('cat python.txt', ['한글 dosya'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = çıktı / 'Hello.class'; 자바클래스.write_bytes(indir('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(çıktı), 'Hello', '한글 bağımsız_değişkenler 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 bağımsız_değişkenler 😀'], 예상결과
            Düzenle_değer('인사.java', 'public class 인사 { public static void main(String[] args) { int değer = 7; System.out.println("한글=" + değer); } }')
            kabuk('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            kabuk('java 인사', ['한글=7', 'exit 0'])
            (çıktı / '인사.class').write_bytes(indir('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(çıktı), '인사']).decode().strip() == '한글=7'
            Düzenle_değer('Hello.java', 'broken', İptal_işlem=True)
            kabuk('javac Hello.java', ['Compiled:', 'exit 0'])
            Düzenle_değer('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            kabuk('javac Broken.java', ['javac error:', 'exit 1'])
            yükle_Dosyalar('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            kabuk('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            kabuk('rm Broken.java', [])
            들여온파일 = çıktı / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            yükle_Dosyalar('Imported.class', (çıktı / 'Imported.class').read_bytes())
            kabuk('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            kabuk('rm Imported.class', [])
            Düzenle_değer('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            kabuk('javac Loop.java', ['Compiled:', 'exit 0'])
            cevap = kabuk('java Loop', ['exit '])
            assert b'instruction limit' in cevap or b'exit -1004' in cevap
            kabuk('rm Loop.java', []); kabuk('rm Loop.class', [])
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
            Düzenle_değer('checks.py', 파이썬검사)
            kabuk('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            kabuk('rm checks.py', [])
            Düzenle_değer('helper.py', 'value = 321')
            kabuk("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            kabuk('rm helper.py', [])
            kabuk("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            kabuk("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                kabuk('python hello.py', ['한글 dosya', 'exit 0'])
                kabuk('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            yükle_Dosyalar('app.elf', (işlem_kök / 'build/user/demo.elf').read_bytes())
            assert indir('app.elf') == (işlem_kök / 'build/user/demo.elf').read_bytes()
            kabuk('run app.elf', ['EL0 C++', 'exit 0'])
            yükle_Dosyalar('app.elf', b'not an ELF')
            kabuk('run app.elf', ['exit -8'])
            kabuk('rm app.elf', [])
            kabuk('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            çizim_yol = çıktı / 'java-framebuffer'; çizim_yol.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(işlem_kök / 'dist/jkoros-native-korean.jar'), '-d', str(çizim_yol), str(işlem_kök / 'sınamalar/자바/화면시험.java')])
            yükle_Dosyalar('화면시험.class', (çizim_yol / '화면시험.class').read_bytes())
            kabuk('java 화면시험', ['화면 klip reddetmek_değer', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            kabuk('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as istemci:
                istemci.settimeout(10)
                istemci.connect(str(모의제어경로))
                with istemci.makefile('rwb') as akış_değer:
                    인사 = json.loads(akış_değer.readline())
                    def 모의제어접속(Çalıştır, 전달인수=None):
                        ağ_belge = {'execute': Çalıştır}
                        if 전달인수: ağ_belge['arguments'] = 전달인수
                        akış_değer.write((json.dumps(ağ_belge) + '\n').encode())
                        akış_değer.flush()
                        while True:
                            yanıt = json.loads(akış_değer.readline())
                            if 'error' in yanıt: raise AssertionError(yanıt)
                            if 'return' in yanıt: return yanıt['return']
                    모의제어접속('qmp_capabilities')
                    ekran_kırpması = çıktı / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(ekran_kırpması), 'format': 'ppm'})
                    def 예제들(yol, 지점들):
                        with yol.open('rb') as piksel_Dosya:
                            assert piksel_Dosya.readline().strip() == b'P6'
                            assert piksel_Dosya.readline().strip() == b'640 480'
                            assert piksel_Dosya.readline().strip() == b'255'
                            piksel_veri = piksel_Dosya.read()
                        assert len(piksel_veri) == 640 * 480 * 3
                        return [list(piksel_veri[(Y_koordinat * 640 + x_koordinatı) * 3:(Y_koordinat * 640 + x_koordinatı) * 3 + 3]) for x_koordinatı, Y_koordinat in 지점들]
                    assert 예제들(ekran_kırpması, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(ekran_kırpması, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def göndermek(누름값, işaret):
                        Ofset_değer = len(döküm)
                        Süreç.stdin.write(누름값); Süreç.stdin.flush()
                        표시까지받기(işaret, Ofset_değer)
                    göndermek(b'gui\n', b'GUI READY:')
                    첫화면 = çıktı / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(çıktı / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    göndermek(b'\r', b'GUI ACTION 0 RESULT 0')
                    göndermek(b'\t', b'GUI FOCUS 1')
                    göndermek(b'\r', b'GUI ACTION 1 RESULT 0')
                    SANİYE_GUI = çıktı / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SANİYE_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(çıktı / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SANİYE_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    göndermek(b'\t', b'GUI FOCUS 2')
                    göndermek(b'\r', b'GUI ACTION 2 RESULT 0')
                    göndermek(b'\t', b'GUI FOCUS 3')
                    göndermek(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(çıktı / 'gui-python.png'), 'format': 'png'})
                    göndermek(b'q', b'jkoros-native> ')
                    doğrulama_Rapor['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Süreç.wait(timeout=10)
            # framebuffer 응답뿐 아니라 fiili_veri scanout 픽셀도 확인한다.
            with ekran_kırpması.open('rb') as Dosya_girdi:
                assert Dosya_girdi.readline().strip() == b'P6'
                치수 = Dosya_girdi.readline().strip()
                assert 치수 == b'640 480', 치수
                assert Dosya_girdi.readline().strip() == b'255'
                화소들 = Dosya_girdi.read()
            assert len(화소들) == 640 * 480 * 3
            def piksel(x_koordinatı, Y_koordinat): return list(화소들[(Y_koordinat * 640 + x_koordinatı) * 3:(Y_koordinat * 640 + x_koordinatı) * 3 + 3])
            예제들 = {'background': piksel(5, 5), 'panel': piksel(45, 85), 'tile': piksel(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            doğrulama_Rapor.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((işlem_kök / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Süreç.poll() is None:
                Süreç.terminate()
                try: Süreç.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Süreç.kill(); Süreç.wait(timeout=5)
            seçici.close()
            Süreç.stdin.close(); Süreç.stdout.close()
            (çıktı / 'serial.log').write_bytes(döküm)
            (çıktı / 'report.json').write_text(json.dumps(doğrulama_Rapor, indent=2) + '\n')


if __name__ == '__main__':
    çalıştır()
