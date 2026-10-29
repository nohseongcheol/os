#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ import 기준, ᎤᏁᏤᎸᎩ


def ᎠᎢᏎᏍᏗ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = 기준 / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            ᎠᏍᏓᏩᏛᏍᏗ = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as ᎤᎾᏓᏡᎬᎢ_ᏧᎬᏩᎶᏗᏯ:
                for Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ in ᎤᎾᏓᏡᎬᎢ_ᏧᎬᏩᎶᏗᏯ.getmembers():
                    if ᎠᏍᏓᏩᏛᏍᏗ not in (ᎠᏍᏓᏩᏛᏍᏗ / Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.name).resolve().parents or Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.issym() or Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.name)
                ᎤᎾᏓᏡᎬᎢ_ᏧᎬᏩᎶᏗᏯ.extractall(str(ᎠᏍᏓᏩᏛᏍᏗ))
            ᎦᏟᏌᏅᎯ_0201f362 = ᎠᏍᏓᏩᏛᏍᏗ / 'jkoros-native-relink'
            def 재연결(ᏚᏙᎥᎢ, 인수들):
                with (출력 / ᏚᏙᎥᎢ).open('wb') as ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ᎦᏟᏌᏅᎯ_0201f362),
                                   stdout=ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = ᎦᏟᏌᏅᎯ_0201f362 / 'vendor/tinycc/libtcc.c'
            본문 = 번역기.read_text()
            위치 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert 본문.count(위치) == 1
            번역기.write_text(본문.replace(위치, 위치 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            ᎤᏓᏴᎳᏛ_ᏧᎬᏩᎶᏗᏯ = ᎦᏟᏌᏅᎯ_0201f362 / 'build/relinked/kernel8.img'
            ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['modified_kernel_sha256'] = hashlib.sha256(ᎤᏓᏴᎳᏛ_ᏧᎬᏩᎶᏗᏯ.read_bytes()).hexdigest()
            assert ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['modified_kernel_sha256'] != ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['kernel_sha256']
            ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = ᎤᏁᏤᎸᎩ()
            인수들[인수들.index('-kernel') + 1] = str(ᎤᏓᏴᎳᏛ_ᏧᎬᏩᎶᏗᏯ)
            ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ = bytearray()
            ᏗᏑᏰᏓ_ᏧᎬᏩᎶᏗᏯ = selectors.DefaultSelector()
            ᏗᏑᏰᏓ_ᏧᎬᏩᎶᏗᏯ.register(ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.stdout, selectors.EVENT_READ)
            def 기다림(ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ not in ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[처음:]:
                    if time.monotonic() > 끝 or ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.poll() is not None:
                        raise AssertionError('Missing ' + repr(ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ) + '\n' + ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[처음:].decode('utf-8', 'replace'))
                    for Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ, _ in ᏗᏑᏰᏓ_ᏧᎬᏩᎶᏗᏯ.select(.1):
                        ᎦᏟᏌᏅᎯ = Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.fileobj.read(65536)
                        if ᎦᏟᏌᏅᎯ:
                            ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.extend(ᎦᏟᏌᏅᎯ)
                return bytes(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[처음:])
            def ᏫᎦᏅᏗ(말, ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ=b'jkoros-native> '):
                처음 = len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
                ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.stdin.write(말.encode() + b'\n')
                ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.stdin.flush()
                return 기다림(ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return ᎪᏪᎶᏗ_ᎠᏍᏆᏂᎪᏙᏗ_ᎦᏟᏌᏅᎯ(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                ᏫᎦᏅᏗ('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    ᏫᎦᏅᏗ(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in ᏫᎦᏅᏗ('.')
                결과 = ᏫᎦᏅᏗ('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = ᏫᎦᏅᏗ('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                ᏗᏑᏰᏓ_ᏧᎬᏩᎶᏗᏯ.close()
                if ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.poll() is None:
                    ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.terminate()
                    try:
                        ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.kill()
                        ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.wait()
                (출력 / 'guest.log').write_bytes(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
        ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['passed'] = True
        print(json.dumps(ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    ᎠᎢᏎᏍᏗ()
