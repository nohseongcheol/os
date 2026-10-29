#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 tota_tshedimosetso 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from diragatsa_Taelo import 기준, Taelo


def dirisa():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = 기준 / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    pego_Boleng = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            tsela = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as setlhopha_Boleng:
                for tsenyo_Boleng in setlhopha_Boleng.getmembers():
                    if tsela not in (tsela / tsenyo_Boleng.name).resolve().parents or tsenyo_Boleng.issym() or tsenyo_Boleng.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + tsenyo_Boleng.name)
                setlhopha_Boleng.extractall(str(tsela))
            Motswedi = tsela / 'jkoros-native-relink'
            def 재연결(leina, 인수들):
                with (출력 / leina).open('wb') as rekota_mola:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(Motswedi),
                                   stdout=rekota_mola, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            pego_Boleng['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = Motswedi / 'vendor/tinycc/libtcc.c'
            diteng_tsa_mokwalo = 번역기.read_text()
            위치 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert diteng_tsa_mokwalo.count(위치) == 1
            번역기.write_text(diteng_tsa_mokwalo.replace(위치, 위치 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            Setshwantsho_Boleng = Motswedi / 'build/relinked/kernel8.img'
            pego_Boleng['modified_kernel_sha256'] = hashlib.sha256(Setshwantsho_Boleng.read_bytes()).hexdigest()
            assert pego_Boleng['modified_kernel_sha256'] != pego_Boleng['kernel_sha256']
            pego_Boleng['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Taelo()
            인수들[인수들.index('-kernel') + 1] = str(Setshwantsho_Boleng)
            Thulaganyo_Boleng = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            rekota_mola = bytearray()
            tlhopho_Boleng = selectors.DefaultSelector()
            tlhopho_Boleng.register(Thulaganyo_Boleng.stdout, selectors.EVENT_READ)
            def 기다림(bontsha_Boleng=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while bontsha_Boleng not in rekota_mola[처음:]:
                    if time.monotonic() > 끝 or Thulaganyo_Boleng.poll() is not None:
                        raise AssertionError('Missing ' + repr(bontsha_Boleng) + '\n' + rekota_mola[처음:].decode('utf-8', 'replace'))
                    for tsenyo_Boleng, _ in tlhopho_Boleng.select(.1):
                        tshedimosetso = tsenyo_Boleng.fileobj.read(65536)
                        if tshedimosetso:
                            rekota_mola.extend(tshedimosetso)
                return bytes(rekota_mola[처음:])
            def romela(Lefoko_SMS, bontsha_Boleng=b'jkoros-native> '):
                처음 = len(rekota_mola)
                Thulaganyo_Boleng.stdin.write(Lefoko_SMS.encode() + b'\n')
                Thulaganyo_Boleng.stdin.flush()
                return 기다림(bontsha_Boleng, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return kwala_faele_tshedimosetso(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                romela('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    romela(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in romela('.')
                결과 = romela('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = romela('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                pego_Boleng['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                tlhopho_Boleng.close()
                if Thulaganyo_Boleng.poll() is None:
                    Thulaganyo_Boleng.terminate()
                    try:
                        Thulaganyo_Boleng.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Thulaganyo_Boleng.kill()
                        Thulaganyo_Boleng.wait()
                (출력 / 'guest.log').write_bytes(rekota_mola)
        pego_Boleng['passed'] = True
        print(json.dumps(pego_Boleng, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(pego_Boleng, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    dirisa()
