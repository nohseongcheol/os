#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 стваран_подаци 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from 실행 import 기준, команда


def 시작():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = 기준 / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    извјештај_вриједност = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            пут = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as група_вриједност:
                for унос_вриједност in група_вриједност.getmembers():
                    if пут not in (пут / унос_вриједност.name).resolve().parents or унос_вриједност.issym() or унос_вриједност.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + унос_вриједност.name)
                група_вриједност.extractall(str(пут))
            извор = пут / 'jkoros-native-relink'
            def 재연결(назив, 인수들):
                with (출력 / назив).open('wb') as дневник_рада_ред:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(извор),
                                   stdout=дневник_рада_ред, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            извјештај_вриједност['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = извор / 'vendor/tinycc/libtcc.c'
            Тијело_текста = 번역기.read_text()
            위치 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert Тијело_текста.count(위치) == 1
            번역기.write_text(Тијело_текста.replace(위치, 위치 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            слика_вриједност = извор / 'build/relinked/kernel8.img'
            извјештај_вриједност['modified_kernel_sha256'] = hashlib.sha256(слика_вриједност.read_bytes()).hexdigest()
            assert извјештај_вриједност['modified_kernel_sha256'] != извјештај_вриједност['kernel_sha256']
            извјештај_вриједност['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = команда()
            인수들[인수들.index('-kernel') + 1] = str(слика_вриједност)
            процес_вриједност = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            дневник_рада_ред = bytearray()
            избор_вриједност = selectors.DefaultSelector()
            избор_вриједност.register(процес_вриједност.stdout, selectors.EVENT_READ)
            def 기다림(приказати_вриједност=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while приказати_вриједност not in дневник_рада_ред[처음:]:
                    if time.monotonic() > 끝 or процес_вриједност.poll() is not None:
                        raise AssertionError('Missing ' + repr(приказати_вриједност) + '\n' + дневник_рада_ред[처음:].decode('utf-8', 'replace'))
                    for унос_вриједност, _ in избор_вриједност.select(.1):
                        подаци = унос_вриједност.fileobj.read(65536)
                        if подаци:
                            дневник_рада_ред.extend(подаци)
                return bytes(дневник_рада_ред[처음:])
            def послати(말, приказати_вриједност=b'jkoros-native> '):
                처음 = len(дневник_рада_ред)
                процес_вриједност.stdin.write(말.encode() + b'\n')
                процес_вриједност.stdin.flush()
                return 기다림(приказати_вриједност, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return писати_фајл_подаци(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                послати('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    послати(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in послати('.')
                결과 = послати('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = послати('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                извјештај_вриједност['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                избор_вриједност.close()
                if процес_вриједност.poll() is None:
                    процес_вриједност.terminate()
                    try:
                        процес_вриједност.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        процес_вриједност.kill()
                        процес_вриједност.wait()
                (출력 / 'guest.log').write_bytes(дневник_рада_ред)
        извјештај_вриједност['passed'] = True
        print(json.dumps(извјештај_вриједност, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(извјештај_вриједност, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    시작()
