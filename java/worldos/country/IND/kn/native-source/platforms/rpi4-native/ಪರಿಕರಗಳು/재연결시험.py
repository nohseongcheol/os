#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 ನಿಜವಾದ_ಡೇಟಾ 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from ಪೂರೈಸು_ಆದೇಶ import ಬಿಂಬಿಸು_ಮೂಲ, ಆಜ್ಞೆ


def ಚಲಾಯಿಸು_2():
    ಪಾರ್ಸರ್_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--sdk', type=Path, default=ಬಿಂಬಿಸು_ಮೂಲ.parent / 'rpi4/build/rootfs')
    인수 = ಪಾರ್ಸರ್_48ee4b1b.parse_args()
    ಔಟ್_ಪುಟ್ = ಬಿಂಬಿಸು_ಮೂಲ / 'build/verification/cosl-relink'
    ಔಟ್_ಪುಟ್.mkdir(parents=True, exist_ok=True)
    ವರದಿ_ಮೌಲ್ಯ = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((ಬಿಂಬಿಸು_ಮೂಲ / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            ಮಾರ್ಗ = Path(임시)
            with tarfile.open(str(ಬಿಂಬಿಸು_ಮೂಲ / 'dist/jkoros-native-relink.tar.gz')) as ಸಮೂಹ_ಮೌಲ್ಯ:
                for ನಮೂದು_ಮೌಲ್ಯ in ಸಮೂಹ_ಮೌಲ್ಯ.getmembers():
                    if ಮಾರ್ಗ not in (ಮಾರ್ಗ / ನಮೂದು_ಮೌಲ್ಯ.name).resolve().parents or ನಮೂದು_ಮೌಲ್ಯ.issym() or ನಮೂದು_ಮೌಲ್ಯ.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + ನಮೂದು_ಮೌಲ್ಯ.name)
                ಸಮೂಹ_ಮೌಲ್ಯ.extractall(str(ಮಾರ್ಗ))
            ಮೂಲ = ಮಾರ್ಗ / 'jkoros-native-relink'
            def 재연결(ಹೆಸರು, 인수들):
                with (ಔಟ್_ಪುಟ್ / ಹೆಸರು).open('wb') as ಲಾಗ್_ದಾಖಲೆ:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ಮೂಲ),
                                   stdout=ಲಾಗ್_ದಾಖಲೆ, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            ವರದಿ_ಮೌಲ್ಯ['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = ಮೂಲ / 'vendor/tinycc/libtcc.c'
            ಮುಖ್ಯ_ಪಠ್ಯ = 번역기.read_text()
            ಸ್ಥಾನ = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert ಮುಖ್ಯ_ಪಠ್ಯ.count(ಸ್ಥಾನ) == 1
            번역기.write_text(ಮುಖ್ಯ_ಪಠ್ಯ.replace(ಸ್ಥಾನ, ಸ್ಥಾನ + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            ಇಮೇಜ್_ಮೌಲ್ಯ = ಮೂಲ / 'build/relinked/kernel8.img'
            ವರದಿ_ಮೌಲ್ಯ['modified_kernel_sha256'] = hashlib.sha256(ಇಮೇಜ್_ಮೌಲ್ಯ.read_bytes()).hexdigest()
            assert ವರದಿ_ಮೌಲ್ಯ['modified_kernel_sha256'] != ವರದಿ_ಮೌಲ್ಯ['kernel_sha256']
            ವರದಿ_ಮೌಲ್ಯ['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = ಆಜ್ಞೆ()
            인수들[인수들.index('-kernel') + 1] = str(ಇಮೇಜ್_ಮೌಲ್ಯ)
            ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ಲಾಗ್_ದಾಖಲೆ = bytearray()
            ಆಯ್ಕೆ_ಮೌಲ್ಯ = selectors.DefaultSelector()
            ಆಯ್ಕೆ_ಮೌಲ್ಯ.register(ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.stdout, selectors.EVENT_READ)
            def ನಿರೀಕ್ಷಣೆ_ಸ್ಥಿತಿ(ಶೋ_ಮೌಲ್ಯ=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while ಶೋ_ಮೌಲ್ಯ not in ಲಾಗ್_ದಾಖಲೆ[처음:]:
                    if time.monotonic() > 끝 or ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.poll() is not None:
                        raise AssertionError('Missing ' + repr(ಶೋ_ಮೌಲ್ಯ) + '\n' + ಲಾಗ್_ದಾಖಲೆ[처음:].decode('utf-8', 'replace'))
                    for ನಮೂದು_ಮೌಲ್ಯ, _ in ಆಯ್ಕೆ_ಮೌಲ್ಯ.select(.1):
                        ಡೇಟಾ = ನಮೂದು_ಮೌಲ್ಯ.fileobj.read(65536)
                        if ಡೇಟಾ:
                            ಲಾಗ್_ದಾಖಲೆ.extend(ಡೇಟಾ)
                return bytes(ಲಾಗ್_ದಾಖಲೆ[처음:])
            def ಕಳುಹಿಸಿ(ಪದ_ಪಠ್ಯ, ಶೋ_ಮೌಲ್ಯ=b'jkoros-native> '):
                처음 = len(ಲಾಗ್_ದಾಖಲೆ)
                ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.stdin.write(ಪದ_ಪಠ್ಯ.encode() + b'\n')
                ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.stdin.flush()
                return ನಿರೀಕ್ಷಣೆ_ಸ್ಥಿತಿ(ಶೋ_ಮೌಲ್ಯ, 처음)
            try:
                ನಿರೀಕ್ಷಣೆ_ಸ್ಥಿತಿ()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return ಬರೆ_ಫೈಲ್_ಡೇಟಾ(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                ಕಳುಹಿಸಿ('load /relink.c', b'hex> ')
                for ಹುದ್ದೆ_ಪದಸೂಚಿ in range(0, len(시험), 64):
                    ಕಳುಹಿಸಿ(시험[ಹುದ್ದೆ_ಪದಸೂಚಿ:ಹುದ್ದೆ_ಪದಸೂಚಿ+64].hex(), b'hex> ')
                assert b'LOADED' in ಕಳುಹಿಸಿ('.')
                ಮಾಪನ = ಕಳುಹಿಸಿ('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in ಮಾಪನ, ಮಾಪನ
                ಮಾಪನ = ಕಳುಹಿಸಿ('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in ಮಾಪನ and b'exit 0' in ಮಾಪನ, ಮಾಪನ
                ವರದಿ_ಮೌಲ್ಯ['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                ಆಯ್ಕೆ_ಮೌಲ್ಯ.close()
                if ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.poll() is None:
                    ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.terminate()
                    try:
                        ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.kill()
                        ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.wait()
                (ಔಟ್_ಪುಟ್ / 'guest.log').write_bytes(ಲಾಗ್_ದಾಖಲೆ)
        ವರದಿ_ಮೌಲ್ಯ['passed'] = True
        print(json.dumps(ವರದಿ_ಮೌಲ್ಯ, ensure_ascii=False, indent=2))
    finally:
        (ಔಟ್_ಪುಟ್ / 'report.json').write_text(json.dumps(ವರದಿ_ಮೌಲ್ಯ, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    ಚಲಾಯಿಸು_2()
