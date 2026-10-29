#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 стваран_подаци 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Изврши_команда import пројектовати_корен, Наредба


def Покрени():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--sdk', type=Path, default=пројектовати_корен.parent / 'rpi4/build/rootfs')
    Аргументи = анализатор_48ee4b1b.parse_args()
    Излаз = пројектовати_корен / 'build/verification/cosl-relink'
    Излаз.mkdir(parents=True, exist_ok=True)
    извештај_вриједност = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((пројектовати_корен / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            ПУТАЊА = Path(임시)
            with tarfile.open(str(пројектовати_корен / 'dist/jkoros-native-relink.tar.gz')) as Група_вриједност:
                for унос_вриједност in Група_вриједност.getmembers():
                    if ПУТАЊА not in (ПУТАЊА / унос_вриједност.name).resolve().parents or унос_вриједност.issym() or унос_вриједност.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + унос_вриједност.name)
                Група_вриједност.extractall(str(ПУТАЊА))
            ИЗВОР = ПУТАЊА / 'jkoros-native-relink'
            def 재연결(Назив, 인수들):
                with (Излаз / Назив).open('wb') as евиденција_ред:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ИЗВОР),
                                   stdout=евиденција_ред, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            извештај_вриједност['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = ИЗВОР / 'vendor/tinycc/libtcc.c'
            тело_текста = 번역기.read_text()
            Положај = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert тело_текста.count(Положај) == 1
            번역기.write_text(тело_текста.replace(Положај, Положај + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(Аргументи.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            слика_вриједност = ИЗВОР / 'build/relinked/kernel8.img'
            извештај_вриједност['modified_kernel_sha256'] = hashlib.sha256(слика_вриједност.read_bytes()).hexdigest()
            assert извештај_вриједност['modified_kernel_sha256'] != извештај_вриједност['kernel_sha256']
            извештај_вриједност['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Наредба()
            인수들[인수들.index('-kernel') + 1] = str(слика_вриједност)
            Процес_вриједност = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            евиденција_ред = bytearray()
            избор_вриједност = selectors.DefaultSelector()
            избор_вриједност.register(Процес_вриједност.stdout, selectors.EVENT_READ)
            def чекај_стање(емисија_вриједност=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while емисија_вриједност not in евиденција_ред[처음:]:
                    if time.monotonic() > 끝 or Процес_вриједност.poll() is not None:
                        raise AssertionError('Missing ' + repr(емисија_вриједност) + '\n' + евиденција_ред[처음:].decode('utf-8', 'replace'))
                    for унос_вриједност, _ in избор_вриједност.select(.1):
                        подаци = унос_вриједност.fileobj.read(65536)
                        if подаци:
                            евиденција_ред.extend(подаци)
                return bytes(евиденција_ред[처음:])
            def послати(Укрштенице_Текст, емисија_вриједност=b'jkoros-native> '):
                처음 = len(евиденција_ред)
                Процес_вриједност.stdin.write(Укрштенице_Текст.encode() + b'\n')
                Процес_вриједност.stdin.flush()
                return чекај_стање(емисија_вриједност, 처음)
            try:
                чекај_стање()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return писати_фајл_подаци(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                послати('load /relink.c', b'hex> ')
                for позиција_индекс in range(0, len(시험), 64):
                    послати(시험[позиција_индекс:позиција_индекс+64].hex(), b'hex> ')
                assert b'LOADED' in послати('.')
                ИСХОД = послати('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in ИСХОД, ИСХОД
                ИСХОД = послати('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in ИСХОД and b'exit 0' in ИСХОД, ИСХОД
                извештај_вриједност['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                избор_вриједност.close()
                if Процес_вриједност.poll() is None:
                    Процес_вриједност.terminate()
                    try:
                        Процес_вриједност.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Процес_вриједност.kill()
                        Процес_вриједност.wait()
                (Излаз / 'guest.log').write_bytes(евиденција_ред)
        извештај_вриједност['passed'] = True
        print(json.dumps(извештај_вриједност, ensure_ascii=False, indent=2))
    finally:
        (Излаз / 'report.json').write_text(json.dumps(извештај_вриједност, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Покрени()
