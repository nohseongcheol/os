#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 giáTrịNốiTiếp/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

vịTrí = Path(__file__).resolve().parents[1]


def đợi(CácPhépKiểmTra, môTả, giáTrịGiớiHạn=15):
    phầnKết = time.monotonic() + giáTrịGiớiHạn
    while time.monotonic() < phầnKết:
        kếtQuả = CácPhépKiểmTra()
        if kếtQuả:
            return kếtQuả
        time.sleep(0.05)
    raise AssertionError('giáTrịThờiGian 초과: ' + môTả)


def KiểmThử(giáTrịLoại):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as giáTrịTạm:
        giáTrịTạm = Path(giáTrịTạm)
        đườngDẫnNốiTiếp = giáTrịTạm / 'serial.sock'
        đườngDẫnBộGiámSát = giáTrịTạm / 'monitor.sock'
        lệnh = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(đườngDẫnNốiTiếp) + ',server,nowait',
                '-monitor', 'unix:' + str(đườngDẫnBộGiámSát) + ',server,nowait']
        lệnh += ['-kernel', str(vịTrí / 'build/kernel.elf')] if giáTrịLoại == 'elf' else [
            '-cdrom', str(vịTrí / 'build/kernel.iso'), '-boot', 'd']
        # giáTrịNốiTiếp 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        lệnh += ['-S']
        giáTrịTiếnTrình = subprocess.Popen(lệnh, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        giáTrịNốiTiếp = socket.socket(socket.AF_UNIX)
        giáTrịBộGiámSát = socket.socket(socket.AF_UNIX)
        bảnGhiNhậtKý = bytearray()
        try:
            def chuẩnBịỔCắmMạng():
                if giáTrịTiếnTrình.poll() is not None:
                    raise AssertionError(giáTrịTiếnTrình.stderr.read().decode('utf-8', 'replace'))
                return đườngDẫnNốiTiếp.exists() and đườngDẫnBộGiámSát.exists()
            đợi(chuẩnBịỔCắmMạng, 'QEMU giáTrịỔCắmMạng')
            giáTrịNốiTiếp.connect(str(đườngDẫnNốiTiếp))
            giáTrịBộGiámSát.connect(str(đườngDẫnBộGiámSát))
            giáTrịNốiTiếp.setblocking(False)
            giáTrịBộGiámSát.sendall(b'cont\n')

            def TệpĐầuMục(ChuỗiKýTự, chạy=0):
                đọc, _, _ = select.select([giáTrịNốiTiếp], [], [], 0.1)
                if đọc:
                    DữLiệu = giáTrịNốiTiếp.recv(65536)
                    if not DữLiệu:
                        raise AssertionError('giáTrịNốiTiếp nốiKết chươngTrìnhRa')
                    bảnGhiNhậtKý.extend(DữLiệu)
                if giáTrịTiếnTrình.poll() is not None:
                    raise AssertionError('QEMU 비정상 chươngTrìnhRa: ' + str(giáTrịTiếnTrình.returncode))
                return ChuỗiKýTự.encode('utf-8') in bảnGhiNhậtKý[chạy:]

            def thửCácLệnh(giáTrịVào, kỳVọng):
                chạy = len(bảnGhiNhậtKý)
                giáTrịNốiTiếp.sendall(giáTrịVào.encode('ascii'))
                đợi(lambda: TệpĐầuMục(kỳVọng, chạy), kỳVọng)
                đợi(lambda: TệpĐầuMục('jkoros> ', chạy), 'lệnh trạngTháiSau 프롬프트')

            đợi(lambda: TệpĐầuMục('READY'), giáTrịLoại + ' KhởiĐộng')
            assert b'JAVA SELFTEST PASS' in bảnGhiNhậtKý
            assert 'Java 기계어 giáTrịNhân chạy'.encode() in bảnGhiNhậtKý
            thửCácLệnh('info\r\n', 'embedded subset JVM / polling kernel')
            thửCácLệnh('help\n', 'free N | echo TEXT')
            thửCácLệnh('mem\n', ' / 8 (각 4096바이트)')
            thửCácLệnh('echo natix\bve\n', 'native\r\n')
            for sốHiệu in range(8):
                thửCácLệnh('alloc\n', 'giáTrịMụcĐoạn sốHiệu: ' + str(sốHiệu))
            thửCácLệnh('alloc\n', 'giáTrịMụcĐoạn sốHiệu: -1')
            thửCácLệnh('free 3\n', '반환됨')
            thửCácLệnh('free 3\n', '할당되지 않은 giáTrịMụcĐoạn')
            thửCácLệnh('free 99\n', '사용법: free 0..7')
            thửCácLệnh('alloc\n', 'giáTrịMụcĐoạn sốHiệu: 3')
            thửCácLệnh('free 0\n', '반환됨')
            thửCácLệnh('test\n', 'JAVA SELFTEST PASS')
            thửCácLệnh('unknown\n', '알 trịSố 없는 명령입니다')
            thửCácLệnh('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            chạy = len(bảnGhiNhậtKý)
            for giáTrịPhím in ('i', 'n', 'f', 'o', 'ret'):
                giáTrịBộGiámSát.sendall(('sendkey ' + giáTrịPhím + ' 30\n').encode())
                time.sleep(0.09)
            đợi(lambda: TệpĐầuMục('embedded subset JVM / polling kernel', chạy), 'PS/2 info giáTrịVào')
            thửCácLệnh('echo ' + 'a' * 150 + '\n', 'a' * 123)
            giáTrịNốiTiếp.sendall(b'halt\n')
            đợi(lambda: TệpĐầuMục('HALTED'), 'việcThựcThiDừngHẳn lệnh')
            assert b'PANIC' not in bảnGhiNhậtKý and b'SELFTEST FAIL' not in bảnGhiNhậtKý
            print('PASS: {} KhởiĐộng, Java tựThân KiểmThử, giáTrịNốiTiếp lệnh, PS/2 giáTrịVào, cấpPhátLưuTrữ/kếtQuảTrảVề, việcThựcThiDừngHẳn'.format(giáTrịLoại))
            return bảnGhiNhậtKý.decode('utf-8', 'replace')
        finally:
            giáTrịNốiTiếp.close()
            giáTrịBộGiámSát.close()
            giáTrịTiếnTrình.terminate()
            try:
                giáTrịTiếnTrình.wait(timeout=3)
            except subprocess.TimeoutExpired:
                giáTrịTiếnTrình.kill()
                giáTrịTiếnTrình.wait()


if __name__ == '__main__':
    kếtQuả = {giáTrịLoại: KiểmThử(giáTrịLoại) for giáTrịLoại in ('elf', 'iso')}
    (vịTrí / 'build/ThửKhởiĐộng.json').write_text(json.dumps(kếtQuả, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
