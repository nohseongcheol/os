#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 իրական_տվյալ 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from կատարել_հրաման import արձակել_արմատ, Հրահանգ


def Գործարկել():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=արձակել_արմատ.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    Ելք = արձակել_արմատ / 'build/verification/cosl-relink'
    Ելք.mkdir(parents=True, exist_ok=True)
    զեկույց_արժեք = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((արձակել_արմատ / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            Ճանապարհ = Path(임시)
            with tarfile.open(str(արձակել_արմատ / 'dist/jkoros-native-relink.tar.gz')) as խումբ_արժեք:
                for մուտքագրում_արժեք in խումբ_արժեք.getmembers():
                    if Ճանապարհ not in (Ճանապարհ / մուտքագրում_արժեք.name).resolve().parents or մուտքագրում_արժեք.issym() or մուտքագրում_արժեք.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + մուտքագրում_արժեք.name)
                խումբ_արժեք.extractall(str(Ճանապարհ))
            ԱՂԲՅՈՒՐ = Ճանապարհ / 'jkoros-native-relink'
            def 재연결(Անուն, 인수들):
                with (Ելք / Անուն).open('wb') as մատյան_տող:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ԱՂԲՅՈՒՐ),
                                   stdout=մատյան_տող, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            զեկույց_արժեք['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = ԱՂԲՅՈՒՐ / 'vendor/tinycc/libtcc.c'
            հիմնական_գրվածք = 번역기.read_text()
            Դիրք = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert հիմնական_գրվածք.count(Դիրք) == 1
            번역기.write_text(հիմնական_գրվածք.replace(Դիրք, Դիրք + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            նկար_արժեք = ԱՂԲՅՈՒՐ / 'build/relinked/kernel8.img'
            զեկույց_արժեք['modified_kernel_sha256'] = hashlib.sha256(նկար_արժեք.read_bytes()).hexdigest()
            assert զեկույց_արժեք['modified_kernel_sha256'] != զեկույց_արժեք['kernel_sha256']
            զեկույց_արժեք['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Հրահանգ()
            인수들[인수들.index('-kernel') + 1] = str(նկար_արժեք)
            Ընթացք_արժեք = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            մատյան_տող = bytearray()
            ընտրվածք_արժեք = selectors.DefaultSelector()
            ընտրվածք_արժեք.register(Ընթացք_արժեք.stdout, selectors.EVENT_READ)
            def 기다림(ցուցադրել_արժեք=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while ցուցադրել_արժեք not in մատյան_տող[처음:]:
                    if time.monotonic() > 끝 or Ընթացք_արժեք.poll() is not None:
                        raise AssertionError('Missing ' + repr(ցուցադրել_արժեք) + '\n' + մատյան_տող[처음:].decode('utf-8', 'replace'))
                    for մուտքագրում_արժեք, _ in ընտրվածք_արժեք.select(.1):
                        տվյալ = մուտքագրում_արժեք.fileobj.read(65536)
                        if տվյալ:
                            մատյան_տող.extend(տվյալ)
                return bytes(մատյան_տող[처음:])
            def ուղարկել(Բառ_Գրվածք, ցուցադրել_արժեք=b'jkoros-native> '):
                처음 = len(մատյան_տող)
                Ընթացք_արժեք.stdin.write(Բառ_Գրվածք.encode() + b'\n')
                Ընթացք_արժեք.stdin.flush()
                return 기다림(ցուցադրել_արժեք, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return գրել_նիշք_տվյալ(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                ուղարկել('load /relink.c', b'hex> ')
                for դիրք_դասիչ in range(0, len(시험), 64):
                    ուղարկել(시험[դիրք_դասիչ:դիրք_դասիչ+64].hex(), b'hex> ')
                assert b'LOADED' in ուղարկել('.')
                չափ = ուղարկել('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in չափ, չափ
                չափ = ուղարկել('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in չափ and b'exit 0' in չափ, չափ
                զեկույց_արժեք['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                ընտրվածք_արժեք.close()
                if Ընթացք_արժեք.poll() is None:
                    Ընթացք_արժեք.terminate()
                    try:
                        Ընթացք_արժեք.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Ընթացք_արժեք.kill()
                        Ընթացք_արժեք.wait()
                (Ելք / 'guest.log').write_bytes(մատյան_տող)
        զեկույց_արժեք['passed'] = True
        print(json.dumps(զեկույց_արժեք, ensure_ascii=False, indent=2))
    finally:
        (Ելք / 'report.json').write_text(json.dumps(զեկույց_արժեք, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Գործարկել()
