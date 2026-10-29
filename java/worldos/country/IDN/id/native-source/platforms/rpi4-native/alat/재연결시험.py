#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 aktual_data 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Jalankan_perintah import Tugas_akar, perintah


def jalankan():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--sdk', type=Path, default=Tugas_akar.parent / 'rpi4/build/rootfs')
    argumen = parser_48ee4b1b.parse_args()
    keluaranTeks = Tugas_akar / 'build/verification/cosl-relink'
    keluaranTeks.mkdir(parents=True, exist_ok=True)
    lapor_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Tugas_akar / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            jalur = Path(임시)
            with tarfile.open(str(Tugas_akar / 'dist/jkoros-native-relink.tar.gz')) as grup_VALUE:
                for entri_VALUE in grup_VALUE.getmembers():
                    if jalur not in (jalur / entri_VALUE.name).resolve().parents or entri_VALUE.issym() or entri_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + entri_VALUE.name)
                grup_VALUE.extractall(str(jalur))
            kodeSumber = jalur / 'jkoros-native-relink'
            def 재연결(Nama_2, 인수들):
                with (keluaranTeks / Nama_2).open('wb') as LOG_baris:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(kodeSumber),
                                   stdout=LOG_baris, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            lapor_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = kodeSumber / 'vendor/tinycc/libtcc.c'
            teks_isi = 번역기.read_text()
            posisi = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert teks_isi.count(posisi) == 1
            번역기.write_text(teks_isi.replace(posisi, posisi + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(argumen.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            foto_VALUE = kodeSumber / 'build/relinked/kernel8.img'
            lapor_VALUE['modified_kernel_sha256'] = hashlib.sha256(foto_VALUE.read_bytes()).hexdigest()
            assert lapor_VALUE['modified_kernel_sha256'] != lapor_VALUE['kernel_sha256']
            lapor_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = perintah()
            인수들[인수들.index('-kernel') + 1] = str(foto_VALUE)
            Proses_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_baris = bytearray()
            pilihan_VALUE = selectors.DefaultSelector()
            pilihan_VALUE.register(Proses_VALUE.stdout, selectors.EVENT_READ)
            def tunggu_Status(show_VALUE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while show_VALUE not in LOG_baris[처음:]:
                    if time.monotonic() > 끝 or Proses_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(show_VALUE) + '\n' + LOG_baris[처음:].decode('utf-8', 'replace'))
                    for entri_VALUE, _ in pilihan_VALUE.select(.1):
                        data = entri_VALUE.fileobj.read(65536)
                        if data:
                            LOG_baris.extend(data)
                return bytes(LOG_baris[처음:])
            def kirim(Kata_SMS, show_VALUE=b'jkoros-native> '):
                처음 = len(LOG_baris)
                Proses_VALUE.stdin.write(Kata_SMS.encode() + b'\n')
                Proses_VALUE.stdin.flush()
                return tunggu_Status(show_VALUE, 처음)
            try:
                tunggu_Status()
                pengujian = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return tulis_file_data(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                kirim('load /relink.c', b'hex> ')
                for posisi_INDEX in range(0, len(pengujian), 64):
                    kirim(pengujian[posisi_INDEX:posisi_INDEX+64].hex(), b'hex> ')
                assert b'LOADED' in kirim('.')
                hasil = kirim('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in hasil, hasil
                hasil = kirim('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in hasil and b'exit 0' in hasil, hasil
                lapor_VALUE['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                pilihan_VALUE.close()
                if Proses_VALUE.poll() is None:
                    Proses_VALUE.terminate()
                    try:
                        Proses_VALUE.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Proses_VALUE.kill()
                        Proses_VALUE.wait()
                (keluaranTeks / 'guest.log').write_bytes(LOG_baris)
        lapor_VALUE['passed'] = True
        print(json.dumps(lapor_VALUE, ensure_ascii=False, indent=2))
    finally:
        (keluaranTeks / 'report.json').write_text(json.dumps(lapor_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    jalankan()
