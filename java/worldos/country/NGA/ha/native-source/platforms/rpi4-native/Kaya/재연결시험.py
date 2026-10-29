#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 Na_hakika_Tarin_bayani 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from gudanar_Umarni import 기준, Umarni


def Tafiyar_da():
    tatsar_manhaja_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    tatsar_manhaja_48ee4b1b.add_argument('--sdk', type=Path, default=기준.parent / 'rpi4/build/rootfs')
    인수 = tatsar_manhaja_48ee4b1b.parse_args()
    출력 = 기준 / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    Rahoto_Daraja = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            Hanyar_shiga = Path(임시)
            with tarfile.open(str(기준 / 'dist/jkoros-native-relink.tar.gz')) as gungu_Daraja:
                for Mashigar_bayanai_Daraja in gungu_Daraja.getmembers():
                    if Hanyar_shiga not in (Hanyar_shiga / Mashigar_bayanai_Daraja.name).resolve().parents or Mashigar_bayanai_Daraja.issym() or Mashigar_bayanai_Daraja.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + Mashigar_bayanai_Daraja.name)
                gungu_Daraja.extractall(str(Hanyar_shiga))
            tushe = Hanyar_shiga / 'jkoros-native-relink'
            def 재연결(Suna, 인수들):
                with (출력 / Suna).open('wb') as logu_naɗa:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(tushe),
                                   stdout=logu_naɗa, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            Rahoto_Daraja['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = tushe / 'vendor/tinycc/libtcc.c'
            Gundarin_zube = 번역기.read_text()
            위치 = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert Gundarin_zube.count(위치) == 1
            번역기.write_text(Gundarin_zube.replace(위치, 위치 + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            Hoto_Daraja = tushe / 'build/relinked/kernel8.img'
            Rahoto_Daraja['modified_kernel_sha256'] = hashlib.sha256(Hoto_Daraja.read_bytes()).hexdigest()
            assert Rahoto_Daraja['modified_kernel_sha256'] != Rahoto_Daraja['kernel_sha256']
            Rahoto_Daraja['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Umarni()
            인수들[인수들.index('-kernel') + 1] = str(Hoto_Daraja)
            haryar_aikin_na_ura_Daraja = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            logu_naɗa = bytearray()
            bangaren_zaɓi_Daraja = selectors.DefaultSelector()
            bangaren_zaɓi_Daraja.register(haryar_aikin_na_ura_Daraja.stdout, selectors.EVENT_READ)
            def jira_Matsayi(Nuna_Daraja=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while Nuna_Daraja not in logu_naɗa[처음:]:
                    if time.monotonic() > 끝 or haryar_aikin_na_ura_Daraja.poll() is not None:
                        raise AssertionError('Missing ' + repr(Nuna_Daraja) + '\n' + logu_naɗa[처음:].decode('utf-8', 'replace'))
                    for Mashigar_bayanai_Daraja, _ in bangaren_zaɓi_Daraja.select(.1):
                        Tarin_bayani = Mashigar_bayanai_Daraja.fileobj.read(65536)
                        if Tarin_bayani:
                            logu_naɗa.extend(Tarin_bayani)
                return bytes(logu_naɗa[처음:])
            def Aika(Microsoft_Word_SMS, Nuna_Daraja=b'jkoros-native> '):
                처음 = len(logu_naɗa)
                haryar_aikin_na_ura_Daraja.stdin.write(Microsoft_Word_SMS.encode() + b'\n')
                haryar_aikin_na_ura_Daraja.stdin.flush()
                return jira_Matsayi(Nuna_Daraja, 처음)
            try:
                jira_Matsayi()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return Rubuta_Fayil_Tarin_bayani(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                Aika('load /relink.c', b'hex> ')
                for 자리 in range(0, len(시험), 64):
                    Aika(시험[자리:자리+64].hex(), b'hex> ')
                assert b'LOADED' in Aika('.')
                결과 = Aika('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in 결과, 결과
                결과 = Aika('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in 결과 and b'exit 0' in 결과, 결과
                Rahoto_Daraja['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                bangaren_zaɓi_Daraja.close()
                if haryar_aikin_na_ura_Daraja.poll() is None:
                    haryar_aikin_na_ura_Daraja.terminate()
                    try:
                        haryar_aikin_na_ura_Daraja.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        haryar_aikin_na_ura_Daraja.kill()
                        haryar_aikin_na_ura_Daraja.wait()
                (출력 / 'guest.log').write_bytes(logu_naɗa)
        Rahoto_Daraja['passed'] = True
        print(json.dumps(Rahoto_Daraja, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(Rahoto_Daraja, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Tafiyar_da()
