#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 фактычны_дадзеныя 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from выканаць_каманда import 기준, Загад


def Выканаць():
    аналізатар_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    аналізатар_48ee4b1b.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = аналізатар_48ee4b1b.parse_args()
    Выхад = 기준 / 'build/verification/cosl-relink'
    Выхад.mkdir(parents=True, exist_ok=True)
    справаздача_значэнне = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            ШЛЯХ = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as Група_значэнне:
                for увядзенне_значэнне in Група_значэнне.getmembers():
                    if ШЛЯХ not in (ШЛЯХ / увядзенне_значэнне.name).resolve().parents or увядзенне_значэнне.issym() or увядзенне_значэнне.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + увядзенне_значэнне.name)
                Група_значэнне.extractall(str(ШЛЯХ))
            КРЫНІЦА = ШЛЯХ / 'jkoros-native-relink'
            def 재연결(Назва, 인수들):
                with (Выхад / Назва).open('wb') as журнал_запіс:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(КРЫНІЦА),
                                   stdout=журнал_запіс, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            справаздача_значэнне['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = КРЫНІЦА / 'vendor/tinycc/libtcc.c'
            асноўны_тэкст = 번역기.read_text()
            Пазіцыя = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert асноўны_тэкст.count(Пазіцыя) == 1
            번역기.write_text(асноўны_тэкст.replace(Пазіцыя, Пазіцыя + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            выява_значэнне = КРЫНІЦА / 'build/relinked/kernel8.img'
            справаздача_значэнне['modified_kernel_sha256'] = hashlib.sha256(выява_значэнне.read_bytes()).hexdigest()
            assert справаздача_значэнне['modified_kernel_sha256'] != справаздача_значэнне['kernel_sha256']
            справаздача_значэнне['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Загад()
            인수들[인수들.index('-kernel') + 1] = str(выява_значэнне)
            Працэс_значэнне = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            журнал_запіс = bytearray()
            вылучанае_значэнне = selectors.DefaultSelector()
            вылучанае_значэнне.register(Працэс_значэнне.stdout, selectors.EVENT_READ)
            def чакае_стан(паказаць_значэнне=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while паказаць_значэнне not in журнал_запіс[처음:]:
                    if time.monotonic() > 끝 or Працэс_значэнне.poll() is not None:
                        raise AssertionError('Missing ' + repr(паказаць_значэнне) + '\n' + журнал_запіс[처음:].decode('utf-8', 'replace'))
                    for увядзенне_значэнне, _ in вылучанае_значэнне.select(.1):
                        дадзеныя = увядзенне_значэнне.fileobj.read(65536)
                        if дадзеныя:
                            журнал_запіс.extend(дадзеныя)
                return bytes(журнал_запіс[처음:])
            def адправіць(Гульні_са_словамі_Тэкст, паказаць_значэнне=b'jkoros-native> '):
                처음 = len(журнал_запіс)
                Працэс_значэнне.stdin.write(Гульні_са_словамі_Тэкст.encode() + b'\n')
                Працэс_значэнне.stdin.flush()
                return чакае_стан(паказаць_значэнне, 처음)
            try:
                чакае_стан()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return напісаць_файл_дадзеныя(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                адправіць('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    адправіць(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in адправіць('.')
                결과 = адправіць('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = адправіць('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                справаздача_значэнне['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                вылучанае_значэнне.close()
                if Працэс_значэнне.poll() is None:
                    Працэс_значэнне.terminate()
                    try:
                        Працэс_значэнне.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Працэс_значэнне.kill()
                        Працэс_значэнне.wait()
                (Выхад / 'guest.log').write_bytes(журнал_запіс)
        справаздача_значэнне['passed'] = True
        print(json.dumps(справаздача_значэнне, ensure_ascii=False, indent=2))
    finally:
        (Выхад / 'report.json').write_text(json.dumps(справаздача_значэнне, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Выканаць()
