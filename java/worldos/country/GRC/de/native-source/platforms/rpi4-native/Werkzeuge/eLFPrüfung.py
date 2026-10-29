#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from befehlAusführen import projektWurzel


def linuxBeispiel(ergebnisDaten):
    ergebnisDaten.mkdir(parents=True, exist_ok=True)
    for ursprünglichDaten, Name in [('ausführenVorgang.S', 'start.o'), ('Gruß.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(projektWurzel/'Beispiele/LinuxABI'/ursprünglichDaten), '-o', str(ergebnisDaten/Name)])
    ausführdateiAbbild = ergebnisDaten/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(ausführdateiAbbild), str(ergebnisDaten/'start.o'), str(ergebnisDaten/'hello.o')])
    inhaltswertWert = ausführdateiAbbild.read_bytes()
    assert len(inhaltswertWert) <= 16384 and inhaltswertWert[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', inhaltswertWert, 16) == (2, 183) and b'JKOROS\0' not in inhaltswertWert
    erwartet = 'LINUX ARM64 ELF PASS\n한글인수\n'
    vergleichGrundlinie = subprocess.check_output(['qemu-aarch64', str(ausführdateiAbbild), '한글인수'], cwd=str(ergebnisDaten)).decode()
    assert vergleichGrundlinie == erwartet, vergleichGrundlinie
    (ergebnisDaten/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(ausführdateiAbbild)]))
    return ausführdateiAbbild, erwartet


def ausführenVorgang():
    ergebnisDaten = projektWurzel/'build/verification/elf'
    ergebnisDaten.mkdir(parents=True, exist_ok=True)
    (ergebnisDaten/'report.json').write_text('{"passed": false}\n')
    ausführdateiAbbild, erwartet = linuxBeispiel(ergebnisDaten)
    ergebnis = subprocess.check_output(['python3', str(projektWurzel/'Werkzeuge/dateiAusführen.py'), '--linux', str(ausführdateiAbbild), '한글인수']).decode().replace('\r\n', '\n')
    assert erwartet+'exit 0' in ergebnis, ergebnis
    (ergebnisDaten/'serial.log').write_text(ergebnis)
    ursprünglich=ausführdateiAbbild.read_bytes()
    programmKopfVersatzwert=struct.unpack_from('<Q',ursprünglich,32)[0]
    for Name,versatzwertWert,formatFestlegen,Wert in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',programmKopfVersatzwert+4,'I',7),('kernel-address',programmKopfVersatzwert+16,'Q',0x400000)]:
        ungültigDaten=bytearray(ursprünglich);struct.pack_into('<'+formatFestlegen,ungültigDaten,versatzwertWert,Wert)
        pfad=ergebnisDaten/Name;pfad.write_bytes(ungültigDaten)
        zurückweisungErgebnis=subprocess.run(['python3',str(projektWurzel/'Werkzeuge/dateiAusführen.py'),'--linux',str(pfad)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert zurückweisungErgebnis.returncode==1 and b'exit -8' in zurückweisungErgebnis.stdout,(Name,zurückweisungErgebnis.stdout)
    validierungBericht = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((projektWurzel/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(ausführdateiAbbild.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (ergebnisDaten/'report.json').write_text(json.dumps(validierungBericht, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': ausführenVorgang()
