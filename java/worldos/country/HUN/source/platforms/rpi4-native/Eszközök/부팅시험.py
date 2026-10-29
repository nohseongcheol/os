#!/usr/bin/env python3
"""tényleges_adat raspi4b 부팅, UART bevitel_ÉRTÉK, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from végrehajt_parancs import teendő_gyök, Parancs


def Futtatás():
    kimenet = teendő_gyök / 'build/verification'
    kimenet.mkdir(parents=True, exist_ok=True)
    átirat = bytearray()
    ellenőrzés_jelent = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Parancs() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        ellenőrzés_jelent['command'] = 명령인수
        Folyamat = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        szelektor = selectors.DefaultSelector()
        szelektor.register(Folyamat.stdout, selectors.EVENT_READ)
        def 표시까지받기(jelölő, Ofszet_ÉRTÉK=0, végrehajtás_IDŐTÚLLÉPÉS=45):
            határidő_IDŐ = time.monotonic() + végrehajtás_IDŐTÚLLÉPÉS
            while jelölő not in átirat[Ofszet_ÉRTÉK:]:
                if time.monotonic() > határidő_IDŐ:
                    raise AssertionError('UART timeout: ' + repr(jelölő))
                for 누름값, _ in szelektor.select(0.2):
                    adatblokk = 누름값.fileobj.read(4096)
                    if adatblokk:
                        átirat.extend(adatblokk)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', átirat):
                    raise AssertionError('kernel failure')
                if Folyamat.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Folyamat.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for jelölő in 확인표시들:
                assert jelölő in átirat, jelölő
            # GTK 없는 aktuális_cikk 호스트에서도 VNC로 tényleges_adat GUI를 볼 szám 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def AZONOS_ÉRTÉK(Méret):
                    KR = b''
                    while len(KR) < Méret:
                        조각 = 화면접속자.recv(Méret - len(KR))
                        if not 조각: raise AssertionError('VNC disconnected')
                        KR += 조각
                    return KR
                assert AZONOS_ÉRTÉK(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in AZONOS_ÉRTÉK(AZONOS_ÉRTÉK(1)[0]); 화면접속자.sendall(b'\x01')
                assert AZONOS_ÉRTÉK(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                kiszolgáló_ÉRTÉK = AZONOS_ÉRTÉK(24)
                assert int.from_bytes(kiszolgáló_ÉRTÉK[:2], 'big') == 640 and int.from_bytes(kiszolgáló_ÉRTÉK[2:4], 'big') == 480
                AZONOS_ÉRTÉK(int.from_bytes(kiszolgáló_ÉRTÉK[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for parancs_bájt, jelölő in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                Ofszet_ÉRTÉK = len(átirat)
                Folyamat.stdin.write(parancs_bájt + b'\n')
                Folyamat.stdin.flush()
                표시까지받기(b'jkoros-native> ', Ofszet_ÉRTÉK)
                assert jelölő in átirat[Ofszet_ÉRTÉK:], jelölő
            def felület(Vonal, 예상결과):
                Ofszet_ÉRTÉK = len(átirat)
                Folyamat.stdin.write(Vonal.encode('utf-8') + b'\n'); Folyamat.stdin.flush()
                표시까지받기(b'jkoros-native> ', Ofszet_ÉRTÉK)
                válasz_1262b476 = bytes(átirat[Ofszet_ÉRTÉK:])
                for Szöveg in 예상결과:
                    assert Szöveg.encode('utf-8') in válasz_1262b476, (Vonal, Szöveg, válasz_1262b476)
                return válasz_1262b476
            def megad(Vonal, kér):
                Ofszet_ÉRTÉK = len(átirat)
                Folyamat.stdin.write(Vonal.encode('utf-8') + b'\n'); Folyamat.stdin.flush()
                표시까지받기(kér, Ofszet_ÉRTÉK)
                return bytes(átirat[Ofszet_ÉRTÉK:])
            def szerkeszt_ÉRTÉK(Név, Tartalom_ÉRTÉK, Mégse_műtét=False):
                megad('edit ' + Név, b'edit> ')
                for Vonal in Tartalom_ÉRTÉK.splitlines(): megad(Vonal, b'edit> ')
                if Mégse_műtét:
                    Ofszet_ÉRTÉK = len(átirat)
                    Folyamat.stdin.write(b'\x03'); Folyamat.stdin.flush()
                    표시까지받기(b'jkoros-native> ', Ofszet_ÉRTÉK)
                    assert b'EDIT CANCELLED' in átirat[Ofszet_ÉRTÉK:]
                else:
                    assert b'SAVED' in megad('.', b'jkoros-native> ')
            def feltölt_Files(Név, adat):
                assert len(adat) <= 16384
                megad('load ' + Név, b'hex> ')
                for 순번 in range(0, len(adat), 64): megad(adat[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in megad('.', b'jkoros-native> ')
            def letölt(Név):
                válasz_1262b476 = felület('hex ' + Név, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', válasz_1262b476, re.S)
                adat = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(adat) == int(일치.group(1)); return adat
            felület('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            felület('java -version', ['not OpenJDK', 'exit 0'])
            felület('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            felület('java Hello "한글 Argumentumok 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Argumentumok 😀', 'exit 0'])
            felület('python --version', ['MicroPython 1.24.1', 'exit 0'])
            felület('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Fájl', 'exit 0'])
            felület('cat python.txt', ['한글 Fájl'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = kimenet / 'Hello.class'; 자바클래스.write_bytes(letölt('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(kimenet), 'Hello', '한글 Argumentumok 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 Argumentumok 😀'], 예상결과
            szerkeszt_ÉRTÉK('인사.java', 'public class 인사 { public static void main(String[] args) { int ÉRTÉK = 7; System.out.println("한글=" + ÉRTÉK); } }')
            felület('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            felület('java 인사', ['한글=7', 'exit 0'])
            (kimenet / '인사.class').write_bytes(letölt('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(kimenet), '인사']).decode().strip() == '한글=7'
            szerkeszt_ÉRTÉK('Hello.java', 'broken', Mégse_műtét=True)
            felület('javac Hello.java', ['Compiled:', 'exit 0'])
            szerkeszt_ÉRTÉK('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            felület('javac Broken.java', ['javac error:', 'exit 1'])
            feltölt_Files('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            felület('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            felület('rm Broken.java', [])
            들여온파일 = kimenet / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            feltölt_Files('Imported.class', (kimenet / 'Imported.class').read_bytes())
            felület('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            felület('rm Imported.class', [])
            szerkeszt_ÉRTÉK('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            felület('javac Loop.java', ['Compiled:', 'exit 0'])
            válasz_1262b476 = felület('java Loop', ['exit '])
            assert b'instruction limit' in válasz_1262b476 or b'exit -1004' in válasz_1262b476
            felület('rm Loop.java', []); felület('rm Loop.class', [])
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
            szerkeszt_ÉRTÉK('checks.py', 파이썬검사)
            felület('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            felület('rm checks.py', [])
            szerkeszt_ÉRTÉK('helper.py', 'value = 321')
            felület("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            felület('rm helper.py', [])
            felület("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            felület("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                felület('python hello.py', ['한글 Fájl', 'exit 0'])
                felület('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            feltölt_Files('app.elf', (teendő_gyök / 'build/user/demo.elf').read_bytes())
            assert letölt('app.elf') == (teendő_gyök / 'build/user/demo.elf').read_bytes()
            felület('run app.elf', ['EL0 C++', 'exit 0'])
            feltölt_Files('app.elf', b'not an ELF')
            felület('run app.elf', ['exit -8'])
            felület('rm app.elf', [])
            felület('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            rajz_útvonal = kimenet / 'java-framebuffer'; rajz_útvonal.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(teendő_gyök / 'dist/jkoros-native-korean.jar'), '-d', str(rajz_útvonal), str(teendő_gyök / '시험/자바/화면시험.java')])
            feltölt_Files('화면시험.class', (rajz_útvonal / '화면시험.class').read_bytes())
            felület('java 화면시험', ['화면 klip elutasít_ÉRTÉK', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            felület('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as kliens:
                kliens.settimeout(10)
                kliens.connect(str(모의제어경로))
                with kliens.makefile('rwb') as Stream_ÉRTÉK:
                    인사 = json.loads(Stream_ÉRTÉK.readline())
                    def 모의제어접속(Végrehajtás, 전달인수=None):
                        hálózat_e_mail = {'execute': Végrehajtás}
                        if 전달인수: hálózat_e_mail['arguments'] = 전달인수
                        Stream_ÉRTÉK.write((json.dumps(hálózat_e_mail) + '\n').encode())
                        Stream_ÉRTÉK.flush()
                        while True:
                            válasz = json.loads(Stream_ÉRTÉK.readline())
                            if 'error' in válasz: raise AssertionError(válasz)
                            if 'return' in válasz: return válasz['return']
                    모의제어접속('qmp_capabilities')
                    képernyőkép = kimenet / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(képernyőkép), 'format': 'ppm'})
                    def 예제들(ÚTVONAL, 지점들):
                        with ÚTVONAL.open('rb') as képpont_Fájl:
                            assert képpont_Fájl.readline().strip() == b'P6'
                            assert képpont_Fájl.readline().strip() == b'640 480'
                            assert képpont_Fájl.readline().strip() == b'255'
                            képpont_adat = képpont_Fájl.read()
                        assert len(képpont_adat) == 640 * 480 * 3
                        return [list(képpont_adat[(Y_koordináta * 640 + x_koordináta) * 3:(Y_koordináta * 640 + x_koordináta) * 3 + 3]) for x_koordináta, Y_koordináta in 지점들]
                    assert 예제들(képernyőkép, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(képernyőkép, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def küld(누름값, jelölő):
                        Ofszet_ÉRTÉK = len(átirat)
                        Folyamat.stdin.write(누름값); Folyamat.stdin.flush()
                        표시까지받기(jelölő, Ofszet_ÉRTÉK)
                    küld(b'gui\n', b'GUI READY:')
                    첫화면 = kimenet / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(kimenet / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    küld(b'\r', b'GUI ACTION 0 RESULT 0')
                    küld(b'\t', b'GUI FOCUS 1')
                    küld(b'\r', b'GUI ACTION 1 RESULT 0')
                    MPERC_vizuális_felület = kimenet / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(MPERC_vizuális_felület), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(kimenet / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(MPERC_vizuális_felület, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    küld(b'\t', b'GUI FOCUS 2')
                    küld(b'\r', b'GUI ACTION 2 RESULT 0')
                    küld(b'\t', b'GUI FOCUS 3')
                    küld(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(kimenet / 'gui-python.png'), 'format': 'png'})
                    küld(b'q', b'jkoros-native> ')
                    ellenőrzés_jelent['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Folyamat.wait(timeout=10)
            # framebuffer 응답뿐 아니라 tényleges_adat scanout 픽셀도 확인한다.
            with képernyőkép.open('rb') as Fájl_bejegyzés:
                assert Fájl_bejegyzés.readline().strip() == b'P6'
                치수 = Fájl_bejegyzés.readline().strip()
                assert 치수 == b'640 480', 치수
                assert Fájl_bejegyzés.readline().strip() == b'255'
                화소들 = Fájl_bejegyzés.read()
            assert len(화소들) == 640 * 480 * 3
            def képpont(x_koordináta, Y_koordináta): return list(화소들[(Y_koordináta * 640 + x_koordináta) * 3:(Y_koordináta * 640 + x_koordináta) * 3 + 3])
            예제들 = {'background': képpont(5, 5), 'panel': képpont(45, 85), 'tile': képpont(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            ellenőrzés_jelent.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((teendő_gyök / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Folyamat.poll() is None:
                Folyamat.terminate()
                try: Folyamat.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Folyamat.kill(); Folyamat.wait(timeout=5)
            szelektor.close()
            Folyamat.stdin.close(); Folyamat.stdout.close()
            (kimenet / 'serial.log').write_bytes(átirat)
            (kimenet / 'report.json').write_text(json.dumps(ellenőrzés_jelent, indent=2) + '\n')


if __name__ == '__main__':
    Futtatás()
