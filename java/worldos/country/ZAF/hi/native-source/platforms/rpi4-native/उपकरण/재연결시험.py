#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 वास्तविक_डेटा 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from निष्पादित_करें_आदेश import प्रोजेक्ट_करें_मूल, आदेश


def चलाएँ():
    पार्सर_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    पार्सर_48ee4b1b.add_argument('--sdk', type=Path, default=प्रोजेक्ट_करें_मूल.parent / 'rpi4/build/rootfs')
    तर्क = पार्सर_48ee4b1b.parse_args()
    निर्गम = प्रोजेक्ट_करें_मूल / 'build/verification/cosl-relink'
    निर्गम.mkdir(parents=True, exist_ok=True)
    रिपोर्ट_मान = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((प्रोजेक्ट_करें_मूल / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            पथ = Path(임시)
            with tarfile.open(str(प्रोजेक्ट_करें_मूल / 'dist/jkoros-native-relink.tar.gz')) as समूह_मान:
                for एन्ट्री_मान in समूह_मान.getmembers():
                    if पथ not in (पथ / एन्ट्री_मान.name).resolve().parents or एन्ट्री_मान.issym() or एन्ट्री_मान.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + एन्ट्री_मान.name)
                समूह_मान.extractall(str(पथ))
            स्रोत = पथ / 'jkoros-native-relink'
            def 재연결(नाम, 인수들):
                with (निर्गम / नाम).open('wb') as लॉग_रिकॉर्ड:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(स्रोत),
                                   stdout=लॉग_रिकॉर्ड, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            रिपोर्ट_मान['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            कंपाइलर_उपकरण = स्रोत / 'vendor/tinycc/libtcc.c'
            मुख्य_पाठ = कंपाइलर_उपकरण.read_text()
            स्थान = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert मुख्य_पाठ.count(स्थान) == 1
            कंपाइलर_उपकरण.write_text(मुख्य_पाठ.replace(स्थान, स्थान + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
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
            लॉग_रिकॉर्ड = bytearray()
            चयन_मान = selectors.DefaultSelector()
            चयन_मान.register(प्रक्रिया_मान.stdout, selectors.EVENT_READ)
            def प्रतीक्षा_स्थिति(शो_मान=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while शो_मान not in लॉग_रिकॉर्ड[처음:]:
                    if time.monotonic() > 끝 or प्रक्रिया_मान.poll() is not None:
                        raise AssertionError('Missing ' + repr(शो_मान) + '\n' + लॉग_रिकॉर्ड[처음:].decode('utf-8', 'replace'))
                    for एन्ट्री_मान, _ in चयन_मान.select(.1):
                        आँकड़े = एन्ट्री_मान.fileobj.read(65536)
                        if आँकड़े:
                            लॉग_रिकॉर्ड.extend(आँकड़े)
                return bytes(लॉग_रिकॉर्ड[처음:])
            def भेजें(शब्द_पाठ, शो_मान=b'jkoros-native> '):
                처음 = len(लॉग_रिकॉर्ड)
                प्रक्रिया_मान.stdin.write(शब्द_पाठ.encode() + b'\n')
                प्रक्रिया_मान.stdin.flush()
                return प्रतीक्षा_स्थिति(शो_मान, 처음)
            try:
                प्रतीक्षा_स्थिति()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return लिखना_फ़ाइल_डेटा(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                भेजें('load /relink.c', b'hex> ')
                for पद_इंडेक्स in range(0, len(시험), 64):
                    भेजें(시험[पद_इंडेक्स:पद_इंडेक्स+64].hex(), b'hex> ')
                assert b'LOADED' in भेजें('.')
                परिणाम = भेजें('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in परिणाम, परिणाम
                परिणाम = भेजें('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in परिणाम and b'exit 0' in परिणाम, परिणाम
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
                (निर्गम / 'guest.log').write_bytes(लॉग_रिकॉर्ड)
        रिपोर्ट_मान['passed'] = True
        print(json.dumps(रिपोर्ट_मान, ensure_ascii=False, indent=2))
    finally:
        (निर्गम / 'report.json').write_text(json.dumps(रिपोर्ट_मान, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    चलाएँ()
