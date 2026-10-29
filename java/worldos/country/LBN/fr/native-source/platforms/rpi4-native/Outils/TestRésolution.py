#!/usr/bin/env python3
"""donnéesEffectif QEMU/VNC에서 Écran taille·valeurFrontière·fenêtre valeurDéplacer·Swing·언어별 그리기를 검사한다."""
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


def TestRésolution(valeurLargeur, valeurHauteur, cheminRésultat):
    with socket.socket() as valeurTemporaire:
        valeurTemporaire.bind(('127.0.0.1', 0)); numéroPort = valeurTemporaire.getsockname()[1]
    texteTaille = '{}x{}'.format(valeurLargeur, valeurHauteur)
    valeurProcessus = subprocess.Popen(['python3', str(racineProjet/'Outils/exécuterCommande.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(numéroPort), '--resolution', texteTaille], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    Sélecteur = selectors.DefaultSelector(); Sélecteur.register(valeurProcessus.stdout, selectors.EVENT_READ)
    enregistrementJournal = bytearray(); valeurDistant = None; valeurTransfert = None

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

    def interpréteurCommandes(texte): return attendreFin(b'\r\n__RESOLUTION_DONE__\r\n', envoyerTexte(texte+'; echo __RESOLUTION_DONE__\n'))

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
        valeurDistant.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        contrôlerPixel((valeurLargeur-1, valeurHauteur-1), (24, 32, 48))
        # Écran droit 아래까지 이동한다. élémentListePrécédentÉlément 640×480 valeurFrontière 밖에서 X를 누른다.
        àPositionPoint(40, 60, 1); àPositionPoint(valeurLargeur-568+28, valeurHauteur-360+12, 1); àPositionPoint(valeurLargeur-568+28, valeurHauteur-360+12, 0)
        contrôlerPixel((valeurLargeur-568, valeurHauteur-360), (32, 80, 144))
        lancer = len(enregistrementJournal); valeurCliquer(valeurLargeur-20, valeurHauteur-345); attendreFin(b'TERMINAL FOCUS 1', lancer)
        contrôlerPixel((valeurLargeur-568, valeurHauteur-360), (24, 32, 48))
        lancer = len(enregistrementJournal); valeurCliquer(80, 16); attendreFin(b'TERMINAL FOCUS 1', lancer)
        interpréteurCommandes('ftpd start')
        valeurTransfert = ftplib.FTP(); valeurTransfert.encoding = 'utf-8'; valeurTransfert.connect('127.0.0.1', numéroPort, timeout=20); valeurTransfert.login()
        # C valeurFrontière 검사는 32비트 unsigned valeurNégatif convertirValeur·rogner 밖·빈 사각형을 포함한다.
        source = '''#include <ABIÉcran.h>
#include <ABIFichier.h>
int main(void) {
    unsigned valeurLargeur=largeurÉcran(), valeurHauteur=hauteurÉcran();
    if(valeurLargeur!=WIDTH || valeurHauteur!=HEIGHT) return 1;
    if(dessinerRectangle(valeurLargeur,valeurHauteur,0,0,0)) return 2;
    if(dessinerRectangle(valeurLargeur,valeurHauteur-1,1,1,0)!=-22) return 3;
    if(dessinerRectangle(valeurLargeur-1,valeurHauteur,1,1,0)!=-22) return 4;
    if(dessinerRectangle(-1,0,1,1,0)!=-22) return 5;
    if(dessinerRectangle(0,0,-1,1,0)!=-22) return 6;
    if(dessinerRectangle(valeurLargeur-1,valeurHauteur-1,1,1,0x332211)) return 7;
    écrireDonnéesFichier(1,"C RESOLUTION PASS\\n",18);
    attendreDessinPour(); return 0;
}
'''.replace('WIDTH', str(valeurLargeur)).replace('HEIGHT', str(valeurHauteur))
        fichiersTéléverser('testÉcran.c', source.encode())
        assert 'exit 0' in interpréteurCommandes('cc /testÉcran.c -o /testÉcran')
        attendreFin(b'C RESOLUTION PASS', envoyerTexte('run /testÉcran\n'))
        contrôlerPixel((valeurLargeur-1, valeurHauteur-1), (17, 34, 51))
        attendreFin(b'jkoros-native> ', envoyerTexte('q'))
        source = '''from français import tailleÉcran, dessinerRectangle, attendreDessinPour, Sortie, ErreurSystème
valeurLargeur, valeurHauteur = tailleÉcran()
assert (valeurLargeur, valeurHauteur) == (WIDTH, HEIGHT)
try:
    dessinerRectangle(valeurLargeur, valeurHauteur-1, 1, 1, 0)
    raise AssertionError("boundary")
except ErreurSystème as erreur:
    assert erreur.numéro == 22
dessinerRectangle(valeurLargeur-1, valeurHauteur-1, 1, 1, 0x665544)
Sortie("PYTHON RESOLUTION PASS")
attendreDessinPour()
'''.replace('WIDTH', str(valeurLargeur)).replace('HEIGHT', str(valeurHauteur))
        fichiersTéléverser('testÉcran.py', source.encode())
        attendreFin(b'PYTHON RESOLUTION PASS', envoyerTexte('python /testÉcran.py\n'))
        contrôlerPixel((valeurLargeur-1, valeurHauteur-1), (68, 85, 102))
        attendreFin(b'jkoros-native> ', envoyerTexte('q'))
        source = '''import français.interne.*;
public class TestRésolution {
    public static void main(String[] arguments) {
        int valeurLargeur=Écran.valeurLargeur(), valeurHauteur=Écran.valeurHauteur();
        if (valeurLargeur!=WIDTH || valeurHauteur!=HEIGHT) throw new ExceptionÉtatValeur("taille");
        try { Écran.rectangle(valeurLargeur,valeurHauteur-1,1,1,0); throw new ExceptionÉtatValeur("rogner"); }
        catch (ExceptionArgumentInvalide erreur) { }
        Écran.effacerEntréeÉlément(0x302018);
        Écran.rectangle(valeurLargeur-1,valeurHauteur-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        Écran.attendreFin();
    }
}
'''.replace('WIDTH', str(valeurLargeur)).replace('HEIGHT', str(valeurHauteur))
        # exception 처리는 Hôte javac 결과를 interne JVM에 올려 검사한다.
        sourceFrontière = cheminRésultat/'해상도경계시험.java'
        sourceFrontière.write_text(source.replace('class TestRésolution', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(racineProjet/'dist/jkoros-native-korean.jar'), '-d', str(cheminRésultat), str(sourceFrontière)])
        fichiersTéléverser('해상도경계시험.class', (cheminRésultat/'해상도경계시험.class').read_bytes())
        attendreFin(b'JAVA RESOLUTION PASS', envoyerTexte('java 해상도경계시험\n'))
        contrôlerPixel((valeurLargeur-1, valeurHauteur-1), (119, 136, 153))
        attendreFin(b'jkoros-native> ', envoyerTexte('q'))
        # 게스트 javac의 valeurPriseEnCharge 문법으로 taille valeurInterroger·effacerEntréeÉlément·다섯 arguments 그리기를 컴파일한다.
        source = '''public class TestRésolution {
    public static void main(String[] arguments) {
        int valeurLargeur=français.interne.Écran.valeurLargeur();
        int valeurHauteur=français.interne.Écran.valeurHauteur();
        if (valeurLargeur!=WIDTH || valeurHauteur!=HEIGHT) return;
        français.interne.Écran.effacerEntréeÉlément(3153944);
        français.interne.Écran.rectangle(valeurLargeur-1,valeurHauteur-1,1,1,10061943);
        français.interne.Sortie.écrireLigne("JAVA RESOLUTION PASS");
        français.interne.Écran.attendreFin();
    }
}
'''.replace('WIDTH', str(valeurLargeur)).replace('HEIGHT', str(valeurHauteur))
        fichiersTéléverser('TestRésolution.java', source.encode())
        résultat = interpréteurCommandes('javac TestRésolution.java'); assert 'exit 0' in résultat, résultat
        attendreFin(b'JAVA RESOLUTION PASS', envoyerTexte('java TestRésolution\n'))
        contrôlerPixel((valeurLargeur-1, valeurHauteur-1), (119, 136, 153))
        attendreFin(b'jkoros-native> ', envoyerTexte('q'))
        fichiersTéléverser('TestSwing.class', (cheminRésultat/'TestSwing.class').read_bytes())
        attendreFin(b'SWING READY', envoyerTexte('java TestSwing\n'))
        positionHorizontal, positionVertical = (valeurLargeur-400)//2, (valeurHauteur-280)//2
        Dessin = contrôlerPixel((positionHorizontal, positionVertical), (32, 80, 144))
        Dessin.save(str(cheminRésultat/(texteTaille+'.png')))
        lancer = len(enregistrementJournal); valeurCliquer(positionHorizontal+80, positionVertical+155)
        attendreFin('SWING CLICK nom'.encode(), lancer)
        lancer = len(enregistrementJournal); valeurCliquer(positionHorizontal+385, positionVertical+15); attendreFin(b'jkoros-native> ', lancer)
        assert 'AFTER_RESOLUTION' in interpréteurCommandes('echo AFTER_RESOLUTION')
        print('PASS:', texteTaille, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if valeurTransfert: valeurTransfert.close()
        if valeurDistant: valeurDistant.close()
        if valeurProcessus.poll() is None:
            valeurProcessus.terminate()
            try: valeurProcessus.wait(timeout=8)
            except subprocess.TimeoutExpired: valeurProcessus.kill(); valeurProcessus.wait()
        Sélecteur.close(); valeurProcessus.stdout.close()
        (cheminRésultat/(texteTaille+'.log')).write_bytes(enregistrementJournal)


def lancer():
    cheminRésultat = racineProjet/'build/verification/resolution'; cheminRésultat.mkdir(parents=True, exist_ok=True)
    enregistrementJournal = {'passed': False, 'kernel_sha256': hashlib.sha256((racineProjet/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for valeurInvalide in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            résultat = subprocess.run(['python3', str(racineProjet/'Outils/exécuterCommande.py'), '--resolution', valeurInvalide], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert résultat.returncode == 2 and b'--resolution' in résultat.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(cheminRésultat), str(racineProjet/'Tests/Java/TestSwing.java')])
        for valeurLargeur, valeurHauteur in ((1920,1080), (1280,720), (640,480)):
            TestRésolution(valeurLargeur, valeurHauteur, cheminRésultat); enregistrementJournal['resolutions'].append([valeurLargeur, valeurHauteur])
        enregistrementJournal.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (cheminRésultat/'report.json').write_text(json.dumps(enregistrementJournal, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': lancer()
