#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

Posición = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        RESULTANTE = 검사()
        if RESULTANTE:
            return RESULTANTE
        time.sleep(0.05)
    raise AssertionError('hora_VALOR 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        monitor_camiño = 임시 / 'monitor.sock'
        Orde = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_camiño) + ',server,nowait']
        Orde += ['-kernel', str(Posición / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(Posición / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Orde += ['-S']
        Proceso_VALOR = subprocess.Popen(Orde, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        monitor_VALOR = socket.socket(socket.AF_UNIX)
        LOG_fila = bytearray()
        try:
            def 소켓준비():
                if Proceso_VALOR.poll() is not None:
                    raise AssertionError(Proceso_VALOR.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and monitor_camiño.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            monitor_VALOR.connect(str(monitor_camiño))
            직렬.setblocking(False)
            monitor_VALOR.sendall(b'cont\n')

            def 포함(cadea_VALOR, Executar_2=0):
                Lectura, _, _ = select.select([직렬], [], [], 0.1)
                if Lectura:
                    datos = 직렬.recv(65536)
                    if not datos:
                        raise AssertionError('직렬 Conectar saír_apl')
                    LOG_fila.extend(datos)
                if Proceso_VALOR.poll() is not None:
                    raise AssertionError('QEMU 비정상 saír_apl: ' + str(Proceso_VALOR.returncode))
                return cadea_VALOR.encode('utf-8') in LOG_fila[Executar_2:]

            def 명령시험(입력, 기대):
                Executar_2 = len(LOG_fila)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, Executar_2), 기대)
                기다리기(lambda: 포함('jkoros> ', Executar_2), 'Orde 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in LOG_fila
            assert '자바 기계어 kernel_VALOR Executar_2'.encode() in LOG_fila
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for ÍNDICE in range(8):
                명령시험('alloc\n', 'sección_VALOR ÍNDICE: ' + str(ÍNDICE))
            명령시험('alloc\n', 'sección_VALOR ÍNDICE: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 sección_VALOR')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'sección_VALOR ÍNDICE: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Executar_2 = len(LOG_fila)
            for Chave_VALOR in ('i', 'n', 'f', 'o', 'ret'):
                monitor_VALOR.sendall(('sendkey ' + Chave_VALOR + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Executar_2), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Orde')
            assert b'PANIC' not in LOG_fila and b'SELFTEST FAIL' not in LOG_fila
            print('PASS: {} 부팅, Java 자체 시험, 직렬 Orde, PS/2 입력, atribuír_Almacenamento/devolver_medida, 정지'.format(종류))
            return LOG_fila.decode('utf-8', 'replace')
        finally:
            직렬.close()
            monitor_VALOR.close()
            Proceso_VALOR.terminate()
            try:
                Proceso_VALOR.wait(timeout=3)
            except subprocess.TimeoutExpired:
                Proceso_VALOR.kill()
                Proceso_VALOR.wait()


if __name__ == '__main__':
    RESULTANTE = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (Posición / 'build/부팅시험.json').write_text(json.dumps(RESULTANTE, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
