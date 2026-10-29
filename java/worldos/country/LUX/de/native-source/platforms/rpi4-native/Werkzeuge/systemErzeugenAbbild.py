#!/usr/bin/env python3
"""Wirtssystem javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from benutzerRaumErzeugenAbbild import benutzerRaumErstellen
from netzwerkErzeugenAbbild import netzwerkErstellen
from beispielsammlungErzeugenAbbild import beispielsammlungErstellen
from entferntErzeugenAbbild import entferntErstellen

projektWurzel = Path(__file__).resolve().parents[1]
ablageWurzel = projektWurzel.parents[1]
pfadErzeugenAbbild = projektWurzel / 'build'


def befehlAusführen(argumentDatenfeld):
    subprocess.check_call([str(ersterWert) for ersterWert in argumentDatenfeld], cwd=str(projektWurzel))


def ausführenVorgang():
    pfadErzeugenAbbild.mkdir(exist_ok=True)
    CÜbersetzer = os.environ.get('ARM64_CC', 'clang')
    cppÜbersetzer = os.environ.get('ARM64_CXX', 'clang++')
    binderWerkzeug = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    objektDateiUmwandler = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    archivWerkzeug = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Werkzeuge in ('javac', CÜbersetzer, cppÜbersetzer, binderWerkzeug, objektDateiUmwandler, archivWerkzeug):
        if not shutil.which(Werkzeuge):
            raise SystemExit('필요한 systemErzeugenAbbild Werkzeuge fehlendMethode: ' + Werkzeuge)
    schriftartInformation = json.loads((projektWurzel / 'vendor/terminal-font.json').read_text())
    schriftartDaten = (projektWurzel / 'vendor/terminal-font.bin').read_bytes()
    if len(schriftartDaten) != 65616 * 32 or hashlib.sha256(schriftartDaten).hexdigest() != schriftartInformation['sha256']:
        raise SystemExit('terminal schriftartWert größe/SHA256 불일치')
    exportierenTabelle = {'jshell_interactive': 'BefehlshülleEinAusgabe.istInteraktiv', 'jshell_output': 'BefehlshülleEinAusgabe.Ausgabe', 'jshell_input': 'BefehlshülleEinAusgabe.Eingabewert', 'java_task': 'Betriebskern.Aufgabe', 'jfs_path_start': 'SpeicherDateien.pfadStarten',
               'jfs_path_byte': 'SpeicherDateien.pfadByte', 'jfs_open': 'SpeicherDateien.öffnen',
               'jfs_read': 'SpeicherDateien.lesen', 'jfs_write': 'SpeicherDateien.schreiben',
               'jfs_seek': 'SpeicherDateien.positionPositionieren', 'jfs_close': 'SpeicherDateien.schließen',
               'jfs_size': 'SpeicherDateien.größe', 'jfs_unlink': 'SpeicherDateien.eintragTilgen',
               'jfs_truncate': 'SpeicherDateien.längeSetzen'}
    exportierenTabelle.update({'jfs_entry_count': 'SpeicherDateien.dateiGrenzwert', 'jfs_entry_length': 'SpeicherDateien.exportiertNameLänge', 'jfs_entry_byte': 'SpeicherDateien.exportiertNameByte', 'jfs_entry_size': 'SpeicherDateien.exportiertDateiGröße'})
    exportierenTabelle.update({'jdraw_prepare': 'BildpufferZusammensetzer.vorbereiten', 'jdraw_width': 'BildpufferZusammensetzer.breiteHolen',
        'jdraw_height': 'BildpufferZusammensetzer.höheHolen', 'jdraw_count_low': 'BildpufferZusammensetzer.zählerNiedrigHolen',
        'jdraw_count_high': 'BildpufferZusammensetzer.zählerHochHolen', 'jdraw_clip': 'BildpufferZusammensetzer.beschneiden',
        'jdraw_clip_value': 'BildpufferZusammensetzer.beschneidenWert', 'jdraw_begin': 'BildpufferZusammensetzer.ausführenVorgang',
        'jdraw_end': 'BildpufferZusammensetzer.beenden', 'jdraw_pixel': 'BildpufferZusammensetzer.bildpunkt',
        'jdraw_rectangle': 'BildpufferZusammensetzer.rechteckFüllen', 'jdraw_pointer': 'BildpufferZusammensetzer.zeiger'})
    exportierenTabelle.update({'jfs_mkdir': 'SpeicherDateien.verzeichnisErstellen', 'jfs_rmdir': 'SpeicherDateien.verzeichnisEntfernen', 'jfs_kind': 'SpeicherDateien.eintragArt'})
    exportierenTabelle.update({'jnet_socket': 'RückschleifeNetzwerk.eintragErstellen', 'jnet_bind': 'RückschleifeNetzwerk.AusführbündelPacken',
        'jnet_put': 'RückschleifeNetzwerk.datenAblegen', 'jnet_get': 'RückschleifeNetzwerk.datenLesen', 'jnet_send': 'RückschleifeNetzwerk.senden',
        'jnet_recv': 'RückschleifeNetzwerk.empfangen', 'jnet_port': 'RückschleifeNetzwerk.endpunktPortLesen', 'jnet_address': 'RückschleifeNetzwerk.adresseLesen',
        'jnet_peer': 'RückschleifeNetzwerk.absenderEndpunkt', 'jnet_close': 'RückschleifeNetzwerk.schließen'})
    exportierenTabelle.update({'jstream_create': 'DatenstromNetzwerk.eintragErstellen', 'jstream_bind': 'DatenstromNetzwerk.AusführbündelPacken', 'jstream_listen': 'DatenstromNetzwerk.endpunktLauschen', 'jstream_connect': 'DatenstromNetzwerk.verbinden', 'jstream_accept': 'DatenstromNetzwerk.verbindungAnnehmen', 'jstream_read': 'DatenstromNetzwerk.lesen', 'jstream_write': 'DatenstromNetzwerk.schreiben', 'jstream_port': 'DatenstromNetzwerk.endpunktPortLesen', 'jstream_peer': 'DatenstromNetzwerk.gegenstellePortLesen', 'jstream_close': 'DatenstromNetzwerk.schließen'})
    for symbolWert in list(exportierenTabelle):
        if symbolWert.startswith('jstream_') or symbolWert.startswith('jnet_') and symbolWert not in ('jnet_put', 'jnet_get'):
            exportierenTabelle[symbolWert.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = exportierenTabelle.pop(symbolWert)
    beispielEinträge = ['public final class Paket { public static void vorbereiten() {']
    for pfad in sorted((projektWurzel / 'Beispiele').iterdir()):
        if pfad.is_file():
            beispielEinträge.append('Befehlsinterpreter.statischDatei(%s, %s);' %
                (json.dumps(pfad.name), json.dumps(pfad.read_text(encoding='utf-8'), ensure_ascii=True)))
    (pfadErzeugenAbbild / 'Paket.java').write_text('\n'.join(beispielEinträge + ['}}']), encoding='utf-8')
    beispielsammlungErstellen(projektWurzel, ablageWurzel, befehlAusführen)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(pfadErzeugenAbbild)) as arbeitendPfad:
        klassePfad = Path(arbeitendPfad)
        befehlAusführen(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', klassePfad, '-sourcepath', klassePfad, '-d', klassePfad] + sorted((projektWurzel / 'Quelltext').glob('*.java')) + [pfadErzeugenAbbild / 'Paket.java', pfadErzeugenAbbild / 'BeispielBündel.java'])
        # Datei·befehlshülle·fenster 세션·통신과 Java Bildschirm 합성 배열을 alleErzeugenAbbild 수용한다.
        argumentDatenfeld = ['sh', ablageWurzel / 'compiler/vorabVonElementZeit.sh', '--entry', 'Betriebskern.ausführenVorgang', '--heap-words', '1048576', '-o', pfadErzeugenAbbild / 'kernel-java.c']
        for symbolWert, methodeEintrag in sorted(exportierenTabelle.items()):
            argumentDatenfeld += ['--export', symbolWert + '=' + methodeEintrag]
        befehlAusführen(argumentDatenfeld + sorted(klassePfad.glob('*.class')))
    (pfadErzeugenAbbild / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    konfigurationBitliste = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    pOSIX = ablageWurzel / 'posix-kor/arm64-native'
    benutzerRaumErstellen(projektWurzel, ablageWurzel, CÜbersetzer, cppÜbersetzer, binderWerkzeug, archivWerkzeug, konfigurationBitliste, befehlAusführen)
    netzwerk = netzwerkErstellen(projektWurzel, CÜbersetzer, archivWerkzeug, konfigurationBitliste, befehlAusführen)
    entferntBenutzen = entferntErstellen(projektWurzel, CÜbersetzer, archivWerkzeug, konfigurationBitliste, befehlAusführen)
    einschlüsse = ['-I', pOSIX / 'Kopfdateien', '-I', pfadErzeugenAbbild]
    aufträgeErzeugenAbbild = [(CÜbersetzer, [], pfadErzeugenAbbild / 'terminal-font.S', 'font.o'),
            (CÜbersetzer, ['-std=c11', '-Wall', '-Wextra', '-Werror'], projektWurzel / 'maschine/terminal.c', 'terminal.o'),
            (CÜbersetzer, ['-std=c11', '-Wall', '-Wextra', '-Werror'], projektWurzel / 'maschine/Bedienelement.c', 'widgets.o'),
            (CÜbersetzer, ['-std=c11'], pfadErzeugenAbbild / 'kernel-java.c', 'java.o'),
            (CÜbersetzer, ['-std=c11', '-Wall', '-Wextra', '-Werror'], projektWurzel / 'maschine/Platine.c', 'board.o'),
            (CÜbersetzer, ['-std=c11', '-Wall', '-Wextra', '-Werror'], projektWurzel / 'maschine/bildschirmZeichnung.c', 'drawing.o'),
            (CÜbersetzer, ['-std=c11', '-Wall', '-Wextra', '-Werror'], projektWurzel / 'maschine/Benutzer.c', 'user.o'),
            (CÜbersetzer, [], projektWurzel / 'Startvorgang/eintragPunktWert.S', 'entry.o'),
            (CÜbersetzer, ['-std=c11', '-Wall', '-Wextra', '-Werror'], pOSIX / 'verbinden.c', 'posix.o'),
            (cppÜbersetzer, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], projektWurzel / 'Prüfungen/DateiAufrufliste.cpp', 'cpp.o')]
    for übersetzerWerkzeug, zusätzlichGebiet, ursprünglichDaten, ausgabe in aufträgeErzeugenAbbild:
        ursprünglichKonfiguration = [dateiEintrag for dateiEintrag in konfigurationBitliste if dateiEintrag != '-mgeneral-regs-only'] if ursprünglichDaten.suffix == '.S' else konfigurationBitliste
        befehlAusführen([übersetzerWerkzeug] + ursprünglichKonfiguration + zusätzlichGebiet + einschlüsse + ['-c', ursprünglichDaten, '-o', pfadErzeugenAbbild / ausgabe])
    befehlAusführen([archivWerkzeug, 'rcs', pfadErzeugenAbbild / 'libposix-kor-arm64.a', pfadErzeugenAbbild / 'posix.o'])
    befehlAusführen([binderWerkzeug, '--gc-sections', '-T', projektWurzel / 'Startvorgang/Bindungsanordnung.ld', '-Map', pfadErzeugenAbbild / 'kernel.map', '-o', pfadErzeugenAbbild / 'kernel.elf'] +
        [pfadErzeugenAbbild / Name for Name in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', pfadErzeugenAbbild / 'libposix-kor-arm64.a', netzwerk, entferntBenutzen, pfadErzeugenAbbild / 'remote/libassh.a', pfadErzeugenAbbild / 'remote/libbearssl.a', '--end-group'])
    befehlAusführen([objektDateiUmwandler, '-O', 'binary', pfadErzeugenAbbild / 'kernel.elf', pfadErzeugenAbbild / 'kernel8.img'])
    bündelInhaltsverzeichnis = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Deutsch.eigen', 'korean_exceptions': 20,
                                 'full_awt_swing': False, 'swing_subset': ['JFrame','JPanel','JLabel','JButton','JTextField','ActionListener','SwingUtilities.invokeLater'], 'java_se_certified': False},
                'python': 'MicroPython 1.24.1 integer build', 'cpython': False,
                'pip': {'kind': 'source installer with host PyPI HTTPS relay', 'commands': ['install','list','uninstall'], 'cpython_pip': False, 'dependencies': False, 'persistent': False},
                'korean_c_api': 'independent structs, enum constants and real function symbols',
                'framebuffer': {'format': 'RGB32', 'default': [640,480], 'maximum': [1920,1080], 'boot_configurable': True, 'size_syscall': 22},
                'shell': 'UTF-8 editor/history, directories, variables, scripts, sequential pipes, redirects, ELF execution',
                'system_commands': ['ipconfig','ip','ifconfig','ping','route','netstat','ss','ps','top','free','df','uptime','poweroff'],
                'system_status': 'real lwIP interface/endpoints, native task/session PIDs, AOT heap pools, RAM filesystem slots',
                'ip_configuration': 'GENET DHCP on real Pi4; static IPv4/netmask/gateway; volatile; close active sockets before address changes',
                'ping': 'real ICMPv4 echo, numeric addresses, count/timeout/RTT; no DNS resolver',
                'poweroff': 'BCM2835 PM firmware-halt watchdog; QEMU guest shutdown; physical Pi untested',
                'pipe_capacity_bytes': 16384, 'posix_shell_complete': False,
                'ram_files': {'count': 64, 'bytes_each': 16384, 'directories': 16, 'persistent': False},
                'user_abi': 1, 'user_elf64': True, 'elf_extension_required': False,
                'linux_static_elf_subset': True, 'full_linux_binary_compatibility': False,
                'mmu': True, 'user_timeout_seconds': 2, 'cooperative_user_sessions': 4,
                'interactive_wait_renews_deadline': True, 'vi': 'native EL0 UTF-8 vi subset',
                'network': 'lwIP 2.2.0 IPv4 TCP/UDP/ARP/ICMP; GENET v5 Ethernet or UART1 SLIP', 'external_network': True,
                'external_network_transport': 'Pi4 GENET (hardware untested); QEMU auxiliary UART SLIP bridge',
                'ftp': 'guest service, passive binary transfers, anonymous root RAM workspace',
                'genet_ethernet': True, 'genet_driver_status': 'implemented; MMIO/MDIO model tests only', 'physical_network_tested': False,
                'ssh': {'implementation': 'guest libassh 1.1 / LGPL-2.1-or-later', 'port': 22, 'password_auth': True, 'console': 'shared kernel shell', 'independent_sessions': False, 'sftp': False, 'port_forwarding': False},
                'vnc': {'implementation': 'guest RFB 3.8 / VNC authentication / raw incremental tiles', 'port': 5900, 'encrypted_pixels': False, 'clients': 1, 'korean_input': 'native two-set F9/Shift+Space'},
                'rdp': False,
                'gui': 'four native terminal windows and Swing subset peers; guest VNC server with native input; optional QEMU VNC bridge',
                'native_usb_input': False, 'full_swing': False, 'swing_subset': True, 'sha256': {}}
    for Name in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        bündelInhaltsverzeichnis['sha256'][Name] = hashlib.sha256((pfadErzeugenAbbild / Name).read_bytes()).hexdigest()
    (pfadErzeugenAbbild / 'build.json').write_text(json.dumps(bündelInhaltsverzeichnis, indent=2) + '\n')
    print('istFertig:', pfadErzeugenAbbild / 'kernel8.img')


if __name__ == '__main__':
    ausführenVorgang()
