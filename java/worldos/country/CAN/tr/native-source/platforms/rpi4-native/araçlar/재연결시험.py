#!/usr/bin/env python3
"""dağıtım_değer 자료만으로 LGPL 재연결과 수정한 TinyCC의 fiili_veri 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from yürütmek_komut import işlem_kök, komut


def çalıştır():
    ayrıştırıcı_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ayrıştırıcı_48ee4b1b.add_argument('--sdk', type=Path, default=işlem_kök.parent / 'rpi4/build/rootfs')
    bağımsız_değişkenler = ayrıştırıcı_48ee4b1b.parse_args()
    metinÇıktısı = işlem_kök / 'build/verification/cosl-relink'
    metinÇıktısı.mkdir(parents=True, exist_ok=True)
    Rapor_değer = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((işlem_kök / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            yol = Path(임시)
            with tarfile.open(str(işlem_kök / 'dist/jkoros-native-relink.tar.gz')) as Grup_değer:
                for girdi_değer in Grup_değer.getmembers():
                    if yol not in (yol / girdi_değer.name).resolve().parents or girdi_değer.issym() or girdi_değer.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + girdi_değer.name)
                Grup_değer.extractall(str(yol))
            kaynakKod = yol / 'jkoros-native-relink'
            def 재연결(İsim, 인수들):
                with (metinÇıktısı / İsim).open('wb') as LOG_KAYIT:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(kaynakKod),
                                   stdout=LOG_KAYIT, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            Rapor_değer['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            derleyici_araç = kaynakKod / 'vendor/tinycc/libtcc.c'
            gövde_metni = derleyici_araç.read_text()
            konum = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert gövde_metni.count(konum) == 1
            derleyici_araç.write_text(gövde_metni.replace(konum, konum + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(bağımsız_değişkenler.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            RESİM_değer = kaynakKod / 'build/relinked/kernel8.img'
            Rapor_değer['modified_kernel_sha256'] = hashlib.sha256(RESİM_değer.read_bytes()).hexdigest()
            assert Rapor_değer['modified_kernel_sha256'] != Rapor_değer['kernel_sha256']
            Rapor_değer['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = komut()
            인수들[인수들.index('-kernel') + 1] = str(RESİM_değer)
            işlem_değer = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_KAYIT = bytearray()
            seçim_değer = selectors.DefaultSelector()
            seçim_değer.register(işlem_değer.stdout, selectors.EVENT_READ)
            def bekleme_durumu(şov_değer=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while şov_değer not in LOG_KAYIT[처음:]:
                    if time.monotonic() > 끝 or işlem_değer.poll() is not None:
                        raise AssertionError('Missing ' + repr(şov_değer) + '\n' + LOG_KAYIT[처음:].decode('utf-8', 'replace'))
                    for girdi_değer, _ in seçim_değer.select(.1):
                        veri = girdi_değer.fileobj.read(65536)
                        if veri:
                            LOG_KAYIT.extend(veri)
                return bytes(LOG_KAYIT[처음:])
            def göndermek(Word_SMS, şov_değer=b'jkoros-native> '):
                처음 = len(LOG_KAYIT)
                işlem_değer.stdin.write(Word_SMS.encode() + b'\n')
                işlem_değer.stdin.flush()
                return bekleme_durumu(şov_değer, 처음)
            try:
                bekleme_durumu()
                sınamalar = '#include <Dosya_ABI.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return yazma_Dosya_veri(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                göndermek('load /relink.c', b'hex> ')
                for konum_dizini in range(0, len(sınamalar), 64):
                    göndermek(sınamalar[konum_dizini:konum_dizini+64].hex(), b'hex> ')
                assert b'LOADED' in göndermek('.')
                sonuç = göndermek('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in sonuç, sonuç
                sonuç = göndermek('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in sonuç and b'exit 0' in sonuç, sonuç
                Rapor_değer['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                seçim_değer.close()
                if işlem_değer.poll() is None:
                    işlem_değer.terminate()
                    try:
                        işlem_değer.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        işlem_değer.kill()
                        işlem_değer.wait()
                (metinÇıktısı / 'guest.log').write_bytes(LOG_KAYIT)
        Rapor_değer['passed'] = True
        print(json.dumps(Rapor_değer, ensure_ascii=False, indent=2))
    finally:
        (metinÇıktısı / 'report.json').write_text(json.dumps(Rapor_değer, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    çalıştır()
