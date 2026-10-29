#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 প্রকৃত_ডাটা 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from কার্যকর_করুন_আদেশ import প্রকল্প_মূল, আদেশ


def চালনা():
    পার্সার_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    পার্সার_48ee4b1b.add_argument('--sdk', type=Path, default=প্রকল্প_মূল.parent / 'rpi4/build/rootfs')
    আর্গুমেন্ট_তালিকা = পার্সার_48ee4b1b.parse_args()
    নির্গম = প্রকল্প_মূল / 'build/verification/cosl-relink'
    নির্গম.mkdir(parents=True, exist_ok=True)
    রিপোর্ট_মান = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((প্রকল্প_মূল / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            পথ_2 = Path(임시)
            with tarfile.open(str(প্রকল্প_মূল / 'dist/jkoros-native-relink.tar.gz')) as দল_মান:
                for ভুক্তি_মান in দল_মান.getmembers():
                    if পথ_2 not in (পথ_2 / ভুক্তি_মান.name).resolve().parents or ভুক্তি_মান.issym() or ভুক্তি_মান.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + ভুক্তি_মান.name)
                দল_মান.extractall(str(পথ_2))
            উৎস_নথি = পথ_2 / 'jkoros-native-relink'
            def 재연결(নাম, 인수들):
                with (নির্গম / নাম).open('wb') as লগ_সারি:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(উৎস_নথি),
                                   stdout=লগ_সারি, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            রিপোর্ট_মান['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = উৎস_নথি / 'vendor/tinycc/libtcc.c'
            মুখ্য_পাঠ = 번역기.read_text()
            অবস্থান = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert মুখ্য_পাঠ.count(অবস্থান) == 1
            번역기.write_text(মুখ্য_পাঠ.replace(অবস্থান, অবস্থান + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(আর্গুমেন্ট_তালিকা.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            ছবি_মান = উৎস_নথি / 'build/relinked/kernel8.img'
            রিপোর্ট_মান['modified_kernel_sha256'] = hashlib.sha256(ছবি_মান.read_bytes()).hexdigest()
            assert রিপোর্ট_মান['modified_kernel_sha256'] != রিপোর্ট_মান['kernel_sha256']
            রিপোর্ট_মান['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = আদেশ()
            인수들[인수들.index('-kernel') + 1] = str(ছবি_মান)
            প্রসেসর_মান = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            লগ_সারি = bytearray()
            বাছাই_মান = selectors.DefaultSelector()
            বাছাই_মান.register(প্রসেসর_মান.stdout, selectors.EVENT_READ)
            def অপেক্ষা_অবস্হা(শো_মান=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while শো_মান not in লগ_সারি[처음:]:
                    if time.monotonic() > 끝 or প্রসেসর_মান.poll() is not None:
                        raise AssertionError('Missing ' + repr(শো_মান) + '\n' + লগ_সারি[처음:].decode('utf-8', 'replace'))
                    for ভুক্তি_মান, _ in বাছাই_মান.select(.1):
                        ডাটা = ভুক্তি_মান.fileobj.read(65536)
                        if ডাটা:
                            লগ_সারি.extend(ডাটা)
                return bytes(লগ_সারি[처음:])
            def পাঠান(শব্দ_পাঠ, শো_মান=b'jkoros-native> '):
                처음 = len(লগ_সারি)
                প্রসেসর_মান.stdin.write(শব্দ_পাঠ.encode() + b'\n')
                প্রসেসর_মান.stdin.flush()
                return অপেক্ষা_অবস্হা(শো_মান, 처음)
            try:
                অপেক্ষা_অবস্হা()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return লেখা_ফাইল_ডাটা(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                পাঠান('load /relink.c', b'hex> ')
                for পদ_সূচি in range(0, len(시험), 64):
                    পাঠান(시험[পদ_সূচি:পদ_সূচি+64].hex(), b'hex> ')
                assert b'LOADED' in পাঠান('.')
                পরিমাপ = পাঠান('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in পরিমাপ, পরিমাপ
                পরিমাপ = পাঠান('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in পরিমাপ and b'exit 0' in পরিমাপ, পরিমাপ
                রিপোর্ট_মান['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                বাছাই_মান.close()
                if প্রসেসর_মান.poll() is None:
                    প্রসেসর_মান.terminate()
                    try:
                        প্রসেসর_মান.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        প্রসেসর_মান.kill()
                        প্রসেসর_মান.wait()
                (নির্গম / 'guest.log').write_bytes(লগ_সারি)
        রিপোর্ট_মান['passed'] = True
        print(json.dumps(রিপোর্ট_মান, ensure_ascii=False, indent=2))
    finally:
        (নির্গম / 'report.json').write_text(json.dumps(রিপোর্ট_মান, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    চালনা()
