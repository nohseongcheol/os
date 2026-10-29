#!/usr/bin/env python3
"""वितरण_मूल्य 자료만으로 LGPL 재연결과 수정한 TinyCC의 वास्तविक_डेटा 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from आज्ञा_कार्यवाही_करा import प्रोजेक्ट_मूळ, आदेश


def सुरू_करा():
    व्याकरणविश्लेषक_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    व्याकरणविश्लेषक_48ee4b1b.add_argument('--sdk', type=Path, default=प्रोजेक्ट_मूळ.parent / 'rpi4/build/rootfs')
    बाबी = व्याकरणविश्लेषक_48ee4b1b.parse_args()
    आउटपुट = प्रोजेक्ट_मूळ / 'build/verification/cosl-relink'
    आउटपुट.mkdir(parents=True, exist_ok=True)
    अहवाल_मूल्य = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((प्रोजेक्ट_मूळ / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as तात्पुरते_मूल्य:
            मार्ग = Path(तात्पुरते_मूल्य)
            with tarfile.open(str(प्रोजेक्ट_मूळ / 'dist/jkoros-native-relink.tar.gz')) as समूह_मूल्य:
                for प्रविष्टी_मूल्य in समूह_मूल्य.getmembers():
                    if मार्ग not in (मार्ग / प्रविष्टी_मूल्य.name).resolve().parents or प्रविष्टी_मूल्य.issym() or प्रविष्टी_मूल्य.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + प्रविष्टी_मूल्य.name)
                समूह_मूल्य.extractall(str(मार्ग))
            स्रोत = मार्ग / 'jkoros-native-relink'
            def पुन्हाजोडा_संचारटोक(नाव, वितर्क_यादी_0ee1a763):
                with (आउटपुट / नाव).open('wb') as लॉग_नोंद:
                    subprocess.run(['python3', 'relink.py'] + वितर्क_यादी_0ee1a763, cwd=str(स्रोत),
                                   stdout=लॉग_नोंद, stderr=subprocess.STDOUT, check=True, timeout=180)
            पुन्हाजोडा_संचारटोक('original.log', ['--verify'])
            अहवाल_मूल्य['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            संकलक_साधन = स्रोत / 'vendor/tinycc/libtcc.c'
            मुख्य_मजकूर = संकलक_साधन.read_text()
            जागा = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert मुख्य_मजकूर.count(जागा) == 1
            संकलक_साधन.write_text(मुख्य_मजकूर.replace(जागा, जागा + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            पुन्हाजोडा_संचारटोक('modified-tinycc.log', ['--tinycc', '--sdk', str(बाबी.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            चित्र_मूल्य = स्रोत / 'build/relinked/kernel8.img'
            अहवाल_मूल्य['modified_kernel_sha256'] = hashlib.sha256(चित्र_मूल्य.read_bytes()).hexdigest()
            assert अहवाल_मूल्य['modified_kernel_sha256'] != अहवाल_मूल्य['kernel_sha256']
            अहवाल_मूल्य['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            वितर्क_यादी_0ee1a763 = आदेश()
            वितर्क_यादी_0ee1a763[वितर्क_यादी_0ee1a763.index('-kernel') + 1] = str(चित्र_मूल्य)
            प्रक्रिया_मूल्य = subprocess.Popen(वितर्क_यादी_0ee1a763 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            लॉग_नोंद = bytearray()
            निवड_मूल्य = selectors.DefaultSelector()
            निवड_मूल्य.register(प्रक्रिया_मूल्य.stdout, selectors.EVENT_READ)
            def प्रतीक्षा_करा_राज्य(मूल्य_शो=b'jkoros-native> ', प्रारंभिक_आयटम=0):
                शेवट = time.monotonic() + 40
                while मूल्य_शो not in लॉग_नोंद[प्रारंभिक_आयटम:]:
                    if time.monotonic() > शेवट or प्रक्रिया_मूल्य.poll() is not None:
                        raise AssertionError('Missing ' + repr(मूल्य_शो) + '\n' + लॉग_नोंद[प्रारंभिक_आयटम:].decode('utf-8', 'replace'))
                    for प्रविष्टी_मूल्य, _ in निवड_मूल्य.select(.1):
                        डेटा = प्रविष्टी_मूल्य.fileobj.read(65536)
                        if डेटा:
                            लॉग_नोंद.extend(डेटा)
                return bytes(लॉग_नोंद[प्रारंभिक_आयटम:])
            def पाठवा(शब्द_मजकूर, मूल्य_शो=b'jkoros-native> '):
                प्रारंभिक_आयटम = len(लॉग_नोंद)
                प्रक्रिया_मूल्य.stdin.write(शब्द_मजकूर.encode() + b'\n')
                प्रक्रिया_मूल्य.stdin.flush()
                return प्रतीक्षा_करा_राज्य(मूल्य_शो, प्रारंभिक_आयटम)
            try:
                प्रतीक्षा_करा_राज्य()
                चाचण्या = '#include <संचिका_द्विमानजोडणी.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return संचिका_डेटा_लिहा(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                पाठवा('load /relink.c', b'hex> ')
                for स्थान_अनुक्रमणिका in range(0, len(चाचण्या), 64):
                    पाठवा(चाचण्या[स्थान_अनुक्रमणिका:स्थान_अनुक्रमणिका+64].hex(), b'hex> ')
                assert b'LOADED' in पाठवा('.')
                मोजमाप = पाठवा('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in मोजमाप, मोजमाप
                मोजमाप = पाठवा('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in मोजमाप and b'exit 0' in मोजमाप, मोजमाप
                अहवाल_मूल्य['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                निवड_मूल्य.close()
                if प्रक्रिया_मूल्य.poll() is None:
                    प्रक्रिया_मूल्य.terminate()
                    try:
                        प्रक्रिया_मूल्य.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        प्रक्रिया_मूल्य.kill()
                        प्रक्रिया_मूल्य.wait()
                (आउटपुट / 'guest.log').write_bytes(लॉग_नोंद)
        अहवाल_मूल्य['passed'] = True
        print(json.dumps(अहवाल_मूल्य, ensure_ascii=False, indent=2))
    finally:
        (आउटपुट / 'report.json').write_text(json.dumps(अहवाल_मूल्य, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    सुरू_करा()
