#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 প্ৰকৃত_ডাটা 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from নিষ্পাদন_আদেশ import 기준, কমান্ড


def সঞ্চালন():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    নিৰ্গম = 기준 / 'build/verification/cosl-relink'
    নিৰ্গম.mkdir(parents=True, exist_ok=True)
    ৰিপ_ৰ্ট_মান = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            পথ = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as দল_মান:
                for প্রবিষ্ট_মান in দল_মান.getmembers():
                    if পথ not in (পথ / প্রবিষ্ট_মান.name).resolve().parents or প্রবিষ্ট_মান.issym() or প্রবিষ্ট_মান.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + প্রবিষ্ট_মান.name)
                দল_মান.extractall(str(পথ))
            উৎস = পথ / 'jkoros-native-relink'
            def 재연결(নাম, 인수들):
                with (নিৰ্গম / নাম).open('wb') as লগ_শাৰী:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(উৎস),
                                   stdout=লগ_শাৰী, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            ৰিপ_ৰ্ট_মান['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = উৎস / 'vendor/tinycc/libtcc.c'
            মূল_পাঠ = 번역기.read_text()
            অৱস্থান = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert মূল_পাঠ.count(অৱস্থান) == 1
            번역기.write_text(মূল_পাঠ.replace(অৱস্থান, অৱস্থান + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            ছবি_মান = উৎস / 'build/relinked/kernel8.img'
            ৰিপ_ৰ্ট_মান['modified_kernel_sha256'] = hashlib.sha256(ছবি_মান.read_bytes()).hexdigest()
            assert ৰিপ_ৰ্ট_মান['modified_kernel_sha256'] != ৰিপ_ৰ্ট_মান['kernel_sha256']
            ৰিপ_ৰ্ট_মান['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = কমান্ড()
            인수들[인수들.index('-kernel') + 1] = str(ছবি_মান)
            প্ৰক্ৰিয়া_মান = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            লগ_শাৰী = bytearray()
            চয়ন_মান = selectors.DefaultSelector()
            চয়ন_মান.register(প্ৰক্ৰিয়া_মান.stdout, selectors.EVENT_READ)
            def 기다림(শ্ব_মান=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while শ্ব_মান not in লগ_শাৰী[처음:]:
                    if time.monotonic() > 끝 or প্ৰক্ৰিয়া_মান.poll() is not None:
                        raise AssertionError('Missing ' + repr(শ্ব_মান) + '\n' + লগ_শাৰী[처음:].decode('utf-8', 'replace'))
                    for প্রবিষ্ট_মান, _ in চয়ন_মান.select(.1):
                        ডাটা = প্রবিষ্ট_মান.fileobj.read(65536)
                        if ডাটা:
                            লগ_শাৰী.extend(ডাটা)
                return bytes(লগ_শাৰী[처음:])
            def ই_মেইল_কৰক(말, শ্ব_মান=b'jkoros-native> '):
                처음 = len(লগ_শাৰী)
                প্ৰক্ৰিয়া_মান.stdin.write(말.encode() + b'\n')
                প্ৰক্ৰিয়া_মান.stdin.flush()
                return 기다림(শ্ব_মান, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return লিখক_ফাইল_ডাটা(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                ই_মেইল_কৰক('load /relink.c', b'hex> ')
                for স্থান_সলনি_কৰক_ইনডেক্স in range(0, len(시험), 64):
                    ই_মেইল_কৰক(시험[স্থান_সলনি_কৰক_ইনডেক্স:স্থান_সলনি_কৰক_ইনডেক্স+64].hex(), b'hex> ')
                assert b'LOADED' in ই_মেইল_কৰক('.')
                পৰিমাপ = ই_মেইল_কৰক('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in পৰিমাপ, পৰিমাপ
                পৰিমাপ = ই_মেইল_কৰক('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in পৰিমাপ and b'exit 0' in পৰিমাপ, পৰিমাপ
                ৰিপ_ৰ্ট_মান['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                চয়ন_মান.close()
                if প্ৰক্ৰিয়া_মান.poll() is None:
                    প্ৰক্ৰিয়া_মান.terminate()
                    try:
                        প্ৰক্ৰিয়া_মান.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        প্ৰক্ৰিয়া_মান.kill()
                        প্ৰক্ৰিয়া_মান.wait()
                (নিৰ্গম / 'guest.log').write_bytes(লগ_শাৰী)
        ৰিপ_ৰ্ট_মান['passed'] = True
        print(json.dumps(ৰিপ_ৰ্ট_মান, ensure_ascii=False, indent=2))
    finally:
        (নিৰ্গম / 'report.json').write_text(json.dumps(ৰিপ_ৰ্ট_মান, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    সঞ্চালন()
