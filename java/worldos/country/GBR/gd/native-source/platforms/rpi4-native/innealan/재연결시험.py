#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 dearbh_dàta 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from gnìomhaich_àithne import tilg_freumh, àithne


def ruith():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=tilg_freumh.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = tilg_freumh / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    aithisg_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((tilg_freumh / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            Slighe = Path(임시)
            with tarfile.open(str(tilg_freumh / 'dist/jkoros-native-relink.tar.gz')) as buidheann_VALUE:
                for cur_a_steach_VALUE in buidheann_VALUE.getmembers():
                    if Slighe not in (Slighe / cur_a_steach_VALUE.name).resolve().parents or cur_a_steach_VALUE.issym() or cur_a_steach_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + cur_a_steach_VALUE.name)
                buidheann_VALUE.extractall(str(Slighe))
            tùs = Slighe / 'jkoros-native-relink'
            def 재연결(Ainm, 인수들):
                with (출력 / Ainm).open('wb') as LOG_ràgh:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(tùs),
                                   stdout=LOG_ràgh, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            aithisg_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = tùs / 'vendor/tinycc/libtcc.c'
            bodhaig_an_teacsa = 번역기.read_text()
            suidhich = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert bodhaig_an_teacsa.count(suidhich) == 1
            번역기.write_text(bodhaig_an_teacsa.replace(suidhich, suidhich + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            IMAGE_VALUE = tùs / 'build/relinked/kernel8.img'
            aithisg_VALUE['modified_kernel_sha256'] = hashlib.sha256(IMAGE_VALUE.read_bytes()).hexdigest()
            assert aithisg_VALUE['modified_kernel_sha256'] != aithisg_VALUE['kernel_sha256']
            aithisg_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = àithne()
            인수들[인수들.index('-kernel') + 1] = str(IMAGE_VALUE)
            Pròiseas_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_ràgh = bytearray()
            taghadh_VALUE = selectors.DefaultSelector()
            taghadh_VALUE.register(Pròiseas_VALUE.stdout, selectors.EVENT_READ)
            def fuirich_cor(show_VALUE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while show_VALUE not in LOG_ràgh[처음:]:
                    if time.monotonic() > 끝 or Pròiseas_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(show_VALUE) + '\n' + LOG_ràgh[처음:].decode('utf-8', 'replace'))
                    for cur_a_steach_VALUE, _ in taghadh_VALUE.select(.1):
                        dàta = cur_a_steach_VALUE.fileobj.read(65536)
                        if dàta:
                            LOG_ràgh.extend(dàta)
                return bytes(LOG_ràgh[처음:])
            def cuir(Word_SMS, show_VALUE=b'jkoros-native> '):
                처음 = len(LOG_ràgh)
                Pròiseas_VALUE.stdin.write(Word_SMS.encode() + b'\n')
                Pròiseas_VALUE.stdin.flush()
                return fuirich_cor(show_VALUE, 처음)
            try:
                fuirich_cor()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return sgrìobh_faidhle_dàta(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                cuir('load /relink.c', b'hex> ')
                for suidhich_INDEX in range(0, len(시험), 64):
                    cuir(시험[suidhich_INDEX:suidhich_INDEX+64].hex(), b'hex> ')
                assert b'LOADED' in cuir('.')
                tomhas = cuir('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in tomhas, tomhas
                tomhas = cuir('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in tomhas and b'exit 0' in tomhas, tomhas
                aithisg_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                taghadh_VALUE.close()
                if Pròiseas_VALUE.poll() is None:
                    Pròiseas_VALUE.terminate()
                    try:
                        Pròiseas_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Pròiseas_VALUE.kill()
                        Pròiseas_VALUE.wait()
                (출력 / 'guest.log').write_bytes(LOG_ràgh)
        aithisg_VALUE['passed'] = True
        print(json.dumps(aithisg_VALUE, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(aithisg_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    ruith()
