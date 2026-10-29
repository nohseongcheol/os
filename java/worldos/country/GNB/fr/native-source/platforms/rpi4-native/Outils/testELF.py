#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from exécuterCommande import racineProjet


def exempleLinux(donnéesRésultat):
    donnéesRésultat.mkdir(parents=True, exist_ok=True)
    for donnéesOriginal, nom in [('lancer.S', 'start.o'), ('Salutation.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(racineProjet/'Exemples/ABILinux'/donnéesOriginal), '-o', str(donnéesRésultat/nom)])
    imageCodeExécutable = donnéesRésultat/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(imageCodeExécutable), str(donnéesRésultat/'start.o'), str(donnéesRésultat/'hello.o')])
    valeurContenuValeur = imageCodeExécutable.read_bytes()
    assert len(valeurContenuValeur) <= 16384 and valeurContenuValeur[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', valeurContenuValeur, 16) == (2, 183) and b'JKOROS\0' not in valeurContenuValeur
    attendu = 'LINUX ARM64 ELF PASS\n한글인수\n'
    ligneRéférenceComparaison = subprocess.check_output(['qemu-aarch64', str(imageCodeExécutable), '한글인수'], cwd=str(donnéesRésultat)).decode()
    assert ligneRéférenceComparaison == attendu, ligneRéférenceComparaison
    (donnéesRésultat/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(imageCodeExécutable)]))
    return imageCodeExécutable, attendu


def lancer():
    donnéesRésultat = racineProjet/'build/verification/elf'
    donnéesRésultat.mkdir(parents=True, exist_ok=True)
    (donnéesRésultat/'report.json').write_text('{"passed": false}\n')
    imageCodeExécutable, attendu = exempleLinux(donnéesRésultat)
    résultat = subprocess.check_output(['python3', str(racineProjet/'Outils/exécuterFichier.py'), '--linux', str(imageCodeExécutable), '한글인수']).decode().replace('\r\n', '\n')
    assert attendu+'exit 0' in résultat, résultat
    (donnéesRésultat/'serial.log').write_text(résultat)
    original=imageCodeExécutable.read_bytes()
    décalageEntêteProgramme=struct.unpack_from('<Q',original,32)[0]
    for nom,valeurDécalage,définirFormat,valeur in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',décalageEntêteProgramme+4,'I',7),('kernel-address',décalageEntêteProgramme+16,'Q',0x400000)]:
        donnéesInvalide=bytearray(original);struct.pack_into('<'+définirFormat,donnéesInvalide,valeurDécalage,valeur)
        chemin=donnéesRésultat/nom;chemin.write_bytes(donnéesInvalide)
        résultatRejet=subprocess.run(['python3',str(racineProjet/'Outils/exécuterFichier.py'),'--linux',str(chemin)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert résultatRejet.returncode==1 and b'exit -8' in résultatRejet.stdout,(nom,résultatRejet.stdout)
    rapportValidation = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((racineProjet/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(imageCodeExécutable.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (donnéesRésultat/'report.json').write_text(json.dumps(rapportValidation, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': lancer()
