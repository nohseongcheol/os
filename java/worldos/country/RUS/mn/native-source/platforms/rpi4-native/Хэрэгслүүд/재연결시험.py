#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 бодит_өгөгдөл 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Гүйцэтгэх_команд import 기준, Тушаал


def Ажиллуулах():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = 기준 / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    тайлан_утга_ddf2aaf3 = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            ЗАМ = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as бүлэг_утга:
                for оролт_утга in бүлэг_утга.getmembers():
                    if ЗАМ not in (ЗАМ / оролт_утга.name).resolve().parents or оролт_утга.issym() or оролт_утга.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + оролт_утга.name)
                бүлэг_утга.extractall(str(ЗАМ))
            ЭХ = ЗАМ / 'jkoros-native-relink'
            def 재연결(Нэр, 인수들):
                with (출력 / Нэр).open('wb') as бичих_мөр_6e8b375a:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ЭХ),
                                   stdout=бичих_мөр_6e8b375a, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            тайлан_утга_ddf2aaf3['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = ЭХ / 'vendor/tinycc/libtcc.c'
            үндсэн_бичвэр = 번역기.read_text()
            위치 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert үндсэн_бичвэр.count(위치) == 1
            번역기.write_text(үндсэн_бичвэр.replace(위치, 위치 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            зураг_утга = ЭХ / 'build/relinked/kernel8.img'
            тайлан_утга_ddf2aaf3['modified_kernel_sha256'] = hashlib.sha256(зураг_утга.read_bytes()).hexdigest()
            assert тайлан_утга_ddf2aaf3['modified_kernel_sha256'] != тайлан_утга_ddf2aaf3['kernel_sha256']
            тайлан_утга_ddf2aaf3['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Тушаал()
            인수들[인수들.index('-kernel') + 1] = str(зураг_утга)
            үйл_явц_утга = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            бичих_мөр_6e8b375a = bytearray()
            сонгосон_хэсэг_утга = selectors.DefaultSelector()
            сонгосон_хэсэг_утга.register(үйл_явц_утга.stdout, selectors.EVENT_READ)
            def 기다림(үзүүлэх_утга=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while үзүүлэх_утга not in бичих_мөр_6e8b375a[처음:]:
                    if time.monotonic() > 끝 or үйл_явц_утга.poll() is not None:
                        raise AssertionError('Missing ' + repr(үзүүлэх_утга) + '\n' + бичих_мөр_6e8b375a[처음:].decode('utf-8', 'replace'))
                    for оролт_утга, _ in сонгосон_хэсэг_утга.select(.1):
                        өгөгдөл = оролт_утга.fileobj.read(65536)
                        if өгөгдөл:
                            бичих_мөр_6e8b375a.extend(өгөгдөл)
                return bytes(бичих_мөр_6e8b375a[처음:])
            def илгээх(Үгэн_Бичвэр, үзүүлэх_утга=b'jkoros-native> '):
                처음 = len(бичих_мөр_6e8b375a)
                үйл_явц_утга.stdin.write(Үгэн_Бичвэр.encode() + b'\n')
                үйл_явц_утга.stdin.flush()
                return 기다림(үзүүлэх_утга, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return бичих_файл_өгөгдөл(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                илгээх('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    илгээх(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in илгээх('.')
                결과 = илгээх('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = илгээх('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                тайлан_утга_ddf2aaf3['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                сонгосон_хэсэг_утга.close()
                if үйл_явц_утга.poll() is None:
                    үйл_явц_утга.terminate()
                    try:
                        үйл_явц_утга.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        үйл_явц_утга.kill()
                        үйл_явц_утга.wait()
                (출력 / 'guest.log').write_bytes(бичих_мөр_6e8b375a)
        тайлан_утга_ddf2aaf3['passed'] = True
        print(json.dumps(тайлан_утга_ddf2aaf3, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(тайлан_утга_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Ажиллуулах()
