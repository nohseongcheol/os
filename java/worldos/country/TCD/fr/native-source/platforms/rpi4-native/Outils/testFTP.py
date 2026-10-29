#!/usr/bin/env python3
"""Real host TCP client -> SLIP -> bare-metal lwIP -> FTP -> Java VFS."""
import ftplib
import hashlib
import io
import json
import selectors
import socket
import subprocess
import time
import zipfile
from pontRéseau import pontRéseau
from exécuterCommande import racineProjet, commande
from DispositifTestRépercuter import DispositifTestRépercuter
from testELF import exempleLinux


def lancer():
    donnéesRésultat = racineProjet / 'build/verification/ftp'; donnéesRésultat.mkdir(parents=True, exist_ok=True)
    rapportValidation = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((racineProjet / 'build/kernel8.img').read_bytes()).hexdigest()}
    transcription = bytearray()
    sourceJava = donnéesRésultat / 'testLot.java'
    sourceJava.write_text('public class testLot { public static void main(String[] arguments) throws Exception { français.interne.Sortie.écrireLigne("JAR exécuterCommande: " + arguments[0]); français.interne.Fichier.écrire("jar.txt", "interne valeurNoyau Fichier"); français.interne.Sortie.écrireLigne(français.interne.Fichier.lire("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(racineProjet/'build/java-library/classes'), '-d', str(donnéesRésultat), str(sourceJava)])
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as lotJava:
        lotJava.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: testLot\r\n\r\n')
        lotJava.write(str(donnéesRésultat/'testLot.class'), 'testLot.class')
    with socket.socket() as temporaire:
        temporaire.bind(('127.0.0.1', 0)); numéroPort = temporaire.getsockname()[1]
    with socket.socket() as temporaire:
        temporaire.bind(('127.0.0.1', 0)); portFluxServeur = temporaire.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as temporaire:
        temporaire.bind(('127.0.0.1', 0)); portDatagrammeServeur = temporaire.getsockname()[1]
    with pontRéseau(numéroPort, ['tcp:{}:9300'.format(portFluxServeur), 'udp:{}:9301'.format(portDatagrammeServeur)], capturer=True) as pont:
        processus = subprocess.Popen(commande() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + pont.argumentTransféré(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        sélecteur = selectors.DefaultSelector(); sélecteur.register(processus.stdout, selectors.EVENT_READ)
        def recevoirMessage(marqueur=b'jkoros-native> ', délaiExpirationExécution=60):
            Données = bytearray(); décalageFin = time.monotonic() + délaiExpirationExécution
            while marqueur not in Données:
                if time.monotonic() > décalageFin or processus.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + Données.decode('utf-8', 'replace'))
                for valeurEnfoncé, _ in sélecteur.select(.1):
                    valeurFragment = valeurEnfoncé.fileobj.read(4096)
                    if valeurFragment: Données.extend(valeurFragment); transcription.extend(valeurFragment)
                if b'PANIC:' in Données or b'FAIL ' in Données: raise AssertionError(Données)
            return Données.decode('utf-8', 'replace').replace('\r\n', '\n')
        def interpréteurCommandes(ligne):
            processus.stdin.write(ligne.encode() + b'\n'); processus.stdin.flush(); return recevoirMessage()
        try:
            recevoirMessage(); assert 'FTP listening' in interpréteurCommandes('ftpd start')
            connexionTransfertFichier = ftplib.FTP(); connexionTransfertFichier.encoding = 'utf-8'; connexionTransfertFichier.connect('127.0.0.1', numéroPort, timeout=20); connexionTransfertFichier.login()
            donnéesChargeUtile = bytes(range(256)) * 32
            connexionTransfertFichier.storbinary('STOR binary.dat', io.BytesIO(donnéesChargeUtile))
            résultat = bytearray(); connexionTransfertFichier.retrbinary('RETR binary.dat', résultat.extend)
            assert résultat == donnéesChargeUtile; assert connexionTransfertFichier.size('binary.dat') == len(donnéesChargeUtile)
            rapportValidation['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            connexionTransfertFichier.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in interpréteurCommandes('cat 한글.txt')
            assert '한글.txt' in connexionTransfertFichier.nlst()
            assert dict(connexionTransfertFichier.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            rapportValidation['checks'].append('UTF-8 filename and content visible in guest shell')
            try: connexionTransfertFichier.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as entréeÉlémentAuxiliaire: assert str(entréeÉlémentAuxiliaire).startswith('552'), str(entréeÉlémentAuxiliaire)
            else: raise AssertionError('oversized upload accepted')
            résultat = bytearray(); connexionTransfertFichier.retrbinary('RETR binary.dat', résultat.extend); assert résultat == donnéesChargeUtile
            rapportValidation['checks'].append('oversized replacement rejected; previous file preserved')
            with connexionTransfertFichier.transfercmd('STOR pending.txt') as fichiersTéléverser:
                # A control command must not change the active upload's destination.
                assert connexionTransfertFichier.size('binary.dat') == len(donnéesChargeUtile)
                fichiersTéléverser.sendall(b'UPLOAD TARGET PRESERVED')
            assert connexionTransfertFichier.voidresp().startswith('226')
            résultat = bytearray(); connexionTransfertFichier.retrbinary('RETR pending.txt', résultat.extend)
            assert résultat == b'UPLOAD TARGET PRESERVED'
            résultat = bytearray(); connexionTransfertFichier.retrbinary('RETR binary.dat', résultat.extend)
            assert résultat == donnéesChargeUtile
            connexionTransfertFichier.delete('pending.txt')
            rapportValidation['checks'].append('interleaved SIZE cannot change the active STOR destination')
            connexionTransfertFichier.storbinary('STOR Salutation.jar', io.BytesIO(archive.getvalue()))
            texte = interpréteurCommandes('java -jar Salutation.jar 누리')
            assert 'JAR exécuterCommande: 누리' in texte and 'interne valeurNoyau Fichier' in texte and 'exit 0' in texte, texte
            texte = interpréteurCommandes('./Salutation.jar 세상')
            assert 'JAR exécuterCommande: 세상' in texte and 'exit 0' in texte, texte
            rapportValidation['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            donnéesOriginal = '#include <ABIFichier.h>\nstruct Données { int nombre; double 비율; };\nint valeurSomme(int n) { return n ? n + valeurSomme(n-1) : 0; }\nint main(void) { struct Données valeur = {valeurSomme(10), 1.25}; if (valeur.nombre != 55 || valeur.비율 * 2 != 2.5) return 3; const char Salutation[] = "CC NATIVE PASS\\n"; int Documentation = ouvrirFichier("cc.txt", ÉcrireLire | ManquantSiCréer | ContenuTronquer, 0600); if (Documentation < 0) return 1; écrireDonnéesFichier(Documentation, Salutation, sizeof(Salutation)-1); fermerFichier(Documentation); écrireDonnéesFichier(1, Salutation, sizeof(Salutation)-1); return 0; }\n'
            connexionTransfertFichier.storbinary('STOR texteHangul.c', io.BytesIO(donnéesOriginal.encode()))
            texte = interpréteurCommandes('cc texteHangul.c -o texteHangul.elf'); assert 'Compiled native ARM64 ELF:' in texte and 'exit 0' in texte, texte
            texte = interpréteurCommandes('run texteHangul.elf'); assert 'CC NATIVE PASS' in texte and 'exit 0' in texte, texte
            assert 'CC NATIVE PASS' in interpréteurCommandes('cat cc.txt')
            fichierCodeExécutable = bytearray(); connexionTransfertFichier.retrbinary('RETR texteHangul.elf', fichierCodeExécutable.extend)
            assert fichierCodeExécutable[:4] == b'\x7fELF' and fichierCodeExécutable[18:20] == b'\xb7\x00'
            connexionTransfertFichier.storbinary('STOR copierValeur.elf', io.BytesIO(fichierCodeExécutable)); texte = interpréteurCommandes('run copierValeur.elf'); assert 'CC NATIVE PASS' in texte and 'exit 0' in texte, texte
            connexionTransfertFichier.storbinary('STOR exécuterCommande', io.BytesIO(fichierCodeExécutable)); texte=interpréteurCommandes('./exécuterCommande');assert 'CC NATIVE PASS' in texte and 'exit 0' in texte,texte
            connexionTransfertFichier.storbinary('STOR nom.txt', io.BytesIO(fichierCodeExécutable)); texte=interpréteurCommandes('./nom.txt');assert 'CC NATIVE PASS' in texte and 'exit 0' in texte,texte
            interpréteurCommandes('rm exécuterCommande nom.txt')
            rapportValidation['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            interpréteurCommandes('rm binary.dat texteHangul.txt texteHangul.c texteHangul.elf copierValeur.elf cc.txt jar.txt')
            fichierLinux,attendu=exempleLinux(donnéesRésultat/'linux-reference')
            connexionTransfertFichier.storbinary('STOR 리눅스인사',io.BytesIO(fichierLinux.read_bytes()))
            texte=interpréteurCommandes('./리눅스인사');assert 'exit -8' in texte,texte
            texte=interpréteurCommandes('run --linux 리눅스인사 한글인수');assert attendu+'exit 0' in texte,texte
            assert 'LINUX ELF FILE IO' in interpréteurCommandes('cat linux.txt')
            connexionTransfertFichier.delete('리눅스인사');connexionTransfertFichier.delete('linux.txt')
            connexionTransfertFichier.storbinary('STOR valeurFaux.elf',io.BytesIO(b'plain text'))
            assert '실행할 nombre 없습니다:' in interpréteurCommandes('./valeurFaux.elf');connexionTransfertFichier.delete('valeurFaux.elf')
            rapportValidation['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with DispositifTestRépercuter() as entréeÉlémentServeurRépercuter:
                sourceRéseauCourt = donnéesRésultat/'CommunicationExtérieur.java'
                sourceRéseauCourt.write_text('''import java.net.*; import java.io.*;
public class CommunicationExtérieur { public static void main(String[] args) throws Exception {
 Socket connecter = français.interne.transportConnexion.connecter("10.0.2.2", Integer.parseInt(args[0]));
 connecter.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] source = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<source.length;i++) if (connecter.getInputStream().read() != (source[i]&255)) throw new RuntimeException("TCP mismatch");
 connecter.close();
 DatagramSocket extrémité = français.interne.Communication.ouvrir(0); français.interne.Communication.délaiExpiration(extrémité, 500);
 français.interne.Communication.envoyer(extrémité, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!français.interne.Communication.recevoir(extrémité).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 extrémité.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(racineProjet/'build/java-library/classes'),'-d',str(donnéesRésultat),str(sourceRéseauCourt)])
                connexionTransfertFichier.storbinary('STOR CommunicationExtérieur.class', io.BytesIO((donnéesRésultat/'CommunicationExtérieur.class').read_bytes()))
                texte = interpréteurCommandes('java CommunicationExtérieur {} {}'.format(entréeÉlémentServeurRépercuter.portTCP, entréeÉlémentServeurRépercuter.portUDP))
                assert 'EXTERNAL TCP UDP PASS' in texte and '10.0.2.2' in texte and 'exit 0' in texte, texte
                assert entréeÉlémentServeurRépercuter.possèdeReçu == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, entréeÉlémentServeurRépercuter.possèdeReçu
                assert not entréeÉlémentServeurRépercuter.erreurs, entréeÉlémentServeurRépercuter.erreurs
            rapportValidation['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            connexionTransfertFichier.delete('CommunicationExtérieur.class')
            sourceServeur=donnéesRésultat/'TestServeur.java'
            sourceServeur.write_text('''import java.net.*; public class TestServeur {
 public static void main(String[] args) throws Exception {
  ServerSocket valeurServeur = new ServerSocket(9300); DatagramSocket extrémité = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket valeurInvité = valeurServeur.accept();
  valeurInvité.getOutputStream().write(valeurInvité.getInputStream().read()+1); valeurInvité.close(); valeurServeur.close();
  byte[] valeurContenuValeur = new byte[8]; DatagramPacket datagramme = new DatagramPacket(valeurContenuValeur, valeurContenuValeur.length); extrémité.receive(datagramme);
  extrémité.send(datagramme); extrémité.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(donnéesRésultat),str(sourceServeur)])
            connexionTransfertFichier.storbinary('STOR TestServeur.class',io.BytesIO((donnéesRésultat/'TestServeur.class').read_bytes()))
            processus.stdin.write('java TestServeur\n'.encode());processus.stdin.flush();recevoirMessage(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',portFluxServeur),timeout=5) as valeurPairRéseau:
                valeurPairRéseau.sendall(b'A');assert valeurPairRéseau.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as valeurPairRéseau:
                valeurPairRéseau.settimeout(5);valeurPairRéseau.sendto(b'UDP-IN',('127.0.0.1',portDatagrammeServeur));assert valeurPairRéseau.recvfrom(512)[0]==b'UDP-IN'
            texte=recevoirMessage();assert 'INBOUND TCP UDP PASS' in texte and 'exit 0' in texte,texte
            rapportValidation['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            connexionTransfertFichier.delete('TestServeur.class')
            séquenceInstructionMachine = 'public class Couleur { public static void main(String[] arguments) throws Exception { int valeurSomme = 0; int nombre = 1; while (nombre <= 10) { valeurSomme = valeurSomme + nombre; nombre = nombre + 1; } français.interne.Sortie.écrireNuméro(valeurSomme); français.interne.Fichier.écrire("aot.txt", "한글 AOT Fichier 😀"); français.interne.Sortie.écrireLigne(français.interne.Fichier.lire("aot.txt")); } }'
            connexionTransfertFichier.storbinary('STOR Couleur.java', io.BytesIO(séquenceInstructionMachine.encode()))
            texte = interpréteurCommandes('javac Couleur.java'); assert 'exit 0' in texte and 'Compiled:' in texte, texte
            texte = interpréteurCommandes('jaot Couleur.class -o Couleur.elf'); assert 'AOT compiled native ARM64 ELF:' in texte and 'exit 0' in texte, texte
            texte = interpréteurCommandes('run Couleur.elf'); assert '\n55\n' in texte and '한글 AOT Fichier 😀' in texte and 'exit 0' in texte, texte
            natif = bytearray(); connexionTransfertFichier.retrbinary('RETR Couleur.elf', natif.extend)
            texte = interpréteurCommandes('jaot Salutation.jar -o Couleur.elf'); assert 'exit 1' in texte and 'unsupported' in texte, texte
            donnéesPréservé = bytearray(); connexionTransfertFichier.retrbinary('RETR Couleur.elf', donnéesPréservé.extend); assert natif == donnéesPréservé
            codeOctets = bytearray(); connexionTransfertFichier.retrbinary('RETR Couleur.class', codeOctets.extend)
            empaqueté = io.BytesIO()
            with zipfile.ZipFile(empaqueté, 'w', zipfile.ZIP_DEFLATED) as lotJava:
                lotJava.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: Couleur\r\n\r\n')
                lotJava.writestr('Couleur.class', codeOctets)
            connexionTransfertFichier.storbinary('STOR Couleur.jar', io.BytesIO(empaqueté.getvalue()))
            texte = interpréteurCommandes('jaot Couleur.jar -o Couleur.elf'); assert 'AOT compiled native ARM64 ELF:' in texte and 'exit 0' in texte, texte
            texte = interpréteurCommandes('run Couleur.elf'); assert '\n55\n' in texte and '한글 AOT Fichier 😀' in texte and 'exit 0' in texte, texte
            rapportValidation['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            rapportValidation['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            sourceStatique=donnéesRésultat/'TestStatique.java'
            sourceStatique.write_text('''public class TestStatique {
 static int racineProjet = 3;
 static int valeurSomme(int n) { return n == 0 ? 0 : n + valeurSomme(n-1); }
 public static void main(String[] arguments) {
  int[] valeur = new int[] {racineProjet, valeurSomme(10)};
  System.out.println(valeur[0] + valeur[1]); System.out.println(arguments[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(donnéesRésultat),str(sourceStatique)])
            connexionTransfertFichier.storbinary('STOR TestStatique.class',io.BytesIO((donnéesRésultat/'TestStatique.class').read_bytes()))
            texte=interpréteurCommandes('jaot TestStatique.class -o TestStatique.elf');assert 'exit 0' in texte,texte
            texte=interpréteurCommandes('run TestStatique.elf 한글인수');assert '\n58\n한글인수\nexit 0' in texte,texte
            connexionTransfertFichier.delete('TestStatique.class');connexionTransfertFichier.delete('TestStatique.elf')
            rapportValidation['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            endommagé=bytearray(archive.getvalue());endommagé[14]^=1
            connexionTransfertFichier.storbinary('STOR Salutation.jar',io.BytesIO(endommagé))
            texte=interpréteurCommandes('java -jar Salutation.jar');assert 'Main-Class\nexit 1' in texte,texte
            rapportValidation['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            connexionTransfertFichier.quit(); assert 'FTP stopped' in interpréteurCommandes('ftpd stop')
            assert not pont.erreur, pont.erreur
            rapportValidation.update(passed=True, frames_to_guest=pont.invitéVersCadres, frames_from_guest=pont.invitéDepuisCadres)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for valeurEnfoncé,_ in sélecteur.select(0):
                valeurFragment=valeurEnfoncé.fileobj.read(65536)
                if valeurFragment: transcription.extend(valeurFragment)
            pont.évènementMettreEnPause.set()
            processus.terminate()
            try: processus.wait(timeout=5)
            except subprocess.TimeoutExpired: processus.kill(); processus.wait()
            sélecteur.close(); processus.stdin.close(); processus.stdout.close()
            rapportValidation['bridge_error'] = pont.erreur
            rapportValidation['frames_to_guest'] = pont.invitéVersCadres; rapportValidation['frames_from_guest'] = pont.invitéDepuisCadres
            (donnéesRésultat/'packets.json').write_text(json.dumps(pont.journalTrace,indent=2)+'\n')
            (donnéesRésultat / 'serial.log').write_bytes(transcription)
            (donnéesRésultat / 'report.json').write_text(json.dumps(rapportValidation, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': lancer()
