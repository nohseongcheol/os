#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 sebenar_data 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from laksanakan_perintah import projek_akar, Perintah


def Jalan():
    penghurai_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    penghurai_48ee4b1b.add_argument('--sdk', type=Path, default=projek_akar.parent / 'rpi4/build/rootfs')
    인수 = penghurai_48ee4b1b.parse_args()
    출력 = projek_akar / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    lapor_VALUE = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((projek_akar / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            LALUAN = Path(임시)
            with tarfile.open(str(projek_akar / 'dist/jkoros-native-relink.tar.gz')) as Kumpulan_VALUE:
                for pemasukan_VALUE in Kumpulan_VALUE.getmembers():
                    if LALUAN not in (LALUAN / pemasukan_VALUE.name).resolve().parents or pemasukan_VALUE.issym() or pemasukan_VALUE.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + pemasukan_VALUE.name)
                Kumpulan_VALUE.extractall(str(LALUAN))
            SUMBER = LALUAN / 'jkoros-native-relink'
            def 재연결(Nama, 인수들):
                with (출력 / Nama).open('wb') as LOG_baris:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(SUMBER),
                                   stdout=LOG_baris, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            lapor_VALUE['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = SUMBER / 'vendor/tinycc/libtcc.c'
            teks_jasad = 번역기.read_text()
            Kedudukan = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert teks_jasad.count(Kedudukan) == 1
            번역기.write_text(teks_jasad.replace(Kedudukan, Kedudukan + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            imej_VALUE = SUMBER / 'build/relinked/kernel8.img'
            lapor_VALUE['modified_kernel_sha256'] = hashlib.sha256(imej_VALUE.read_bytes()).hexdigest()
            assert lapor_VALUE['modified_kernel_sha256'] != lapor_VALUE['kernel_sha256']
            lapor_VALUE['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Perintah()
            인수들[인수들.index('-kernel') + 1] = str(imej_VALUE)
            Proses_VALUE = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_baris = bytearray()
            pilihan_VALUE = selectors.DefaultSelector()
            pilihan_VALUE.register(Proses_VALUE.stdout, selectors.EVENT_READ)
            def keadaan_tunggu(tayang_VALUE=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while tayang_VALUE not in LOG_baris[처음:]:
                    if time.monotonic() > 끝 or Proses_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(tayang_VALUE) + '\n' + LOG_baris[처음:].decode('utf-8', 'replace'))
                    for pemasukan_VALUE, _ in pilihan_VALUE.select(.1):
                        data = pemasukan_VALUE.fileobj.read(65536)
                        if data:
                            LOG_baris.extend(data)
                return bytes(LOG_baris[처음:])
            def e_mel_9aee63bd(Word_SMS, tayang_VALUE=b'jkoros-native> '):
                처음 = len(LOG_baris)
                Proses_VALUE.stdin.write(Word_SMS.encode() + b'\n')
                Proses_VALUE.stdin.flush()
                return keadaan_tunggu(tayang_VALUE, 처음)
            try:
                keadaan_tunggu()
                ujian = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return tulis_fail_data(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                e_mel_9aee63bd('load /relink.c', b'hex> ')
                for jawatan_INDEX in range(0, len(ujian), 64):
                    e_mel_9aee63bd(ujian[jawatan_INDEX:jawatan_INDEX+64].hex(), b'hex> ')
                assert b'LOADED' in e_mel_9aee63bd('.')
                ukuran = e_mel_9aee63bd('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in ukuran, ukuran
                ukuran = e_mel_9aee63bd('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in ukuran and b'exit 0' in ukuran, ukuran
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
                (출력 / 'guest.log').write_bytes(LOG_baris)
        lapor_VALUE['passed'] = True
        print(json.dumps(lapor_VALUE, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(lapor_VALUE, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Jalan()
