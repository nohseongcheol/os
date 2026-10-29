#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 laatii_keɓe 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from 실행 import 기준, ginol


def huutoraade():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = 기준 / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    ciimtol_njaru = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            laawol = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as seto_njaru:
                for naatnugol_njaru in seto_njaru.getmembers():
                    if laawol not in (laawol / naatnugol_njaru.name).resolve().parents or naatnugol_njaru.issym() or naatnugol_njaru.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + naatnugol_njaru.name)
                seto_njaru.extractall(str(laawol))
            sewnde = laawol / 'jkoros-native-relink'
            def 재연결(innde, 인수들):
                with (출력 / innde).open('wb') as suurnal_winndande:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(sewnde),
                                   stdout=suurnal_winndande, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            ciimtol_njaru['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = sewnde / 'vendor/tinycc/libtcc.c'
            본문 = 번역기.read_text()
            위치 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert 본문.count(위치) == 1
            번역기.write_text(본문.replace(위치, 위치 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            natal_njaru = sewnde / 'build/relinked/kernel8.img'
            ciimtol_njaru['modified_kernel_sha256'] = hashlib.sha256(natal_njaru.read_bytes()).hexdigest()
            assert ciimtol_njaru['modified_kernel_sha256'] != ciimtol_njaru['kernel_sha256']
            ciimtol_njaru['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = ginol()
            인수들[인수들.index('-kernel') + 1] = str(natal_njaru)
            Yuɓɓo_golle_njaru = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            suurnal_winndande = bytearray()
            cuɓal_njaru = selectors.DefaultSelector()
            cuɓal_njaru.register(Yuɓɓo_golle_njaru.stdout, selectors.EVENT_READ)
            def 기다림(hollirde_njaru=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while hollirde_njaru not in suurnal_winndande[처음:]:
                    if time.monotonic() > 끝 or Yuɓɓo_golle_njaru.poll() is not None:
                        raise AssertionError('Missing ' + repr(hollirde_njaru) + '\n' + suurnal_winndande[처음:].decode('utf-8', 'replace'))
                    for naatnugol_njaru, _ in cuɓal_njaru.select(.1):
                        keɓe = naatnugol_njaru.fileobj.read(65536)
                        if keɓe:
                            suurnal_winndande.extend(keɓe)
                return bytes(suurnal_winndande[처음:])
            def neldude(말, hollirde_njaru=b'jkoros-native> '):
                처음 = len(suurnal_winndande)
                Yuɓɓo_golle_njaru.stdin.write(말.encode() + b'\n')
                Yuɓɓo_golle_njaru.stdin.flush()
                return 기다림(hollirde_njaru, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return winndude_fiilde_keɓe(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                neldude('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    neldude(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in neldude('.')
                결과 = neldude('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = neldude('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                ciimtol_njaru['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                cuɓal_njaru.close()
                if Yuɓɓo_golle_njaru.poll() is None:
                    Yuɓɓo_golle_njaru.terminate()
                    try:
                        Yuɓɓo_golle_njaru.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Yuɓɓo_golle_njaru.kill()
                        Yuɓɓo_golle_njaru.wait()
                (출력 / 'guest.log').write_bytes(suurnal_winndande)
        ciimtol_njaru['passed'] = True
        print(json.dumps(ciimtol_njaru, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(ciimtol_njaru, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    huutoraade()
