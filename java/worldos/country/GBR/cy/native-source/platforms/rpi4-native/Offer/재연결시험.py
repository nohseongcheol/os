#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 go_iawn_data 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Gweithredu_gorchymyn import prosiect_gwraidd, Gorchymyn


def Gweithredu_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=prosiect_gwraidd.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    Allbwn = prosiect_gwraidd / 'build/verification/cosl-relink'
    Allbwn.mkdir(parents=True, exist_ok=True)
    adrodd_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((prosiect_gwraidd / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            LLWYBR = Path(임시)
            with tarfile.open(str(prosiect_gwraidd / 'dist/jkoros-native-relink.tar.gz')) as Grŵp_VALUE:
                for cofnod_VALUE in Grŵp_VALUE.getmembers():
                    if LLWYBR not in (LLWYBR / cofnod_VALUE.name).resolve().parents or cofnod_VALUE.issym() or cofnod_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + cofnod_VALUE.name)
                Grŵp_VALUE.extractall(str(LLWYBR))
            FFYNHONNELL = LLWYBR / 'jkoros-native-relink'
            def 재연결(Enw, 인수들):
                with (Allbwn / Enw).open('wb') as LOG_rhes:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(FFYNHONNELL),
                                   stdout=LOG_rhes, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            adrodd_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = FFYNHONNELL / 'vendor/tinycc/libtcc.c'
            corff_y_testun = 번역기.read_text()
            safle = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert corff_y_testun.count(safle) == 1
            번역기.write_text(corff_y_testun.replace(safle, safle + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            llun_VALUE = FFYNHONNELL / 'build/relinked/kernel8.img'
            adrodd_VALUE['modified_kernel_sha256'] = hashlib.sha256(llun_VALUE.read_bytes()).hexdigest()
            assert adrodd_VALUE['modified_kernel_sha256'] != adrodd_VALUE['kernel_sha256']
            adrodd_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Gorchymyn()
            인수들[인수들.index('-kernel') + 1] = str(llun_VALUE)
            Proses_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_rhes = bytearray()
            dewisiad_VALUE = selectors.DefaultSelector()
            dewisiad_VALUE.register(Proses_VALUE.stdout, selectors.EVENT_READ)
            def aros_cyflwr(sioe_VALUE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while sioe_VALUE not in LOG_rhes[처음:]:
                    if time.monotonic() > 끝 or Proses_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(sioe_VALUE) + '\n' + LOG_rhes[처음:].decode('utf-8', 'replace'))
                    for cofnod_VALUE, _ in dewisiad_VALUE.select(.1):
                        data = cofnod_VALUE.fileobj.read(65536)
                        if data:
                            LOG_rhes.extend(data)
                return bytes(LOG_rhes[처음:])
            def anfon(Word_SMS, sioe_VALUE=b'jkoros-native> '):
                처음 = len(LOG_rhes)
                Proses_VALUE.stdin.write(Word_SMS.encode() + b'\n')
                Proses_VALUE.stdin.flush()
                return aros_cyflwr(sioe_VALUE, 처음)
            try:
                aros_cyflwr()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return ysgrifennu_ffeil_data(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                anfon('load /relink.c', b'hex> ')
                for safle_INDEX in range(0, len(시험), 64):
                    anfon(시험[safle_INDEX:safle_INDEX+64].hex(), b'hex> ')
                assert b'LOADED' in anfon('.')
                mesur = anfon('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in mesur, mesur
                mesur = anfon('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in mesur and b'exit 0' in mesur, mesur
                adrodd_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                dewisiad_VALUE.close()
                if Proses_VALUE.poll() is None:
                    Proses_VALUE.terminate()
                    try:
                        Proses_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Proses_VALUE.kill()
                        Proses_VALUE.wait()
                (Allbwn / 'guest.log').write_bytes(LOG_rhes)
        adrodd_VALUE['passed'] = True
        print(json.dumps(adrodd_VALUE, ensure_ascii=False, indent=2))
    finally:
        (Allbwn / 'report.json').write_text(json.dumps(adrodd_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Gweithredu_2()
