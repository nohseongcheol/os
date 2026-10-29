#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 තථ්_ය_දත්ත 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from ක්_රියාත්මක_කරන්න_විධානය import 기준, විධානය


def ක්_රියාත්මක_කරන්න_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    විස්තාරක = 해석기.parse_args()
    출력 = 기준 / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    වාර්තාව_අගය = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            මාර්_ගය = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as සමූහය_අගය:
                for පිවිසුම_අගය in සමූහය_අගය.getmembers():
                    if මාර්_ගය not in (මාර්_ගය / පිවිසුම_අගය.name).resolve().parents or පිවිසුම_අගය.issym() or පිවිසුම_අගය.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + පිවිසුම_අගය.name)
                සමූහය_අගය.extractall(str(මාර්_ගය))
            මූලය = මාර්_ගය / 'jkoros-native-relink'
            def 재연결(නම, 인수들):
                with (출력 / නම).open('wb') as ලොගය_පේළිය:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(මූලය),
                                   stdout=ලොගය_පේළිය, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            වාර්තාව_අගය['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = මූලය / 'vendor/tinycc/libtcc.c'
            කඳ_පෙළ = 번역기.read_text()
            පිහිටීම = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert කඳ_පෙළ.count(පිහිටීම) == 1
            번역기.write_text(කඳ_පෙළ.replace(පිහිටීම, පිහිටීම + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(විස්තාරක.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            අනුරුව_අගය = මූලය / 'build/relinked/kernel8.img'
            වාර්තාව_අගය['modified_kernel_sha256'] = hashlib.sha256(අනුරුව_අගය.read_bytes()).hexdigest()
            assert වාර්තාව_අගය['modified_kernel_sha256'] != වාර්තාව_අගය['kernel_sha256']
            වාර්තාව_අගය['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = විධානය()
            인수들[인수들.index('-kernel') + 1] = str(අනුරුව_අගය)
            ක්_රියාවලිය_අගය = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ලොගය_පේළිය = bytearray()
            තේරීම_අගය = selectors.DefaultSelector()
            තේරීම_අගය.register(ක්_රියාවලිය_අගය.stdout, selectors.EVENT_READ)
            def 기다림(දර්ශනය_අගය=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while දර්ශනය_අගය not in ලොගය_පේළිය[처음:]:
                    if time.monotonic() > 끝 or ක්_රියාවලිය_අගය.poll() is not None:
                        raise AssertionError('Missing ' + repr(දර්ශනය_අගය) + '\n' + ලොගය_පේළිය[처음:].decode('utf-8', 'replace'))
                    for පිවිසුම_අගය, _ in තේරීම_අගය.select(.1):
                        දත්ත = පිවිසුම_අගය.fileobj.read(65536)
                        if දත්ත:
                            ලොගය_පේළිය.extend(දත්ත)
                return bytes(ලොගය_පේළිය[처음:])
            def ඊමේල්(말, දර්ශනය_අගය=b'jkoros-native> '):
                처음 = len(ලොගය_පේළිය)
                ක්_රියාවලිය_අගය.stdin.write(말.encode() + b'\n')
                ක්_රියාවලිය_අගය.stdin.flush()
                return 기다림(දර්ශනය_අගය, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return ලියන්න_ගොනුව_දත්ත(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                ඊමේල්('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    ඊමේල්(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in ඊමේල්('.')
                결과 = ඊමේල්('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = ඊමේල්('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                වාර්තාව_අගය['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                තේරීම_අගය.close()
                if ක්_රියාවලිය_අගය.poll() is None:
                    ක්_රියාවලිය_අගය.terminate()
                    try:
                        ක්_රියාවලිය_අගය.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        ක්_රියාවලිය_අගය.kill()
                        ක්_රියාවලිය_අගය.wait()
                (출력 / 'guest.log').write_bytes(ලොගය_පේළිය)
        වාර්තාව_අගය['passed'] = True
        print(json.dumps(වාර්තාව_අගය, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(වාර්තාව_අගය, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    ක්_රියාත්මක_කරන්න_2()
