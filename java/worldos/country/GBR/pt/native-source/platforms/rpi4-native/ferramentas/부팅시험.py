#!/usr/bin/env python3
"""real_dados raspi4b arranque_da_máquina, UART entrada_VALOR, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from Executar_comando import ação_raiz, comando


def iniciar():
    saída = ação_raiz / 'build/verification'
    saída.mkdir(parents=True, exist_ok=True)
    transcrição = bytearray()
    validação_relatar = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as 작업경로:
        모의제어경로 = Path(작업경로) / 'qmp.sock'
        명령인수 = comando() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(모의제어경로),
                           '-vnc', 'unix:{}'.format(Path(작업경로) / 'vnc.sock')]
        validação_relatar['command'] = 명령인수
        Processo = subprocess.Popen(명령인수, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        seletor = selectors.DefaultSelector()
        seletor.register(Processo.stdout, selectors.EVENT_READ)
        def 표시까지받기(favorito, DESLOC_VALOR=0, execução_TEMPOLIMITE=45):
            data_limite_time = time.monotonic() + execução_TEMPOLIMITE
            while favorito not in transcrição[DESLOC_VALOR:]:
                if time.monotonic() > data_limite_time:
                    raise AssertionError('UART timeout: ' + repr(favorito))
                for 누름값, _ in seletor.select(0.2):
                    bloco_de_dados = 누름값.fileobj.read(4096)
                    if bloco_de_dados:
                        transcrição.extend(bloco_de_dados)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', transcrição):
                    raise AssertionError('kernel failure')
                if Processo.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(Processo.returncode))
        try:
            표시까지받기(b'jkoros-native> ')
            확인표시들 = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for favorito in 확인표시들:
                assert favorito in transcrição, favorito
            # GTK 없는 em_dia_item 호스트에서도 VNC로 real_dados GUI를 볼 número 있어야 한다.
            with socket.socket(socket.AF_UNIX) as tela_cliente:
                tela_cliente.settimeout(5); tela_cliente.connect(str(Path(작업경로) / 'vnc.sock'))
                def EXATO_VALOR(Tamanho):
                    resultado = b''
                    while len(resultado) < Tamanho:
                        fragmento_VALOR = tela_cliente.recv(Tamanho - len(resultado))
                        if not fragmento_VALOR: raise AssertionError('VNC disconnected')
                        resultado += fragmento_VALOR
                    return resultado
                assert EXATO_VALOR(12) == b'RFB 003.008\n'
                tela_cliente.sendall(b'RFB 003.008\n')
                assert 1 in EXATO_VALOR(EXATO_VALOR(1)[0]); tela_cliente.sendall(b'\x01')
                assert EXATO_VALOR(4) == b'\x00\x00\x00\x00'; tela_cliente.sendall(b'\x01')
                servidor_VALOR = EXATO_VALOR(24)
                assert int.from_bytes(servidor_VALOR[:2], 'big') == 640 and int.from_bytes(servidor_VALOR[2:4], 'big') == 480
                EXATO_VALOR(int.from_bytes(servidor_VALOR[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for comando_byte, favorito in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', 'testes.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                DESLOC_VALOR = len(transcrição)
                Processo.stdin.write(comando_byte + b'\n')
                Processo.stdin.flush()
                표시까지받기(b'jkoros-native> ', DESLOC_VALOR)
                assert favorito in transcrição[DESLOC_VALOR:], favorito
            def shell(linha_de_entrada, 예상결과):
                DESLOC_VALOR = len(transcrição)
                Processo.stdin.write(linha_de_entrada.encode('utf-8') + b'\n'); Processo.stdin.flush()
                표시까지받기(b'jkoros-native> ', DESLOC_VALOR)
                réplica = bytes(transcrição[DESLOC_VALOR:])
                for texto in 예상결과:
                    assert texto.encode('utf-8') in réplica, (linha_de_entrada, texto, réplica)
                return réplica
            def inserir(linha_de_entrada, aviso_1dd14da4):
                DESLOC_VALOR = len(transcrição)
                Processo.stdin.write(linha_de_entrada.encode('utf-8') + b'\n'); Processo.stdin.flush()
                표시까지받기(aviso_1dd14da4, DESLOC_VALOR)
                return bytes(transcrição[DESLOC_VALOR:])
            def Editar_VALOR(Nome, Conteúdo_VALOR, Close_cirurgia=False):
                inserir('edit ' + Nome, b'edit> ')
                for linha_de_entrada in Conteúdo_VALOR.splitlines(): inserir(linha_de_entrada, b'edit> ')
                if Close_cirurgia:
                    DESLOC_VALOR = len(transcrição)
                    Processo.stdin.write(b'\x03'); Processo.stdin.flush()
                    표시까지받기(b'jkoros-native> ', DESLOC_VALOR)
                    assert b'EDIT CANCELLED' in transcrição[DESLOC_VALOR:]
                else:
                    assert b'SAVED' in inserir('.', b'jkoros-native> ')
            def Upload_Arquivos(Nome, dados):
                assert len(dados) <= 16384
                inserir('load ' + Nome, b'hex> ')
                for 순번 in range(0, len(dados), 64): inserir(dados[순번:순번+64].hex(), b'hex> ')
                assert b'LOADED' in inserir('.', b'jkoros-native> ')
            def baixar(Nome):
                réplica = shell('hex ' + Nome, ['HEX BEGIN', 'HEX END'])
                일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', réplica, re.S)
                dados = bytes.fromhex(''.join(일치.group(2).decode('ascii').split()))
                assert len(dados) == int(일치.group(1)); return dados
            shell('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            shell('java -version', ['not OpenJDK', 'exit 0'])
            shell('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            shell('java Hello "한글 argumentos 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 argumentos 😀', 'exit 0'])
            shell('python --version', ['MicroPython 1.24.1', 'exit 0'])
            shell('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 ficheiro', 'exit 0'])
            shell('cat python.txt', ['한글 ficheiro'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            자바클래스 = saída / 'Hello.class'; 자바클래스.write_bytes(baixar('Hello.class'))
            예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(saída), 'Hello', '한글 argumentos 😀']).decode('utf-8')
            assert 예상결과.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 argumentos 😀'], 예상결과
            Editar_VALOR('saudação_ae353e94.java', 'public class saudação_ae353e94 { public static void main(String[] args) { int VALOR = 7; System.out.println("한글=" + VALOR); } }')
            shell('javac saudação_ae353e94.java', ['Compiled: saudação_ae353e94.class', 'exit 0'])
            shell('java saudação_ae353e94', ['한글=7', 'exit 0'])
            (saída / 'saudação_ae353e94.class').write_bytes(baixar('saudação_ae353e94.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(saída), 'saudação_ae353e94']).decode().strip() == '한글=7'
            Editar_VALOR('Hello.java', 'broken', Close_cirurgia=True)
            shell('javac Hello.java', ['Compiled:', 'exit 0'])
            Editar_VALOR('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            shell('javac Broken.java', ['javac error:', 'exit 1'])
            Upload_Arquivos('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            shell('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            shell('rm Broken.java', [])
            들여온파일 = saída / 'Imported.java'
            들여온파일.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(들여온파일)])
            Upload_Arquivos('Imported.class', (saída / 'Imported.class').read_bytes())
            shell('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            shell('rm Imported.class', [])
            Editar_VALOR('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            shell('javac Loop.java', ['Compiled:', 'exit 0'])
            réplica = shell('java Loop', ['exit '])
            assert b'instruction limit' in réplica or b'exit -1004' in réplica
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
                shell('python hello.py', ['한글 ficheiro', 'exit 0'])
                shell('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            Upload_Arquivos('app.elf', (ação_raiz / 'build/user/demo.elf').read_bytes())
            assert baixar('app.elf') == (ação_raiz / 'build/user/demo.elf').read_bytes()
            shell('run app.elf', ['EL0 C++', 'exit 0'])
            Upload_Arquivos('app.elf', b'not an ELF')
            shell('run app.elf', ['exit -8'])
            shell('rm app.elf', [])
            shell('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            desenho_caminho = saída / 'java-framebuffer'; desenho_caminho.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(ação_raiz / 'dist/jkoros-native-korean.jar'), '-d', str(desenho_caminho), str(ação_raiz / 'testes/자바/teste_tela.java')])
            Upload_Arquivos('teste_tela.class', (desenho_caminho / 'teste_tela.class').read_bytes())
            shell('java teste_tela', ['tela recortar rejeitar_VALOR', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            shell('rm teste_tela.class', [])
            with socket.socket(socket.AF_UNIX) as cliente:
                cliente.settimeout(10)
                cliente.connect(str(모의제어경로))
                with cliente.makefile('rwb') as fluxo_VALOR:
                    saudação_ae353e94 = json.loads(fluxo_VALOR.readline())
                    def 모의제어접속(Executar, 전달인수=None):
                        rede_email = {'execute': Executar}
                        if 전달인수: rede_email['arguments'] = 전달인수
                        fluxo_VALOR.write((json.dumps(rede_email) + '\n').encode())
                        fluxo_VALOR.flush()
                        while True:
                            resposta = json.loads(fluxo_VALOR.readline())
                            if 'error' in resposta: raise AssertionError(resposta)
                            if 'return' in resposta: return resposta['return']
                    모의제어접속('qmp_capabilities')
                    captura_de_tela = saída / 'framebuffer.ppm'
                    모의제어접속('screendump', {'filename': str(captura_de_tela), 'format': 'ppm'})
                    def 예제들(caminho, 지점들):
                        with caminho.open('rb') as pixel_Arquivo:
                            assert pixel_Arquivo.readline().strip() == b'P6'
                            assert pixel_Arquivo.readline().strip() == b'640 480'
                            assert pixel_Arquivo.readline().strip() == b'255'
                            pixel_dados = pixel_Arquivo.read()
                        assert len(pixel_dados) == 640 * 480 * 3
                        return [list(pixel_dados[(Y_coordenada * 640 + coordenada_X) * 3:(Y_coordenada * 640 + coordenada_X) * 3 + 3]) for coordenada_X, Y_coordenada in 지점들]
                    assert 예제들(captura_de_tela, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert 예제들(captura_de_tela, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def enviar(누름값, favorito):
                        DESLOC_VALOR = len(transcrição)
                        Processo.stdin.write(누름값); Processo.stdin.flush()
                        표시까지받기(favorito, DESLOC_VALOR)
                    enviar(b'gui\n', b'GUI READY:')
                    첫화면 = saída / 'gui-programs.ppm'
                    모의제어접속('screendump', {'filename': str(첫화면), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(saída / 'gui-programs.png'), 'format': 'png'})
                    assert 예제들(첫화면, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    enviar(b'\r', b'GUI ACTION 0 RESULT 0')
                    enviar(b'\t', b'GUI FOCUS 1')
                    enviar(b'\r', b'GUI ACTION 1 RESULT 0')
                    SEGUNDO_GUI = saída / 'gui-network.ppm'
                    모의제어접속('screendump', {'filename': str(SEGUNDO_GUI), 'format': 'ppm'})
                    모의제어접속('screendump', {'filename': str(saída / 'gui-network.png'), 'format': 'png'})
                    assert 예제들(SEGUNDO_GUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    enviar(b'\t', b'GUI FOCUS 2')
                    enviar(b'\r', b'GUI ACTION 2 RESULT 0')
                    enviar(b'\t', b'GUI FOCUS 3')
                    enviar(b'\r', b'GUI ACTION 3 RESULT 0')
                    모의제어접속('screendump', {'filename': str(saída / 'gui-python.png'), 'format': 'png'})
                    enviar(b'q', b'jkoros-native> ')
                    validação_relatar['qemu'] = saudação_ae353e94['QMP']['version']
                    모의제어접속('quit')
            Processo.wait(timeout=10)
            # framebuffer 응답뿐 아니라 real_dados scanout 픽셀도 확인한다.
            with captura_de_tela.open('rb') as Arquivo_entrada:
                assert Arquivo_entrada.readline().strip() == b'P6'
                치수 = Arquivo_entrada.readline().strip()
                assert 치수 == b'640 480', 치수
                assert Arquivo_entrada.readline().strip() == b'255'
                화소들 = Arquivo_entrada.read()
            assert len(화소들) == 640 * 480 * 3
            def pixel(coordenada_X, Y_coordenada): return list(화소들[(Y_coordenada * 640 + coordenada_X) * 3:(Y_coordenada * 640 + coordenada_X) * 3 + 3])
            예제들 = {'background': pixel(5, 5), 'panel': pixel(45, 85), 'tile': pixel(65, 115)}
            assert 예제들 == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, 예제들
            validação_relatar.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
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
                framebuffer=예제들, kernel_sha256=hashlib.sha256((ação_raiz / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if Processo.poll() is None:
                Processo.terminate()
                try: Processo.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    Processo.kill(); Processo.wait(timeout=5)
            seletor.close()
            Processo.stdin.close(); Processo.stdout.close()
            (saída / 'serial.log').write_bytes(transcrição)
            (saída / 'report.json').write_text(json.dumps(validação_relatar, indent=2) + '\n')


if __name__ == '__main__':
    iniciar()
