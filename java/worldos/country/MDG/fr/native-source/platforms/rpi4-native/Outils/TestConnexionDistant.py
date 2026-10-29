#!/usr/bin/env python3
"""donnéesEffectif OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import struct
import subprocess
import tempfile
import threading
import time
import selectors
from Crypto.Cipher import DES
from exécuterCommande import racineProjet, commande
from pontRéseau import pontRéseau


def lancer():
    Analyseur = argparse.ArgumentParser(description=__doc__)
    Analyseur.add_argument('--kernel', type=Path, default=racineProjet / 'build/kernel8.img')
    Analyseur.add_argument('--access', type=Path, default=racineProjet / 'build/remote/access.json')
    Analyseur.add_argument('--output', type=Path, default=racineProjet / 'build/verification/native-remote')
    arguments = Analyseur.parse_args()
    Sortie = arguments.output
    Sortie.mkdir(parents=True, exist_ok=True)
    réglages = json.loads(arguments.access.read_text())
    valeurRapport = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(arguments.kernel.read_bytes()).hexdigest(), 'checks': []}
    def portVide():
        with socket.socket() as connecter:
            connecter.bind(('127.0.0.5', 0))
            return connecter.getsockname()[1]
    portInterpréteurCommandes, portÉcran, portFichier = portVide(), portVide(), portVide()
    enregistrementJournal = bytearray()
    valeurProcessus = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as valeurTemporaire, pontRéseau(portFichier,
                ['tcp:{}:22'.format(portInterpréteurCommandes), 'tcp:{}:5900'.format(portÉcran)], adresseHôte='127.0.0.5') as valeurPont:
            Arguments = commande()
            Arguments[Arguments.index('-kernel') + 1] = str(arguments.kernel.resolve())
            valeurProcessus = subprocess.Popen(Arguments + ['-display','none','-monitor','none','-serial','stdio'] + valeurPont.argumentTransféré(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def rassemblerValeurs():
                while True:
                    Données = valeurProcessus.stdout.read(4096)
                    if not Données: break
                    enregistrementJournal.extend(Données)
            valeurFilExécution = threading.Thread(target=rassemblerValeurs, daemon=True)
            valeurFilExécution.start()
            def attendreÉtatValeur(texteMot, élémentListeInitialValeur=0, valeurLimite=60):
                terminaison = time.monotonic() + valeurLimite
                while texteMot not in enregistrementJournal[élémentListeInitialValeur:]:
                    if time.monotonic()>terminaison or valeurProcessus.poll() is not None:
                        raise AssertionError('Missing '+repr(texteMot)+'\n'+enregistrementJournal[élémentListeInitialValeur:].decode('utf-8','replace'))
                    time.sleep(.02)
            attendreÉtatValeur(b'jkoros-native> ')
            valeurAssistant = Path(valeurTemporaire)/'askpass'
            valeurAssistant.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            valeurAssistant.chmod(0o700)
            environnement = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(valeurAssistant), SSH_ASKPASS_REQUIRE='force')
            def interpréteurCommandesSécuriser(valeurMotPasse, valeurInstructionMachine, ajouterFinEntréeÉlément=()):
                environnement['JKOROS_TEST_PASSWORD']=valeurMotPasse
                arguments=['ssh','-v']+list(ajouterFinEntréeÉlément)+['-p',str(portInterpréteurCommandes),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(valeurTemporaire)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',valeurInstructionMachine]
                résultat=subprocess.run(arguments,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=environnement,start_new_session=True,timeout=50)
                return résultat
            résultat=interpréteurCommandesSécuriser('!' + réglages['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Sortie/'ssh-rejected.log').write_bytes(résultat.stderr)
            assert résultat.returncode!=0 and b'Permission denied' in résultat.stderr and b'SHOULD_NOT_RUN' not in enregistrementJournal, résultat.stderr
            valeurRapport['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            résultat=interpréteurCommandesSécuriser(réglages['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Sortie/'ssh.log').write_bytes(résultat.stderr)
            (Sortie/'ssh-output.txt').write_bytes(résultat.stdout)
            assert résultat.returncode==0 and b'SSH_NATIVE_PASS' in résultat.stdout, (résultat.returncode,résultat.stdout,résultat.stderr)
            valeurRapport['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in résultat.stderr, résultat.stderr
            valeurRapport['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            résultat=interpréteurCommandesSécuriser(réglages['ssh_password'], 'cd /example/java; java ExempleSortie; cd /')
            assert résultat.returncode==0 and 'JAVA Sortie: 안녕하세요 😀'.encode() in résultat.stdout,résultat.stdout
            valeurRapport['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            résultat=interpréteurCommandesSécuriser(réglages['ssh_password'], 'missing_remote_command')
            assert résultat.returncode==127,résultat.returncode
            valeurRapport['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            résultat=interpréteurCommandesSécuriser(réglages['ssh_password'], 'cat /example/java/ExempleFenêtre.java', ('-o', 'RekeyLimit=1K'))
            (Sortie/'ssh-rekey.log').write_bytes(résultat.stderr)
            assert résultat.returncode==0 and 'class ExempleFenêtre'.encode() in résultat.stdout, (résultat.returncode,résultat.stdout,résultat.stderr)
            assert résultat.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, résultat.stderr
            valeurRapport['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            argumentsInteractif=['ssh','-tt','-p',str(portInterpréteurCommandes),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(valeurTemporaire)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            sessionInteractif=subprocess.Popen(argumentsInteractif,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=environnement,start_new_session=True,bufsize=0)
            transcription=bytearray();valeurSélection=selectors.DefaultSelector();valeurSélection.register(sessionInteractif.stdout,selectors.EVENT_READ)
            def lireInteractif(afficherValeur):
                valeurÉchéance=time.monotonic()+30
                while afficherValeur not in transcription:
                    if time.monotonic()>valeurÉchéance or sessionInteractif.poll() is not None:raise AssertionError('SSH interactive missing '+repr(afficherValeur)+' '+repr(bytes(transcription)))
                    for valeurEntréeÉlément,_ in valeurSélection.select(.1):
                        valeurFragment=valeurEntréeÉlément.fileobj.read(4096)
                        if valeurFragment:transcription.extend(valeurFragment)
            try:
                lireInteractif(b'shared native console')
                sessionInteractif.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');sessionInteractif.stdin.flush();lireInteractif(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                sessionInteractif.stdin.write(b'\x04');sessionInteractif.stdin.flush();valeurResteDivision,erreur=sessionInteractif.communicate(timeout=15)
                assert sessionInteractif.returncode==0 and b'PTY allocation request failed' not in erreur,(sessionInteractif.returncode,erreur)
                (Sortie/'ssh-interactive.txt').write_bytes(transcription+valeurResteDivision)
            finally:
                valeurSélection.close()
                if sessionInteractif.poll() is None:sessionInteractif.kill();sessionInteractif.wait()
            valeurRapport['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def valeurExactement(connecter, nombre):
                Données=bytearray()
                while len(Données)<nombre:
                    valeurFragmentBloc=connecter.recv(nombre-len(Données))
                    if not valeurFragmentBloc: raise AssertionError('RFB EOF')
                    Données.extend(valeurFragmentBloc)
                return bytes(Données)
            def authentificationÉcran(valeurMotPasse):
                connecter=socket.create_connection(('127.0.0.5',portÉcran),10);connecter.settimeout(30)
                assert valeurExactement(connecter,12)==b'RFB 003.008\n'
                connecter.sendall(b'RFB 003.008\n');assert valeurExactement(connecter,2)==b'\x01\x02'
                connecter.sendall(b'\x02');valeurDéfi=valeurExactement(connecter,16)
                motPasseEntrée=valeurMotPasse.encode('ascii')[:8].ljust(8, b'\0')
                matériauTouche=bytes(int('{:08b}'.format(nombre)[::-1],2) for nombre in motPasseEntrée)
                connecter.sendall(DES.new(matériauTouche,DES.MODE_ECB).encrypt(valeurDéfi))
                valeurÉtatValeur=struct.unpack('!I',valeurExactement(connecter,4))[0]
                return connecter,valeurÉtatValeur
            motPasseInvalide='!' if not réglages['vnc_password'].startswith('!') else '?'
            connecter,valeurÉtatValeur=authentificationÉcran(motPasseInvalide);assert valeurÉtatValeur==1;connecter.close();time.sleep(.6)
            valeurRapport['checks'].append('VNC incorrect password rejected')
            connecter,valeurÉtatValeur=authentificationÉcran(réglages['vnc_password']);assert valeurÉtatValeur==0
            with connecter:
                connecter.sendall(b'\x01');étatValeurInitialValeur=valeurExactement(connecter,24);valeurLargeur,valeurHauteur=struct.unpack('!HH',étatValeurInitialValeur[:4]);nom=valeurExactement(connecter,struct.unpack('!I',étatValeurInitialValeur[20:24])[0])
                assert (valeurLargeur,valeurHauteur)==(640,480) and b'jkoros native'==nom
                def Écran(étapeIncrément=0):
                    connecter.sendall(struct.pack('!BBHHHH',3,étapeIncrément,0,0,valeurLargeur,valeurHauteur));valeurTête=valeurExactement(connecter,4);nombre=struct.unpack('!H',valeurTête[2:])[0];valeurTotal=0
                    Dessin=bytearray(valeurLargeur*valeurHauteur*4)
                    for _ in range(nombre):
                        coordonnéeCoordonnéeHorizontale,coordonnéeCoordonnéeVerticale,largeurRégion,hauteurRégion,modeMéthode=struct.unpack('!HHHHi',valeurExactement(connecter,12));assert modeMéthode==0 and coordonnéeCoordonnéeHorizontale+largeurRégion<=valeurLargeur and coordonnéeCoordonnéeVerticale+hauteurRégion<=valeurHauteur
                        pixel=valeurExactement(connecter,largeurRégion*hauteurRégion*4);valeurTotal+=len(pixel)
                        for ligne in range(hauteurRégion):Dessin[((coordonnéeCoordonnéeVerticale+ligne)*valeurLargeur+coordonnéeCoordonnéeHorizontale)*4:((coordonnéeCoordonnéeVerticale+ligne)*valeurLargeur+coordonnéeCoordonnéeHorizontale+largeurRégion)*4]=pixel[ligne*largeurRégion*4:(ligne+1)*largeurRégion*4]
                    if not étapeIncrément:
                        from PIL import Image
                        Image.frombytes('RGB',(valeurLargeur,valeurHauteur),bytes(Dessin),'raw','BGRX').save(str(Sortie/'native-vnc.png'))
                    return nombre,valeurTotal
                nombre,valeurTotal=Écran();assert nombre>0 and valeurTotal==valeurLargeur*valeurHauteur*4
                valeurRapport['checks'].append('Native framebuffer RFB full update {} bytes'.format(valeurTotal))
                nombre,valeurTotal=Écran(1);assert valeurTotal<valeurLargeur*valeurHauteur*4
                valeurRapport['checks'].append('RFB incremental update')
                élémentListeInitialValeur=len(enregistrementJournal)
                for valeurCaractère in 'echo VNC_NATIVE_PASS\r':
                    symbole=0xff0d if valeurCaractère=='\r' else ord(valeurCaractère)
                    connecter.sendall(struct.pack('!BBHI',4,1,0,symbole));connecter.sendall(struct.pack('!BBHI',4,0,0,symbole))
                attendreÉtatValeur(b'VNC_NATIVE_PASS',élémentListeInitialValeur)
                valeurRapport['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def traitTouche(symbole,valeurEnfoncer=1):connecter.sendall(struct.pack('!BBHI',4,valeurEnfoncer,0,symbole))
                élémentListeInitialValeur=len(enregistrementJournal)
                for valeurCaractère in 'echo ':traitTouche(ord(valeurCaractère))
                traitTouche(0xffc6)
                for valeurCaractère in 'gksrmf':traitTouche(ord(valeurCaractère))
                traitTouche(0xffc6);traitTouche(0xff0d)
                attendreÉtatValeur('\r\n한글\r\n'.encode(),élémentListeInitialValeur)
                valeurRapport['checks'].append('Native VNC F9 two-set Hangul composition')
                connecter.sendall(struct.pack('!BBHH',5,0,120,100))
                valeurRapport['checks'].append('VNC pointer input accepted')
            valeurProcessus.stdin.write(b'poweroff\n');valeurProcessus.stdin.flush();valeurProcessus.wait(timeout=15);assert valeurProcessus.returncode==0
            valeurRapport['passed']=True
    finally:
        if valeurProcessus and valeurProcessus.poll() is None:
            valeurProcessus.terminate()
            try: valeurProcessus.wait(timeout=5)
            except subprocess.TimeoutExpired: valeurProcessus.kill();valeurProcessus.wait()
        (Sortie/'serial.log').write_bytes(enregistrementJournal)
        (Sortie/'report.json').write_text(json.dumps(valeurRapport,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(valeurRapport,ensure_ascii=False,indent=2))


if __name__=='__main__': lancer()
