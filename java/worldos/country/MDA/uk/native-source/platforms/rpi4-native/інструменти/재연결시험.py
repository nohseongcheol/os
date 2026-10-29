#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 фактично_дані 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Виконати_команда import Дії_корінь, команда


def запустити():
    аналізатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    аналізатор_48ee4b1b.add_argument('--sdk', type=Path, default=Дії_корінь.parent / 'rpi4/build/rootfs')
    аргументи = аналізатор_48ee4b1b.parse_args()
    Вивід = Дії_корінь / 'build/verification/cosl-relink'
    Вивід.mkdir(parents=True, exist_ok=True)
    звіт_значення = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Дії_корінь / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            шлях = Path(임시)
            with tarfile.open(str(Дії_корінь / 'dist/jkoros-native-relink.tar.gz')) as Група_значення:
                for запис_значення_962f286b in Група_значення.getmembers():
                    if шлях not in (шлях / запис_значення_962f286b.name).resolve().parents or запис_значення_962f286b.issym() or запис_значення_962f286b.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + запис_значення_962f286b.name)
                Група_значення.extractall(str(шлях))
            вихіднийКод = шлях / 'jkoros-native-relink'
            def 재연결(Назва, 인수들):
                with (Вивід / Назва).open('wb') as журнал_запис:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(вихіднийКод),
                                   stdout=журнал_запис, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            звіт_значення['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            компілятор_інструмент = вихіднийКод / 'vendor/tinycc/libtcc.c'
            основний_текст = компілятор_інструмент.read_text()
            позиція = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert основний_текст.count(позиція) == 1
            компілятор_інструмент.write_text(основний_текст.replace(позиція, позиція + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(аргументи.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            фото_значення = вихіднийКод / 'build/relinked/kernel8.img'
            звіт_значення['modified_kernel_sha256'] = hashlib.sha256(фото_значення.read_bytes()).hexdigest()
            assert звіт_значення['modified_kernel_sha256'] != звіт_значення['kernel_sha256']
            звіт_значення['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = команда()
            인수들[인수들.index('-kernel') + 1] = str(фото_значення)
            процес_значення = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            журнал_запис = bytearray()
            вибране_значення = selectors.DefaultSelector()
            вибране_значення.register(процес_значення.stdout, selectors.EVENT_READ)
            def стан_очікування(показувати_значення=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while показувати_значення not in журнал_запис[처음:]:
                    if time.monotonic() > 끝 or процес_значення.poll() is not None:
                        raise AssertionError('Missing ' + repr(показувати_значення) + '\n' + журнал_запис[처음:].decode('utf-8', 'replace'))
                    for запис_значення_962f286b, _ in вибране_значення.select(.1):
                        дані = запис_значення_962f286b.fileobj.read(65536)
                        if дані:
                            журнал_запис.extend(дані)
                return bytes(журнал_запис[처음:])
            def надсилати(Ігри_в_слова_Текст, показувати_значення=b'jkoros-native> '):
                처음 = len(журнал_запис)
                процес_значення.stdin.write(Ігри_в_слова_Текст.encode() + b'\n')
                процес_значення.stdin.flush()
                return стан_очікування(показувати_значення, 처음)
            try:
                стан_очікування()
                випробування = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return записування_Файл_дані(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                надсилати('load /relink.c', b'hex> ')
                for індекс_розташування in range(0, len(випробування), 64):
                    надсилати(випробування[індекс_розташування:індекс_розташування+64].hex(), b'hex> ')
                assert b'LOADED' in надсилати('.')
                результат = надсилати('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in результат, результат
                результат = надсилати('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in результат and b'exit 0' in результат, результат
                звіт_значення['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                вибране_значення.close()
                if процес_значення.poll() is None:
                    процес_значення.terminate()
                    try:
                        процес_значення.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        процес_значення.kill()
                        процес_значення.wait()
                (Вивід / 'guest.log').write_bytes(журнал_запис)
        звіт_значення['passed'] = True
        print(json.dumps(звіт_значення, ensure_ascii=False, indent=2))
    finally:
        (Вивід / 'report.json').write_text(json.dumps(звіт_значення, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    запустити()
