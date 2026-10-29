#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 प्रत्यक्ष_डेटा 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from पाळो_दिवचो_आदेश import प्रॉजॅक्ट_रूट, आदेश


def चलोवप():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=प्रॉजॅक्ट_रूट.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = प्रॉजॅक्ट_रूट / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    अहवाल_मोल = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((प्रॉजॅक्ट_रूट / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            पाथ = Path(임시)
            with tarfile.open(str(प्रॉजॅक्ट_रूट / 'dist/jkoros-native-relink.tar.gz')) as गट_मोल:
                for प्रवेश_मोल in गट_मोल.getmembers():
                    if पाथ not in (पाथ / प्रवेश_मोल.name).resolve().parents or प्रवेश_मोल.issym() or प्रवेश_मोल.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + प्रवेश_मोल.name)
                गट_मोल.extractall(str(पाथ))
            स्त्रोत = पाथ / 'jkoros-native-relink'
            def 재연결(नांव, 인수들):
                with (출력 / नांव).open('wb') as LOG_नोंद:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(स्त्रोत),
                                   stdout=LOG_नोंद, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            अहवाल_मोल['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = स्त्रोत / 'vendor/tinycc/libtcc.c'
            देखीचो_उतारो = 번역기.read_text()
            स्थिती = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert देखीचो_उतारो.count(स्थिती) == 1
            번역기.write_text(देखीचो_उतारो.replace(स्थिती, स्थिती + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            IMAGE_मोल = स्त्रोत / 'build/relinked/kernel8.img'
            अहवाल_मोल['modified_kernel_sha256'] = hashlib.sha256(IMAGE_मोल.read_bytes()).hexdigest()
            assert अहवाल_मोल['modified_kernel_sha256'] != अहवाल_मोल['kernel_sha256']
            अहवाल_मोल['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = आदेश()
            인수들[인수들.index('-kernel') + 1] = str(IMAGE_मोल)
            प्रक्रिया_मोल = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_नोंद = bytearray()
            निवड_मोल = selectors.DefaultSelector()
            निवड_मोल.register(प्रक्रिया_मोल.stdout, selectors.EVENT_READ)
            def 기다림(शो_मोल=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while शो_मोल not in LOG_नोंद[처음:]:
                    if time.monotonic() > 끝 or प्रक्रिया_मोल.poll() is not None:
                        raise AssertionError('Missing ' + repr(शो_मोल) + '\n' + LOG_नोंद[처음:].decode('utf-8', 'replace'))
                    for प्रवेश_मोल, _ in निवड_मोल.select(.1):
                        डेटा = प्रवेश_मोल.fileobj.read(65536)
                        if डेटा:
                            LOG_नोंद.extend(डेटा)
                return bytes(LOG_नोंद[처음:])
            def धाडचें(Word_SMS, शो_मोल=b'jkoros-native> '):
                처음 = len(LOG_नोंद)
                प्रक्रिया_मोल.stdin.write(Word_SMS.encode() + b'\n')
                प्रक्रिया_मोल.stdin.flush()
                return 기다림(शो_मोल, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return बरोवचें_फायल_डेटा(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                धाडचें('load /relink.c', b'hex> ')
                for स्थिती_INDEX in range(0, len(시험), 64):
                    धाडचें(시험[स्थिती_INDEX:स्थिती_INDEX+64].hex(), b'hex> ')
                assert b'LOADED' in धाडचें('.')
                मेजप = धाडचें('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in मेजप, मेजप
                मेजप = धाडचें('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in मेजप and b'exit 0' in मेजप, मेजप
                अहवाल_मोल['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                निवड_मोल.close()
                if प्रक्रिया_मोल.poll() is None:
                    प्रक्रिया_मोल.terminate()
                    try:
                        प्रक्रिया_मोल.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        प्रक्रिया_मोल.kill()
                        प्रक्रिया_मोल.wait()
                (출력 / 'guest.log').write_bytes(LOG_नोंद)
        अहवाल_मोल['passed'] = True
        print(json.dumps(अहवाल_मोल, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(अहवाल_मोल, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    चलोवप()
