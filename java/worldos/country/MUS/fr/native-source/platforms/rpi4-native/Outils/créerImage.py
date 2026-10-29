#!/usr/bin/env python3
"""SD용 MBR/FAT32 이미지만 생성한다. 물리 디스크는 열지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import tarfile
import tempfile
from exécuterCommande import racineProjet
from DistributionCOSL import EmballerExécutables


def calculerHachage(chemin):
    valeur = hashlib.sha256()
    with chemin.open('rb') as entréeÉlémentFichier:
        for blocDonnées in iter(lambda: entréeÉlémentFichier.read(1024 * 1024), b''): valeur.update(blocDonnées)
    return valeur.hexdigest()


def lancer():
    Analyseur = argparse.ArgumentParser(description=__doc__)
    Analyseur.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD Amorçage HDMI/프레임버퍼 taille')
    valeurRésolution = Analyseur.parse_args().resolution
    valeurLargeur, valeurHauteur = map(int, valeurRésolution.split('x'))
    groupeÉcran, modeÉcran = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[valeurRésolution]
    valeurMicrologiciel = racineProjet / 'vendor/pi4-firmware.tar.gz'
    attendu = valeurMicrologiciel.with_name(valeurMicrologiciel.name + '.sha256')
    licence = racineProjet / 'vendor/LICENCE.broadcom'
    if not valeurMicrologiciel.is_file() or not attendu.is_file():
        raise SystemExit('공식 Pi Amorçage 펌웨어 valeurGroupe valeurNécessaire: ' + str(valeurMicrologiciel))
    if calculerHachage(valeurMicrologiciel) != attendu.read_text().split()[0]:
        raise SystemExit('펌웨어 valeurGroupe SHA256 불일치')
    if not licence.is_file():
        raise SystemExit('Amorçage 펌웨어 라이선스 Fichier méthodeManquant: ' + str(licence))
    cheminDistribution = racineProjet / 'dist'
    cheminDistribution.mkdir(exist_ok=True)
    lotRelierDeNouveau = EmballerExécutables()
    capacitéTotal, lancer = 128 * 1024 * 1024, 2048
    nombreÉlémentsSecteur = capacitéTotal // 512 - lancer
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(racineProjet / 'build')) as cheminTravailEnCours:
        valeurÉtapePhase = Path(cheminTravailEnCours)
        cheminAmorçage = valeurÉtapePhase / 'boot'
        (cheminAmorçage / 'overlays').mkdir(parents=True)
        listeFichier = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(valeurMicrologiciel)) as archive:
            for nom in listeFichier:
                membre = archive.getmember('./' + nom)
                if not membre.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + nom)
                with archive.extractfile(membre) as adresseOriginal, (cheminAmorçage / nom).open('wb') as positionValeurDestination:
                    shutil.copyfileobj(adresseOriginal, positionValeurDestination)
        shutil.copyfile(str(racineProjet / 'build/kernel8.img'), str(cheminAmorçage / 'kernel8.img'))
        réglages = (racineProjet / 'Amorçage/config.txt').read_text()
        réglages = réglages.replace('hdmi_group=2', 'hdmi_group=' + str(groupeÉcran)).replace('hdmi_mode=4', 'hdmi_mode=' + str(modeÉcran))
        réglages = réglages.replace('framebuffer_width=640', 'framebuffer_width=' + str(valeurLargeur)).replace('framebuffer_height=480', 'framebuffer_height=' + str(valeurHauteur))
        (cheminAmorçage / 'config.txt').write_text(réglages)
        shutil.copyfile(str(licence), str(cheminAmorçage / 'LICENCE.broadcom'))
        shutil.copyfile(str(racineProjet / 'vendor/LICENSE.micropython'), str(cheminAmorçage / 'LICENSE.micropython'))
        for nom in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(racineProjet.parents[1] / nom), str(cheminAmorçage / nom))
        shutil.copyfile(str(lotRelierDeNouveau), str(cheminAmorçage / lotRelierDeNouveau.name))
        for donnéesOriginal, nom in ((racineProjet/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (racineProjet/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (racineProjet/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (racineProjet/'vendor/LICENSE.genet','LICENSE.genet'),
                             (racineProjet/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (racineProjet/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (racineProjet/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (racineProjet/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(donnéesOriginal), str(cheminAmorçage/nom))
        for nom in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(racineProjet / 'vendor' / nom), str(cheminAmorçage / nom))
        (cheminAmorçage / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 Outils/exécuterCommande.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 Outils/exécuterCommande.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+espace / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/Guide.md.\n')
        fichierPartition = valeurÉtapePhase / 'boot.fat'
        with fichierPartition.open('wb') as entréeÉlémentFichier: entréeÉlémentFichier.truncate(nombreÉlémentsSecteur * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(lancer), '-n', 'JKJAVA', str(fichierPartition)])
        subprocess.check_call(['mcopy', '-i', str(fichierPartition), '-s'] + [str(positionDonnées) for positionDonnées in sorted(cheminAmorçage.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 construireSystème 결과와 égal 확인한다.
        extrait = valeurÉtapePhase / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(fichierPartition), '::/kernel8.img', str(extrait)])
        if calculerHachage(extrait) != calculerHachage(racineProjet / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 valeurNoyau SHA256 불일치')
        image = valeurÉtapePhase / 'jkoros-native-rpi4.img'
        EnregistrementAmorçageMaître = bytearray(512)
        EnregistrementAmorçageMaître[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', lancer, nombreÉlémentsSecteur)
        EnregistrementAmorçageMaître[510:512] = b'\x55\xaa'
        with image.open('wb') as donnéesRésultat:
            donnéesRésultat.truncate(capacitéTotal); donnéesRésultat.write(EnregistrementAmorçageMaître); donnéesRésultat.seek(lancer * 512)
            with fichierPartition.open('rb') as adresseOriginal: shutil.copyfileobj(adresseOriginal, donnéesRésultat)
        manifesteLot = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
                    'license': 'COSL with third-party/LGPL carve-outs',
                    'relink_archive': lotRelierDeNouveau.name, 'relink_sha256': calculerHachage(lotRelierDeNouveau),
                    'user_abi': 1, 'elf_extension_required': False, 'linux_static_elf_subset': True,
                    'full_linux_binary_compatibility': False,
                    'openjdk': False, 'guest_java': 'jkoros JVM 0.4 subset/JAR with Korean library and native Swing subset',
                    'guest_c_compiler': 'TinyCC ARM64, own ABI', 'guest_aot': 'static Java int/reference subset to native ARM64 ELF',
                    'all_class_or_jar_compatible': False,
                    'python': 'MicroPython 1.24.1 integer build', 'cpython': False,
                    'network': 'lwIP IPv4 TCP/UDP/ARP/ICMP; GENET v5 DHCP or QEMU UART1 SLIP', 'ftp': 'guest anonymous passive RAM service',
                    'genet_ethernet': True, 'physical_network_tested': False,
                    'ssh': 'native libassh server :22, shared console', 'vnc': 'native authenticated RFB 3.8 :5900', 'rdp': False,
                    'gui': 'four resizable terminal windows and native Swing subset peers',
                    'terminal_resize': 'hover corner; hold left mouse button and drag; live shell/vi grid',
                    'java_gui_example': '/example/java/ExempleFenêtre.java; run: java ExempleFenêtre',
                    'framebuffer_resolution': [valeurLargeur, valeurHauteur], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+espace / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': valeurMicrologiciel.name, 'source_sha256': calculerHachage(valeurMicrologiciel),
                    'image_sha256': calculerHachage(image), 'boot_files': {}}
        for positionDonnées in sorted(cheminAmorçage.rglob('*')):
            if positionDonnées.is_file(): manifesteLot['boot_files'][str(positionDonnées.relative_to(cheminAmorçage))] = calculerHachage(positionDonnées)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux construireImage/Utilisateur 디스크는 건드리지 않는다.
        os.replace(str(image), str(cheminDistribution / image.name))
        baseArchive = valeurÉtapePhase / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(baseArchive), 'zip', str(cheminAmorçage))
        os.replace(str(baseArchive) + '.zip', str(cheminDistribution / 'jkoros-native-rpi4-boot.zip'))
        (cheminDistribution / 'manifest.json').write_text(json.dumps(manifesteLot, indent=2) + '\n')
    print('générer:', cheminDistribution / 'jkoros-native-rpi4.img')
    print('donnéesEffectif Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    lancer()
