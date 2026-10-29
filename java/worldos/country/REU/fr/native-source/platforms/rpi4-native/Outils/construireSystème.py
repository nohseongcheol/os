#!/usr/bin/env python3
"""Hôte javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from construireEspaceUtilisateur import créerEspaceUtilisateur
from construireRéseau import créerRéseau
from construireRecueilExemples import créerRecueilExemples
from construireDistant import créerDistant

racineProjet = Path(__file__).resolve().parents[1]
racineDépôt = racineProjet.parents[1]
construireChemin = racineProjet / 'build'


def exécuterCommande(tableauArgument):
    subprocess.check_call([str(valeurPremier) for valeurPremier in tableauArgument], cwd=str(racineProjet))


def lancer():
    construireChemin.mkdir(exist_ok=True)
    CompilateurC = os.environ.get('ARM64_CC', 'clang')
    compilateurCpp = os.environ.get('ARM64_CXX', 'clang++')
    outilÉditeurLiens = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    convertisseurFichierObjet = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    outilArchive = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Outils in ('javac', CompilateurC, compilateurCpp, outilÉditeurLiens, convertisseurFichierObjet, outilArchive):
        if not shutil.which(Outils):
            raise SystemExit('필요한 construireSystème Outils méthodeManquant: ' + Outils)
    informationPolice = json.loads((racineProjet / 'vendor/terminal-font.json').read_text())
    donnéesPolice = (racineProjet / 'vendor/terminal-font.bin').read_bytes()
    if len(donnéesPolice) != 65616 * 32 or hashlib.sha256(donnéesPolice).hexdigest() != informationPolice['sha256']:
        raise SystemExit('terminal valeurPolice taille/SHA256 불일치')
    tableExporter = {'jshell_interactive': 'EntréeSortieInterpréteurCommandes.estInteractif', 'jshell_output': 'EntréeSortieInterpréteurCommandes.Sortie', 'jshell_input': 'EntréeSortieInterpréteurCommandes.valeurEntrée', 'java_task': 'Noyau.Tâche', 'jfs_path_start': 'FichiersMémoire.démarrerChemin',
               'jfs_path_byte': 'FichiersMémoire.octetChemin', 'jfs_open': 'FichiersMémoire.ouvrir',
               'jfs_read': 'FichiersMémoire.lire', 'jfs_write': 'FichiersMémoire.écrire',
               'jfs_seek': 'FichiersMémoire.positionnerPosition', 'jfs_close': 'FichiersMémoire.fermer',
               'jfs_size': 'FichiersMémoire.taille', 'jfs_unlink': 'FichiersMémoire.effacerEntréeÉlément',
               'jfs_truncate': 'FichiersMémoire.définirLongueur'}
    tableExporter.update({'jfs_entry_count': 'FichiersMémoire.limiteFichier', 'jfs_entry_length': 'FichiersMémoire.longueurNomExporté', 'jfs_entry_byte': 'FichiersMémoire.octetNomExporté', 'jfs_entry_size': 'FichiersMémoire.tailleFichierExporté'})
    tableExporter.update({'jdraw_prepare': 'ComposeurTamponImage.préparer', 'jdraw_width': 'ComposeurTamponImage.obtenirLargeur',
        'jdraw_height': 'ComposeurTamponImage.obtenirHauteur', 'jdraw_count_low': 'ComposeurTamponImage.obtenirBasCompteur',
        'jdraw_count_high': 'ComposeurTamponImage.obtenirHautCompteur', 'jdraw_clip': 'ComposeurTamponImage.rogner',
        'jdraw_clip_value': 'ComposeurTamponImage.valeurRogner', 'jdraw_begin': 'ComposeurTamponImage.lancer',
        'jdraw_end': 'ComposeurTamponImage.terminer', 'jdraw_pixel': 'ComposeurTamponImage.pixel',
        'jdraw_rectangle': 'ComposeurTamponImage.remplirRectangle', 'jdraw_pointer': 'ComposeurTamponImage.pointeur'})
    tableExporter.update({'jfs_mkdir': 'FichiersMémoire.créerRépertoire', 'jfs_rmdir': 'FichiersMémoire.supprimerRépertoire', 'jfs_kind': 'FichiersMémoire.genreEntréeÉlément'})
    tableExporter.update({'jnet_socket': 'RéseauBoucleRetour.créerEntréeÉlément', 'jnet_bind': 'RéseauBoucleRetour.EmballerExécutables',
        'jnet_put': 'RéseauBoucleRetour.placerDonnées', 'jnet_get': 'RéseauBoucleRetour.lireDonnées', 'jnet_send': 'RéseauBoucleRetour.envoyer',
        'jnet_recv': 'RéseauBoucleRetour.recevoir', 'jnet_port': 'RéseauBoucleRetour.lirePortExtrémité', 'jnet_address': 'RéseauBoucleRetour.lireAdresse',
        'jnet_peer': 'RéseauBoucleRetour.extrémitéÉmetteur', 'jnet_close': 'RéseauBoucleRetour.fermer'})
    tableExporter.update({'jstream_create': 'RéseauFlux.créerEntréeÉlément', 'jstream_bind': 'RéseauFlux.EmballerExécutables', 'jstream_listen': 'RéseauFlux.écouterExtrémité', 'jstream_connect': 'RéseauFlux.connecter', 'jstream_accept': 'RéseauFlux.accepterConnexion', 'jstream_read': 'RéseauFlux.lire', 'jstream_write': 'RéseauFlux.écrire', 'jstream_port': 'RéseauFlux.lirePortExtrémité', 'jstream_peer': 'RéseauFlux.lirePortPairRéseau', 'jstream_close': 'RéseauFlux.fermer'})
    for valeurSymbole in list(tableExporter):
        if valeurSymbole.startswith('jstream_') or valeurSymbole.startswith('jnet_') and valeurSymbole not in ('jnet_put', 'jnet_get'):
            tableExporter[valeurSymbole.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = tableExporter.pop(valeurSymbole)
    entréesListeExemple = ['public final class Paquet { public static void préparer() {']
    for chemin in sorted((racineProjet / 'Exemples').iterdir()):
        if chemin.is_file():
            entréesListeExemple.append('InterpréteurCommandes.fichierStatique(%s, %s);' %
                (json.dumps(chemin.name), json.dumps(chemin.read_text(encoding='utf-8'), ensure_ascii=True)))
    (construireChemin / 'Paquet.java').write_text('\n'.join(entréesListeExemple + ['}}']), encoding='utf-8')
    créerRecueilExemples(racineProjet, racineDépôt, exécuterCommande)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(construireChemin)) as cheminTravailEnCours:
        cheminClasse = Path(cheminTravailEnCours)
        exécuterCommande(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', cheminClasse, '-sourcepath', cheminClasse, '-d', cheminClasse] + sorted((racineProjet / 'source').glob('*.java')) + [construireChemin / 'Paquet.java', construireChemin / 'LotExemple.java'])
        # Fichier·interpréteurCommandes·fenêtre 세션·통신과 Java Écran 합성 배열을 construireTous 수용한다.
        tableauArgument = ['sh', racineDépôt / 'compiler/tempsDeAnticipé.sh', '--entry', 'Noyau.lancer', '--heap-words', '1048576', '-o', construireChemin / 'kernel-java.c']
        for valeurSymbole, entréeÉlémentMéthode in sorted(tableExporter.items()):
            tableauArgument += ['--export', valeurSymbole + '=' + entréeÉlémentMéthode]
        exécuterCommande(tableauArgument + sorted(cheminClasse.glob('*.class')))
    (construireChemin / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    bitsConfiguration = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    pOSIX = racineDépôt / 'posix-kor/arm64-native'
    créerEspaceUtilisateur(racineProjet, racineDépôt, CompilateurC, compilateurCpp, outilÉditeurLiens, outilArchive, bitsConfiguration, exécuterCommande)
    réseau = créerRéseau(racineProjet, CompilateurC, outilArchive, bitsConfiguration, exécuterCommande)
    utiliserDistant = créerDistant(racineProjet, CompilateurC, outilArchive, bitsConfiguration, exécuterCommande)
    inclusions = ['-I', pOSIX / 'Entêtes', '-I', construireChemin]
    construireTravaux = [(CompilateurC, [], construireChemin / 'terminal-font.S', 'font.o'),
            (CompilateurC, ['-std=c11', '-Wall', '-Wextra', '-Werror'], racineProjet / 'machine/terminal.c', 'terminal.o'),
            (CompilateurC, ['-std=c11', '-Wall', '-Wextra', '-Werror'], racineProjet / 'machine/ComposantVisuel.c', 'widgets.o'),
            (CompilateurC, ['-std=c11'], construireChemin / 'kernel-java.c', 'java.o'),
            (CompilateurC, ['-std=c11', '-Wall', '-Wextra', '-Werror'], racineProjet / 'machine/CarteMatérielle.c', 'board.o'),
            (CompilateurC, ['-std=c11', '-Wall', '-Wextra', '-Werror'], racineProjet / 'machine/dessinÉcran.c', 'drawing.o'),
            (CompilateurC, ['-std=c11', '-Wall', '-Wextra', '-Werror'], racineProjet / 'machine/Utilisateur.c', 'user.o'),
            (CompilateurC, [], racineProjet / 'Amorçage/valeurPointEntréeÉlément.S', 'entry.o'),
            (CompilateurC, ['-std=c11', '-Wall', '-Wextra', '-Werror'], pOSIX / 'connecter.c', 'posix.o'),
            (compilateurCpp, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], racineProjet / 'Tests/AppelsFichier.cpp', 'cpp.o')]
    for outilCompilateur, régionSupplémentaire, donnéesOriginal, sortie in construireTravaux:
        configurationOriginal = [entréeÉlémentFichier for entréeÉlémentFichier in bitsConfiguration if entréeÉlémentFichier != '-mgeneral-regs-only'] if donnéesOriginal.suffix == '.S' else bitsConfiguration
        exécuterCommande([outilCompilateur] + configurationOriginal + régionSupplémentaire + inclusions + ['-c', donnéesOriginal, '-o', construireChemin / sortie])
    exécuterCommande([outilArchive, 'rcs', construireChemin / 'libposix-kor-arm64.a', construireChemin / 'posix.o'])
    exécuterCommande([outilÉditeurLiens, '--gc-sections', '-T', racineProjet / 'Amorçage/DispositionLiens.ld', '-Map', construireChemin / 'kernel.map', '-o', construireChemin / 'kernel.elf'] +
        [construireChemin / nom for nom in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', construireChemin / 'libposix-kor-arm64.a', réseau, utiliserDistant, construireChemin / 'remote/libassh.a', construireChemin / 'remote/libbearssl.a', '--end-group'])
    exécuterCommande([convertisseurFichierObjet, '-O', 'binary', construireChemin / 'kernel.elf', construireChemin / 'kernel8.img'])
    manifesteLot = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'français.interne', 'korean_exceptions': 20,
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
                'vnc': {'implementation': 'guest RFB 3.8 / VNC authentication / raw incremental tiles', 'port': 5900, 'encrypted_pixels': False, 'clients': 1, 'korean_input': 'native two-set F9/Shift+espace'},
                'rdp': False,
                'gui': 'four native terminal windows and Swing subset peers; guest VNC server with native input; optional QEMU VNC bridge',
                'native_usb_input': False, 'full_swing': False, 'swing_subset': True, 'sha256': {}}
    for nom in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        manifesteLot['sha256'][nom] = hashlib.sha256((construireChemin / nom).read_bytes()).hexdigest()
    (construireChemin / 'build.json').write_text(json.dumps(manifesteLot, indent=2) + '\n')
    print('estTerminé:', construireChemin / 'kernel8.img')


if __name__ == '__main__':
    lancer()
