#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 اصل_کوائف 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from نفاذ_کریں_حکم import عکس_ڈالنا_روٹ, حکم


def چلائیں():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=عکس_ڈالنا_روٹ.parent / 'rpi4/build/rootfs')
    دلائل = 해석기.parse_args()
    اخراج_کا_مقام = عکس_ڈالنا_روٹ / 'build/verification/cosl-relink'
    اخراج_کا_مقام.mkdir(parents=True, exist_ok=True)
    رپورٹ_قدر = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((عکس_ڈالنا_روٹ / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            راستہ_2 = Path(임시)
            with tarfile.open(str(عکس_ڈالنا_روٹ / 'dist/jkoros-native-relink.tar.gz')) as گروپ_قدر:
                for اندراج_قدر in گروپ_قدر.getmembers():
                    if راستہ_2 not in (راستہ_2 / اندراج_قدر.name).resolve().parents or اندراج_قدر.issym() or اندراج_قدر.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + اندراج_قدر.name)
                گروپ_قدر.extractall(str(راستہ_2))
            ماخذ_فائل = راستہ_2 / 'jkoros-native-relink'
            def 재연결(نام, 인수들):
                with (اخراج_کا_مقام / نام).open('wb') as لاگ_صف:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ماخذ_فائل),
                                   stdout=لاگ_صف, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            رپورٹ_قدر['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = ماخذ_فائل / 'vendor/tinycc/libtcc.c'
            بنیادی_متن = 번역기.read_text()
            مقام = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert بنیادی_متن.count(مقام) == 1
            번역기.write_text(بنیادی_متن.replace(مقام, مقام + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(دلائل.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            نقش_قدر = ماخذ_فائل / 'build/relinked/kernel8.img'
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
            def انتظار_حالت(دکھانا_قدر=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while دکھانا_قدر not in لاگ_صف[처음:]:
                    if time.monotonic() > 끝 or عمل_قدر.poll() is not None:
                        raise AssertionError('Missing ' + repr(دکھانا_قدر) + '\n' + لاگ_صف[처음:].decode('utf-8', 'replace'))
                    for اندراج_قدر, _ in انتخاب_قدر.select(.1):
                        کوائف = اندراج_قدر.fileobj.read(65536)
                        if کوائف:
                            لاگ_صف.extend(کوائف)
                return bytes(لاگ_صف[처음:])
            def بھیجیں(الفاظ_متن, دکھانا_قدر=b'jkoros-native> '):
                처음 = len(لاگ_صف)
                عمل_قدر.stdin.write(الفاظ_متن.encode() + b'\n')
                عمل_قدر.stdin.flush()
                return انتظار_حالت(دکھانا_قدر, 처음)
            try:
                انتظار_حالت()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return لکھیں_فائل_کوائف(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                بھیجیں('load /relink.c', b'hex> ')
                for پوزیشن_ٹھیک_کریں_اشاریہ in range(0, len(시험), 64):
                    بھیجیں(시험[پوزیشن_ٹھیک_کریں_اشاریہ:پوزیشن_ٹھیک_کریں_اشاریہ+64].hex(), b'hex> ')
                assert b'LOADED' in بھیجیں('.')
                پیمائش = بھیجیں('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in پیمائش, پیمائش
                پیمائش = بھیجیں('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in پیمائش and b'exit 0' in پیمائش, پیمائش
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
                (اخراج_کا_مقام / 'guest.log').write_bytes(لاگ_صف)
        رپورٹ_قدر['passed'] = True
        print(json.dumps(رپورٹ_قدر, ensure_ascii=False, indent=2))
    finally:
        (اخراج_کا_مقام / 'report.json').write_text(json.dumps(رپورٹ_قدر, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    چلائیں()
