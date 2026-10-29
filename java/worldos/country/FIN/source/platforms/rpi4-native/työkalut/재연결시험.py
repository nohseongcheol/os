#!/usr/bin/env python3
"""jakelu_ARVO 자료만으로 LGPL 재연결과 수정한 TinyCC의 todellinen_data 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Suorita_komento import aloite_juuri, komento


def Suorita_2():
    jäsennin_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    jäsennin_48ee4b1b.add_argument('--sdk', type=Path, default=aloite_juuri.parent / 'rpi4/build/rootfs')
    argumentit = jäsennin_48ee4b1b.parse_args()
    tulostuspaikka = aloite_juuri / 'build/verification/cosl-relink'
    tulostuspaikka.mkdir(parents=True, exist_ok=True)
    raportti_ARVO = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((aloite_juuri / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            polku_2 = Path(임시)
            with tarfile.open(str(aloite_juuri / 'dist/jkoros-native-relink.tar.gz')) as Ryhmä_ARVO:
                for merkintä_ARVO_962f286b in Ryhmä_ARVO.getmembers():
                    if polku_2 not in (polku_2 / merkintä_ARVO_962f286b.name).resolve().parents or merkintä_ARVO_962f286b.issym() or merkintä_ARVO_962f286b.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + merkintä_ARVO_962f286b.name)
                Ryhmä_ARVO.extractall(str(polku_2))
            lähdetiedosto = polku_2 / 'jkoros-native-relink'
            def 재연결(Nimi, 인수들):
                with (tulostuspaikka / Nimi).open('wb') as LOG_TIETUE:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(lähdetiedosto),
                                   stdout=LOG_TIETUE, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            raportti_ARVO['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            kääntäjä_työkalu = lähdetiedosto / 'vendor/tinycc/libtcc.c'
            leipäteksti = kääntäjä_työkalu.read_text()
            paikka = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert leipäteksti.count(paikka) == 1
            kääntäjä_työkalu.write_text(leipäteksti.replace(paikka, paikka + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(argumentit.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            KUVA_ARVO = lähdetiedosto / 'build/relinked/kernel8.img'
            raportti_ARVO['modified_kernel_sha256'] = hashlib.sha256(KUVA_ARVO.read_bytes()).hexdigest()
            assert raportti_ARVO['modified_kernel_sha256'] != raportti_ARVO['kernel_sha256']
            raportti_ARVO['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = komento()
            인수들[인수들.index('-kernel') + 1] = str(KUVA_ARVO)
            prosessi_ARVO = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_TIETUE = bytearray()
            valinta_ARVO = selectors.DefaultSelector()
            valinta_ARVO.register(prosessi_ARVO.stdout, selectors.EVENT_READ)
            def odotustila(näyttää_ARVO=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while näyttää_ARVO not in LOG_TIETUE[처음:]:
                    if time.monotonic() > 끝 or prosessi_ARVO.poll() is not None:
                        raise AssertionError('Missing ' + repr(näyttää_ARVO) + '\n' + LOG_TIETUE[처음:].decode('utf-8', 'replace'))
                    for merkintä_ARVO_962f286b, _ in valinta_ARVO.select(.1):
                        data = merkintä_ARVO_962f286b.fileobj.read(65536)
                        if data:
                            LOG_TIETUE.extend(data)
                return bytes(LOG_TIETUE[처음:])
            def lähettää(Word_SMS, näyttää_ARVO=b'jkoros-native> '):
                처음 = len(LOG_TIETUE)
                prosessi_ARVO.stdin.write(Word_SMS.encode() + b'\n')
                prosessi_ARVO.stdin.flush()
                return odotustila(näyttää_ARVO, 처음)
            try:
                odotustila()
                testit = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return kirjoitus_Tiedosto_data(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                lähettää('load /relink.c', b'hex> ')
                for sijainti in range(0, len(testit), 64):
                    lähettää(testit[sijainti:sijainti+64].hex(), b'hex> ')
                assert b'LOADED' in lähettää('.')
                TULOS = lähettää('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in TULOS, TULOS
                TULOS = lähettää('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in TULOS and b'exit 0' in TULOS, TULOS
                raportti_ARVO['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                valinta_ARVO.close()
                if prosessi_ARVO.poll() is None:
                    prosessi_ARVO.terminate()
                    try:
                        prosessi_ARVO.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        prosessi_ARVO.kill()
                        prosessi_ARVO.wait()
                (tulostuspaikka / 'guest.log').write_bytes(LOG_TIETUE)
        raportti_ARVO['passed'] = True
        print(json.dumps(raportti_ARVO, ensure_ascii=False, indent=2))
    finally:
        (tulostuspaikka / 'report.json').write_text(json.dumps(raportti_ARVO, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Suorita_2()
