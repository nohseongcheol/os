#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

위치 = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        결과 = 검사()
        if 결과:
            return 결과
        time.sleep(0.05)
    raise AssertionError('lokaci_Daraja 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        Allon_kwamfuta_Hanyar_shiga = 임시 / 'monitor.sock'
        Umarni = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(Allon_kwamfuta_Hanyar_shiga) + ',server,nowait']
        Umarni += ['-kernel', str(위치 / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(위치 / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        Umarni += ['-S']
        haryar_aikin_na_ura_Daraja = subprocess.Popen(Umarni, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        Allon_kwamfuta_Daraja = socket.socket(socket.AF_UNIX)
        logu_naɗa = bytearray()
        try:
            def 소켓준비():
                if haryar_aikin_na_ura_Daraja.poll() is not None:
                    raise AssertionError(haryar_aikin_na_ura_Daraja.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and Allon_kwamfuta_Hanyar_shiga.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            Allon_kwamfuta_Daraja.connect(str(Allon_kwamfuta_Hanyar_shiga))
            직렬.setblocking(False)
            Allon_kwamfuta_Daraja.sendall(b'cont\n')

            def 포함(Zare_Daraja, Tafiyar_da=0):
                Yi_Karatu, _, _ = select.select([직렬], [], [], 0.1)
                if Yi_Karatu:
                    Tarin_bayani = 직렬.recv(65536)
                    if not Tarin_bayani:
                        raise AssertionError('직렬 Haɗi Mafita_Shiri')
                    logu_naɗa.extend(Tarin_bayani)
                if haryar_aikin_na_ura_Daraja.poll() is not None:
                    raise AssertionError('QEMU 비정상 Mafita_Shiri: ' + str(haryar_aikin_na_ura_Daraja.returncode))
                return Zare_Daraja.encode('utf-8') in logu_naɗa[Tafiyar_da:]

            def 명령시험(입력, 기대):
                Tafiyar_da = len(logu_naɗa)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, Tafiyar_da), 기대)
                기다리기(lambda: 포함('jkoros> ', Tafiyar_da), 'Umarni 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in logu_naɗa
            assert '자바 기계어 Kwara_Daraja Tafiyar_da'.encode() in logu_naɗa
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for Indes in range(8):
                명령시험('alloc\n', 'Sashi_Daraja Indes: ' + str(Indes))
            명령시험('alloc\n', 'Sashi_Daraja Indes: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 Sashi_Daraja')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'Sashi_Daraja Indes: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Tafiyar_da = len(logu_naɗa)
            for Makulli_Daraja in ('i', 'n', 'f', 'o', 'ret'):
                Allon_kwamfuta_Daraja.sendall(('sendkey ' + Makulli_Daraja + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', Tafiyar_da), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 Umarni')
            assert b'PANIC' not in logu_naɗa and b'SELFTEST FAIL' not in logu_naɗa
            print('PASS: {} 부팅, Java 자체 시험, 직렬 Umarni, PS/2 입력, kasafta_Wurin_adana/반환, 정지'.format(종류))
            return logu_naɗa.decode('utf-8', 'replace')
        finally:
            직렬.close()
            Allon_kwamfuta_Daraja.close()
            haryar_aikin_na_ura_Daraja.terminate()
            try:
                haryar_aikin_na_ura_Daraja.wait(timeout=3)
            except subprocess.TimeoutExpired:
                haryar_aikin_na_ura_Daraja.kill()
                haryar_aikin_na_ura_Daraja.wait()


if __name__ == '__main__':
    결과 = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (위치 / 'build/부팅시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
