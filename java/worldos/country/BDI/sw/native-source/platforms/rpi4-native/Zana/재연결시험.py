#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 halisi_data 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from tekeleza_amri import 기준, amri


def endesha():
    kichanganuzi_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    kichanganuzi_48ee4b1b.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = kichanganuzi_48ee4b1b.parse_args()
    출력 = 기준 / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    ripoti_thamani = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            njia = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as Kikundi_thamani:
                for ingizo_thamani in Kikundi_thamani.getmembers():
                    if njia not in (njia / ingizo_thamani.name).resolve().parents or ingizo_thamani.issym() or ingizo_thamani.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + ingizo_thamani.name)
                Kikundi_thamani.extractall(str(njia))
            chanzo = njia / 'jkoros-native-relink'
            def 재연결(Jina, 인수들):
                with (출력 / Jina).open('wb') as batli_REKODI:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(chanzo),
                                   stdout=batli_REKODI, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            ripoti_thamani['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = chanzo / 'vendor/tinycc/libtcc.c'
            Matini_kiini = 번역기.read_text()
            위치 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert Matini_kiini.count(위치) == 1
            번역기.write_text(Matini_kiini.replace(위치, 위치 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            picha_thamani = chanzo / 'build/relinked/kernel8.img'
            ripoti_thamani['modified_kernel_sha256'] = hashlib.sha256(picha_thamani.read_bytes()).hexdigest()
            assert ripoti_thamani['modified_kernel_sha256'] != ripoti_thamani['kernel_sha256']
            ripoti_thamani['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = amri()
            인수들[인수들.index('-kernel') + 1] = str(picha_thamani)
            Mchakato_thamani = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            batli_REKODI = bytearray()
            uteuzi_thamani = selectors.DefaultSelector()
            uteuzi_thamani.register(Mchakato_thamani.stdout, selectors.EVENT_READ)
            def subiri_hali(onyesha_thamani=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while onyesha_thamani not in batli_REKODI[처음:]:
                    if time.monotonic() > 끝 or Mchakato_thamani.poll() is not None:
                        raise AssertionError('Missing ' + repr(onyesha_thamani) + '\n' + batli_REKODI[처음:].decode('utf-8', 'replace'))
                    for ingizo_thamani, _ in uteuzi_thamani.select(.1):
                        data = ingizo_thamani.fileobj.read(65536)
                        if data:
                            batli_REKODI.extend(data)
                return bytes(batli_REKODI[처음:])
            def tuma(Neno_SMS, onyesha_thamani=b'jkoros-native> '):
                처음 = len(batli_REKODI)
                Mchakato_thamani.stdin.write(Neno_SMS.encode() + b'\n')
                Mchakato_thamani.stdin.flush()
                return subiri_hali(onyesha_thamani, 처음)
            try:
                subiri_hali()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return andika_faili_data(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                tuma('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    tuma(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in tuma('.')
                결과 = tuma('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = tuma('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                ripoti_thamani['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                uteuzi_thamani.close()
                if Mchakato_thamani.poll() is None:
                    Mchakato_thamani.terminate()
                    try:
                        Mchakato_thamani.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Mchakato_thamani.kill()
                        Mchakato_thamani.wait()
                (출력 / 'guest.log').write_bytes(batli_REKODI)
        ripoti_thamani['passed'] = True
        print(json.dumps(ripoti_thamani, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(ripoti_thamani, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    endesha()
