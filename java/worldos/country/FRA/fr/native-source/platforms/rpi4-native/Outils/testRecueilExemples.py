#!/usr/bin/env python3
"""Run all examples in the real combined VNC + SLIP/FTP native VM."""
import ftplib
import hashlib
import io
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from vueBureau import valeurExact
from ServeurÉchoExemple import ServeursRépercuter
from exécuterCommande import racineProjet


def testLangue(Langue,entréeÉlémentServeurRépercuter,donnéesRésultat):
    with socket.socket() as temporaire:
        temporaire.bind(('127.0.0.1',0));numéroPortTransfertFichier=temporaire.getsockname()[1]
    processus=subprocess.Popen(['python3',str(racineProjet/'Outils/exécuterCommande.py'),'--desktop','--network','--port','0','--ftp-port',str(numéroPortTransfertFichier)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    sélecteur=selectors.DefaultSelector();sélecteur.register(processus.stdout,selectors.EVENT_READ)
    transcription=bytearray();client=None;connexionTransfertFichier=None
    def recevoirMessage(marqueur,lancer=0):
        décalageFin=time.monotonic()+60
        while marqueur not in transcription[lancer:]:
            if time.monotonic()>décalageFin or processus.poll() is not None:raise AssertionError(transcription[lancer:].decode('utf-8','replace'))
            for valeurEnfoncé,_ in sélecteur.select(.1):
                Données=valeurEnfoncé.fileobj.read(65536)
                if Données:transcription.extend(Données)
        return transcription[lancer:].decode('utf-8','replace').replace('\r\n','\n')
    def valeurEnfoncé(valeurSymbole,estEnfoncementEnCours=True):client.sendall(struct.pack('>BBHI',4,int(estEnfoncementEnCours),0,valeurSymbole))
    def démarrerDécalage(ligne):
        lancer=len(transcription)
        for codeCaractère in ligne+'\n':
            valeurSymbole=0xff0d if codeCaractère=='\n' else ord(codeCaractère) if ord(codeCaractère)<256 else 0x1000000|ord(codeCaractère)
            valeurEnfoncé(valeurSymbole);valeurEnfoncé(valeurSymbole,False)
        return lancer
    def interpréteurCommandes(ligne):return recevoirMessage(b'jkoros-native> ',démarrerDécalage(ligne))
    def exécuterCommande(ligne,attendu):
        texte=interpréteurCommandes(ligne);assert attendu in texte and 'exit 0' in texte,(ligne,texte)
        return texte
    def listePixels():
        client.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        couleurRGB=bytearray(640*480*3)
        while True:
            valeurCatégorie=valeurExact(client,1)[0]
            if valeurCatégorie==2:continue
            if valeurCatégorie==3:
                nombreÉlémentsÉlémentListe=struct.unpack('>I',valeurExact(client,7)[3:])[0];valeurExact(client,nombreÉlémentsÉlémentListe);continue
            assert valeurCatégorie==0,valeurCatégorie
            nombreÉlémentsEntréeÉlément=struct.unpack('>H',valeurExact(client,3)[1:])[0]
            for _ in range(nombreÉlémentsEntréeÉlément):
                coordonnéeCoordonnéeHorizontale,coordonnéeCoordonnéeVerticale,valeurLargeurDemandé,valeurHauteurDemandé,jeuCaractères=struct.unpack('>HHHHi',valeurExact(client,12));assert jeuCaractères==0,jeuCaractères
                Données=valeurExact(client,valeurLargeurDemandé*valeurHauteurDemandé*4)
                for positionRangée in range(valeurHauteurDemandé):
                    for positionColonne in range(valeurLargeurDemandé):
                        donnéesOriginal=(positionRangée*valeurLargeurDemandé+positionColonne)*4;valeurCible=((coordonnéeCoordonnéeVerticale+positionRangée)*640+coordonnéeCoordonnéeHorizontale+positionColonne)*3
                        couleurRGB[valeurCible:valeurCible+3]=bytes((Données[donnéesOriginal+2],Données[donnéesOriginal+1],Données[donnéesOriginal]))
            if nombreÉlémentsEntréeÉlément:return couleurRGB
    try:
        recevoirMessage(b'TERMINAL READY');recevoirMessage(b'jkoros-native> ',transcription.rfind(b'TERMINAL READY'))
        numéroPort=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transcription).group(1))
        client=socket.create_connection(('127.0.0.1',numéroPort),timeout=10)
        assert valeurExact(client,12)==b'RFB 003.008\n';client.sendall(b'RFB 003.008\n')
        assert 1 in valeurExact(client,valeurExact(client,1)[0]);client.sendall(b'\x01');assert valeurExact(client,4)==b'\0'*4
        client.sendall(b'\x01');valeurInitialValeur=valeurExact(client,24);valeurExact(client,struct.unpack('>I',valeurInitialValeur[20:])[0])
        client.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        client.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in interpréteurCommandes('ftpd start')
        connexionTransfertFichier=ftplib.FTP();connexionTransfertFichier.encoding='utf-8';connexionTransfertFichier.connect('127.0.0.1',numéroPortTransfertFichier,timeout=20);connexionTransfertFichier.login()
        donnéesChargeUtile=('GUI와 FTP 동시 valeurUtiliser '+Langue+' 😀\n').encode()
        connexionTransfertFichier.storbinary('STOR 함께.txt',io.BytesIO(donnéesChargeUtile))
        assert donnéesChargeUtile.decode().strip() in interpréteurCommandes('cat /함께.txt')
        nombreÉlémentsReçu=bytearray();connexionTransfertFichier.retrbinary('RETR 함께.txt',nombreÉlémentsReçu.extend);assert nombreÉlémentsReçu==donnéesChargeUtile;connexionTransfertFichier.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        envoyerListe=interpréteurCommandes('ls /example')
        assert all(nom in envoyerListe for nom in ('java/','c/','python/','README.md')),envoyerListe
        if Langue=='java':
            manifesteLot=json.loads((racineProjet/'build/examples/manifest.json').read_text())
            for chemin,pointEntréeÉlément in manifesteLot.items():
                interpréteurCommandes('cp '+chemin+' /example-check.bin')
                valeurContenuValeur=bytearray();connexionTransfertFichier.retrbinary('RETR example-check.bin',valeurContenuValeur.extend)
                assert len(valeurContenuValeur)==pointEntréeÉlément['bytes'] and hashlib.sha256(valeurContenuValeur).hexdigest()==pointEntréeÉlément['sha256'],chemin
            connexionTransfertFichier.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binaire=bytes(range(256))*64
            connexionTransfertFichier.storbinary('STOR boundary.bin',io.BytesIO(binaire))
            valeurContenuValeur=bytearray();connexionTransfertFichier.retrbinary('RETR boundary.bin',valeurContenuValeur.extend)
            assert valeurContenuValeur==binaire and 'boundary.bin' in connexionTransfertFichier.nlst()
            interpréteurCommandes('cp /boundary.bin /boundary-copy.bin')
            valeurContenuValeur=bytearray();connexionTransfertFichier.retrbinary('RETR boundary-copy.bin',valeurContenuValeur.extend)
            assert valeurContenuValeur==binaire
            connexionTransfertFichier.delete('boundary.bin');connexionTransfertFichier.delete('boundary-copy.bin')
        assert 'ExempleSortie' in interpréteurCommandes('ls /example/'+Langue)
        interpréteurCommandes('cd /example/'+Langue)
        tableNom={'java':'JAVA','c':'C','python':'PYTHON'}[Langue]
        fichierAttendu=tableNom+' Fichier: 한글 Données 😀\n'
        if Langue=='java':
            exécuterCommande('javac ExempleSortie.java','Compiled:');exécuterCommande('java ExempleSortie','JAVA Sortie: 안녕하세요 😀')
            exécuterCommande('javac ExempleFichier.java','Compiled:');exécuterCommande('java ExempleFichier',fichierAttendu)
            exécuterCommande('java ExempleRéseau {} {}'.format(entréeÉlémentServeurRépercuter.portTCP,entréeÉlémentServeurRépercuter.portUDP),'JAVA 네트워크 vérifier: TCP UDP 한글')
            commandeGraphisme='java ExempleDessin'
        elif Langue=='c':
            for nom,valeurTransféré,attendu in [('Sortie','', 'C Sortie: 안녕하세요 😀'),('Fichier','',fichierAttendu),
                    ('네트워크',' '+str(entréeÉlémentServeurRépercuter.portUDP),'C 네트워크 vérifier: UDP 한글')]:
                exécuterCommande('cc '+nom+'Exemples.c -o exécuterCommande','Compiled native ARM64 ELF:')
                exécuterCommande('./exécuterCommande'+valeurTransféré,attendu)
            exécuterCommande('cc ExempleDessin.c -o exécuterCommande','Compiled native ARM64 ELF:');commandeGraphisme='./exécuterCommande'
        else:
            for nom,valeurTransféré,attendu in [('Sortie','','PYTHON Sortie: 안녕하세요 😀'),('Fichier','',fichierAttendu),
                    ('네트워크',' '+str(entréeÉlémentServeurRépercuter.portUDP),'PYTHON 네트워크 vérifier: UDP 한글')]:
                exécuterCommande('python '+nom+'Exemples.py'+valeurTransféré,attendu)
            commandeGraphisme='python ExempleDessin.py'
        démarrerDessin=démarrerDécalage(commandeGraphisme)
        texte=recevoirMessage('그림을 확인한 valeurRetourArrièreCôté Enter를 누르세요.\r\n'.encode(),démarrerDessin)
        assert tableNom+' 그래픽: 빨강 초록 파랑' in texte and 'exit 0' not in texte,texte
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        connexionTransfertFichier.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        nombreÉlémentsReçu=bytearray();connexionTransfertFichier.retrbinary('RETR 도중.txt',nombreÉlémentsReçu.extend);assert nombreÉlémentsReçu==b'FTP DURING GRAPHICS';connexionTransfertFichier.delete('도중.txt')
        couleurRGB=listePixels()
        for coordonnéeCoordonnéeVerticale,couleurPixel in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            valeurDécalage=(coordonnéeCoordonnéeVerticale*640+610)*3;assert tuple(couleurRGB[valeurDécalage:valeurDécalage+3])==couleurPixel,(Langue,coordonnéeCoordonnéeVerticale,tuple(couleurRGB[valeurDécalage:valeurDécalage+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(couleurRGB)).save(str(donnéesRésultat/(Langue+'-graphics.png')))
        valeurEnfoncé(0xff0d);valeurEnfoncé(0xff0d,False)
        assert 'exit 0' in recevoirMessage(b'jkoros-native> ',démarrerDessin)
        if Langue=='java':
            démarrerFenêtre=démarrerDécalage('java ExempleFenêtre')
            recevoirMessage('GUI Exemples préparer: ExempleFenêtre'.encode(),démarrerFenêtre)
            def valeurCliquer(positionHorizontal,positionVertical):
                for bouton in (1,0):client.sendall(struct.pack('>BBHH',5,bouton,positionHorizontal,positionVertical))
            time.sleep(.3)
            imagePrécédentÉlément=Image.frombytes('RGB',(640,480),bytes(listePixels()))
            valeurCliquer(160,196)
            for _ in range(2):valeurEnfoncé(0xff08);valeurEnfoncé(0xff08,False)
            for valeurCaractère in '한글':valeurEnfoncé(0x1000000|ord(valeurCaractère));valeurEnfoncé(0x1000000|ord(valeurCaractère),False)
            for nombreÉlémentsRépétition in (1,2):
                lancer=len(transcription);valeurCliquer(180,242)
                recevoirMessage(('GUI Salutation: 안녕하세요, 한글님! ('+str(nombreÉlémentsRépétition)+')').encode(),lancer)
            time.sleep(.3)
            dessinFenêtre=Image.frombytes('RGB',(640,480),bytes(listePixels()))
            assert imagePrécédentÉlément.crop((110,272,530,300)).tobytes()!=dessinFenêtre.crop((110,272,530,300)).tobytes()
            dessinFenêtre.save(str(donnéesRésultat/'java-swing.png'))
            lancer=len(transcription);valeurCliquer(535,105)
            assert 'exit 0' in recevoirMessage(b'jkoros-native> ',lancer)
        # Download the guest-created bytes through FTP in the same GUI VM.
        nomEntréeÉlémentFichier={'java':'java.txt','c':'c.txt','python':'python.txt'}[Langue]
        interpréteurCommandes('cp '+nomEntréeÉlémentFichier+' /valider.txt')
        nombreÉlémentsReçu=bytearray();connexionTransfertFichier.retrbinary('RETR valider.txt',nombreÉlémentsReçu.extend);assert nombreÉlémentsReçu==fichierAttendu.encode()
        interpréteurCommandes('echo preserved > ExempleSortie.'+('py' if Langue=='python' else Langue))
        assert 'EXAMPLES READY' in interpréteurCommandes('example '+Langue)
        assert '\npreserved\n' in interpréteurCommandes('cat ExempleSortie.'+('py' if Langue=='python' else Langue))
        assert '한/opérandeZéro valeurTouche, Shift+Space 또는 F9' in interpréteurCommandes('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in interpréteurCommandes('echo GUI NETWORK TOGETHER')
        connexionTransfertFichier.quit();connexionTransfertFichier=None;assert 'FTP stopped' in interpréteurCommandes('ftpd stop')
        print('PASS '+Langue+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if connexionTransfertFichier:
            try:connexionTransfertFichier.close()
            except OSError:pass
        if client:client.close()
        processus.terminate()
        try:processus.wait(timeout=8)
        except subprocess.TimeoutExpired:processus.kill();processus.wait()
        sélecteur.close();processus.stdout.close();(donnéesRésultat/(Langue+'-serial.log')).write_bytes(transcription)


def lancer():
    donnéesRésultat=racineProjet/'build/verification/examples';donnéesRésultat.mkdir(parents=True,exist_ok=True)
    rapportValidation={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((racineProjet/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with ServeursRépercuter() as entréeÉlémentServeurRépercuter:
            for Langue in ('java','c','python'):
                testLangue(Langue,entréeÉlémentServeurRépercuter,donnéesRésultat);rapportValidation['languages'].append(Langue)
            attendu=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert entréeÉlémentServeurRépercuter.possèdeReçu==[(valeurCatégorie,Données.encode()) for valeurCatégorie,Données in attendu],entréeÉlémentServeurRépercuter.possèdeReçu
            rapportValidation['host_network_payloads']=[{'protocol':valeurCatégorie,'text':Données.decode()} for valeurCatégorie,Données in entréeÉlémentServeurRépercuter.possèdeReçu]
        rapportValidation.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(donnéesRésultat/'report.json').write_text(json.dumps(rapportValidation,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':lancer()
