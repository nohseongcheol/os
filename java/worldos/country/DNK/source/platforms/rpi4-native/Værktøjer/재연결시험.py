#!/usr/bin/env python3
"""distribution_VÆRDI 자료만으로 LGPL 재연결과 수정한 TinyCC의 faktisk_data 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Udfør_kommando import To_do_rod, Kommando


def Kør_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--sdk', type=Path, default=To_do_rod.parent / 'rpi4/build/rootfs')
    Argumenter = parser_48ee4b1b.parse_args()
    Udgang = To_do_rod / 'build/verification/cosl-relink'
    Udgang.mkdir(parents=True, exist_ok=True)
    rapport_VÆRDI = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((To_do_rod / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            Sti = Path(임시)
            with tarfile.open(str(To_do_rod / 'dist/jkoros-native-relink.tar.gz')) as gruppe_VÆRDI:
                for post_VÆRDI_962f286b in gruppe_VÆRDI.getmembers():
                    if Sti not in (Sti / post_VÆRDI_962f286b.name).resolve().parents or post_VÆRDI_962f286b.issym() or post_VÆRDI_962f286b.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + post_VÆRDI_962f286b.name)
                gruppe_VÆRDI.extractall(str(Sti))
            KILDE = Sti / 'jkoros-native-relink'
            def 재연결(Navn, 인수들):
                with (Udgang / Navn).open('wb') as LOG_post:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(KILDE),
                                   stdout=LOG_post, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            rapport_VÆRDI['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            compiler_værktøj = KILDE / 'vendor/tinycc/libtcc.c'
            brødtekst = compiler_værktøj.read_text()
            Placering = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert brødtekst.count(Placering) == 1
            compiler_værktøj.write_text(brødtekst.replace(Placering, Placering + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(Argumenter.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            Image_VÆRDI = KILDE / 'build/relinked/kernel8.img'
            rapport_VÆRDI['modified_kernel_sha256'] = hashlib.sha256(Image_VÆRDI.read_bytes()).hexdigest()
            assert rapport_VÆRDI['modified_kernel_sha256'] != rapport_VÆRDI['kernel_sha256']
            rapport_VÆRDI['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Kommando()
            인수들[인수들.index('-kernel') + 1] = str(Image_VÆRDI)
            Proces_VÆRDI = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_post = bytearray()
            markering_VÆRDI = selectors.DefaultSelector()
            markering_VÆRDI.register(Proces_VÆRDI.stdout, selectors.EVENT_READ)
            def ventetilstand(vise_VÆRDI=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while vise_VÆRDI not in LOG_post[처음:]:
                    if time.monotonic() > 끝 or Proces_VÆRDI.poll() is not None:
                        raise AssertionError('Missing ' + repr(vise_VÆRDI) + '\n' + LOG_post[처음:].decode('utf-8', 'replace'))
                    for post_VÆRDI_962f286b, _ in markering_VÆRDI.select(.1):
                        data = post_VÆRDI_962f286b.fileobj.read(65536)
                        if data:
                            LOG_post.extend(data)
                return bytes(LOG_post[처음:])
            def maile(Ord_sms, vise_VÆRDI=b'jkoros-native> '):
                처음 = len(LOG_post)
                Proces_VÆRDI.stdin.write(Ord_sms.encode() + b'\n')
                Proces_VÆRDI.stdin.flush()
                return ventetilstand(vise_VÆRDI, 처음)
            try:
                ventetilstand()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return skrive_fil_data(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                maile('load /relink.c', b'hex> ')
                for positionsindeks in range(0, len(시험), 64):
                    maile(시험[positionsindeks:positionsindeks+64].hex(), b'hex> ')
                assert b'LOADED' in maile('.')
                KR = maile('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in KR, KR
                KR = maile('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in KR and b'exit 0' in KR, KR
                rapport_VÆRDI['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                markering_VÆRDI.close()
                if Proces_VÆRDI.poll() is None:
                    Proces_VÆRDI.terminate()
                    try:
                        Proces_VÆRDI.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Proces_VÆRDI.kill()
                        Proces_VÆRDI.wait()
                (Udgang / 'guest.log').write_bytes(LOG_post)
        rapport_VÆRDI['passed'] = True
        print(json.dumps(rapport_VÆRDI, ensure_ascii=False, indent=2))
    finally:
        (Udgang / 'report.json').write_text(json.dumps(rapport_VÆRDI, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Kør_2()
