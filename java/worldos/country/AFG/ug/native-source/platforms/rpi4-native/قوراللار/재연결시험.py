#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 ھەقىقىي_مەلۇمات 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from ئىجرا_قىلىش_بۇيرۇق import كۆرسىتىش_يىلتىز, بۇيرۇق


def ئىجرا_قىل_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=كۆرسىتىش_يىلتىز.parent / 'rpi4/build/rootfs')
    ئۆزگەرگۈچىلەر = 해석기.parse_args()
    چىقار = كۆرسىتىش_يىلتىز / 'build/verification/cosl-relink'
    چىقار.mkdir(parents=True, exist_ok=True)
    خەۋەر_قىممىتى = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((كۆرسىتىش_يىلتىز / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            يول = Path(임시)
            with tarfile.open(str(كۆرسىتىش_يىلتىز / 'dist/jkoros-native-relink.tar.gz')) as توپ_قىممىتى:
                for كىرگۈزۈش_قىممىتى in توپ_قىممىتى.getmembers():
                    if يول not in (يول / كىرگۈزۈش_قىممىتى.name).resolve().parents or كىرگۈزۈش_قىممىتى.issym() or كىرگۈزۈش_قىممىتى.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + كىرگۈزۈش_قىممىتى.name)
                توپ_قىممىتى.extractall(str(يول))
            مەنبە = يول / 'jkoros-native-relink'
            def 재연결(ئاتى, 인수들):
                with (چىقار / ئاتى).open('wb') as خاتىرە_قۇر:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(مەنبە),
                                   stdout=خاتىرە_قۇر, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            خەۋەر_قىممىتى['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = مەنبە / 'vendor/tinycc/libtcc.c'
            مەزمۇن = 번역기.read_text()
            ئورۇن = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert مەزمۇن.count(ئورۇن) == 1
            번역기.write_text(مەزمۇن.replace(ئورۇن, ئورۇن + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(ئۆزگەرگۈچىلەر.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            رەسىم_قىممىتى = مەنبە / 'build/relinked/kernel8.img'
            خەۋەر_قىممىتى['modified_kernel_sha256'] = hashlib.sha256(رەسىم_قىممىتى.read_bytes()).hexdigest()
            assert خەۋەر_قىممىتى['modified_kernel_sha256'] != خەۋەر_قىممىتى['kernel_sha256']
            خەۋەر_قىممىتى['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = بۇيرۇق()
            인수들[인수들.index('-kernel') + 1] = str(رەسىم_قىممىتى)
            جەريان_قىممىتى = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            خاتىرە_قۇر = bytearray()
            تاللاش_قىممىتى = selectors.DefaultSelector()
            تاللاش_قىممىتى.register(جەريان_قىممىتى.stdout, selectors.EVENT_READ)
            def 기다림(كۆرسەتمەك_قىممىتى=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while كۆرسەتمەك_قىممىتى not in خاتىرە_قۇر[처음:]:
                    if time.monotonic() > 끝 or جەريان_قىممىتى.poll() is not None:
                        raise AssertionError('Missing ' + repr(كۆرسەتمەك_قىممىتى) + '\n' + خاتىرە_قۇر[처음:].decode('utf-8', 'replace'))
                    for كىرگۈزۈش_قىممىتى, _ in تاللاش_قىممىتى.select(.1):
                        مەلۇمات = كىرگۈزۈش_قىممىتى.fileobj.read(65536)
                        if مەلۇمات:
                            خاتىرە_قۇر.extend(مەلۇمات)
                return bytes(خاتىرە_قۇر[처음:])
            def ئەۋەتمەك(سۆز_تېكست, كۆرسەتمەك_قىممىتى=b'jkoros-native> '):
                처음 = len(خاتىرە_قۇر)
                جەريان_قىممىتى.stdin.write(سۆز_تېكست.encode() + b'\n')
                جەريان_قىممىتى.stdin.flush()
                return 기다림(كۆرسەتمەك_قىممىتى, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return يازماق_ھۆججەت_مەلۇمات(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                ئەۋەتمەك('load /relink.c', b'hex> ')
                for ئورۇنلاشتۇرۇش_ئىندېكس in range(0, len(시험), 64):
                    ئەۋەتمەك(시험[ئورۇنلاشتۇرۇش_ئىندېكس:ئورۇنلاشتۇرۇش_ئىندېكس+64].hex(), b'hex> ')
                assert b'LOADED' in ئەۋەتمەك('.')
                ئۆلچەم = ئەۋەتمەك('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in ئۆلچەم, ئۆلچەم
                ئۆلچەم = ئەۋەتمەك('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in ئۆلچەم and b'exit 0' in ئۆلچەم, ئۆلچەم
                خەۋەر_قىممىتى['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                تاللاش_قىممىتى.close()
                if جەريان_قىممىتى.poll() is None:
                    جەريان_قىممىتى.terminate()
                    try:
                        جەريان_قىممىتى.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        جەريان_قىممىتى.kill()
                        جەريان_قىممىتى.wait()
                (چىقار / 'guest.log').write_bytes(خاتىرە_قۇر)
        خەۋەر_قىممىتى['passed'] = True
        print(json.dumps(خەۋەر_قىممىتى, ensure_ascii=False, indent=2))
    finally:
        (چىقار / 'report.json').write_text(json.dumps(خەۋەر_قىممىتى, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    ئىجرا_قىل_2()
