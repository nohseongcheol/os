#!/usr/bin/env python3
"""fördelning_värde 자료만으로 LGPL 재연결과 수정한 TinyCC의 verklig_data 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from köra_kommando import åtgärd_rot, kommando


def Kör():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--sdk', type=Path, default=åtgärd_rot.parent / 'rpi4/build/rootfs')
    argument = parser_48ee4b1b.parse_args()
    utmatningsposition = åtgärd_rot / 'build/verification/cosl-relink'
    utmatningsposition.mkdir(parents=True, exist_ok=True)
    Rapport_värde = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((åtgärd_rot / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            sökväg_2 = Path(임시)
            with tarfile.open(str(åtgärd_rot / 'dist/jkoros-native-relink.tar.gz')) as grupp_värde:
                for post_värde in grupp_värde.getmembers():
                    if sökväg_2 not in (sökväg_2 / post_värde.name).resolve().parents or post_värde.issym() or post_värde.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + post_värde.name)
                grupp_värde.extractall(str(sökväg_2))
            källfil = sökväg_2 / 'jkoros-native-relink'
            def 재연결(Namn, 인수들):
                with (utmatningsposition / Namn).open('wb') as LOG_POST:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(källfil),
                                   stdout=LOG_POST, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            Rapport_värde['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            kompilerare_verktyg = källfil / 'vendor/tinycc/libtcc.c'
            brödtext = kompilerare_verktyg.read_text()
            position = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert brödtext.count(position) == 1
            kompilerare_verktyg.write_text(brödtext.replace(position, position + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(argument.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            BILD_värde = källfil / 'build/relinked/kernel8.img'
            Rapport_värde['modified_kernel_sha256'] = hashlib.sha256(BILD_värde.read_bytes()).hexdigest()
            assert Rapport_värde['modified_kernel_sha256'] != Rapport_värde['kernel_sha256']
            Rapport_värde['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = kommando()
            인수들[인수들.index('-kernel') + 1] = str(BILD_värde)
            Process_värde = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_POST = bytearray()
            markering_värde = selectors.DefaultSelector()
            markering_värde.register(Process_värde.stdout, selectors.EVENT_READ)
            def tillståndet_Vänta(visa_värde=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while visa_värde not in LOG_POST[처음:]:
                    if time.monotonic() > 끝 or Process_värde.poll() is not None:
                        raise AssertionError('Missing ' + repr(visa_värde) + '\n' + LOG_POST[처음:].decode('utf-8', 'replace'))
                    for post_värde, _ in markering_värde.select(.1):
                        data = post_värde.fileobj.read(65536)
                        if data:
                            LOG_POST.extend(data)
                return bytes(LOG_POST[처음:])
            def skicka(Ord_SMS, visa_värde=b'jkoros-native> '):
                처음 = len(LOG_POST)
                Process_värde.stdin.write(Ord_SMS.encode() + b'\n')
                Process_värde.stdin.flush()
                return tillståndet_Vänta(visa_värde, 처음)
            try:
                tillståndet_Vänta()
                tester = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return skriva_fil_data(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                skicka('load /relink.c', b'hex> ')
                for positionsindex in range(0, len(tester), 64):
                    skicka(tester[positionsindex:positionsindex+64].hex(), b'hex> ')
                assert b'LOADED' in skicka('.')
                RESULTAT = skicka('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in RESULTAT, RESULTAT
                RESULTAT = skicka('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in RESULTAT and b'exit 0' in RESULTAT, RESULTAT
                Rapport_värde['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                markering_värde.close()
                if Process_värde.poll() is None:
                    Process_värde.terminate()
                    try:
                        Process_värde.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Process_värde.kill()
                        Process_värde.wait()
                (utmatningsposition / 'guest.log').write_bytes(LOG_POST)
        Rapport_värde['passed'] = True
        print(json.dumps(Rapport_värde, ensure_ascii=False, indent=2))
    finally:
        (utmatningsposition / 'report.json').write_text(json.dumps(Rapport_värde, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Kör()
