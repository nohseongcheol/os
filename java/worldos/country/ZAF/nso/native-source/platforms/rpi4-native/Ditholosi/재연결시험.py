#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 kgonthe_data 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from phethagatša_taelo import 기준, Taelo


def Diriša():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = 기준 / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    pego_boleng = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            Tsejana = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as sehlopha_boleng:
                for go_tsenya_tshedimošo_boleng in sehlopha_boleng.getmembers():
                    if Tsejana not in (Tsejana / go_tsenya_tshedimošo_boleng.name).resolve().parents or go_tsenya_tshedimošo_boleng.issym() or go_tsenya_tshedimošo_boleng.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + go_tsenya_tshedimošo_boleng.name)
                sehlopha_boleng.extractall(str(Tsejana))
            mohlodi = Tsejana / 'jkoros-native-relink'
            def 재연결(Leina, 인수들):
                with (출력 / Leina).open('wb') as pego_rei:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(mohlodi),
                                   stdout=pego_rei, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            pego_boleng['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = mohlodi / 'vendor/tinycc/libtcc.c'
            mmele_wa_sengwalwa = 번역기.read_text()
            위치 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert mmele_wa_sengwalwa.count(위치) == 1
            번역기.write_text(mmele_wa_sengwalwa.replace(위치, 위치 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            seswantšho_boleng = mohlodi / 'build/relinked/kernel8.img'
            pego_boleng['modified_kernel_sha256'] = hashlib.sha256(seswantšho_boleng.read_bytes()).hexdigest()
            assert pego_boleng['modified_kernel_sha256'] != pego_boleng['kernel_sha256']
            pego_boleng['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Taelo()
            인수들[인수들.index('-kernel') + 1] = str(seswantšho_boleng)
            tiragalo_boleng = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            pego_rei = bytearray()
            kgetho_boleng = selectors.DefaultSelector()
            kgetho_boleng.register(tiragalo_boleng.stdout, selectors.EVENT_READ)
            def 기다림(bontšha_boleng=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while bontšha_boleng not in pego_rei[처음:]:
                    if time.monotonic() > 끝 or tiragalo_boleng.poll() is not None:
                        raise AssertionError('Missing ' + repr(bontšha_boleng) + '\n' + pego_rei[처음:].decode('utf-8', 'replace'))
                    for go_tsenya_tshedimošo_boleng, _ in kgetho_boleng.select(.1):
                        data = go_tsenya_tshedimošo_boleng.fileobj.read(65536)
                        if data:
                            pego_rei.extend(data)
                return bytes(pego_rei[처음:])
            def Romela(Thalokontšu_SMS, bontšha_boleng=b'jkoros-native> '):
                처음 = len(pego_rei)
                tiragalo_boleng.stdin.write(Thalokontšu_SMS.encode() + b'\n')
                tiragalo_boleng.stdin.flush()
                return 기다림(bontšha_boleng, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return ngwala_faele_data(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                Romela('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    Romela(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in Romela('.')
                결과 = Romela('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = Romela('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                pego_boleng['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                kgetho_boleng.close()
                if tiragalo_boleng.poll() is None:
                    tiragalo_boleng.terminate()
                    try:
                        tiragalo_boleng.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        tiragalo_boleng.kill()
                        tiragalo_boleng.wait()
                (출력 / 'guest.log').write_bytes(pego_rei)
        pego_boleng['passed'] = True
        print(json.dumps(pego_boleng, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(pego_boleng, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Diriša()
