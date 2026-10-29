#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 실제 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from 실행 import 기준, Baiko


def Alefaso():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = 기준 / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    보고 = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            LALANA = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as 묶음:
                for 항목 in 묶음.getmembers():
                    if LALANA not in (LALANA / 항목.name).resolve().parents or 항목.issym() or 항목.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + 항목.name)
                묶음.extractall(str(LALANA))
            LOHARANO = LALANA / 'jkoros-native-relink'
            def 재연결(Anarana, 인수들):
                with (출력 / Anarana).open('wb') as 기록:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(LOHARANO),
                                   stdout=기록, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            보고['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = LOHARANO / 'vendor/tinycc/libtcc.c'
            본문 = 번역기.read_text()
            위치 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert 본문.count(위치) == 1
            번역기.write_text(본문.replace(위치, 위치 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            영상 = LOHARANO / 'build/relinked/kernel8.img'
            보고['modified_kernel_sha256'] = hashlib.sha256(영상.read_bytes()).hexdigest()
            assert 보고['modified_kernel_sha256'] != 보고['kernel_sha256']
            보고['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Baiko()
            인수들[인수들.index('-kernel') + 1] = str(영상)
            과정 = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            기록 = bytearray()
            선택 = selectors.DefaultSelector()
            선택.register(과정.stdout, selectors.EVENT_READ)
            def 기다림(표시=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while 표시 not in 기록[처음:]:
                    if time.monotonic() > 끝 or 과정.poll() is not None:
                        raise AssertionError('Missing ' + repr(표시) + '\n' + 기록[처음:].decode('utf-8', 'replace'))
                    for 항목, _ in 선택.select(.1):
                        자료 = 항목.fileobj.read(65536)
                        if 자료:
                            기록.extend(자료)
                return bytes(기록[처음:])
            def 보내기(말, 표시=b'jkoros-native> '):
                처음 = len(기록)
                과정.stdin.write(말.encode() + b'\n')
                과정.stdin.flush()
                return 기다림(표시, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return 파일자료쓰기(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                보내기('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    보내기(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in 보내기('.')
                결과 = 보내기('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = 보내기('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                보고['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                선택.close()
                if 과정.poll() is None:
                    과정.terminate()
                    try:
                        과정.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        과정.kill()
                        과정.wait()
                (출력 / 'guest.log').write_bytes(기록)
        보고['passed'] = True
        print(json.dumps(보고, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(보고, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Alefaso()
