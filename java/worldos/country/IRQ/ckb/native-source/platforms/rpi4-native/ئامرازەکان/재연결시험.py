#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 ڕاستەکی_دەیتا 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from جێبەجێکردن_فەرمان import 기준, فەرمان


def ڕادان():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = 기준 / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    ڕاپۆرت_نرخ = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            گوزەر = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as گروپ_نرخ:
                for تێنووسین_نرخ in گروپ_نرخ.getmembers():
                    if گوزەر not in (گوزەر / تێنووسین_نرخ.name).resolve().parents or تێنووسین_نرخ.issym() or تێنووسین_نرخ.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + تێنووسین_نرخ.name)
                گروپ_نرخ.extractall(str(گوزەر))
            ژێدەر = گوزەر / 'jkoros-native-relink'
            def 재연결(ناو, 인수들):
                with (출력 / ناو).open('wb') as تۆمار_ڕزن:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ژێدەر),
                                   stdout=تۆمار_ڕزن, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            ڕاپۆرت_نرخ['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = ژێدەر / 'vendor/tinycc/libtcc.c'
            دەقی_تێکستەکە = 번역기.read_text()
            위치 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert دەقی_تێکستەکە.count(위치) == 1
            번역기.write_text(دەقی_تێکستەکە.replace(위치, 위치 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            وێنە_نرخ = ژێدەر / 'build/relinked/kernel8.img'
            ڕاپۆرت_نرخ['modified_kernel_sha256'] = hashlib.sha256(وێنە_نرخ.read_bytes()).hexdigest()
            assert ڕاپۆرت_نرخ['modified_kernel_sha256'] != ڕاپۆرت_نرخ['kernel_sha256']
            ڕاپۆرت_نرخ['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = فەرمان()
            인수들[인수들.index('-kernel') + 1] = str(وێنە_نرخ)
            پرۆسە_نرخ = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            تۆمار_ڕزن = bytearray()
            بژاردە_نرخ = selectors.DefaultSelector()
            بژاردە_نرخ.register(پرۆسە_نرخ.stdout, selectors.EVENT_READ)
            def چاوەڕوان_کردن_دۆخ(نیشاندان_نرخ=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while نیشاندان_نرخ not in تۆمار_ڕزن[처음:]:
                    if time.monotonic() > 끝 or پرۆسە_نرخ.poll() is not None:
                        raise AssertionError('Missing ' + repr(نیشاندان_نرخ) + '\n' + تۆمار_ڕزن[처음:].decode('utf-8', 'replace'))
                    for تێنووسین_نرخ, _ in بژاردە_نرخ.select(.1):
                        دەیتا = تێنووسین_نرخ.fileobj.read(65536)
                        if دەیتا:
                            تۆمار_ڕزن.extend(دەیتا)
                return bytes(تۆمار_ڕزن[처음:])
            def ناردن(وشە_دەق, نیشاندان_نرخ=b'jkoros-native> '):
                처음 = len(تۆمار_ڕزن)
                پرۆسە_نرخ.stdin.write(وشە_دەق.encode() + b'\n')
                پرۆسە_نرخ.stdin.flush()
                return چاوەڕوان_کردن_دۆخ(نیشاندان_نرخ, 처음)
            try:
                چاوەڕوان_کردن_دۆخ()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return ڕایت_کردن_فایل_دەیتا(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                ناردن('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    ناردن(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in ناردن('.')
                결과 = ناردن('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = ناردن('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                ڕاپۆرت_نرخ['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                بژاردە_نرخ.close()
                if پرۆسە_نرخ.poll() is None:
                    پرۆسە_نرخ.terminate()
                    try:
                        پرۆسە_نرخ.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        پرۆسە_نرخ.kill()
                        پرۆسە_نرخ.wait()
                (출력 / 'guest.log').write_bytes(تۆمار_ڕزن)
        ڕاپۆرت_نرخ['passed'] = True
        print(json.dumps(ڕاپۆرت_نرخ, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(ڕاپۆرت_نرخ, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    ڕادان()
