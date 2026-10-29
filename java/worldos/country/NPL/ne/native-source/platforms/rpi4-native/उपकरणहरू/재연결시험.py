#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 वास्तविक_लगत 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from कार्यान्वयन_गर्नुहोस्_आदेश import परियोजना_रूट, आदेश


def चलाउनुहोस्():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=परियोजना_रूट.parent / 'rpi4/build/rootfs')
    तर्क = 해석기.parse_args()
    출력 = परियोजना_रूट / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    रिपोर्ट_मान = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((परियोजना_रूट / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            मार्ग = Path(임시)
            with tarfile.open(str(परियोजना_रूट / 'dist/jkoros-native-relink.tar.gz')) as समूह_मान:
                for प्रविष्टि_मान in समूह_मान.getmembers():
                    if मार्ग not in (मार्ग / प्रविष्टि_मान.name).resolve().parents or प्रविष्टि_मान.issym() or प्रविष्टि_मान.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + प्रविष्टि_मान.name)
                समूह_मान.extractall(str(मार्ग))
            स्रोत = मार्ग / 'jkoros-native-relink'
            def 재연결(नाम, 인수들):
                with (출력 / नाम).open('wb') as लग_रेकर्ड:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(स्रोत),
                                   stdout=लग_रेकर्ड, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            रिपोर्ट_मान['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = स्रोत / 'vendor/tinycc/libtcc.c'
            मुख्य_पाठ = 번역기.read_text()
            स्थिति = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert मुख्य_पाठ.count(स्थिति) == 1
            번역기.write_text(मुख्य_पाठ.replace(स्थिति, स्थिति + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(तर्क.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            छवि_मान = स्रोत / 'build/relinked/kernel8.img'
            रिपोर्ट_मान['modified_kernel_sha256'] = hashlib.sha256(छवि_मान.read_bytes()).hexdigest()
            assert रिपोर्ट_मान['modified_kernel_sha256'] != रिपोर्ट_मान['kernel_sha256']
            रिपोर्ट_मान['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = आदेश()
            인수들[인수들.index('-kernel') + 1] = str(छवि_मान)
            प्रक्रिया_मान = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            लग_रेकर्ड = bytearray()
            चयन_मान = selectors.DefaultSelector()
            चयन_मान.register(प्रक्रिया_मान.stdout, selectors.EVENT_READ)
            def 기다림(शो_मान=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while शो_मान not in लग_रेकर्ड[처음:]:
                    if time.monotonic() > 끝 or प्रक्रिया_मान.poll() is not None:
                        raise AssertionError('Missing ' + repr(शो_मान) + '\n' + लग_रेकर्ड[처음:].decode('utf-8', 'replace'))
                    for प्रविष्टि_मान, _ in चयन_मान.select(.1):
                        लगत = प्रविष्टि_मान.fileobj.read(65536)
                        if लगत:
                            लग_रेकर्ड.extend(लगत)
                return bytes(लग_रेकर्ड[처음:])
            def पठाउनुहोस्(शब्द_पाठ, शो_मान=b'jkoros-native> '):
                처음 = len(लग_रेकर्ड)
                प्रक्रिया_मान.stdin.write(शब्द_पाठ.encode() + b'\n')
                प्रक्रिया_मान.stdin.flush()
                return 기다림(शो_मान, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return लेख्नुहोस्_फाइल_लगत(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                पठाउनुहोस्('load /relink.c', b'hex> ')
                for राख्नुहोस्_अनुक्रमणिका in range(0, len(시험), 64):
                    पठाउनुहोस्(시험[राख्नुहोस्_अनुक्रमणिका:राख्नुहोस्_अनुक्रमणिका+64].hex(), b'hex> ')
                assert b'LOADED' in पठाउनुहोस्('.')
                मापन = पठाउनुहोस्('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in मापन, मापन
                मापन = पठाउनुहोस्('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in मापन and b'exit 0' in मापन, मापन
                रिपोर्ट_मान['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                चयन_मान.close()
                if प्रक्रिया_मान.poll() is None:
                    प्रक्रिया_मान.terminate()
                    try:
                        प्रक्रिया_मान.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        प्रक्रिया_मान.kill()
                        प्रक्रिया_मान.wait()
                (출력 / 'guest.log').write_bytes(लग_रेकर्ड)
        रिपोर्ट_मान['passed'] = True
        print(json.dumps(रिपोर्ट_मान, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(रिपोर्ट_मान, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    चलाउनुहोस्()
