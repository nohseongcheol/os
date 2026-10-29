#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 nyakuri_amakurushingiro 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from gukora_ibwiriza import 기준, Icyo_wifuza


def ihuriro():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = 기준 / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    raporo_agaciro = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            Inzira = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as itsinda_agaciro:
                for icyinjizwa_agaciro in itsinda_agaciro.getmembers():
                    if Inzira not in (Inzira / icyinjizwa_agaciro.name).resolve().parents or icyinjizwa_agaciro.issym() or icyinjizwa_agaciro.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + icyinjizwa_agaciro.name)
                itsinda_agaciro.extractall(str(Inzira))
            Inkomoko = Inzira / 'jkoros-native-relink'
            def 재연결(Izina, 인수들):
                with (출력 / Izina).open('wb') as kubika_umurongo:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(Inkomoko),
                                   stdout=kubika_umurongo, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            raporo_agaciro['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = Inkomoko / 'vendor/tinycc/libtcc.c'
            igihimba_cy_umwandiko = 번역기.read_text()
            위치 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert igihimba_cy_umwandiko.count(위치) == 1
            번역기.write_text(igihimba_cy_umwandiko.replace(위치, 위치 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            ishusho_agaciro = Inkomoko / 'build/relinked/kernel8.img'
            raporo_agaciro['modified_kernel_sha256'] = hashlib.sha256(ishusho_agaciro.read_bytes()).hexdigest()
            assert raporo_agaciro['modified_kernel_sha256'] != raporo_agaciro['kernel_sha256']
            raporo_agaciro['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Icyo_wifuza()
            인수들[인수들.index('-kernel') + 1] = str(ishusho_agaciro)
            Inzira_agaciro = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            kubika_umurongo = bytearray()
            ihitamo_agaciro = selectors.DefaultSelector()
            ihitamo_agaciro.register(Inzira_agaciro.stdout, selectors.EVENT_READ)
            def 기다림(kugaragaza_agaciro=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while kugaragaza_agaciro not in kubika_umurongo[처음:]:
                    if time.monotonic() > 끝 or Inzira_agaciro.poll() is not None:
                        raise AssertionError('Missing ' + repr(kugaragaza_agaciro) + '\n' + kubika_umurongo[처음:].decode('utf-8', 'replace'))
                    for icyinjizwa_agaciro, _ in ihitamo_agaciro.select(.1):
                        amakurushingiro = icyinjizwa_agaciro.fileobj.read(65536)
                        if amakurushingiro:
                            kubika_umurongo.extend(amakurushingiro)
                return bytes(kubika_umurongo[처음:])
            def kohereza(Ijambo_SMS, kugaragaza_agaciro=b'jkoros-native> '):
                처음 = len(kubika_umurongo)
                Inzira_agaciro.stdin.write(Ijambo_SMS.encode() + b'\n')
                Inzira_agaciro.stdin.flush()
                return 기다림(kugaragaza_agaciro, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return kwandika_dosiye_amakurushingiro(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                kohereza('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    kohereza(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in kohereza('.')
                결과 = kohereza('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = kohereza('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                raporo_agaciro['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                ihitamo_agaciro.close()
                if Inzira_agaciro.poll() is None:
                    Inzira_agaciro.terminate()
                    try:
                        Inzira_agaciro.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Inzira_agaciro.kill()
                        Inzira_agaciro.wait()
                (출력 / 'guest.log').write_bytes(kubika_umurongo)
        raporo_agaciro['passed'] = True
        print(json.dumps(raporo_agaciro, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(raporo_agaciro, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    ihuriro()
