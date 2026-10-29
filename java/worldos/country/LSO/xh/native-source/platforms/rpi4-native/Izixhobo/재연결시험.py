#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 eyona_yenzekileyo_iingcombolo 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from ukwenza_umyalelo import 기준, Umyalelo


def Phumeza():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = 해석기.parse_args()
    출력 = 기준 / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    ingxelo_ixabiso_ddf2aaf3 = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            INDLELA = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as iqela_ixabiso:
                for ufako_nkcukacha_ixabiso in iqela_ixabiso.getmembers():
                    if INDLELA not in (INDLELA / ufako_nkcukacha_ixabiso.name).resolve().parents or ufako_nkcukacha_ixabiso.issym() or ufako_nkcukacha_ixabiso.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + ufako_nkcukacha_ixabiso.name)
                iqela_ixabiso.extractall(str(INDLELA))
            UMTHOMBO = INDLELA / 'jkoros-native-relink'
            def 재연결(Igama, 인수들):
                with (출력 / Igama).open('wb') as ilog_umqolo:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(UMTHOMBO),
                                   stdout=ilog_umqolo, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            ingxelo_ixabiso_ddf2aaf3['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = UMTHOMBO / 'vendor/tinycc/libtcc.c'
            isiqu_sombhalo = 번역기.read_text()
            위치 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert isiqu_sombhalo.count(위치) == 1
            번역기.write_text(isiqu_sombhalo.replace(위치, 위치 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            umfanekiso_ixabiso = UMTHOMBO / 'build/relinked/kernel8.img'
            ingxelo_ixabiso_ddf2aaf3['modified_kernel_sha256'] = hashlib.sha256(umfanekiso_ixabiso.read_bytes()).hexdigest()
            assert ingxelo_ixabiso_ddf2aaf3['modified_kernel_sha256'] != ingxelo_ixabiso_ddf2aaf3['kernel_sha256']
            ingxelo_ixabiso_ddf2aaf3['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Umyalelo()
            인수들[인수들.index('-kernel') + 1] = str(umfanekiso_ixabiso)
            Inkqubo_ixabiso = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ilog_umqolo = bytearray()
            ukukhetha_ixabiso = selectors.DefaultSelector()
            ukukhetha_ixabiso.register(Inkqubo_ixabiso.stdout, selectors.EVENT_READ)
            def 기다림(bonisa_ixabiso=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while bonisa_ixabiso not in ilog_umqolo[처음:]:
                    if time.monotonic() > 끝 or Inkqubo_ixabiso.poll() is not None:
                        raise AssertionError('Missing ' + repr(bonisa_ixabiso) + '\n' + ilog_umqolo[처음:].decode('utf-8', 'replace'))
                    for ufako_nkcukacha_ixabiso, _ in ukukhetha_ixabiso.select(.1):
                        iingcombolo = ufako_nkcukacha_ixabiso.fileobj.read(65536)
                        if iingcombolo:
                            ilog_umqolo.extend(iingcombolo)
                return bytes(ilog_umqolo[처음:])
            def thumela(Igama_I_SMS, bonisa_ixabiso=b'jkoros-native> '):
                처음 = len(ilog_umqolo)
                Inkqubo_ixabiso.stdin.write(Igama_I_SMS.encode() + b'\n')
                Inkqubo_ixabiso.stdin.flush()
                return 기다림(bonisa_ixabiso, 처음)
            try:
                기다림()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return bhala_ifayile_iingcombolo(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                thumela('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    thumela(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in thumela('.')
                결과 = thumela('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = thumela('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                ingxelo_ixabiso_ddf2aaf3['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                ukukhetha_ixabiso.close()
                if Inkqubo_ixabiso.poll() is None:
                    Inkqubo_ixabiso.terminate()
                    try:
                        Inkqubo_ixabiso.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Inkqubo_ixabiso.kill()
                        Inkqubo_ixabiso.wait()
                (출력 / 'guest.log').write_bytes(ilog_umqolo)
        ingxelo_ixabiso_ddf2aaf3['passed'] = True
        print(json.dumps(ingxelo_ixabiso_ddf2aaf3, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(ingxelo_ixabiso_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Phumeza()
