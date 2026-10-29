#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 ដែលពិត_ទិន្នន័យ 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from អនុវត្ត_ពាក្យបញ្ជា import បញ្ចាំង_ឬស, ពាក្យ_បញ្ជា


def រត់():
    មុខងារ_ញែក_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    មុខងារ_ញែក_48ee4b1b.add_argument('--sdk', type=Path, default=បញ្ចាំង_ឬស.parent / 'rpi4/build/rootfs')
    អាគុយម៉ង់ = មុខងារ_ញែក_48ee4b1b.parse_args()
    លទ្ធផល = បញ្ចាំង_ឬស / 'build/verification/cosl-relink'
    លទ្ធផល.mkdir(parents=True, exist_ok=True)
    រាយការណ៍_តំលៃ = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((បញ្ចាំង_ឬស / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            ផ្លូវ = Path(임시)
            with tarfile.open(str(បញ្ចាំង_ឬស / 'dist/jkoros-native-relink.tar.gz')) as ក្រុម_តំលៃ:
                for ការបញ្ចូល_តំលៃ in ក្រុម_តំលៃ.getmembers():
                    if ផ្លូវ not in (ផ្លូវ / ការបញ្ចូល_តំលៃ.name).resolve().parents or ការបញ្ចូល_តំលៃ.issym() or ការបញ្ចូល_តំលៃ.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + ការបញ្ចូល_តំលៃ.name)
                ក្រុម_តំលៃ.extractall(str(ផ្លូវ))
            ប្រភព = ផ្លូវ / 'jkoros-native-relink'
            def 재연결(ឈ្មោះ, 인수들):
                with (លទ្ធផល / ឈ្មោះ).open('wb') as កំណត់_ហេតុ_ថត:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ប្រភព),
                                   stdout=កំណត់_ហេតុ_ថត, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            រាយការណ៍_តំលៃ['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = ប្រភព / 'vendor/tinycc/libtcc.c'
            តួអត្ថបទ = 번역기.read_text()
            កំណត់ទីតាំង = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert តួអត្ថបទ.count(កំណត់ទីតាំង) == 1
            번역기.write_text(តួអត្ថបទ.replace(កំណត់ទីតាំង, កំណត់ទីតាំង + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(អាគុយម៉ង់.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            រូបថត_តំលៃ = ប្រភព / 'build/relinked/kernel8.img'
            រាយការណ៍_តំលៃ['modified_kernel_sha256'] = hashlib.sha256(រូបថត_តំលៃ.read_bytes()).hexdigest()
            assert រាយការណ៍_តំលៃ['modified_kernel_sha256'] != រាយការណ៍_តំលៃ['kernel_sha256']
            រាយការណ៍_តំលៃ['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = ពាក្យ_បញ្ជា()
            인수들[인수들.index('-kernel') + 1] = str(រូបថត_តំលៃ)
            ដំណើរការ_តំលៃ = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            កំណត់_ហេតុ_ថត = bytearray()
            ការជ្រើស_តំលៃ = selectors.DefaultSelector()
            ការជ្រើស_តំលៃ.register(ដំណើរការ_តំលៃ.stdout, selectors.EVENT_READ)
            def រង់ចាំ_ភាព(បង្ហាញ_តំលៃ=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while បង្ហាញ_តំលៃ not in កំណត់_ហេតុ_ថត[처음:]:
                    if time.monotonic() > 끝 or ដំណើរការ_តំលៃ.poll() is not None:
                        raise AssertionError('Missing ' + repr(បង្ហាញ_តំលៃ) + '\n' + កំណត់_ហេតុ_ថត[처음:].decode('utf-8', 'replace'))
                    for ការបញ្ចូល_តំលៃ, _ in ការជ្រើស_តំលៃ.select(.1):
                        ទិន្នន័យ = ការបញ្ចូល_តំលៃ.fileobj.read(65536)
                        if ទិន្នន័យ:
                            កំណត់_ហេតុ_ថត.extend(ទិន្នន័យ)
                return bytes(កំណត់_ហេតុ_ថត[처음:])
            def ផ្ញើ(ពាក្យ_អត្ថបទ, បង្ហាញ_តំលៃ=b'jkoros-native> '):
                처음 = len(កំណត់_ហេតុ_ថត)
                ដំណើរការ_តំលៃ.stdin.write(ពាក្យ_អត្ថបទ.encode() + b'\n')
                ដំណើរការ_តំលៃ.stdin.flush()
                return រង់ចាំ_ភាព(បង្ហាញ_តំលៃ, 처음)
            try:
                រង់ចាំ_ភាព()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return សរសេរ_ឯកសារ_ទិន្នន័យ(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                ផ្ញើ('load /relink.c', b'hex> ')
                for កំណត់ទីតាំង_សន្ទស្សន៏ in range(0, len(시험), 64):
                    ផ្ញើ(시험[កំណត់ទីតាំង_សន្ទស្សន៏:កំណត់ទីតាំង_សន្ទស្សន៏+64].hex(), b'hex> ')
                assert b'LOADED' in ផ្ញើ('.')
                ការវាស់វែង = ផ្ញើ('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in ការវាស់វែង, ការវាស់វែង
                ការវាស់វែង = ផ្ញើ('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in ការវាស់វែង and b'exit 0' in ការវាស់វែង, ការវាស់វែង
                រាយការណ៍_តំលៃ['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                ការជ្រើស_តំលៃ.close()
                if ដំណើរការ_តំលៃ.poll() is None:
                    ដំណើរការ_តំលៃ.terminate()
                    try:
                        ដំណើរការ_តំលៃ.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        ដំណើរការ_តំលៃ.kill()
                        ដំណើរការ_តំលៃ.wait()
                (លទ្ធផល / 'guest.log').write_bytes(កំណត់_ហេតុ_ថត)
        រាយការណ៍_តំលៃ['passed'] = True
        print(json.dumps(រាយការណ៍_តំលៃ, ensure_ascii=False, indent=2))
    finally:
        (លទ្ធផល / 'report.json').write_text(json.dumps(រាយការណ៍_តំលៃ, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    រត់()
