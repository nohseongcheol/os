#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 gangan_détà 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from ṣiṣẹ́_àṣẹ import 기준, Àṣẹ


def Rọ́ọ̀nù():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = 기준 / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    ìjábọ̀_iye = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            ọ̀nà = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as Àjọṣe_iye:
                for ìgbéwọlé_iye in Àjọṣe_iye.getmembers():
                    if ọ̀nà not in (ọ̀nà / ìgbéwọlé_iye.name).resolve().parents or ìgbéwọlé_iye.issym() or ìgbéwọlé_iye.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + ìgbéwọlé_iye.name)
                Àjọṣe_iye.extractall(str(ọ̀nà))
            orísun = ọ̀nà / 'jkoros-native-relink'
            def 재연결(Orúkọ, 인수들):
                with (출력 / Orúkọ).open('wb') as àkọsílẹ̀_ìṣe_ìlà_ìbú:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(orísun),
                                   stdout=àkọsílẹ̀_ìṣe_ìlà_ìbú, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            ìjábọ̀_iye['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = orísun / 'vendor/tinycc/libtcc.c'
            kókó_ọ̀rọ̀_ìkọ = 번역기.read_text()
            위치 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert kókó_ọ̀rọ̀_ìkọ.count(위치) == 1
            번역기.write_text(kókó_ọ̀rọ̀_ìkọ.replace(위치, 위치 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            àwòrán_iye = orísun / 'build/relinked/kernel8.img'
            ìjábọ̀_iye['modified_kernel_sha256'] = hashlib.sha256(àwòrán_iye.read_bytes()).hexdigest()
            assert ìjábọ̀_iye['modified_kernel_sha256'] != ìjábọ̀_iye['kernel_sha256']
            ìjábọ̀_iye['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Àṣẹ()
            인수들[인수들.index('-kernel') + 1] = str(àwòrán_iye)
            Ìlànà_iye = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            àkọsílẹ̀_ìṣe_ìlà_ìbú = bytearray()
            ẹ̀yàn_iye = selectors.DefaultSelector()
            ẹ̀yàn_iye.register(Ìlànà_iye.stdout, selectors.EVENT_READ)
            def 기다림(ṣàfihàn_iye=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while ṣàfihàn_iye not in àkọsílẹ̀_ìṣe_ìlà_ìbú[처음:]:
                    if time.monotonic() > 끝 or Ìlànà_iye.poll() is not None:
                        raise AssertionError('Missing ' + repr(ṣàfihàn_iye) + '\n' + àkọsílẹ̀_ìṣe_ìlà_ìbú[처음:].decode('utf-8', 'replace'))
                    for ìgbéwọlé_iye, _ in ẹ̀yàn_iye.select(.1):
                        détà = ìgbéwọlé_iye.fileobj.read(65536)
                        if détà:
                            àkọsílẹ̀_ìṣe_ìlà_ìbú.extend(détà)
                return bytes(àkọsílẹ̀_ìṣe_ìlà_ìbú[처음:])
            def í_meèlì(Ọ̀rọ̀_SMS, ṣàfihàn_iye=b'jkoros-native> '):
                처음 = len(àkọsílẹ̀_ìṣe_ìlà_ìbú)
                Ìlànà_iye.stdin.write(Ọ̀rọ̀_SMS.encode() + b'\n')
                Ìlànà_iye.stdin.flush()
                return 기다림(ṣàfihàn_iye, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return kọ_fáìlì_détà(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                í_meèlì('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    í_meèlì(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in í_meèlì('.')
                결과 = í_meèlì('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = í_meèlì('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                ìjábọ̀_iye['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                ẹ̀yàn_iye.close()
                if Ìlànà_iye.poll() is None:
                    Ìlànà_iye.terminate()
                    try:
                        Ìlànà_iye.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Ìlànà_iye.kill()
                        Ìlànà_iye.wait()
                (출력 / 'guest.log').write_bytes(àkọsílẹ̀_ìṣe_ìlà_ìbú)
        ìjábọ̀_iye['passed'] = True
        print(json.dumps(ìjábọ̀_iye, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(ìjábọ̀_iye, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Rọ́ọ̀nù()
