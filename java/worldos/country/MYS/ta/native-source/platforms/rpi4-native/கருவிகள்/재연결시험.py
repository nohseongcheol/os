#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 அசல்_தரவு 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from இயக்கு_கட்டளை import திட்டப்பணி_மூலம், கட்டளை


def செயல்படுத்துக():
    பார்சர்_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    பார்சர்_48ee4b1b.add_argument('--sdk', type=Path, default=திட்டப்பணி_மூலம்.parent / 'rpi4/build/rootfs')
    செயலுருபுகள் = பார்சர்_48ee4b1b.parse_args()
    வெளியீட்டு_இடம் = திட்டப்பணி_மூலம் / 'build/verification/cosl-relink'
    வெளியீட்டு_இடம்.mkdir(parents=True, exist_ok=True)
    அறிக்கை_மதிப்பு = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((திட்டப்பணி_மூலம் / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            பாதை_2 = Path(임시)
            with tarfile.open(str(திட்டப்பணி_மூலம் / 'dist/jkoros-native-relink.tar.gz')) as குழு_மதிப்பு:
                for உள்ளீடு_மதிப்பு in குழு_மதிப்பு.getmembers():
                    if பாதை_2 not in (பாதை_2 / உள்ளீடு_மதிப்பு.name).resolve().parents or உள்ளீடு_மதிப்பு.issym() or உள்ளீடு_மதிப்பு.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + உள்ளீடு_மதிப்பு.name)
                குழு_மதிப்பு.extractall(str(பாதை_2))
            மூலக்_கோப்பு = பாதை_2 / 'jkoros-native-relink'
            def 재연결(பெயர், 인수들):
                with (வெளியீட்டு_இடம் / பெயர்).open('wb') as பதிவு_பதிவு:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(மூலக்_கோப்பு),
                                   stdout=பதிவு_பதிவு, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            அறிக்கை_மதிப்பு['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = மூலக்_கோப்பு / 'vendor/tinycc/libtcc.c'
            தகவல்_உரை = 번역기.read_text()
            இடம் = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert தகவல்_உரை.count(இடம்) == 1
            번역기.write_text(தகவல்_உரை.replace(இடம், இடம் + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(செயலுருபுகள்.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            படம்_மதிப்பு = மூலக்_கோப்பு / 'build/relinked/kernel8.img'
            அறிக்கை_மதிப்பு['modified_kernel_sha256'] = hashlib.sha256(படம்_மதிப்பு.read_bytes()).hexdigest()
            assert அறிக்கை_மதிப்பு['modified_kernel_sha256'] != அறிக்கை_மதிப்பு['kernel_sha256']
            அறிக்கை_மதிப்பு['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = கட்டளை()
            인수들[인수들.index('-kernel') + 1] = str(படம்_மதிப்பு)
            செயலகம்_மதிப்பு = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            பதிவு_பதிவு = bytearray()
            தேர்வு_மதிப்பு = selectors.DefaultSelector()
            தேர்வு_மதிப்பு.register(செயலகம்_மதிப்பு.stdout, selectors.EVENT_READ)
            def காத்திரு_நிலை(காட்சி_மதிப்பு_487749b8=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while காட்சி_மதிப்பு_487749b8 not in பதிவு_பதிவு[처음:]:
                    if time.monotonic() > 끝 or செயலகம்_மதிப்பு.poll() is not None:
                        raise AssertionError('Missing ' + repr(காட்சி_மதிப்பு_487749b8) + '\n' + பதிவு_பதிவு[처음:].decode('utf-8', 'replace'))
                    for உள்ளீடு_மதிப்பு, _ in தேர்வு_மதிப்பு.select(.1):
                        தரவு = உள்ளீடு_மதிப்பு.fileobj.read(65536)
                        if தரவு:
                            பதிவு_பதிவு.extend(தரவு)
                return bytes(பதிவு_பதிவு[처음:])
            def அனுப்பு(சொல்_உரை, காட்சி_மதிப்பு_487749b8=b'jkoros-native> '):
                처음 = len(பதிவு_பதிவு)
                செயலகம்_மதிப்பு.stdin.write(சொல்_உரை.encode() + b'\n')
                செயலகம்_மதிப்பு.stdin.flush()
                return காத்திரு_நிலை(காட்சி_மதிப்பு_487749b8, 처음)
            try:
                காத்திரு_நிலை()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return எழுது_கோப்பு_தரவு(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                அனுப்பு('load /relink.c', b'hex> ')
                for நிலை_அடைவு in range(0, len(시험), 64):
                    அனுப்பு(시험[நிலை_அடைவு:நிலை_அடைவு+64].hex(), b'hex> ')
                assert b'LOADED' in அனுப்பு('.')
                அளவிடக்கூடியது = அனுப்பு('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in அளவிடக்கூடியது, அளவிடக்கூடியது
                அளவிடக்கூடியது = அனுப்பு('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in அளவிடக்கூடியது and b'exit 0' in அளவிடக்கூடியது, அளவிடக்கூடியது
                அறிக்கை_மதிப்பு['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                தேர்வு_மதிப்பு.close()
                if செயலகம்_மதிப்பு.poll() is None:
                    செயலகம்_மதிப்பு.terminate()
                    try:
                        செயலகம்_மதிப்பு.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        செயலகம்_மதிப்பு.kill()
                        செயலகம்_மதிப்பு.wait()
                (வெளியீட்டு_இடம் / 'guest.log').write_bytes(பதிவு_பதிவு)
        அறிக்கை_மதிப்பு['passed'] = True
        print(json.dumps(அறிக்கை_மதிப்பு, ensure_ascii=False, indent=2))
    finally:
        (வெளியீட்டு_இடம் / 'report.json').write_text(json.dumps(அறிக்கை_மதிப்பு, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    செயல்படுத்துக()
