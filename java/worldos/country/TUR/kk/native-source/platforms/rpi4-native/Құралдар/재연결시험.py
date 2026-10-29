#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 нақты_деректер 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from орындау_пәрмен import жоба_түбір, Команда


def Орындау_2():
    талдау_құралы_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    талдау_құралы_48ee4b1b.add_argument('--sdk', type=Path, default=жоба_түбір.parent / 'rpi4/build/rootfs')
    Аргументтер = талдау_құралы_48ee4b1b.parse_args()
    Шығысы = жоба_түбір / 'build/verification/cosl-relink'
    Шығысы.mkdir(parents=True, exist_ok=True)
    есеп_мән = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((жоба_түбір / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            Жол_2 = Path(임시)
            with tarfile.open(str(жоба_түбір / 'dist/jkoros-native-relink.tar.gz')) as Топ_мән:
                for енгізу_мән in Топ_мән.getmembers():
                    if Жол_2 not in (Жол_2 / енгізу_мән.name).resolve().parents or енгізу_мән.issym() or енгізу_мән.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + енгізу_мән.name)
                Топ_мән.extractall(str(Жол_2))
            Неден = Жол_2 / 'jkoros-native-relink'
            def 재연결(Аты, 인수들):
                with (Шығысы / Аты).open('wb') as журнал_жол:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(Неден),
                                   stdout=журнал_жол, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            есеп_мән['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = Неден / 'vendor/tinycc/libtcc.c'
            негізгі_мәтін = 번역기.read_text()
            Орны = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert негізгі_мәтін.count(Орны) == 1
            번역기.write_text(негізгі_мәтін.replace(Орны, Орны + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(Аргументтер.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            сурет_мән = Неден / 'build/relinked/kernel8.img'
            есеп_мән['modified_kernel_sha256'] = hashlib.sha256(сурет_мән.read_bytes()).hexdigest()
            assert есеп_мән['modified_kernel_sha256'] != есеп_мән['kernel_sha256']
            есеп_мән['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Команда()
            인수들[인수들.index('-kernel') + 1] = str(сурет_мән)
            Процесс_мән = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            журнал_жол = bytearray()
            таңдау_мән = selectors.DefaultSelector()
            таңдау_мән.register(Процесс_мән.stdout, selectors.EVENT_READ)
            def күту_күйі(көрсету_мән=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while көрсету_мән not in журнал_жол[처음:]:
                    if time.monotonic() > 끝 or Процесс_мән.poll() is not None:
                        raise AssertionError('Missing ' + repr(көрсету_мән) + '\n' + журнал_жол[처음:].decode('utf-8', 'replace'))
                    for енгізу_мән, _ in таңдау_мән.select(.1):
                        деректер = енгізу_мән.fileobj.read(65536)
                        if деректер:
                            журнал_жол.extend(деректер)
                return bytes(журнал_жол[처음:])
            def жіберу(Сөз_Мәтін, көрсету_мән=b'jkoros-native> '):
                처음 = len(журнал_жол)
                Процесс_мән.stdin.write(Сөз_Мәтін.encode() + b'\n')
                Процесс_мән.stdin.flush()
                return күту_күйі(көрсету_мән, 처음)
            try:
                күту_күйі()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return жазу_файл_деректер(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                жіберу('load /relink.c', b'hex> ')
                for лауазым_индекс in range(0, len(시험), 64):
                    жіберу(시험[лауазым_индекс:лауазым_индекс+64].hex(), b'hex> ')
                assert b'LOADED' in жіберу('.')
                НӘТИЖЕ = жіберу('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in НӘТИЖЕ, НӘТИЖЕ
                НӘТИЖЕ = жіберу('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in НӘТИЖЕ and b'exit 0' in НӘТИЖЕ, НӘТИЖЕ
                есеп_мән['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                таңдау_мән.close()
                if Процесс_мән.poll() is None:
                    Процесс_мән.terminate()
                    try:
                        Процесс_мән.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Процесс_мән.kill()
                        Процесс_мән.wait()
                (Шығысы / 'guest.log').write_bytes(журнал_жол)
        есеп_мән['passed'] = True
        print(json.dumps(есеп_мән, ensure_ascii=False, indent=2))
    finally:
        (Шығысы / 'report.json').write_text(json.dumps(есеп_мән, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Орындау_2()
