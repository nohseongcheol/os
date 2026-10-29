#!/usr/bin/env python3
"""distribuzione_VALORE 묶음에서 libassh/TinyCC를 교체하고 nativo 커널을 retry_VALORE 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

azione_radice = Path(__file__).resolve().parent


def Esegui_comando(Word_SMS):
    subprocess.check_call([str(voce_VALORE) for voce_VALORE in Word_SMS], cwd=str(azione_radice))


def avvia():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 verificare')
    parser_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a usare_VALORE')
    parser_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 retry_VALORE 컴파일하고 커널에 탑재')
    parser_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    argomenti = parser_48ee4b1b.parse_args()
    specifica = json.loads((azione_radice / 'relink.json').read_text())
    costruire = azione_radice / 'build'
    새묶음 = costruire / 'relinked'
    새묶음.mkdir(exist_ok=True)
    compilatore_strumento = os.environ.get('ARM64_CC', 'clang')
    Connettore = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Archivio_strumento = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    remoto_Impostazioni = json.loads((costruire / 'remote/libassh-build.json').read_text())
    Impostazioni = remoto_Impostazioni['flags']
    if argomenti.libassh_archive:
        Sicurezza_aggregare = argomenti.libassh_archive.resolve()
    else:
        목적들 = []
        dichiarazioni = ['-I', azione_radice / 'remoto_VALORE', '-I', azione_radice / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Nome in remoto_Impostazioni['sources']:
            meta_VALORE = 새묶음 / (Path(Nome).stem + '.o')
            Esegui_comando([compilatore_strumento] + Impostazioni + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + dichiarazioni +
                 ['-c', azione_radice / Nome, '-o', meta_VALORE])
            목적들.append(meta_VALORE)
        Sicurezza_aggregare = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Esegui_comando([Archivio_strumento, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Sicurezza_aggregare)
    if argomenti.tinycc:
        if not argomenti.sdk:
            parser_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        sviluppo = argomenti.sdk.resolve()
        aritmetico_VALORE = sorted((sviluppo / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not aritmetico_VALORE or not (sviluppo / 'usr/include/stdio.h').is_file():
            parser_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [selezione_VALORE for selezione_VALORE in Impostazioni if selezione_VALORE != '-mgeneral-regs-only']
        meta_VALORE = 새묶음 / 'compilatore_strumento.o'
        Esegui_comando([compilatore_strumento] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', azione_radice / 'C_compilatore', '-I', azione_radice / 'vendor/tinycc', '-I', azione_radice / 'spazio_utente',
             '-I', costruire / 'ccompiler', '-isystem', sviluppo / 'usr/include', '-c', azione_radice / 'C_compilatore/compilatore_strumento.c', '-o', meta_VALORE])
        Esegui_comando([Connettore, '--gc-sections', '-T', azione_radice / 'spazio_utente/disposizione_di_collegamento.ld', '-z', 'max-page-size=4096',
             '-o', costruire / 'user/cc.elf', costruire / 'user/start.o', costruire / 'user/runtime.o', meta_VALORE] +
             [costruire / 'ccompiler' / (Nome + '.o') for Nome in ('CLR_Supporto', 'avvia', '미리번역', 'Reso_bridge')] +
             [costruire / 'user' / (Nome + '.o') for Nome in ('jar', 'tinflate', 'crc32', 'adler32')] + [aritmetico_VALORE[-1]])
        intestazione_VALORE = costruire / 'programs.h'
        intestazione_VALORE.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((costruire / 'user/cc.elf').stat().st_size), intestazione_VALORE.read_text()))
        Esegui_comando([compilatore_strumento] + Impostazioni + ['-c', costruire / 'programs.S', '-o', azione_radice / 'objects/programs.o'])
        Esegui_comando([compilatore_strumento] + Impostazioni + ['-std=c11', '-I', azione_radice / 'posix-kor/arm64-native/dichiarazioni', '-I', costruire,
             '-c', azione_radice / 'computer/spazio_utente.c', '-o', azione_radice / 'objects/user.o'])
    Esegui_comando([Connettore, '--gc-sections', '-T', azione_radice / 'avvio_macchina/disposizione_di_collegamento.ld', '-o', 새묶음 / 'kernel.elf'] +
         [azione_radice / percorso for percorso in specifica['objects']] + ['--start-group'] +
         [Sicurezza_aggregare if percorso == 'objects/libassh.a' else azione_radice / percorso for percorso in specifica['libraries']] + ['--end-group'])
    Esegui_comando([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hash_File = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if argomenti.verify and hash_File != specifica['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hash_File)
    print('RELINK PASS', hash_File, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    avvia()
