#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 ਅਸਲ_ਸਮੱਗਰੀ 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ import ਪ੍ਰੋਜੈਕਟ_ਰੂਟ, ਕਮਾਂਡ


def ਚਲਾਓ_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.parent / 'rpi4/build/rootfs')
    ਆਰਗੂਮੈਂਟ = 해석기.parse_args()
    ਆਉਟਪੁੱਟ = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/verification/cosl-relink'
    ਆਉਟਪੁੱਟ.mkdir(parents=True, exist_ok=True)
    ਵਿਵਰਨ_ਕੀਮਤ = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            ਮਾਰਗ = Path(임시)
            with tarfile.open(str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'dist/jkoros-native-relink.tar.gz')) as ਸਮੂਹ_ਕੀਮਤ:
                for ਦਾਖਲਾ_ਕੀਮਤ in ਸਮੂਹ_ਕੀਮਤ.getmembers():
                    if ਮਾਰਗ not in (ਮਾਰਗ / ਦਾਖਲਾ_ਕੀਮਤ.name).resolve().parents or ਦਾਖਲਾ_ਕੀਮਤ.issym() or ਦਾਖਲਾ_ਕੀਮਤ.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + ਦਾਖਲਾ_ਕੀਮਤ.name)
                ਸਮੂਹ_ਕੀਮਤ.extractall(str(ਮਾਰਗ))
            ਸਰੋਤ = ਮਾਰਗ / 'jkoros-native-relink'
            def 재연결(ਨਾਂ, 인수들):
                with (ਆਉਟਪੁੱਟ / ਨਾਂ).open('wb') as ਲੌਗ_ਕਤਾਰ:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ਸਰੋਤ),
                                   stdout=ਲੌਗ_ਕਤਾਰ, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = ਸਰੋਤ / 'vendor/tinycc/libtcc.c'
            ਮੁੱਖ_ਪਾਠ = 번역기.read_text()
            ਸਥਿਤੀ = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert ਮੁੱਖ_ਪਾਠ.count(ਸਥਿਤੀ) == 1
            번역기.write_text(ਮੁੱਖ_ਪਾਠ.replace(ਸਥਿਤੀ, ਸਥਿਤੀ + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(ਆਰਗੂਮੈਂਟ.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            ਤਸਵੀਰ_ਕੀਮਤ = ਸਰੋਤ / 'build/relinked/kernel8.img'
            ਵਿਵਰਨ_ਕੀਮਤ['modified_kernel_sha256'] = hashlib.sha256(ਤਸਵੀਰ_ਕੀਮਤ.read_bytes()).hexdigest()
            assert ਵਿਵਰਨ_ਕੀਮਤ['modified_kernel_sha256'] != ਵਿਵਰਨ_ਕੀਮਤ['kernel_sha256']
            ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = ਕਮਾਂਡ()
            인수들[인수들.index('-kernel') + 1] = str(ਤਸਵੀਰ_ਕੀਮਤ)
            ਕਾਰਵਾਈ_ਕੀਮਤ = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ਲੌਗ_ਕਤਾਰ = bytearray()
            ਚੋਣ_ਕੀਮਤ = selectors.DefaultSelector()
            ਚੋਣ_ਕੀਮਤ.register(ਕਾਰਵਾਈ_ਕੀਮਤ.stdout, selectors.EVENT_READ)
            def 기다림(ਸ਼ੋਅ_ਕੀਮਤ=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while ਸ਼ੋਅ_ਕੀਮਤ not in ਲੌਗ_ਕਤਾਰ[처음:]:
                    if time.monotonic() > 끝 or ਕਾਰਵਾਈ_ਕੀਮਤ.poll() is not None:
                        raise AssertionError('Missing ' + repr(ਸ਼ੋਅ_ਕੀਮਤ) + '\n' + ਲੌਗ_ਕਤਾਰ[처음:].decode('utf-8', 'replace'))
                    for ਦਾਖਲਾ_ਕੀਮਤ, _ in ਚੋਣ_ਕੀਮਤ.select(.1):
                        ਸਮੱਗਰੀ = ਦਾਖਲਾ_ਕੀਮਤ.fileobj.read(65536)
                        if ਸਮੱਗਰੀ:
                            ਲੌਗ_ਕਤਾਰ.extend(ਸਮੱਗਰੀ)
                return bytes(ਲੌਗ_ਕਤਾਰ[처음:])
            def ਈਮੇਲ(ਸ਼ਬਦ_ਪਾਠ, ਸ਼ੋਅ_ਕੀਮਤ=b'jkoros-native> '):
                처음 = len(ਲੌਗ_ਕਤਾਰ)
                ਕਾਰਵਾਈ_ਕੀਮਤ.stdin.write(ਸ਼ਬਦ_ਪਾਠ.encode() + b'\n')
                ਕਾਰਵਾਈ_ਕੀਮਤ.stdin.flush()
                return 기다림(ਸ਼ੋਅ_ਕੀਮਤ, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return ਲਿੱਖੋ_ਲਿਖਤ_ਪੱਤਰ_ਸਮੱਗਰੀ(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                ਈਮੇਲ('load /relink.c', b'hex> ')
                for ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ in range(0, len(시험), 64):
                    ਈਮੇਲ(시험[ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ:ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ+64].hex(), b'hex> ')
                assert b'LOADED' in ਈਮੇਲ('.')
                ਮਾਪ = ਈਮੇਲ('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in ਮਾਪ, ਮਾਪ
                ਮਾਪ = ਈਮੇਲ('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in ਮਾਪ and b'exit 0' in ਮਾਪ, ਮਾਪ
                ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                ਚੋਣ_ਕੀਮਤ.close()
                if ਕਾਰਵਾਈ_ਕੀਮਤ.poll() is None:
                    ਕਾਰਵਾਈ_ਕੀਮਤ.terminate()
                    try:
                        ਕਾਰਵਾਈ_ਕੀਮਤ.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        ਕਾਰਵਾਈ_ਕੀਮਤ.kill()
                        ਕਾਰਵਾਈ_ਕੀਮਤ.wait()
                (ਆਉਟਪੁੱਟ / 'guest.log').write_bytes(ਲੌਗ_ਕਤਾਰ)
        ਵਿਵਰਨ_ਕੀਮਤ['passed'] = True
        print(json.dumps(ਵਿਵਰਨ_ਕੀਮਤ, ensure_ascii=False, indent=2))
    finally:
        (ਆਉਟਪੁੱਟ / 'report.json').write_text(json.dumps(ਵਿਵਰਨ_ਕੀਮਤ, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    ਚਲਾਓ_2()
