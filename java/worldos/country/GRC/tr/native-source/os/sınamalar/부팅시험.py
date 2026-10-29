#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

konum = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        sonuç = 검사()
        if sonuç:
            return sonuç
        time.sleep(0.05)
    raise AssertionError('zaman_değeri 초과: ' + 설명)


def sınamalar(Tip_değer):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        izlemek_yol = 임시 / 'monitor.sock'
        komut = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(izlemek_yol) + ',server,nowait']
        komut += ['-kernel', str(konum / 'build/kernel.elf')] if Tip_değer == 'elf' else [
            '-cdrom', str(konum / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        komut += ['-S']
        işlem_değer = subprocess.Popen(komut, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        izlemek_değer = socket.socket(socket.AF_UNIX)
        LOG_KAYIT = bytearray()
        try:
            def Hazırlan_yuva():
                if işlem_değer.poll() is not None:
                    raise AssertionError(işlem_değer.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and izlemek_yol.exists()
            기다리기(Hazırlan_yuva, 'QEMU yuva_değer')
            직렬.connect(str(직렬경로))
            izlemek_değer.connect(str(izlemek_yol))
            직렬.setblocking(False)
            izlemek_değer.sendall(b'cont\n')

            def bildirimler(dize_değer, çalıştır=0):
                Okuma, _, _ = select.select([직렬], [], [], 0.1)
                if Okuma:
                    veri = 직렬.recv(65536)
                    if not veri:
                        raise AssertionError('직렬 Bağlan Çıkış_program')
                    LOG_KAYIT.extend(veri)
                if işlem_değer.poll() is not None:
                    raise AssertionError('QEMU 비정상 Çıkış_program: ' + str(işlem_değer.returncode))
                return dize_değer.encode('utf-8') in LOG_KAYIT[çalıştır:]

            def 명령시험(artış_değer, 기대):
                çalıştır = len(LOG_KAYIT)
                직렬.sendall(artış_değer.encode('ascii'))
                기다리기(lambda: bildirimler(기대, çalıştır), 기대)
                기다리기(lambda: bildirimler('jkoros> ', çalıştır), 'komut 후 프롬프트')

            기다리기(lambda: bildirimler('READY'), Tip_değer + ' makine_başlatma')
            assert b'JAVA SELFTEST PASS' in LOG_KAYIT
            assert '자바 기계어 çekirdek_değer çalıştır'.encode() in LOG_KAYIT
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for Dizin in range(8):
                명령시험('alloc\n', 'bölüm_değer_366e0bfa Dizin: ' + str(Dizin))
            명령시험('alloc\n', 'bölüm_değer_366e0bfa Dizin: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 bölüm_değer_366e0bfa')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'bölüm_değer_366e0bfa Dizin: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            çalıştır = len(LOG_KAYIT)
            for tuş_değer in ('i', 'n', 'f', 'o', 'ret'):
                izlemek_değer.sendall(('sendkey ' + tuş_değer + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: bildirimler('embedded subset JVM / polling kernel', çalıştır), 'PS/2 info artış_değer')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: bildirimler('HALTED'), '정지 komut')
            assert b'PANIC' not in LOG_KAYIT and b'SELFTEST FAIL' not in LOG_KAYIT
            print('PASS: {} makine_başlatma, Java Öz sınamalar, 직렬 komut, PS/2 artış_değer, ayırmak_Depolama/İade_KR, 정지'.format(Tip_değer))
            return LOG_KAYIT.decode('utf-8', 'replace')
        finally:
            직렬.close()
            izlemek_değer.close()
            işlem_değer.terminate()
            try:
                işlem_değer.wait(timeout=3)
            except subprocess.TimeoutExpired:
                işlem_değer.kill()
                işlem_değer.wait()


if __name__ == '__main__':
    sonuç = {Tip_değer: sınamalar(Tip_değer) for Tip_değer in ('elf', 'iso')}
    (konum / 'build/부팅시험.json').write_text(json.dumps(sonuç, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
