#!/usr/bin/env python3
"""verteilungWert 묶음에서 libassh/TinyCC를 교체하고 eigen 커널을 erneutVersuchenWert 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

projektWurzel = Path(__file__).resolve().parent


def befehlAusführen(maschinenwortText):
    subprocess.check_call([str(eintragWert) for eintragWert in maschinenwortText], cwd=str(projektWurzel))


def ausführenVorgang():
    Strukturanalysierer = argparse.ArgumentParser(description=__doc__)
    Strukturanalysierer.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 überprüfen')
    Strukturanalysierer.add_argument('--libassh-archive', type=Path, help='별도로 wertVerändern·컴파일한 libassh.a benutzenWert')
    Strukturanalysierer.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 erneutVersuchenWert 컴파일하고 커널에 탑재')
    Strukturanalysierer.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    argumente = Strukturanalysierer.parse_args()
    vorgabe = json.loads((projektWurzel / 'relink.json').read_text())
    systemErzeugenAbbild = projektWurzel / 'build'
    neuBündel = systemErzeugenAbbild / 'relinked'
    neuBündel.mkdir(exist_ok=True)
    übersetzerWerkzeug = os.environ.get('ARM64_CC', 'clang')
    verbinder = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    archivWerkzeug = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    entferntEinstellungen = json.loads((systemErzeugenAbbild / 'remote/libassh-build.json').read_text())
    einstellungen = entferntEinstellungen['flags']
    if argumente.libassh_archive:
        sicherheitBündel = argumente.libassh_archive.resolve()
    else:
        zielstellen = []
        Kopfdateien = ['-I', projektWurzel / 'entferntWert', '-I', projektWurzel / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Name in entferntEinstellungen['sources']:
            zielWert = neuBündel / (Path(Name).stem + '.o')
            befehlAusführen([übersetzerWerkzeug] + einstellungen + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + Kopfdateien +
                 ['-c', projektWurzel / Name, '-o', zielWert])
            zielstellen.append(zielWert)
        sicherheitBündel = neuBündel / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(neuBündel)) as vorläufigWert:
            vorläufigBündel = Path(vorläufigWert) / 'libassh.a'
            befehlAusführen([archivWerkzeug, 'rcs', vorläufigBündel] + zielstellen)
            vorläufigBündel.replace(sicherheitBündel)
    if argumente.tinycc:
        if not argumente.sdk:
            Strukturanalysierer.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        entwicklung = argumente.sdk.resolve()
        arithmetikWert = sorted((entwicklung / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not arithmetikWert or not (entwicklung / 'usr/include/stdio.h').is_file():
            Strukturanalysierer.error('SDK must contain ARM64 musl headers and libgcc.a')
        eingeschaltetKonfigurieren = [auswahlWert for auswahlWert in einstellungen if auswahlWert != '-mgeneral-regs-only']
        zielWert = neuBündel / 'übersetzerWerkzeug.o'
        befehlAusführen([übersetzerWerkzeug] + eingeschaltetKonfigurieren + ['-ffunction-sections', '-fdata-sections',
             '-I', projektWurzel / 'CÜbersetzer', '-I', projektWurzel / 'vendor/tinycc', '-I', projektWurzel / 'Benutzer',
             '-I', systemErzeugenAbbild / 'ccompiler', '-isystem', entwicklung / 'usr/include', '-c', projektWurzel / 'CÜbersetzer/übersetzerWerkzeug.c', '-o', zielWert])
        befehlAusführen([verbinder, '--gc-sections', '-T', projektWurzel / 'Benutzer/Bindungsanordnung.ld', '-z', 'max-page-size=4096',
             '-o', systemErzeugenAbbild / 'user/cc.elf', systemErzeugenAbbild / 'user/start.o', systemErzeugenAbbild / 'user/runtime.o', zielWert] +
             [systemErzeugenAbbild / 'ccompiler' / (Name + '.o') for Name in ('LaufzeitUnterstützung', 'ausführenVorgang', 'vorabVonElementZeit', 'zurückkehrenBrücke')] +
             [systemErzeugenAbbild / 'user' / (Name + '.o') for Name in ('jar', 'tinflate', 'crc32', 'adler32')] + [arithmetikWert[-1]])
        kopfWert = systemErzeugenAbbild / 'programs.h'
        kopfWert.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda istGleich: istGleich.group(1) + str((systemErzeugenAbbild / 'user/cc.elf').stat().st_size), kopfWert.read_text()))
        befehlAusführen([übersetzerWerkzeug] + einstellungen + ['-c', systemErzeugenAbbild / 'programs.S', '-o', projektWurzel / 'objects/programs.o'])
        befehlAusführen([übersetzerWerkzeug] + einstellungen + ['-std=c11', '-I', projektWurzel / 'posix-kor/arm64-native/Kopfdateien', '-I', systemErzeugenAbbild,
             '-c', projektWurzel / 'maschine/Benutzer.c', '-o', projektWurzel / 'objects/user.o'])
    befehlAusführen([verbinder, '--gc-sections', '-T', projektWurzel / 'Startvorgang/Bindungsanordnung.ld', '-o', neuBündel / 'kernel.elf'] +
         [projektWurzel / pfad for pfad in vorgabe['objects']] + ['--start-group'] +
         [sicherheitBündel if pfad == 'objects/libassh.a' else projektWurzel / pfad for pfad in vorgabe['libraries']] + ['--end-group'])
    befehlAusführen([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', neuBündel / 'kernel.elf', neuBündel / 'kernel8.img'])
    prüfsummeDatei = hashlib.sha256((neuBündel / 'kernel8.img').read_bytes()).hexdigest()
    if argumente.verify and prüfsummeDatei != vorgabe['kernel_sha256']:
        raise SystemExit('neuverbindenEndpunkt 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + prüfsummeDatei)
    print('RELINK PASS', prüfsummeDatei, neuBündel / 'kernel8.img')


if __name__ == '__main__':
    ausführenVorgang()
