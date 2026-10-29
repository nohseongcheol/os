#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 ትክክለኛ_ውሂብ 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from ፈጽም_ትእዛዝ import አሳይ_ስር, ትእዛዝ


def ማስኬጃ():
    አግልሎ_ማስቀመጥ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--sdk', type=Path, default=አሳይ_ስር.parent / 'rpi4/build/rootfs')
    인수 = አግልሎ_ማስቀመጥ_48ee4b1b.parse_args()
    ውጤት = አሳይ_ስር / 'build/verification/cosl-relink'
    ውጤት.mkdir(parents=True, exist_ok=True)
    ዘገባ_እሴት = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((አሳይ_ስር / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            መተላለፊያ = Path(임시)
            with tarfile.open(str(አሳይ_ስር / 'dist/jkoros-native-relink.tar.gz')) as ቡድን_እሴት:
                for ምዝግብ_እሴት in ቡድን_እሴት.getmembers():
                    if መተላለፊያ not in (መተላለፊያ / ምዝግብ_እሴት.name).resolve().parents or ምዝግብ_እሴት.issym() or ምዝግብ_እሴት.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + ምዝግብ_እሴት.name)
                ቡድን_እሴት.extractall(str(መተላለፊያ))
            ምንጭ = መተላለፊያ / 'jkoros-native-relink'
            def 재연결(ስም, 인수들):
                with (ውጤት / ስም).open('wb') as መዝግብ_ረድፍ:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ምንጭ),
                                   stdout=መዝግብ_ረድፍ, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            ዘገባ_እሴት['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = ምንጭ / 'vendor/tinycc/libtcc.c'
            የጽሁፍ_አካል = 번역기.read_text()
            አካባቢ = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert የጽሁፍ_አካል.count(አካባቢ) == 1
            번역기.write_text(የጽሁፍ_አካል.replace(አካባቢ, አካባቢ + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            ምስል_እሴት = ምንጭ / 'build/relinked/kernel8.img'
            ዘገባ_እሴት['modified_kernel_sha256'] = hashlib.sha256(ምስል_እሴት.read_bytes()).hexdigest()
            assert ዘገባ_እሴት['modified_kernel_sha256'] != ዘገባ_እሴት['kernel_sha256']
            ዘገባ_እሴት['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = ትእዛዝ()
            인수들[인수들.index('-kernel') + 1] = str(ምስል_እሴት)
            ሂደት_እሴት = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            መዝግብ_ረድፍ = bytearray()
            የተመረጠ_እሴት = selectors.DefaultSelector()
            የተመረጠ_እሴት.register(ሂደት_እሴት.stdout, selectors.EVENT_READ)
            def መጠበቅ_ዞን(አሳይ_እሴት=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while አሳይ_እሴት not in መዝግብ_ረድፍ[처음:]:
                    if time.monotonic() > 끝 or ሂደት_እሴት.poll() is not None:
                        raise AssertionError('Missing ' + repr(አሳይ_እሴት) + '\n' + መዝግብ_ረድፍ[처음:].decode('utf-8', 'replace'))
                    for ምዝግብ_እሴት, _ in የተመረጠ_እሴት.select(.1):
                        ውሂብ = ምዝግብ_እሴት.fileobj.read(65536)
                        if ውሂብ:
                            መዝግብ_ረድፍ.extend(ውሂብ)
                return bytes(መዝግብ_ረድፍ[처음:])
            def ላክ(ቃል_ጽሁፍ, አሳይ_እሴት=b'jkoros-native> '):
                처음 = len(መዝግብ_ረድፍ)
                ሂደት_እሴት.stdin.write(ቃል_ጽሁፍ.encode() + b'\n')
                ሂደት_እሴት.stdin.flush()
                return መጠበቅ_ዞን(አሳይ_እሴት, 처음)
            try:
                መጠበቅ_ዞን()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return ጻፍ_ፋይል_ውሂብ(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                ላክ('load /relink.c', b'hex> ')
                for በቦታ_አስቀመጠ_መረጃ_ጠቆመ in range(0, len(시험), 64):
                    ላክ(시험[በቦታ_አስቀመጠ_መረጃ_ጠቆመ:በቦታ_አስቀመጠ_መረጃ_ጠቆመ+64].hex(), b'hex> ')
                assert b'LOADED' in ላክ('.')
                ልኬት = ላክ('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in ልኬት, ልኬት
                ልኬት = ላክ('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in ልኬት and b'exit 0' in ልኬት, ልኬት
                ዘገባ_እሴት['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                የተመረጠ_እሴት.close()
                if ሂደት_እሴት.poll() is None:
                    ሂደት_እሴት.terminate()
                    try:
                        ሂደት_እሴት.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        ሂደት_እሴት.kill()
                        ሂደት_እሴት.wait()
                (ውጤት / 'guest.log').write_bytes(መዝግብ_ረድፍ)
        ዘገባ_እሴት['passed'] = True
        print(json.dumps(ዘገባ_እሴት, ensure_ascii=False, indent=2))
    finally:
        (ውጤት / 'report.json').write_text(json.dumps(ዘገባ_እሴት, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    ማስኬጃ()
