#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 વાસ્તવિક_ડેટા 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from અમલ_કરો_આદેશ import પ્રોજેક્ટ_રૂટ, આદેશ


def ચલાવો_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=પ્રોજેક્ટ_રૂટ.parent / 'rpi4/build/rootfs')
    દલીલો = 해석기.parse_args()
    આઉટપુટ = પ્રોજેક્ટ_રૂટ / 'build/verification/cosl-relink'
    આઉટપુટ.mkdir(parents=True, exist_ok=True)
    અહેવાલ_મૂલ્ય = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((પ્રોજેક્ટ_રૂટ / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            પથ = Path(임시)
            with tarfile.open(str(પ્રોજેક્ટ_રૂટ / 'dist/jkoros-native-relink.tar.gz')) as સમૂહ_મૂલ્ય:
                for પ્રવેશ_મૂલ્ય in સમૂહ_મૂલ્ય.getmembers():
                    if પથ not in (પથ / પ્રવેશ_મૂલ્ય.name).resolve().parents or પ્રવેશ_મૂલ્ય.issym() or પ્રવેશ_મૂલ્ય.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + પ્રવેશ_મૂલ્ય.name)
                સમૂહ_મૂલ્ય.extractall(str(પથ))
            સ્રોત = પથ / 'jkoros-native-relink'
            def 재연결(નામ, 인수들):
                with (આઉટપુટ / નામ).open('wb') as લૉગ_પંક્તિ:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(સ્રોત),
                                   stdout=લૉગ_પંક્તિ, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            અહેવાલ_મૂલ્ય['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = સ્રોત / 'vendor/tinycc/libtcc.c'
            મુખ્ય_પાઠ = 번역기.read_text()
            સ્થાન = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert મુખ્ય_પાઠ.count(સ્થાન) == 1
            번역기.write_text(મુખ્ય_પાઠ.replace(સ્થાન, સ્થાન + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(દલીલો.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            છબી_મૂલ્ય = સ્રોત / 'build/relinked/kernel8.img'
            અહેવાલ_મૂલ્ય['modified_kernel_sha256'] = hashlib.sha256(છબી_મૂલ્ય.read_bytes()).hexdigest()
            assert અહેવાલ_મૂલ્ય['modified_kernel_sha256'] != અહેવાલ_મૂલ્ય['kernel_sha256']
            અહેવાલ_મૂલ્ય['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = આદેશ()
            인수들[인수들.index('-kernel') + 1] = str(છબી_મૂલ્ય)
            પ્રક્રિયા_મૂલ્ય = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            લૉગ_પંક્તિ = bytearray()
            ચયન_મૂલ્ય = selectors.DefaultSelector()
            ચયન_મૂલ્ય.register(પ્રક્રિયા_મૂલ્ય.stdout, selectors.EVENT_READ)
            def પ્રતીક્ષા_સ્થિતિ(શૉ_મૂલ્ય=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while શૉ_મૂલ્ય not in લૉગ_પંક્તિ[처음:]:
                    if time.monotonic() > 끝 or પ્રક્રિયા_મૂલ્ય.poll() is not None:
                        raise AssertionError('Missing ' + repr(શૉ_મૂલ્ય) + '\n' + લૉગ_પંક્તિ[처음:].decode('utf-8', 'replace'))
                    for પ્રવેશ_મૂલ્ય, _ in ચયન_મૂલ્ય.select(.1):
                        ડેટા = પ્રવેશ_મૂલ્ય.fileobj.read(65536)
                        if ડેટા:
                            લૉગ_પંક્તિ.extend(ડેટા)
                return bytes(લૉગ_પંક્તિ[처음:])
            def મોકલો(શબ્દ_પાઠ, શૉ_મૂલ્ય=b'jkoros-native> '):
                처음 = len(લૉગ_પંક્તિ)
                પ્રક્રિયા_મૂલ્ય.stdin.write(શબ્દ_પાઠ.encode() + b'\n')
                પ્રક્રિયા_મૂલ્ય.stdin.flush()
                return પ્રતીક્ષા_સ્થિતિ(શૉ_મૂલ્ય, 처음)
            try:
                પ્રતીક્ષા_સ્થિતિ()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return લખો_ફાઇલ_ડેટા(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                મોકલો('load /relink.c', b'hex> ')
                for સ્થિતિ_અનુક્રમણિકા in range(0, len(시험), 64):
                    મોકલો(시험[સ્થિતિ_અનુક્રમણિકા:સ્થિતિ_અનુક્રમણિકા+64].hex(), b'hex> ')
                assert b'LOADED' in મોકલો('.')
                પરિમાણ = મોકલો('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in પરિમાણ, પરિમાણ
                પરિમાણ = મોકલો('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in પરિમાણ and b'exit 0' in પરિમાણ, પરિમાણ
                અહેવાલ_મૂલ્ય['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                ચયન_મૂલ્ય.close()
                if પ્રક્રિયા_મૂલ્ય.poll() is None:
                    પ્રક્રિયા_મૂલ્ય.terminate()
                    try:
                        પ્રક્રિયા_મૂલ્ય.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        પ્રક્રિયા_મૂલ્ય.kill()
                        પ્રક્રિયા_મૂલ્ય.wait()
                (આઉટપુટ / 'guest.log').write_bytes(લૉગ_પંક્તિ)
        અહેવાલ_મૂલ્ય['passed'] = True
        print(json.dumps(અહેવાલ_મૂલ્ય, ensure_ascii=False, indent=2))
    finally:
        (આઉટપુટ / 'report.json').write_text(json.dumps(અહેવાલ_મૂલ્ય, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    ચલાવો_2()
