#!/usr/bin/env python3
"""QEMU의 donnéesEffectif CPU valeurPermission, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
import ftplib
import hashlib
import io
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time

from exécuterCommande import racineProjet, commande
from pontRéseau import pontRéseau
from DispositifTestRépercuter import DispositifTestRépercuter


def lancer():
    Sortie = racineProjet / 'build/verification/execution-network-review'
    Sortie.mkdir(parents=True, exist_ok=True)
    valeurRapport = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((racineProjet / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    fichiersSource = {
        'ContrôlerPrivilège': '''public class ContrôlerPrivilège {
 public static void main(String[] arguments) {
  System.out.println("EL0_PROBE_READY");
  int nombre = 0; while (true) { nombre++; }
 }
}''',
        'ContrôlerRéseau': '''import java.net.*;
public class ContrôlerRéseau {
 public static void main(String[] arguments) throws Exception {
  Socket connecter = new Socket("10.0.2.2", Integer.parseInt(arguments[0]));
  connecter.setSoTimeout(3000);
  byte[] texte = "TCP 한글\\n".getBytes("UTF-8");
  connecter.getOutputStream().write(texte);
  for (int indicePosition = 0; indicePosition < texte.length; indicePosition++)
   if (connecter.getInputStream().read() != (texte[indicePosition] & 255)) throw new RuntimeException("TCP mismatch");
  connecter.close();
  DatagramSocket extrémité = new DatagramSocket(); extrémité.setSoTimeout(3000);
  texte = "UDP 한글".getBytes("UTF-8");
  extrémité.send(new DatagramPacket(texte, texte.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(arguments[1])));
  byte[] réponse = new byte[64]; DatagramPacket datagramme = new DatagramPacket(réponse, réponse.length);
  extrémité.receive(datagramme);
  if (datagramme.getLength() != texte.length) throw new RuntimeException("UDP length");
  for (int indicePosition = 0; indicePosition < texte.length; indicePosition++)
   if (réponse[indicePosition] != texte[indicePosition]) throw new RuntimeException("UDP mismatch");
  extrémité.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'ContrôlerRecevoir': '''import java.net.*;
public class ContrôlerRecevoir {
 public static void main(String[] arguments) throws Exception {
  ServerSocket valeurServeur = new ServerSocket(9300); valeurServeur.setSoTimeout(5000);
  DatagramSocket extrémité = new DatagramSocket(9301); extrémité.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket connecter = valeurServeur.accept(); connecter.setSoTimeout(5000);
  connecter.getOutputStream().write(connecter.getInputStream().read() + 1);
  connecter.close(); valeurServeur.close();
  byte[] Données = new byte[64]; DatagramPacket datagramme = new DatagramPacket(Données, Données.length);
  extrémité.receive(datagramme); extrémité.send(datagramme); extrémité.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for nom, source in fichiersSource.items():
        (Sortie / (nom + '.java')).write_text(source, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Sortie)] +
                          [str(Sortie / (nom + '.java')) for nom in fichiersSource])
    enregistrementJournal = bytearray()
    def numéroPortVide(catégorieType=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, catégorieType) as chercherValeur:
            chercherValeur.bind(('127.0.0.4', 0))
            return chercherValeur.getsockname()[1]
    numéroPortFichier, portTCP, portUDP = numéroPortVide(), numéroPortVide(), numéroPortVide(socket.SOCK_DGRAM)
    valeurProcessus = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as valeurTemporaire, pontRéseau(
                numéroPortFichier, ['tcp:{}:9300'.format(portTCP), 'udp:{}:9301'.format(portUDP)],
                capturer=True, adresseHôte='127.0.0.4') as valeurPont:
            cheminContrôle = Path(valeurTemporaire) / 'qmp.sock'
            valeurProcessus = subprocess.Popen(commande() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(cheminContrôle)] + valeurPont.argumentTransféré(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            élémentListeChoisir = selectors.DefaultSelector()
            élémentListeChoisir.register(valeurProcessus.stdout, selectors.EVENT_READ)
            def recevoir(afficherValeur=b'jkoros-native> ', élémentListeInitialValeur=0, valeurLimite=60):
                terminaison = time.monotonic() + valeurLimite
                while afficherValeur not in enregistrementJournal[élémentListeInitialValeur:]:
                    if time.monotonic() > terminaison or valeurProcessus.poll() is not None:
                        raise AssertionError('Missing ' + repr(afficherValeur) + '\n' + enregistrementJournal[élémentListeInitialValeur:].decode('utf-8', 'replace'))
                    for valeurTouche, _ in élémentListeChoisir.select(.05):
                        valeurFragment = valeurTouche.fileobj.read(65536)
                        if valeurFragment:
                            enregistrementJournal.extend(valeurFragment)
                return enregistrementJournal[élémentListeInitialValeur:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def envoyer(Données):
                valeurProcessus.stdin.write(Données)
                valeurProcessus.stdin.flush()
            def interpréteurCommandes(texte):
                print(texte, flush=True)
                élémentListeInitialValeur = len(enregistrementJournal)
                envoyer((texte + '\n').encode())
                return recevoir(élémentListeInitialValeur=élémentListeInitialValeur)
            recevoir()
            with socket.socket(socket.AF_UNIX) as valeurContrôle:
                valeurContrôle.settimeout(10)
                valeurContrôle.connect(str(cheminContrôle))
                valeurFlux = valeurContrôle.makefile('rwb')
                json.loads(valeurFlux.readline())
                def requête(valeurInstructionMachine, arguments=None):
                    Données = {'execute': valeurInstructionMachine}
                    if arguments is not None:
                        Données['arguments'] = arguments
                    valeurFlux.write((json.dumps(Données) + '\n').encode())
                    valeurFlux.flush()
                    while True:
                        réponse = json.loads(valeurFlux.readline())
                        if 'error' in réponse:
                            raise AssertionError(réponse)
                        if 'return' in réponse:
                            return réponse['return']
                requête('qmp_capabilities')
                def lirePermission():
                    requête('stop')
                    try:
                        return requête('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        requête('cont')
                valeurRapport['shell_cpu'] = lirePermission()
                assert 'EL1h' in valeurRapport['shell_cpu'], valeurRapport['shell_cpu']
                valeurRapport['initial_ps'] = interpréteurCommandes('ps')
                assert 'kernel/shell' in valeurRapport['initial_ps']
                valeurRapport['ipconfig'] = interpréteurCommandes('ipconfig')
                assert 'inet 10.0.2.15' in valeurRapport['ipconfig']
                valeurRapport['gateway_ping'] = interpréteurCommandes('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in valeurRapport['gateway_ping']
                assert 'FTP listening' in interpréteurCommandes('ftpd start')
                with ftplib.FTP() as valeurTransfert:
                    valeurTransfert.encoding = 'utf-8'
                    valeurTransfert.connect('127.0.0.4', numéroPortFichier, timeout=20)
                    valeurTransfert.login()
                    for nom in fichiersSource:
                        valeurTransfert.storbinary('STOR ' + nom + '.class', io.BytesIO((Sortie / (nom + '.class')).read_bytes()))
                élémentListeInitialValeur = len(enregistrementJournal)
                envoyer('java ContrôlerPrivilège\n'.encode())
                recevoir(b'EL0_PROBE_READY\r\n', élémentListeInitialValeur)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    valeurRapport['java_cpu'] = lirePermission()
                    if 'EL0t' in valeurRapport['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in valeurRapport['java_cpu'], valeurRapport['java_cpu']
                recevoir(élémentListeInitialValeur=élémentListeInitialValeur)
                valeurRapport['after_exit_ps'] = interpréteurCommandes('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', valeurRapport['after_exit_ps'])
                valeurRapport['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with DispositifTestRépercuter() as valeurPairRéseau:
                    texte = interpréteurCommandes('java ContrôlerRéseau {} {}'.format(valeurPairRéseau.portTCP, valeurPairRéseau.portUDP))
                    assert 'OUTBOUND_TCP_UDP_PASS' in texte and 'exit 0' in texte, texte
                    assert valeurPairRéseau.possèdeReçu == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, valeurPairRéseau.possèdeReçu
                    assert not valeurPairRéseau.erreurs, valeurPairRéseau.erreurs
                    valeurRapport['outbound_peers'] = {valeurGenre: Données.decode() for valeurGenre, Données in valeurPairRéseau.possèdeReçu.items()}
                élémentListeInitialValeur = len(enregistrementJournal)
                envoyer('java ContrôlerRecevoir\n'.encode())
                recevoir(b'INBOUND_READY\r\n', élémentListeInitialValeur)
                with socket.create_connection(('127.0.0.4', portTCP), timeout=5) as valeurPairRéseau:
                    valeurPairRéseau.sendall(b'A')
                    assert valeurPairRéseau.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as valeurPairRéseau:
                    valeurPairRéseau.settimeout(5)
                    valeurPairRéseau.sendto(b'UDP-IN', ('127.0.0.4', portUDP))
                    assert valeurPairRéseau.recvfrom(64)[0] == b'UDP-IN'
                texte = recevoir(élémentListeInitialValeur=élémentListeInitialValeur)
                assert 'INBOUND_TCP_UDP_PASS' in texte and 'exit 0' in texte, texte
                valeurRapport['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in interpréteurCommandes('terminal')
                interpréteurCommandes('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                élémentListeInitialValeur = len(enregistrementJournal)
                envoyer('java ExempleFenêtre\n'.encode())
                recevoir('GUI Exemples préparer: ExempleFenêtre\r\n'.encode(), élémentListeInitialValeur)
                élémentListeInitialValeur = len(enregistrementJournal)
                envoyer(bytes([30, 2, 1, 0, 0, 0, 0]))
                recevoir(élémentListeInitialValeur=élémentListeInitialValeur)
                valeurRapport['suspended_java_ps'] = interpréteurCommandes('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java ExempleFenêtre', valeurRapport['suspended_java_ps']), valeurRapport['suspended_java_ps']
                valeurRapport['top'] = interpréteurCommandes('top -n 1')
                assert 'java ExempleFenêtre' in valeurRapport['top'] and 'kernel/shell' in valeurRapport['top']
                valeurRapport['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                valeurRapport['network_trace'] = valeurPont.journalTrace
                assert not valeurPont.erreur, valeurPont.erreur
                envoyer(b'poweroff\n')
                assert valeurProcessus.wait(timeout=15) == 0
                valeurRapport['passed'] = True
            élémentListeChoisir.close()
    except Exception as erreur:
        valeurRapport['error'] = str(erreur)
        raise
    finally:
        if valeurProcessus is not None and valeurProcessus.poll() is None:
            valeurProcessus.terminate()
            try:
                valeurProcessus.wait(timeout=10)
            except subprocess.TimeoutExpired:
                valeurProcessus.kill()
                valeurProcessus.wait()
        (Sortie / 'serial.log').write_bytes(enregistrementJournal)
        (Sortie / 'report.json').write_text(json.dumps(valeurRapport, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({valeurTouche: valeurRapport[valeurTouche] for valeurTouche in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    lancer()
