#!/usr/bin/env python3
"""donnéesEffectif QEMU/VNC에서 terminal valeurCoin valeurGlisser·pointeur·동적 valeurCaractère entréeÉlémentEmplacement·valeurÉditer valeurContenuValeur 보존를 검사한다."""
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
from PIL import Image
from vueBureau import valeurExact
from exécuterCommande import racineProjet


def testRedimensionnementFenêtre(valeurLargeur, valeurHauteur, cheminRésultat):
    with socket.socket() as valeurTemporaire:
        valeurTemporaire.bind(('127.0.0.1', 0)); numéroPort = valeurTemporaire.getsockname()[1]
    texteTaille = '{}x{}'.format(valeurLargeur, valeurHauteur)
    valeurProcessus = subprocess.Popen(['python3', str(racineProjet/'Outils/exécuterCommande.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(numéroPort), '--resolution', texteTaille], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    Sélecteur = selectors.DefaultSelector(); Sélecteur.register(valeurProcessus.stdout, selectors.EVENT_READ)
    enregistrementJournal = bytearray(); valeurDistant = None; valeurTransfert = None; cachéPointeur=[False]

    def attendreFin(afficherValeur, lancer=0):
        valeurÉchéance = time.monotonic() + 60
        while afficherValeur not in enregistrementJournal[lancer:]:
            if time.monotonic() > valeurÉchéance or valeurProcessus.poll() is not None or b'HALTED' in enregistrementJournal or b'PANIC:' in enregistrementJournal:
                raise AssertionError(enregistrementJournal[lancer:].decode('utf-8', 'replace'))
            for évènement, _ in Sélecteur.select(.1):
                Données = évènement.fileobj.read(65536)
                if Données: enregistrementJournal.extend(Données)
        return enregistrementJournal[lancer:].decode('utf-8', 'replace')

    def boutonCliquer(symbole, estEnfoncé=True): valeurDistant.sendall(struct.pack('>BBHI', 4, int(estEnfoncé), 0, symbole))

    def envoyerTexte(texte):
        lancer = len(enregistrementJournal)
        for valeurCaractère in texte:
            symbole = 0xff0d if valeurCaractère == '\n' else ord(valeurCaractère) if ord(valeurCaractère) < 256 else 0x1000000 | ord(valeurCaractère)
            boutonCliquer(symbole); boutonCliquer(symbole, False)
        return lancer

    def interpréteurCommandes(texte): return attendreFin(b'\r\n__RESIZE_DONE__\r\n', envoyerTexte(texte+'; echo __RESIZE_DONE__\n'))

    def àPositionPoint(positionHorizontal, positionVertical, estEnfoncé): valeurDistant.sendall(struct.pack('>BBHH', 5, estEnfoncé, positionHorizontal, positionVertical))

    def valeurCliquer(positionHorizontal, positionVertical): àPositionPoint(positionHorizontal, positionVertical, 1); àPositionPoint(positionHorizontal, positionVertical, 0)

    def imageMatriceBits():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 donnéesEffectif 너비를 쓴다.
        valeurDistant.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, valeurLargeur, valeurHauteur))
        Dessin = Image.new('RGB', (valeurLargeur, valeurHauteur)); valeurAire = 0
        while True:
            valeurGenre = valeurExact(valeurDistant, 1)[0]
            if valeurGenre == 2: continue
            if valeurGenre == 3:
                longueur = struct.unpack('>I', valeurExact(valeurDistant, 7)[3:])[0]; valeurExact(valeurDistant, longueur); continue
            assert valeurGenre == 0, valeurGenre
            nombreÉlémentsÉlémentListe = struct.unpack('>H', valeurExact(valeurDistant, 3)[1:])[0]
            for _ in range(nombreÉlémentsÉlémentListe):
                positionHorizontal, positionVertical, étendueLargeur, longueur, valeurEncodage = struct.unpack('>HHHHi', valeurExact(valeurDistant, 12))
                if valeurEncodage == -239:
                    assert étendueLargeur==0 and longueur==0, 'remote cursor must be hidden'
                    cachéPointeur[0]=True
                    continue
                assert valeurEncodage == 0 and positionHorizontal+étendueLargeur <= valeurLargeur and positionVertical+longueur <= valeurHauteur
                Dessin.paste(Image.frombytes('RGB', (étendueLargeur, longueur), valeurExact(valeurDistant, étendueLargeur*longueur*4), 'raw', 'BGRX'), (positionHorizontal, positionVertical))
                valeurAire += étendueLargeur*longueur
            if valeurAire:
                assert valeurAire == valeurLargeur*valeurHauteur, valeurAire
                return Dessin

    def contrôlerPixel(valeurCoordonnée, valeurCouleur):
        valeurÉchéance = time.monotonic()+10
        while True:
            Dessin = imageMatriceBits()
            if Dessin.getpixel(valeurCoordonnée) == valeurCouleur: return Dessin
            if time.monotonic() > valeurÉchéance: raise AssertionError((valeurCoordonnée, Dessin.getpixel(valeurCoordonnée), valeurCouleur))

    def fichiersTéléverser(nom, Données): valeurTransfert.storbinary('STOR '+nom, io.BytesIO(Données))

    try:
        attendreFin(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+texteTaille+' RGB32').encode() in enregistrementJournal
        print('BOOT:', texteTaille, flush=True)
        numéroDistant = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', enregistrementJournal).group(1))
        valeurDistant = socket.create_connection(('127.0.0.1', numéroDistant), timeout=20)
        assert valeurExact(valeurDistant, 12) == b'RFB 003.008\n'; valeurDistant.sendall(b'RFB 003.008\n')
        assert 1 in valeurExact(valeurDistant, valeurExact(valeurDistant, 1)[0]); valeurDistant.sendall(b'\x01')
        assert valeurExact(valeurDistant, 4) == b'\0'*4; valeurDistant.sendall(b'\x01')
        étatValeurInitialValeur = valeurExact(valeurDistant, 24); assert struct.unpack('>HH', étatValeurInitialValeur[:4]) == (valeurLargeur, valeurHauteur)
        valeurExact(valeurDistant, struct.unpack('>I', étatValeurInitialValeur[20:])[0])
        valeurDistant.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        valeurDistant.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        contrôlerPixel((valeurLargeur-1, valeurHauteur-1), (24, 32, 48))
        def brièvementMettreEnPause(valeurSecondes=.25):
            terminaison=time.monotonic()+valeurSecondes
            while time.monotonic()<terminaison:
                for évènement,_ in Sélecteur.select(.02):
                    Données=évènement.fileobj.read(65536)
                    if Données:enregistrementJournal.extend(Données)
        fenêtre=[12,48,568,360]
        def vérifierTaille():
            valeurColonne,valeurRangée=(fenêtre[2]-24)//8,(fenêtre[3]-56)//16
            texte=interpréteurCommandes('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(valeurColonne,valeurRangée) in texte,texte
            # donnéesEffectif fenêtre 테두리: 단지 taille valeurInterroger 값만 바뀐 것이 아닌지 확인한다.
            àPositionPoint(valeurLargeur-1,10,0);brièvementMettreEnPause()
            contrôlerPixel((fenêtre[0],fenêtre[1]),(32,80,144))
            Dessin=contrôlerPixel((fenêtre[0]+fenêtre[2]-1,fenêtre[1]+fenêtre[3]-1),(39,49,64))
            return Dessin
        def valeurCoin(direction):
            return (fenêtre[0]+(3 if direction in (1,3) else fenêtre[2]-4),fenêtre[1]+(3 if direction<=2 else fenêtre[3]-4))
        def glisserRedimensionner(direction,valeurDifférence,bouton=1):
            opérandePremier,valeurTrois=valeurCoin(direction);àPositionPoint(opérandePremier,valeurTrois,0);brièvementMettreEnPause()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            pixelBlancCouleur=(opérandePremier-7 if direction in (1,4) else opérandePremier+7,valeurTrois-7)
            contrôlerPixel(pixelBlancCouleur,(255,255,255))
            àPositionPoint(opérandePremier,valeurTrois,bouton)
            horizontalFin=max(0,min(valeurLargeur-1,opérandePremier+valeurDifférence[0]));verticalFin=max(0,min(valeurHauteur-1,valeurTrois+valeurDifférence[1]))
            àPositionPoint(horizontalFin,verticalFin,bouton);àPositionPoint(horizontalFin,verticalFin,0);brièvementMettreEnPause()
            if bouton==1:
                valeurGauche,valeurSommet,étendueLargeur,longueur=fenêtre;valeurDroit,valeurBasExtrémité=valeurGauche+étendueLargeur,valeurSommet+longueur
                if direction in (1,3):valeurGauche=max(0,min(valeurDroit-360,valeurGauche+horizontalFin-opérandePremier))
                else:valeurDroit=max(valeurGauche+360,min(valeurLargeur,valeurDroit+horizontalFin-opérandePremier))
                if direction<=2:valeurSommet=max(34,min(valeurBasExtrémité-216,valeurSommet+verticalFin-valeurTrois))
                else:valeurBasExtrémité=max(valeurSommet+216,min(valeurHauteur,valeurBasExtrémité+verticalFin-valeurTrois))
                fenêtre[:]=[valeurGauche,valeurSommet,valeurDroit-valeurGauche,valeurBasExtrémité-valeurSommet]
        vérifierTaille();assert cachéPointeur[0]
        glisserRedimensionner(4,(-100,-60),4);vérifierTaille() # droit 버튼은 크기를 바꾸지 않는다.
        for direction,valeurDifférence in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            glisserRedimensionner(direction,valeurDifférence);vérifierTaille()
        # valeurEntrée 중인 긴 texteHangul 명령은 nouvelleLigne/positionHorizontal 스크롤과 무관하게 그대로 실행된다.
        texteLong='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        envoyerTexte("echo '"+texteLong+"'");brièvementMettreEnPause()
        glisserRedimensionner(4,(-1000,-1000));assert fenêtre[2:]==[360,216]
        glisserRedimensionner(4,(valeurLargeur,valeurHauteur))
        lancer=envoyerTexte('\n');attendreFin(('\r\n'+texteLong+'\r\n').encode(),lancer);vérifierTaille()
        # vi가 valeurÉditer 중에 Écran 크기를 valeurRéessayer 읽고, 저장하지 않은 한글도 유지한다.
        interpréteurCommandes('ftpd start')
        valeurTransfert=ftplib.FTP();valeurTransfert.encoding='utf-8';valeurTransfert.connect('127.0.0.1',numéroPort,timeout=20);valeurTransfert.login()
        attendreFin(b'NORMAL',envoyerTexte('vi /크기자료.txt\n'))
        attendreFin(b'INSERT',envoyerTexte('i미저장 한글 Données\n'));brièvementMettreEnPause()
        glisserRedimensionner(4,(-valeurLargeur,-valeurHauteur))
        # ANSI valeurRangée 이동에 새 valeurRangée 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((fenêtre[3]-56)//16)).encode() in enregistrementJournal[-4096:]
        envoyerTexte('작은 창에서도 valeurContinuation écrire\n');brièvementMettreEnPause()
        glisserRedimensionner(4,(valeurLargeur,valeurHauteur))
        envoyerTexte('큰 창에서도 valeurContinuation écrire\n');brièvementMettreEnPause()
        boutonCliquer(0xff1b);boutonCliquer(0xff1b,False);brièvementMettreEnPause()
        attendreFin(b'jkoros-native> ',envoyerTexte(':wq\n'))
        valeurContenuValeur=bytearray();valeurTransfert.retrbinary('RETR 크기자료.txt',valeurContenuValeur.extend)
        assert valeurContenuValeur=='미저장 한글 Données\n작은 창에서도 valeurContinuation écrire\n큰 창에서도 valeurContinuation écrire\n'.encode(),valeurContenuValeur
        vérifierTaille().save(str(cheminRésultat/(texteTaille+'-large.png')))
        # 두 번째 창은 valeurDéfaut taille, valeurRéessayer élémentListePremier 창을 고르면 앞에서 바꾼 크기가 유지된다.
        lancer=len(enregistrementJournal);valeurCliquer(70,16);attendreFin(b'TERMINAL FOCUS 2',lancer)
        assert 'TERMINAL SIZE 68x19' in interpréteurCommandes('terminal size')
        lancer=len(enregistrementJournal);valeurCliquer(180,16);attendreFin(b'TERMINAL FOCUS 1',lancer);vérifierTaille()
        glisserRedimensionner(4,(-valeurLargeur,-valeurHauteur));vérifierTaille().save(str(cheminRésultat/(texteTaille+'-small.png')))
        # taille changerValeur valeurRetourArrièreCôté X 닫기도 새로운 droit 가장자리를 사용한다.
        lancer=len(enregistrementJournal);valeurCliquer(fenêtre[0]+fenêtre[2]-20,fenêtre[1]+15);attendreFin(b'TERMINAL FOCUS 2',lancer)
        assert 'RESIZE CLOSED' in interpréteurCommandes('echo RESIZE CLOSED')
        print('PASS:',texteTaille,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if valeurTransfert:valeurTransfert.close()
        if valeurDistant:valeurDistant.close()
        if valeurProcessus.poll() is None:
            valeurProcessus.terminate()
            try:valeurProcessus.wait(timeout=8)
            except subprocess.TimeoutExpired:valeurProcessus.kill();valeurProcessus.wait()
        Sélecteur.close();valeurProcessus.stdout.close();(cheminRésultat/(texteTaille+'.log')).write_bytes(enregistrementJournal)


def lancer():
    cheminRésultat=racineProjet/'build/verification/resize';cheminRésultat.mkdir(parents=True,exist_ok=True)
    enregistrementJournal={'passed':False,'kernel_sha256':hashlib.sha256((racineProjet/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for valeurLargeur,valeurHauteur in ((640,480),(1920,1080)):
            testRedimensionnementFenêtre(valeurLargeur,valeurHauteur,cheminRésultat);enregistrementJournal['resolutions'].append([valeurLargeur,valeurHauteur])
        enregistrementJournal.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(cheminRésultat/'report.json').write_text(json.dumps(enregistrementJournal,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':lancer()
