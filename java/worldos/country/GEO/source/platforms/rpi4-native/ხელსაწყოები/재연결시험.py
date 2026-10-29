#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 რეალური_მონაცემები 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from შესრულება_ბრძანება import პროეცირება_ფესვი, ბრძანება


def გაშვება():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=პროეცირება_ფესვი.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = პროეცირება_ფესვი / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    ანგარიში_მნიშვნელობა = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((პროეცირება_ფესვი / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            გეზი = Path(임시)
            with tarfile.open(str(პროეცირება_ფესვი / 'dist/jkoros-native-relink.tar.gz')) as ჯგუფი_მნიშვნელობა:
                for შენატანი_მნიშვნელობა in ჯგუფი_მნიშვნელობა.getmembers():
                    if გეზი not in (გეზი / შენატანი_მნიშვნელობა.name).resolve().parents or შენატანი_მნიშვნელობა.issym() or შენატანი_მნიშვნელობა.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + შენატანი_მნიშვნელობა.name)
                ჯგუფი_მნიშვნელობა.extractall(str(გეზი))
            წყარო = გეზი / 'jkoros-native-relink'
            def 재연결(სახელი, 인수들):
                with (출력 / სახელი).open('wb') as ჟურნალი_ჩაწერა:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(წყარო),
                                   stdout=ჟურნალი_ჩაწერა, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            ანგარიში_მნიშვნელობა['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = წყარო / 'vendor/tinycc/libtcc.c'
            ძირითადი_ტექსტი = 번역기.read_text()
            პოზიცია = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert ძირითადი_ტექსტი.count(პოზიცია) == 1
            번역기.write_text(ძირითადი_ტექსტი.replace(პოზიცია, პოზიცია + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            ნახატი_მნიშვნელობა = წყარო / 'build/relinked/kernel8.img'
            ანგარიში_მნიშვნელობა['modified_kernel_sha256'] = hashlib.sha256(ნახატი_მნიშვნელობა.read_bytes()).hexdigest()
            assert ანგარიში_მნიშვნელობა['modified_kernel_sha256'] != ანგარიში_მნიშვნელობა['kernel_sha256']
            ანგარიში_მნიშვნელობა['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = ბრძანება()
            인수들[인수들.index('-kernel') + 1] = str(ნახატი_მნიშვნელობა)
            პროცესი_მნიშვნელობა = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ჟურნალი_ჩაწერა = bytearray()
            მონიშნული_ობიექტი_მნიშვნელობა = selectors.DefaultSelector()
            მონიშნული_ობიექტი_მნიშვნელობა.register(პროცესი_მნიშვნელობა.stdout, selectors.EVENT_READ)
            def მოლოდინი_სტატუსი(ჩვენება_მნიშვნელობა=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while ჩვენება_მნიშვნელობა not in ჟურნალი_ჩაწერა[처음:]:
                    if time.monotonic() > 끝 or პროცესი_მნიშვნელობა.poll() is not None:
                        raise AssertionError('Missing ' + repr(ჩვენება_მნიშვნელობა) + '\n' + ჟურნალი_ჩაწერა[처음:].decode('utf-8', 'replace'))
                    for შენატანი_მნიშვნელობა, _ in მონიშნული_ობიექტი_მნიშვნელობა.select(.1):
                        მონაცემები = შენატანი_მნიშვნელობა.fileobj.read(65536)
                        if მონაცემები:
                            ჟურნალი_ჩაწერა.extend(მონაცემები)
                return bytes(ჟურნალი_ჩაწერა[처음:])
            def გაგზავნა(სიტყვები_ტექსტი, ჩვენება_მნიშვნელობა=b'jkoros-native> '):
                처음 = len(ჟურნალი_ჩაწერა)
                პროცესი_მნიშვნელობა.stdin.write(სიტყვები_ტექსტი.encode() + b'\n')
                პროცესი_მნიშვნელობა.stdin.flush()
                return მოლოდინი_სტატუსი(ჩვენება_მნიშვნელობა, 처음)
            try:
                მოლოდინი_სტატუსი()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return ჩაწერა_ფაილი_მონაცემები(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                გაგზავნა('load /relink.c', b'hex> ')
                for პოზიცია_ინდექსი in range(0, len(시험), 64):
                    გაგზავნა(시험[პოზიცია_ინდექსი:პოზიცია_ინდექსი+64].hex(), b'hex> ')
                assert b'LOADED' in გაგზავნა('.')
                გაზომვა = გაგზავნა('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in გაზომვა, გაზომვა
                გაზომვა = გაგზავნა('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in გაზომვა and b'exit 0' in გაზომვა, გაზომვა
                ანგარიში_მნიშვნელობა['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                მონიშნული_ობიექტი_მნიშვნელობა.close()
                if პროცესი_მნიშვნელობა.poll() is None:
                    პროცესი_მნიშვნელობა.terminate()
                    try:
                        პროცესი_მნიშვნელობა.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        პროცესი_მნიშვნელობა.kill()
                        პროცესი_მნიშვნელობა.wait()
                (출력 / 'guest.log').write_bytes(ჟურნალი_ჩაწერა)
        ანგარიში_მნიშვნელობა['passed'] = True
        print(json.dumps(ანგარიში_მნიშვნელობა, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(ანგარიში_მნიშვნელობა, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    გაშვება()
