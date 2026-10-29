#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 воқеӣ_иттилоот 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from иҷро_кардан_фармон import 기준, фармон


def порча():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = 기준 / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    гузориш_қимат = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            масир = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as гуруҳ_қимат:
                for ворида_қимат in гуруҳ_қимат.getmembers():
                    if масир not in (масир / ворида_қимат.name).resolve().parents or ворида_қимат.issym() or ворида_қимат.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + ворида_қимат.name)
                гуруҳ_қимат.extractall(str(масир))
            манбаъ = масир / 'jkoros-native-relink'
            def 재연결(Ном, 인수들):
                with (출력 / Ном).open('wb') as сабт_кардан_сабт:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(манбаъ),
                                   stdout=сабт_кардан_сабт, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            гузориш_қимат['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = манбаъ / 'vendor/tinycc/libtcc.c'
            матни_асосӣ = 번역기.read_text()
            위치 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert матни_асосӣ.count(위치) == 1
            번역기.write_text(матни_асосӣ.replace(위치, 위치 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            расм_қимат = манбаъ / 'build/relinked/kernel8.img'
            гузориш_қимат['modified_kernel_sha256'] = hashlib.sha256(расм_қимат.read_bytes()).hexdigest()
            assert гузориш_қимат['modified_kernel_sha256'] != гузориш_қимат['kernel_sha256']
            гузориш_қимат['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = фармон()
            인수들[인수들.index('-kernel') + 1] = str(расм_қимат)
            Раванд_қимат = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            сабт_кардан_сабт = bytearray()
            интихоб_қимат = selectors.DefaultSelector()
            интихоб_қимат.register(Раванд_қимат.stdout, selectors.EVENT_READ)
            def 기다림(намоиш_додан_қимат=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while намоиш_додан_қимат not in сабт_кардан_сабт[처음:]:
                    if time.monotonic() > 끝 or Раванд_қимат.poll() is not None:
                        raise AssertionError('Missing ' + repr(намоиш_додан_қимат) + '\n' + сабт_кардан_сабт[처음:].decode('utf-8', 'replace'))
                    for ворида_қимат, _ in интихоб_қимат.select(.1):
                        иттилоот = ворида_қимат.fileobj.read(65536)
                        if иттилоот:
                            сабт_кардан_сабт.extend(иттилоот)
                return bytes(сабт_кардан_сабт[처음:])
            def фиристодан(Калимабозӣ_Матн, намоиш_додан_қимат=b'jkoros-native> '):
                처음 = len(сабт_кардан_сабт)
                Раванд_қимат.stdin.write(Калимабозӣ_Матн.encode() + b'\n')
                Раванд_қимат.stdin.flush()
                return 기다림(намоиш_додан_қимат, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return навиштан_файл_иттилоот(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                фиристодан('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    фиристодан(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in фиристодан('.')
                결과 = фиристодан('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = фиристодан('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                гузориш_қимат['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                интихоб_қимат.close()
                if Раванд_қимат.poll() is None:
                    Раванд_қимат.terminate()
                    try:
                        Раванд_қимат.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Раванд_қимат.kill()
                        Раванд_қимат.wait()
                (출력 / 'guest.log').write_bytes(сабт_кардан_сабт)
        гузориш_қимат['passed'] = True
        print(json.dumps(гузориш_қимат, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(гузориш_қимат, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    порча()
