#!/usr/bin/env python3
"""effettivo_dati raspi4b avvio_macchina, UART input_VALORE, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from Esegui_comando import azione_radice, comando


def avvia():
    output = azione_radice / 'build/verification'
    output.mkdir(parents=True, exist_ok=True)
    trascrizione = bytearray()
    convalida_Report = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = comando() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        convalida_Report['command'] = 명령인수
        Processi = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        selettore = selectors.DefaultSelector()
        selettore.register(Processi.stdout, selectors.EVENT_READ)
        def 표시까지받기(marcatore, SCARTO_VALORE=0, esecuzione_TIMEOUT=45):
            scadenza_time = time.monotonic() + esecuzione_TIMEOUT
            while marcatore not in trascrizione[SCARTO_VALORE:]:
                if time.monotonic() > scadenza_time:
                    raise AssertionError('UART timeout: ' + repr(marcatore))
                for 누름값, _ in selettore.select(0.2):
                    blocco_di_dati = 누름값.fileobj.read(4096)
                    if blocco_di_dati:
                        trascrizione.extend(blocco_di_dati)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', trascrizione):
                    raise AssertionError('kernel failure')
                if Processi.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Processi.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for marcatore in 확인표시들:
                assert marcatore in trascrizione, marcatore
            # GTK 없는 Regolari_articolo 호스트에서도 VNC로 effettivo_dati GUI를 볼 numero 있어야 한다.
            with socket.socket(socket.AF_UNIX) as schermata_client:
                schermata_client.settimeout(5); schermata_client.connect(str(Path(작업경로) / 'vnc.sock'))
                def IDENTICO_VALORE(Dimensione):
                    risultato = b''
                    while len(risultato) < Dimensione:
                        blocco_VALORE_652d4b53 = schermata_client.recv(Dimensione - len(risultato))
                        if not blocco_VALORE_652d4b53: raise AssertionError('VNC disconnected')
                        risultato += blocco_VALORE_652d4b53
                    return risultato
                assert IDENTICO_VALORE(12) == b'RFB 003.008\n'
                schermata_client.sendall(b'RFB 003.008\n')
                assert 1 in IDENTICO_VALORE(IDENTICO_VALORE(1)[0]); schermata_client.sendall(b'\x01')
                assert IDENTICO_VALORE(4) == b'\x00\x00\x00\x00'; schermata_client.sendall(b'\x01')
                server_VALORE = IDENTICO_VALORE(24)
                assert int.from_bytes(server_VALORE[:2], 'big') == 640 and int.from_bytes(server_VALORE[2:4], 'big') == 480
                IDENTICO_VALORE(int.from_bytes(server_VALORE[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for comando_byte, marcatore in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', 'prove.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                SCARTO_VALORE = len(trascrizione)
                Processi.stdin.write(comando_byte + b'\n')
                Processi.stdin.flush()
                표시까지받기(b'jkoros-native> ', SCARTO_VALORE)
                assert marcatore in trascrizione[SCARTO_VALORE:], marcatore
            def Shell(riga_di_ingresso, 예상결과):
                SCARTO_VALORE = len(trascrizione)
                Processi.stdin.write(riga_di_ingresso.encode('utf-8') + b'\n'); Processi.stdin.flush()
                표시까지받기(b'jkoros-native> ', SCARTO_VALORE)
                risposta = bytes(trascrizione[SCARTO_VALORE:])
                for testo in 예상결과:
                    assert testo.encode('utf-8') in risposta, (riga_di_ingresso, testo, risposta)
                return risposta
            def immettere(riga_di_ingresso, prompt):
                SCARTO_VALORE = len(trascrizione)
                Processi.stdin.write(riga_di_ingresso.encode('utf-8') + b'\n'); Processi.stdin.flush()
                표시까지받기(prompt, SCARTO_VALORE)
                return bytes(trascrizione[SCARTO_VALORE:])
            def Modifica_VALORE(Nome, Contenuto_VALORE, Chiudi_operazione=False):
                immettere('edit ' + Nome, b'edit> ')
                for riga_di_ingresso in Contenuto_VALORE.splitlines(): immettere(riga_di_ingresso, b'edit> ')
                if Chiudi_operazione:
                    SCARTO_VALORE = len(trascrizione)
                    Processi.stdin.write(b'\x03'); Processi.stdin.flush()
                    표시까지받기(b'jkoros-native> ', SCARTO_VALORE)
                    assert b'EDIT CANCELLED' in trascrizione[SCARTO_VALORE:]
                else:
                    assert b'SAVED' in immettere('.', b'jkoros-native> ')
            def Upload_File(Nome, dati):
                assert len(dati) <= 16384
                immettere('load ' + Nome, b'hex> ')
                for 순번 in range(0, len(dati), 64): immettere(dati[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in immettere('.', b'jkoros-native> ')
            def download(Nome):
                risposta = Shell('hex ' + Nome, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', risposta, re.S)
                dati = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(dati) == int(일치.group(1)); return dati
            Shell('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            Shell('java -version', ['not OpenJDK', 'exit 0'])
            Shell('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            Shell('java Hello "한글 argomenti 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 argomenti 😀', 'exit 0'])
            Shell('python --version', ['MicroPython 1.24.1', 'exit 0'])
            Shell('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 file', 'exit 0'])
            Shell('cat python.txt', ['한글 file'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = output / 'Hello.class'; 자바클래스.write_bytes(download('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(output), 'Hello', '한글 argomenti 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 argomenti 😀'], 예상결과
            Modifica_VALORE('messaggio_di_saluto_ae353e94.java', 'public class messaggio_di_saluto_ae353e94 { public static void main(String[] args) { int VALORE = 7; System.out.println("한글=" + VALORE); } }')
            Shell('javac messaggio_di_saluto_ae353e94.java', ['Compiled: messaggio_di_saluto_ae353e94.class', 'exit 0'])
            Shell('java messaggio_di_saluto_ae353e94', ['한글=7', 'exit 0'])
            (output / 'messaggio_di_saluto_ae353e94.class').write_bytes(download('messaggio_di_saluto_ae353e94.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(output), 'messaggio_di_saluto_ae353e94']).decode().strip() == '한글=7'
            Modifica_VALORE('Hello.java', 'broken', Chiudi_operazione=True)
            Shell('javac Hello.java', ['Compiled:', 'exit 0'])
            Modifica_VALORE('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            Shell('javac Broken.java', ['javac error:', 'exit 1'])
            Upload_File('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            Shell('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            Shell('rm Broken.java', [])
            들여온파일 = output / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Upload_File('Imported.class', (output / 'Imported.class').read_bytes())
            Shell('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            Shell('rm Imported.class', [])
            Modifica_VALORE('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            Shell('javac Loop.java', ['Compiled:', 'exit 0'])
            risposta = Shell('java Loop', ['exit '])
            assert b'instruction limit' in risposta or b'exit -1004' in risposta
            Shell('rm Loop.java', []); Shell('rm Loop.class', [])
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
            Modifica_VALORE('checks.py', 파이썬검사)
            Shell('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            Shell('rm checks.py', [])
            Modifica_VALORE('helper.py', 'value = 321')
            Shell("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            Shell('rm helper.py', [])
            Shell("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            Shell("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                Shell('python hello.py', ['한글 file', 'exit 0'])
                Shell('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Upload_File('app.elf', (azione_radice / 'build/user/demo.elf').read_bytes())
            assert download('app.elf') == (azione_radice / 'build/user/demo.elf').read_bytes()
            Shell('run app.elf', ['EL0 C++', 'exit 0'])
            Upload_File('app.elf', b'not an ELF')
            Shell('run app.elf', ['exit -8'])
            Shell('rm app.elf', [])
            Shell('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            disegno_percorso = output / 'java-framebuffer'; disegno_percorso.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(azione_radice / 'dist/jkoros-native-korean.jar'), '-d', str(disegno_percorso), str(azione_radice / 'prove/자바/test_schermata.java')])
            Upload_File('test_schermata.class', (disegno_percorso / 'test_schermata.class').read_bytes())
            Shell('java test_schermata', ['schermata ritagliare rifiutare_VALORE', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            Shell('rm test_schermata.class', [])
            with socket.socket(socket.AF_UNIX) as client:
                client.settimeout(10)
                client.connect(str(모의제어경로))
                with client.makefile('rwb') as Stream_VALORE:
                    messaggio_di_saluto_ae353e94 = json.loads(Stream_VALORE.readline())
                    def 모의제어접속(Esegui, 전달인수=None):
                        rete_documento = {'execute': Esegui}
                        if 전달인수: rete_documento['arguments'] = 전달인수
                        Stream_VALORE.write((json.dumps(rete_documento) + '\n').encode())
                        Stream_VALORE.flush()
                        while True:
                            replica = json.loads(Stream_VALORE.readline())
                            if 'error' in replica: raise AssertionError(replica)
                            if 'return' in replica: return replica['return']
                    모의제어접속('qmp_capabilities')
                    screenshot = output / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(screenshot), 'format': 'ppm'})
                    def 예제들(percorso, 지점들):
                        with percorso.open('rb') as pixel_File:
                            assert pixel_File.readline().strip() == b'P6'
                            assert pixel_File.readline().strip() == b'640 480'
                            assert pixel_File.readline().strip() == b'255'
                            pixel_dati = pixel_File.read()
                        assert len(pixel_dati) == 640 * 480 * 3
                        return [list(pixel_dati[(Y_coordinata * 640 + coordinata_x) * 3:(Y_coordinata * 640 + coordinata_x) * 3 + 3]) for coordinata_x, Y_coordinata in 지점들]
                    assert 예제들(screenshot, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(screenshot, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def inviare(누름값, marcatore):
                        SCARTO_VALORE = len(trascrizione)
                        Processi.stdin.write(누름값); Processi.stdin.flush()
                        표시까지받기(marcatore, SCARTO_VALORE)
                    inviare(b'gui\n', b'GUI READY:')
                    첫화면 = output / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(output / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    inviare(b'\r', b'GUI ACTION 0 RESULT 0')
                    inviare(b'\t', b'GUI FOCUS 1')
                    inviare(b'\r', b'GUI ACTION 1 RESULT 0')
                    SECONDO_GUI = output / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SECONDO_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(output / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SECONDO_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    inviare(b'\t', b'GUI FOCUS 2')
                    inviare(b'\r', b'GUI ACTION 2 RESULT 0')
                    inviare(b'\t', b'GUI FOCUS 3')
                    inviare(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(output / 'gui-python.png'), 'format': 'png'})
                    inviare(b'q', b'jkoros-native> ')
                    convalida_Report['qemu'] = messaggio_di_saluto_ae353e94['QMP']['version']
                    모의제어접속('quit')
            Processi.wait(timeout=10)
            # framebuffer 응답뿐 아니라 effettivo_dati scanout 픽셀도 확인한다.
            with screenshot.open('rb') as File_voce:
                assert File_voce.readline().strip() == b'P6'
                치수 = File_voce.readline().strip()
                assert 치수 == b'640 480', 치수
                assert File_voce.readline().strip() == b'255'
                화소들 = File_voce.read()
            assert len(화소들) == 640 * 480 * 3
            def pixel(coordinata_x, Y_coordinata): return list(화소들[(Y_coordinata * 640 + coordinata_x) * 3:(Y_coordinata * 640 + coordinata_x) * 3 + 3])
            예제들 = {'background': pixel(5, 5), 'panel': pixel(45, 85), 'tile': pixel(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            convalida_Report.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((azione_radice / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Processi.poll() is None:
                Processi.terminate()
                try: Processi.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Processi.kill(); Processi.wait(timeout=5)
            selettore.close()
            Processi.stdin.close(); Processi.stdout.close()
            (output / 'serial.log').write_bytes(trascrizione)
            (output / 'report.json').write_text(json.dumps(convalida_Report, indent=2) + '\n')


if __name__ == '__main__':
    avvia()
