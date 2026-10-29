#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 real_dades 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from Executa_ordre import Project_rel, Ordre


def Executa_2():
    analitzador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analitzador_48ee4b1b.add_argument('--sdk', type=Path, default=Project_rel.parent / 'rpi4/build/rootfs')
    인수 = analitzador_48ee4b1b.parse_args()
    Sortida = Project_rel / 'build/verification/cosl-relink'
    Sortida.mkdir(parents=True, exist_ok=True)
    informe_VALOR = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_rel / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            Camí = Path(임시)
            with tarfile.open(str(Project_rel / 'dist/jkoros-native-relink.tar.gz')) as Grup_VALOR:
                for introducció_VALOR in Grup_VALOR.getmembers():
                    if Camí not in (Camí / introducció_VALOR.name).resolve().parents or introducció_VALOR.issym() or introducció_VALOR.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + introducció_VALOR.name)
                Grup_VALOR.extractall(str(Camí))
            FONT = Camí / 'jkoros-native-relink'
            def 재연결(Nom, 인수들):
                with (Sortida / Nom).open('wb') as LOG_fila:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(FONT),
                                   stdout=LOG_fila, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            informe_VALOR['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = FONT / 'vendor/tinycc/libtcc.c'
            text_del_cos = 번역기.read_text()
            Posició = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert text_del_cos.count(Posició) == 1
            번역기.write_text(text_del_cos.replace(Posició, Posició + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            IMATGE_VALOR = FONT / 'build/relinked/kernel8.img'
            informe_VALOR['modified_kernel_sha256'] = hashlib.sha256(IMATGE_VALOR.read_bytes()).hexdigest()
            assert informe_VALOR['modified_kernel_sha256'] != informe_VALOR['kernel_sha256']
            informe_VALOR['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Ordre()
            인수들[인수들.index('-kernel') + 1] = str(IMATGE_VALOR)
            Procés_VALOR = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_fila = bytearray()
            selecció_VALOR = selectors.DefaultSelector()
            selecció_VALOR.register(Procés_VALOR.stdout, selectors.EVENT_READ)
            def Espera_Estat(mostrar_VALOR=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while mostrar_VALOR not in LOG_fila[처음:]:
                    if time.monotonic() > 끝 or Procés_VALOR.poll() is not None:
                        raise AssertionError('Missing ' + repr(mostrar_VALOR) + '\n' + LOG_fila[처음:].decode('utf-8', 'replace'))
                    for introducció_VALOR, _ in selecció_VALOR.select(.1):
                        dades = introducció_VALOR.fileobj.read(65536)
                        if dades:
                            LOG_fila.extend(dades)
                return bytes(LOG_fila[처음:])
            def enviar(Word_SMS, mostrar_VALOR=b'jkoros-native> '):
                처음 = len(LOG_fila)
                Procés_VALOR.stdin.write(Word_SMS.encode() + b'\n')
                Procés_VALOR.stdin.flush()
                return Espera_Estat(mostrar_VALOR, 처음)
            try:
                Espera_Estat()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return escriure_arxiu_dades(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                enviar('load /relink.c', b'hex> ')
                for càrrec_INDEX in range(0, len(시험), 64):
                    enviar(시험[càrrec_INDEX:càrrec_INDEX+64].hex(), b'hex> ')
                assert b'LOADED' in enviar('.')
                RESULTAT = enviar('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in RESULTAT, RESULTAT
                RESULTAT = enviar('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in RESULTAT and b'exit 0' in RESULTAT, RESULTAT
                informe_VALOR['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                selecció_VALOR.close()
                if Procés_VALOR.poll() is None:
                    Procés_VALOR.terminate()
                    try:
                        Procés_VALOR.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Procés_VALOR.kill()
                        Procés_VALOR.wait()
                (Sortida / 'guest.log').write_bytes(LOG_fila)
        informe_VALOR['passed'] = True
        print(json.dumps(informe_VALOR, ensure_ascii=False, indent=2))
    finally:
        (Sortida / 'report.json').write_text(json.dumps(informe_VALOR, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Executa_2()
