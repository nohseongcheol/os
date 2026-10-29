#!/usr/bin/env python3
"""real_dades raspi4b 부팅, UART 입력, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from Executa_ordre import Project_rel, Ordre


def Executa_2():
    출력결과 = Project_rel / 'build/verification'
    출력결과.mkdir(parents=True, exist_ok=True)
    대화기록 = bytearray()
    validació_informe = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = Ordre() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        validació_informe['command'] = 명령인수
        Procés = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        준비선택기 = selectors.DefaultSelector()
        준비선택기.register(Procés.stdout, selectors.EVENT_READ)
        def 표시까지받기(확인표시, DESPLAÇAMENT_VALOR=0, 시간제한=45):
            마감시각 = time.monotonic() + 시간제한
            while 확인표시 not in 대화기록[DESPLAÇAMENT_VALOR:]:
                if time.monotonic() > 마감시각:
                    raise AssertionError('UART timeout: ' + repr(확인표시))
                for 누름값, _ in 준비선택기.select(0.2):
                    dades_bloquejar = 누름값.fileobj.read(4096)
                    if dades_bloquejar:
                        대화기록.extend(dades_bloquejar)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', 대화기록):
                    raise AssertionError('kernel failure')
                if Procés.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Procés.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for 확인표시 in 확인표시들:
                assert 확인표시 in 대화기록, 확인표시
            # GTK 없는 현재 호스트에서도 VNC로 real_dades GUI를 볼 수 있어야 한다.
            with socket.socket(socket.AF_UNIX) as 화면접속자:
                화면접속자.settimeout(5); 화면접속자.connect(str(Path(작업경로) / 'vnc.sock'))
                def IGUAL_VALOR(Mida):
                    RESULTAT = b''
                    while len(RESULTAT) < Mida:
                        조각 = 화면접속자.recv(Mida - len(RESULTAT))
                        if not 조각: raise AssertionError('VNC disconnected')
                        RESULTAT += 조각
                    return RESULTAT
                assert IGUAL_VALOR(12) == b'RFB 003.008\n'
                화면접속자.sendall(b'RFB 003.008\n')
                assert 1 in IGUAL_VALOR(IGUAL_VALOR(1)[0]); 화면접속자.sendall(b'\x01')
                assert IGUAL_VALOR(4) == b'\x00\x00\x00\x00'; 화면접속자.sendall(b'\x01')
                servidor_VALOR = IGUAL_VALOR(24)
                assert int.from_bytes(servidor_VALOR[:2], 'big') == 640 and int.from_bytes(servidor_VALOR[2:4], 'big') == 480
                IGUAL_VALOR(int.from_bytes(servidor_VALOR[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for ordre_byte, 확인표시 in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', '시험.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                DESPLAÇAMENT_VALOR = len(대화기록)
                Procés.stdin.write(ordre_byte + b'\n')
                Procés.stdin.flush()
                표시까지받기(b'jkoros-native> ', DESPLAÇAMENT_VALOR)
                assert 확인표시 in 대화기록[DESPLAÇAMENT_VALOR:], 확인표시
            def shell(línia, 예상결과):
                DESPLAÇAMENT_VALOR = len(대화기록)
                Procés.stdin.write(línia.encode('utf-8') + b'\n'); Procés.stdin.flush()
                표시까지받기(b'jkoros-native> ', DESPLAÇAMENT_VALOR)
                resposta_1262b476 = bytes(대화기록[DESPLAÇAMENT_VALOR:])
                for SMS in 예상결과:
                    assert SMS.encode('utf-8') in resposta_1262b476, (línia, SMS, resposta_1262b476)
                return resposta_1262b476
            def introduir(línia, sol_licitar):
                DESPLAÇAMENT_VALOR = len(대화기록)
                Procés.stdin.write(línia.encode('utf-8') + b'\n'); Procés.stdin.flush()
                표시까지받기(sol_licitar, DESPLAÇAMENT_VALOR)
                return bytes(대화기록[DESPLAÇAMENT_VALOR:])
            def Editar_VALOR(Nom, contingut_VALOR, Cancel_la_cirurgia=False):
                introduir('edit ' + Nom, b'edit> ')
                for línia in contingut_VALOR.splitlines(): introduir(línia, b'edit> ')
                if Cancel_la_cirurgia:
                    DESPLAÇAMENT_VALOR = len(대화기록)
                    Procés.stdin.write(b'\x03'); Procés.stdin.flush()
                    표시까지받기(b'jkoros-native> ', DESPLAÇAMENT_VALOR)
                    assert b'EDIT CANCELLED' in 대화기록[DESPLAÇAMENT_VALOR:]
                else:
                    assert b'SAVED' in introduir('.', b'jkoros-native> ')
            def pujar_Fitxers(Nom, dades):
                assert len(dades) <= 16384
                introduir('load ' + Nom, b'hex> ')
                for 순번 in range(0, len(dades), 64): introduir(dades[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in introduir('.', b'jkoros-native> ')
            def baixar(Nom):
                resposta_1262b476 = shell('hex ' + Nom, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', resposta_1262b476, re.S)
                dades = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(dades) == int(일치.group(1)); return dades
            shell('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            shell('java -version', ['not OpenJDK', 'exit 0'])
            shell('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            shell('java Hello "한글 인수 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀', 'exit 0'])
            shell('python --version', ['MicroPython 1.24.1', 'exit 0'])
            shell('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Fitxer', 'exit 0'])
            shell('cat python.txt', ['한글 Fitxer'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = 출력결과 / 'Hello.class'; 자바클래스.write_bytes(baixar('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), 'Hello', '한글 인수 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 인수 😀'], 예상결과
            Editar_VALOR('인사.java', 'public class 인사 { public static void main(String[] args) { int VALOR = 7; System.out.println("한글=" + VALOR); } }')
            shell('javac 인사.java', ['Compiled: 인사.class', 'exit 0'])
            shell('java 인사', ['한글=7', 'exit 0'])
            (출력결과 / '인사.class').write_bytes(baixar('인사.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(출력결과), '인사']).decode().strip() == '한글=7'
            Editar_VALOR('Hello.java', 'broken', Cancel_la_cirurgia=True)
            shell('javac Hello.java', ['Compiled:', 'exit 0'])
            Editar_VALOR('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            shell('javac Broken.java', ['javac error:', 'exit 1'])
            pujar_Fitxers('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            shell('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            shell('rm Broken.java', [])
            들여온파일 = 출력결과 / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            pujar_Fitxers('Imported.class', (출력결과 / 'Imported.class').read_bytes())
            shell('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            shell('rm Imported.class', [])
            Editar_VALOR('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            shell('javac Loop.java', ['Compiled:', 'exit 0'])
            resposta_1262b476 = shell('java Loop', ['exit '])
            assert b'instruction limit' in resposta_1262b476 or b'exit -1004' in resposta_1262b476
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
            Editar_VALOR('checks.py', 파이썬검사)
            shell('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            shell('rm checks.py', [])
            Editar_VALOR('helper.py', 'value = 321')
            shell("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            shell('rm helper.py', [])
            shell("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            shell("python -c 'while True: pass'", ['exit -1004'])
            for 순번 in range(4):
                shell('python hello.py', ['한글 Fitxer', 'exit 0'])
                shell('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            pujar_Fitxers('app.elf', (Project_rel / 'build/user/demo.elf').read_bytes())
            assert baixar('app.elf') == (Project_rel / 'build/user/demo.elf').read_bytes()
            shell('run app.elf', ['EL0 C++', 'exit 0'])
            pujar_Fitxers('app.elf', b'not an ELF')
            shell('run app.elf', ['exit -8'])
            shell('rm app.elf', [])
            shell('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            dibuix_camí = 출력결과 / 'java-framebuffer'; dibuix_camí.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_rel / 'dist/jkoros-native-korean.jar'), '-d', str(dibuix_camí), str(Project_rel / '시험/자바/화면시험.java')])
            pujar_Fitxers('화면시험.class', (dibuix_camí / '화면시험.class').read_bytes())
            shell('java 화면시험', ['화면 clip rebutjar_VALOR', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            shell('rm 화면시험.class', [])
            with socket.socket(socket.AF_UNIX) as client:
                client.settimeout(10)
                client.connect(str(모의제어경로))
                with client.makefile('rwb') as flux_VALOR:
                    인사 = json.loads(flux_VALOR.readline())
                    def 모의제어접속(Executa, 전달인수=None):
                        xarxa_correu = {'execute': Executa}
                        if 전달인수: xarxa_correu['arguments'] = 전달인수
                        flux_VALOR.write((json.dumps(xarxa_correu) + '\n').encode())
                        flux_VALOR.flush()
                        while True:
                            resposta = json.loads(flux_VALOR.readline())
                            if 'error' in resposta: raise AssertionError(resposta)
                            if 'return' in resposta: return resposta['return']
                    모의제어접속('qmp_capabilities')
                    retall_de_pantalla = 출력결과 / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(retall_de_pantalla), 'format': 'ppm'})
                    def 예제들(Camí, 지점들):
                        with Camí.open('rb') as píxel_arxiu:
                            assert píxel_arxiu.readline().strip() == b'P6'
                            assert píxel_arxiu.readline().strip() == b'640 480'
                            assert píxel_arxiu.readline().strip() == b'255'
                            píxel_dades = píxel_arxiu.read()
                        assert len(píxel_dades) == 640 * 480 * 3
                        return [list(píxel_dades[(Y_coordenada * 640 + X_coordenada) * 3:(Y_coordenada * 640 + X_coordenada) * 3 + 3]) for X_coordenada, Y_coordenada in 지점들]
                    assert 예제들(retall_de_pantalla, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(retall_de_pantalla, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def enviar(누름값, 확인표시):
                        DESPLAÇAMENT_VALOR = len(대화기록)
                        Procés.stdin.write(누름값); Procés.stdin.flush()
                        표시까지받기(확인표시, DESPLAÇAMENT_VALOR)
                    enviar(b'gui\n', b'GUI READY:')
                    첫화면 = 출력결과 / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    enviar(b'\r', b'GUI ACTION 0 RESULT 0')
                    enviar(b'\t', b'GUI FOCUS 1')
                    enviar(b'\r', b'GUI ACTION 1 RESULT 0')
                    SEGON_GUI = 출력결과 / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SEGON_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SEGON_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    enviar(b'\t', b'GUI FOCUS 2')
                    enviar(b'\r', b'GUI ACTION 2 RESULT 0')
                    enviar(b'\t', b'GUI FOCUS 3')
                    enviar(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(출력결과 / 'gui-python.png'), 'format': 'png'})
                    enviar(b'q', b'jkoros-native> ')
                    validació_informe['qemu'] = 인사['QMP']['version']
                    모의제어접속('quit')
            Procés.wait(timeout=10)
            # framebuffer 응답뿐 아니라 real_dades scanout 픽셀도 확인한다.
            with retall_de_pantalla.open('rb') as arxiu_introducció:
                assert arxiu_introducció.readline().strip() == b'P6'
                치수 = arxiu_introducció.readline().strip()
                assert 치수 == b'640 480', 치수
                assert arxiu_introducció.readline().strip() == b'255'
                화소들 = arxiu_introducció.read()
            assert len(화소들) == 640 * 480 * 3
            def píxel(X_coordenada, Y_coordenada): return list(화소들[(Y_coordenada * 640 + X_coordenada) * 3:(Y_coordenada * 640 + X_coordenada) * 3 + 3])
            예제들 = {'background': píxel(5, 5), 'panel': píxel(45, 85), 'tile': píxel(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            validació_informe.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((Project_rel / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Procés.poll() is None:
                Procés.terminate()
                try: Procés.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Procés.kill(); Procés.wait(timeout=5)
            준비선택기.close()
            Procés.stdin.close(); Procés.stdout.close()
            (출력결과 / 'serial.log').write_bytes(대화기록)
            (출력결과 / 'report.json').write_text(json.dumps(validació_informe, indent=2) + '\n')


if __name__ == '__main__':
    Executa_2()
