#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

paikka = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        TULOS = 검사()
        if TULOS:
            return TULOS
        time.sleep(0.05)
    raise AssertionError('AIKA_ARVO 초과: ' + 설명)


def testit(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        näyttö_polku = 임시 / 'monitor.sock'
        komento = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(näyttö_polku) + ',server,nowait']
        komento += ['-kernel', str(paikka / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(paikka / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        komento += ['-S']
        prosessi_ARVO = subprocess.Popen(komento, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        näyttö_ARVO = socket.socket(socket.AF_UNIX)
        LOG_TIETUE = bytearray()
        try:
            def Valmistele_vastake():
                if prosessi_ARVO.poll() is not None:
                    raise AssertionError(prosessi_ARVO.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and näyttö_polku.exists()
            기다리기(Valmistele_vastake, 'QEMU vastake_ARVO')
            직렬.connect(str(직렬경로))
            näyttö_ARVO.connect(str(näyttö_polku))
            직렬.setblocking(False)
            näyttö_ARVO.sendall(b'cont\n')

            def esittelyt(merkkijono_ARVO, Suorita_2=0):
                Luku, _, _ = select.select([직렬], [], [], 0.1)
                if Luku:
                    data = 직렬.recv(65536)
                    if not data:
                        raise AssertionError('직렬 Yhdistä Lopeta_ohjelma')
                    LOG_TIETUE.extend(data)
                if prosessi_ARVO.poll() is not None:
                    raise AssertionError('QEMU 비정상 Lopeta_ohjelma: ' + str(prosessi_ARVO.returncode))
                return merkkijono_ARVO.encode('utf-8') in LOG_TIETUE[Suorita_2:]

            def 명령시험(syöte_ARVO, 기대):
                Suorita_2 = len(LOG_TIETUE)
                직렬.sendall(syöte_ARVO.encode('ascii'))
                기다리기(lambda: esittelyt(기대, Suorita_2), 기대)
                기다리기(lambda: esittelyt('jkoros> ', Suorita_2), 'komento 후 프롬프트')

            기다리기(lambda: esittelyt('READY'), 종류 + ' koneen_käynnistys')
            assert b'JAVA SELFTEST PASS' in LOG_TIETUE
            assert '자바 기계어 ydin_ARVO Suorita_2'.encode() in LOG_TIETUE
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for INDEKSI in range(8):
                명령시험('alloc\n', 'osa_ARVO INDEKSI: ' + str(INDEKSI))
            명령시험('alloc\n', 'osa_ARVO INDEKSI: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 osa_ARVO')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'osa_ARVO INDEKSI: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 numero 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            Suorita_2 = len(LOG_TIETUE)
            for Avain_ARVO in ('i', 'n', 'f', 'o', 'ret'):
                näyttö_ARVO.sendall(('sendkey ' + Avain_ARVO + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: esittelyt('embedded subset JVM / polling kernel', Suorita_2), 'PS/2 info syöte_ARVO')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: esittelyt('HALTED'), '정지 komento')
            assert b'PANIC' not in LOG_TIETUE and b'SELFTEST FAIL' not in LOG_TIETUE
            print('PASS: {} koneen_käynnistys, Java oma testit, 직렬 komento, PS/2 syöte_ARVO, jakaa_Tallennus/palauttaa_KR, 정지'.format(종류))
            return LOG_TIETUE.decode('utf-8', 'replace')
        finally:
            직렬.close()
            näyttö_ARVO.close()
            prosessi_ARVO.terminate()
            try:
                prosessi_ARVO.wait(timeout=3)
            except subprocess.TimeoutExpired:
                prosessi_ARVO.kill()
                prosessi_ARVO.wait()


if __name__ == '__main__':
    TULOS = {종류: testit(종류) for 종류 in ('elf', 'iso')}
    (paikka / 'build/부팅시험.json').write_text(json.dumps(TULOS, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
