#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

posição = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        resultado = 검사()
        if resultado:
            return resultado
        time.sleep(0.05)
    raise AssertionError('valor_temporal 초과: ' + 설명)


def testes(Tipo_VALOR):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        monitor_caminho = 임시 / 'monitor.sock'
        comando = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_caminho) + ',server,nowait']
        comando += ['-kernel', str(posição / 'build/kernel.elf')] if Tipo_VALOR == 'elf' else [
            '-cdrom', str(posição / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        comando += ['-S']
        Processo_VALOR = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        monitor_VALOR = socket.socket(socket.AF_UNIX)
        LOG_linha = bytearray()
        try:
            def Preparar_soquete():
                if Processo_VALOR.poll() is not None:
                    raise AssertionError(Processo_VALOR.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and monitor_caminho.exists()
            기다리기(Preparar_soquete, 'QEMU soquete_VALOR')
            직렬.connect(str(직렬경로))
            monitor_VALOR.connect(str(monitor_caminho))
            직렬.setblocking(False)
            monitor_VALOR.sendall(b'cont\n')

            def declarações(cadeia_VALOR, iniciar=0):
                Leitura, _, _ = select.select([직렬], [], [], 0.1)
                if Leitura:
                    dados = 직렬.recv(65536)
                    if not dados:
                        raise AssertionError('직렬 Ligar sair_app')
                    LOG_linha.extend(dados)
                if Processo_VALOR.poll() is not None:
                    raise AssertionError('QEMU 비정상 sair_app: ' + str(Processo_VALOR.returncode))
                return cadeia_VALOR.encode('utf-8') in LOG_linha[iniciar:]

            def 명령시험(entrada_VALOR, 기대):
                iniciar = len(LOG_linha)
                직렬.sendall(entrada_VALOR.encode('ascii'))
                기다리기(lambda: declarações(기대, iniciar), 기대)
                기다리기(lambda: declarações('jkoros> ', iniciar), 'comando 후 프롬프트')

            기다리기(lambda: declarações('READY'), Tipo_VALOR + ' arranque_da_máquina')
            assert b'JAVA SELFTEST PASS' in LOG_linha
            assert '자바 기계어 kernel_VALOR iniciar'.encode() in LOG_linha
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for ÍNDICE in range(8):
                명령시험('alloc\n', 'seção_VALOR ÍNDICE: ' + str(ÍNDICE))
            명령시험('alloc\n', 'seção_VALOR ÍNDICE: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 seção_VALOR')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'seção_VALOR ÍNDICE: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 número 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            iniciar = len(LOG_linha)
            for Chave_VALOR in ('i', 'n', 'f', 'o', 'ret'):
                monitor_VALOR.sendall(('sendkey ' + Chave_VALOR + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: declarações('embedded subset JVM / polling kernel', iniciar), 'PS/2 info entrada_VALOR')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: declarações('HALTED'), '정지 comando')
            assert b'PANIC' not in LOG_linha and b'SELFTEST FAIL' not in LOG_linha
            print('PASS: {} arranque_da_máquina, Java nativo testes, 직렬 comando, PS/2 entrada_VALOR, alocar_Armazenamento/devolver_RC, 정지'.format(Tipo_VALOR))
            return LOG_linha.decode('utf-8', 'replace')
        finally:
            직렬.close()
            monitor_VALOR.close()
            Processo_VALOR.terminate()
            try:
                Processo_VALOR.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Processo_VALOR.kill()
                Processo_VALOR.wait()


if __name__ == '__main__':
    resultado = {Tipo_VALOR: testes(Tipo_VALOR) for Tipo_VALOR in ('elf', 'iso')}
    (posição / 'build/부팅시험.json').write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
