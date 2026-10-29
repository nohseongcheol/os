#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 ትኽክለኛ_ሓበሬታ 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from ተግብር_ትእዛዝ import 기준, ትእዛዝ


def ኣኺድ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = 기준 / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    ጸብጻብ_ዋጋ = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            መገዲ = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as ጉጅለ_ዋጋ:
                for ምእታው_ዋጋ in ጉጅለ_ዋጋ.getmembers():
                    if መገዲ not in (መገዲ / ምእታው_ዋጋ.name).resolve().parents or ምእታው_ዋጋ.issym() or ምእታው_ዋጋ.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + ምእታው_ዋጋ.name)
                ጉጅለ_ዋጋ.extractall(str(መገዲ))
            ምንጪ = መገዲ / 'jkoros-native-relink'
            def 재연결(ሽም, 인수들):
                with (출력 / ሽም).open('wb') as ምዝጉብ_ሪጋ:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ምንጪ),
                                   stdout=ምዝጉብ_ሪጋ, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            ጸብጻብ_ዋጋ['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = ምንጪ / 'vendor/tinycc/libtcc.c'
            ዋና_ጽሑፍ = 번역기.read_text()
            위치 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert ዋና_ጽሑፍ.count(위치) == 1
            번역기.write_text(ዋና_ጽሑፍ.replace(위치, 위치 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            ምስሊ_ዋጋ = ምንጪ / 'build/relinked/kernel8.img'
            ጸብጻብ_ዋጋ['modified_kernel_sha256'] = hashlib.sha256(ምስሊ_ዋጋ.read_bytes()).hexdigest()
            assert ጸብጻብ_ዋጋ['modified_kernel_sha256'] != ጸብጻብ_ዋጋ['kernel_sha256']
            ጸብጻብ_ዋጋ['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = ትእዛዝ()
            인수들[인수들.index('-kernel') + 1] = str(ምስሊ_ዋጋ)
            መስርሕ_ዋጋ = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ምዝጉብ_ሪጋ = bytearray()
            ምሩጽ_ዋጋ = selectors.DefaultSelector()
            ምሩጽ_ዋጋ.register(መስርሕ_ዋጋ.stdout, selectors.EVENT_READ)
            def 기다림(ኣርእይ_ዋጋ=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while ኣርእይ_ዋጋ not in ምዝጉብ_ሪጋ[처음:]:
                    if time.monotonic() > 끝 or መስርሕ_ዋጋ.poll() is not None:
                        raise AssertionError('Missing ' + repr(ኣርእይ_ዋጋ) + '\n' + ምዝጉብ_ሪጋ[처음:].decode('utf-8', 'replace'))
                    for ምእታው_ዋጋ, _ in ምሩጽ_ዋጋ.select(.1):
                        ሓበሬታ = ምእታው_ዋጋ.fileobj.read(65536)
                        if ሓበሬታ:
                            ምዝጉብ_ሪጋ.extend(ሓበሬታ)
                return bytes(ምዝጉብ_ሪጋ[처음:])
            def ለኣኽ(ናይ_ቃል_ጸወታ_ጽሑፍ, ኣርእይ_ዋጋ=b'jkoros-native> '):
                처음 = len(ምዝጉብ_ሪጋ)
                መስርሕ_ዋጋ.stdin.write(ናይ_ቃል_ጸወታ_ጽሑፍ.encode() + b'\n')
                መስርሕ_ዋጋ.stdin.flush()
                return 기다림(ኣርእይ_ዋጋ, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return ጸሓፍ_ፋይል_ሓበሬታ(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                ለኣኽ('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    ለኣኽ(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in ለኣኽ('.')
                결과 = ለኣኽ('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = ለኣኽ('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                ጸብጻብ_ዋጋ['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                ምሩጽ_ዋጋ.close()
                if መስርሕ_ዋጋ.poll() is None:
                    መስርሕ_ዋጋ.terminate()
                    try:
                        መስርሕ_ዋጋ.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        መስርሕ_ዋጋ.kill()
                        መስርሕ_ዋጋ.wait()
                (출력 / 'guest.log').write_bytes(ምዝጉብ_ሪጋ)
        ጸብጻብ_ዋጋ['passed'] = True
        print(json.dumps(ጸብጻብ_ዋጋ, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(ጸብጻብ_ዋጋ, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    ኣኺድ()
