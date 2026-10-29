#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 ପ୍ରକୃତ_ଡାଟା 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ import ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍, ନିର୍ଦ୍ଦେଶ


def ଚଳାନ୍ତୁ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    ନିର୍ଗମ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/verification/cosl-relink'
    ନିର୍ଗମ.mkdir(parents=True, exist_ok=True)
    ରିପୋର୍ଟ_ମୂଲ୍ୟ = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            ପଥ = Path(임시)
            with tarfile.open(str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'dist/jkoros-native-relink.tar.gz')) as ଗୋଷ୍ଠୀ_ମୂଲ୍ୟ:
                for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in ଗୋଷ୍ଠୀ_ମୂଲ୍ୟ.getmembers():
                    if ପଥ not in (ପଥ / ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.name).resolve().parents or ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.issym() or ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.name)
                ଗୋଷ୍ଠୀ_ମୂଲ୍ୟ.extractall(str(ପଥ))
            ଉତ୍ସ = ପଥ / 'jkoros-native-relink'
            def 재연결(ନାମ, 인수들):
                with (ନିର୍ଗମ / ନାମ).open('wb') as ଲଗ୍_ଧାଡ଼ି:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ଉତ୍ସ),
                                   stdout=ଲଗ୍_ଧାଡ଼ି, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = ଉତ୍ସ / 'vendor/tinycc/libtcc.c'
            ମୂଳ_ପାଠ = 번역기.read_text()
            ଅବସ୍ଥାନ = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert ମୂଳ_ପାଠ.count(ଅବସ୍ଥାନ) == 1
            번역기.write_text(ମୂଳ_ପାଠ.replace(ଅବସ୍ଥାନ, ଅବସ୍ଥାନ + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            ଚିତ୍ର_ମୂଲ୍ୟ = ଉତ୍ସ / 'build/relinked/kernel8.img'
            ରିପୋର୍ଟ_ମୂଲ୍ୟ['modified_kernel_sha256'] = hashlib.sha256(ଚିତ୍ର_ମୂଲ୍ୟ.read_bytes()).hexdigest()
            assert ରିପୋର୍ଟ_ମୂଲ୍ୟ['modified_kernel_sha256'] != ରିପୋର୍ଟ_ମୂଲ୍ୟ['kernel_sha256']
            ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = ନିର୍ଦ୍ଦେଶ()
            인수들[인수들.index('-kernel') + 1] = str(ଚିତ୍ର_ମୂଲ୍ୟ)
            ପ୍ରୋସେସ୍_ମୂଲ୍ୟ = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ଲଗ୍_ଧାଡ଼ି = bytearray()
            ଚୟନ_ମୂଲ୍ୟ = selectors.DefaultSelector()
            ଚୟନ_ମୂଲ୍ୟ.register(ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.stdout, selectors.EVENT_READ)
            def ଅପେକ୍ଷା_ସ୍ଥିତି(ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ not in ଲଗ୍_ଧାଡ଼ି[처음:]:
                    if time.monotonic() > 끝 or ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.poll() is not None:
                        raise AssertionError('Missing ' + repr(ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ) + '\n' + ଲଗ୍_ଧାଡ଼ି[처음:].decode('utf-8', 'replace'))
                    for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ, _ in ଚୟନ_ମୂଲ୍ୟ.select(.1):
                        ଡାଟା = ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.fileobj.read(65536)
                        if ଡାଟା:
                            ଲଗ୍_ଧାଡ଼ି.extend(ଡାଟା)
                return bytes(ଲଗ୍_ଧାଡ଼ି[처음:])
            def ପଠାନ୍ତୁ(말, ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ=b'jkoros-native> '):
                처음 = len(ଲଗ୍_ଧାଡ଼ି)
                ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.stdin.write(말.encode() + b'\n')
                ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.stdin.flush()
                return ଅପେକ୍ଷା_ସ୍ଥିତି(ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ, 처음)
            try:
                ଅପେକ୍ଷା_ସ୍ଥିତି()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return ଲିଖନ_ଫାଇଲ୍_ଡାଟା(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                ପଠାନ୍ତୁ('load /relink.c', b'hex> ')
                for ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା in range(0, len(시험), 64):
                    ପଠାନ୍ତୁ(시험[ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା:ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା+64].hex(), b'hex> ')
                assert b'LOADED' in ପଠାନ୍ତୁ('.')
                ମାପ = ପଠାନ୍ତୁ('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in ମାପ, ମାପ
                ମାପ = ପଠାନ୍ତୁ('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in ମାପ and b'exit 0' in ମାପ, ମାପ
                ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                ଚୟନ_ମୂଲ୍ୟ.close()
                if ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.poll() is None:
                    ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.terminate()
                    try:
                        ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.kill()
                        ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.wait()
                (ନିର୍ଗମ / 'guest.log').write_bytes(ଲଗ୍_ଧାଡ଼ି)
        ରିପୋର୍ଟ_ମୂଲ୍ୟ['passed'] = True
        print(json.dumps(ରିପୋର୍ଟ_ମୂଲ୍ୟ, ensure_ascii=False, indent=2))
    finally:
        (ନିର୍ଗମ / 'report.json').write_text(json.dumps(ରିପୋର୍ଟ_ମୂଲ୍ୟ, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    ଚଳାନ୍ତୁ()
