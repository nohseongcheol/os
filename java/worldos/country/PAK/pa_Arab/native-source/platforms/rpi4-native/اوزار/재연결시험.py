#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 اصلی_کوائف 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from نفاذ_کرو_حکم import 기준, حکم


def چلاؤ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = 기준 / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    رپورٹ_قدر = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            راہ = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as گروپ_قدر:
                for داخلہ_قدر in گروپ_قدر.getmembers():
                    if راہ not in (راہ / داخلہ_قدر.name).resolve().parents or داخلہ_قدر.issym() or داخلہ_قدر.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + داخلہ_قدر.name)
                گروپ_قدر.extractall(str(راہ))
            ماخذ = راہ / 'jkoros-native-relink'
            def 재연결(ناں, 인수들):
                with (출력 / ناں).open('wb') as لاگ_صف:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ماخذ),
                                   stdout=لاگ_صف, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            رپورٹ_قدر['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = ماخذ / 'vendor/tinycc/libtcc.c'
            متن_دا_ڈھانچہ = 번역기.read_text()
            위치 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert متن_دا_ڈھانچہ.count(위치) == 1
            번역기.write_text(متن_دا_ڈھانچہ.replace(위치, 위치 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            نقش_قدر = ماخذ / 'build/relinked/kernel8.img'
            رپورٹ_قدر['modified_kernel_sha256'] = hashlib.sha256(نقش_قدر.read_bytes()).hexdigest()
            assert رپورٹ_قدر['modified_kernel_sha256'] != رپورٹ_قدر['kernel_sha256']
            رپورٹ_قدر['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = حکم()
            인수들[인수들.index('-kernel') + 1] = str(نقش_قدر)
            عمل_قدر = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            لاگ_صف = bytearray()
            انتخاب_قدر = selectors.DefaultSelector()
            انتخاب_قدر.register(عمل_قدر.stdout, selectors.EVENT_READ)
            def 기다림(نمایش_کرو_قدر=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while نمایش_کرو_قدر not in لاگ_صف[처음:]:
                    if time.monotonic() > 끝 or عمل_قدر.poll() is not None:
                        raise AssertionError('Missing ' + repr(نمایش_کرو_قدر) + '\n' + لاگ_صف[처음:].decode('utf-8', 'replace'))
                    for داخلہ_قدر, _ in انتخاب_قدر.select(.1):
                        کوائف = داخلہ_قدر.fileobj.read(65536)
                        if کوائف:
                            لاگ_صف.extend(کوائف)
                return bytes(لاگ_صف[처음:])
            def بھیجو(لفظ_متن, نمایش_کرو_قدر=b'jkoros-native> '):
                처음 = len(لاگ_صف)
                عمل_قدر.stdin.write(لفظ_متن.encode() + b'\n')
                عمل_قدر.stdin.flush()
                return 기다림(نمایش_کرو_قدر, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return لکھو_فائل_کوائف(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                بھیجو('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    بھیجو(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in بھیجو('.')
                결과 = بھیجو('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = بھیجو('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                رپورٹ_قدر['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                انتخاب_قدر.close()
                if عمل_قدر.poll() is None:
                    عمل_قدر.terminate()
                    try:
                        عمل_قدر.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        عمل_قدر.kill()
                        عمل_قدر.wait()
                (출력 / 'guest.log').write_bytes(لاگ_صف)
        رپورٹ_قدر['passed'] = True
        print(json.dumps(رپورٹ_قدر, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(رپورٹ_قدر, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    چلاؤ()
