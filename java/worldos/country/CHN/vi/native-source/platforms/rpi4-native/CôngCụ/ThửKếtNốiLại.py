#!/usr/bin/env python3
"""giáTrịBảnPhânPhối 자료만으로 LGPL 재연결과 수정한 TinyCC의 dữLiệuThựcTế 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from thựcThiLệnh import gốcCâyDựÁn, lệnh


def chạy():
    BộPhânTích = argparse.ArgumentParser(description=__doc__)
    BộPhânTích.add_argument('--sdk', type=Path, default=gốcCâyDựÁn.parent / 'rpi4/build/rootfs')
    cácĐốiSố = BộPhânTích.parse_args()
    ĐầuRa = gốcCâyDựÁn / 'build/verification/cosl-relink'
    ĐầuRa.mkdir(parents=True, exist_ok=True)
    giáTrịBáoCáo = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((gốcCâyDựÁn / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as giáTrịTạm:
            đườngDẫn = Path(giáTrịTạm)
            with tarfile.open(str(gốcCâyDựÁn / 'dist/jkoros-native-relink.tar.gz')) as giáTrịNhóm:
                for giáTrịMục in giáTrịNhóm.getmembers():
                    if đườngDẫn not in (đườngDẫn / giáTrịMục.name).resolve().parents or giáTrịMục.issym() or giáTrịMục.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + giáTrịMục.name)
                giáTrịNhóm.extractall(str(đườngDẫn))
            mãNguồn = đườngDẫn / 'jkoros-native-relink'
            def điểmCuốiKếtNốiLại(tên, danhSáchCácĐốiSố):
                with (ĐầuRa / tên).open('wb') as bảnGhiNhậtKý:
                    subprocess.run(['python3', 'relink.py'] + danhSáchCácĐốiSố, cwd=str(mãNguồn),
                                   stdout=bảnGhiNhậtKý, stderr=subprocess.STDOUT, check=True, timeout=180)
            điểmCuốiKếtNốiLại('original.log', ['--verify'])
            giáTrịBáoCáo['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            côngCụTrìnhBiênDịch = mãNguồn / 'vendor/tinycc/libtcc.c'
            vănBảnThân = côngCụTrìnhBiênDịch.read_text()
            vịTrí = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert vănBảnThân.count(vịTrí) == 1
            côngCụTrìnhBiênDịch.write_text(vănBảnThân.replace(vịTrí, vịTrí + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            điểmCuốiKếtNốiLại('modified-tinycc.log', ['--tinycc', '--sdk', str(cácĐốiSố.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            giáTrịẢnh = mãNguồn / 'build/relinked/kernel8.img'
            giáTrịBáoCáo['modified_kernel_sha256'] = hashlib.sha256(giáTrịẢnh.read_bytes()).hexdigest()
            assert giáTrịBáoCáo['modified_kernel_sha256'] != giáTrịBáoCáo['kernel_sha256']
            giáTrịBáoCáo['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            danhSáchCácĐốiSố = lệnh()
            danhSáchCácĐốiSố[danhSáchCácĐốiSố.index('-kernel') + 1] = str(giáTrịẢnh)
            giáTrịTiếnTrình = subprocess.Popen(danhSáchCácĐốiSố + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            bảnGhiNhậtKý = bytearray()
            giáTrịViệcChọn = selectors.DefaultSelector()
            giáTrịViệcChọn.register(giáTrịTiếnTrình.stdout, selectors.EVENT_READ)
            def chờTrạngThái(hiệnGiáTrị=b'jkoros-native> ', phầnMụcBanĐầu=0):
                phầnKết = time.monotonic() + 40
                while hiệnGiáTrị not in bảnGhiNhậtKý[phầnMụcBanĐầu:]:
                    if time.monotonic() > phầnKết or giáTrịTiếnTrình.poll() is not None:
                        raise AssertionError('Missing ' + repr(hiệnGiáTrị) + '\n' + bảnGhiNhậtKý[phầnMụcBanĐầu:].decode('utf-8', 'replace'))
                    for giáTrịMục, _ in giáTrịViệcChọn.select(.1):
                        DữLiệu = giáTrịMục.fileobj.read(65536)
                        if DữLiệu:
                            bảnGhiNhậtKý.extend(DữLiệu)
                return bytes(bảnGhiNhậtKý[phầnMụcBanĐầu:])
            def gửi(vănBảnTừ, hiệnGiáTrị=b'jkoros-native> '):
                phầnMụcBanĐầu = len(bảnGhiNhậtKý)
                giáTrịTiếnTrình.stdin.write(vănBảnTừ.encode() + b'\n')
                giáTrịTiếnTrình.stdin.flush()
                return chờTrạngThái(hiệnGiáTrị, phầnMụcBanĐầu)
            try:
                chờTrạngThái()
                KiểmThử = '#include <ABITệp.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return ghiDữLiệuTệp(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                gửi('load /relink.c', b'hex> ')
                for chỉSốVịTrí in range(0, len(KiểmThử), 64):
                    gửi(KiểmThử[chỉSốVịTrí:chỉSốVịTrí+64].hex(), b'hex> ')
                assert b'LOADED' in gửi('.')
                kếtQuả = gửi('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in kếtQuả, kếtQuả
                kếtQuả = gửi('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in kếtQuả and b'exit 0' in kếtQuả, kếtQuả
                giáTrịBáoCáo['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                giáTrịViệcChọn.close()
                if giáTrịTiếnTrình.poll() is None:
                    giáTrịTiếnTrình.terminate()
                    try:
                        giáTrịTiếnTrình.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        giáTrịTiếnTrình.kill()
                        giáTrịTiếnTrình.wait()
                (ĐầuRa / 'guest.log').write_bytes(bảnGhiNhậtKý)
        giáTrịBáoCáo['passed'] = True
        print(json.dumps(giáTrịBáoCáo, ensure_ascii=False, indent=2))
    finally:
        (ĐầuRa / 'report.json').write_text(json.dumps(giáTrịBáoCáo, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    chạy()
