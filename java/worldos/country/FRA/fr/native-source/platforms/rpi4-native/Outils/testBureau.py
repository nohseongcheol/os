#!/usr/bin/env python3
"""donnéesEffectif RFB 클라이언트로 QEMU 창의 한글/valeurTouche/클립보드/마우스와 Écran 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from vueBureau import valeurExact
from exécuterCommande import racineProjet


def lancer():
    sortie=racineProjet/'build/verification/desktop'; sortie.mkdir(parents=True,exist_ok=True)
    processus=subprocess.Popen(['python3',str(racineProjet/'Outils/vueBureau.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    moniteurDisponibilitéÉtat=selectors.DefaultSelector(); moniteurDisponibilitéÉtat.register(processus.stdout,selectors.EVENT_READ)
    transcription=bytearray(); rapportValidation={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((racineProjet/'build/kernel8.img').read_bytes()).hexdigest()}
    def jusquÀ(marqueur,lancer=0):
        tempsÉchéance=time.monotonic()+45
        while marqueur not in transcription[lancer:]:
            if time.monotonic()>tempsÉchéance or processus.poll() is not None: raise AssertionError(transcription[lancer:].decode('utf-8','replace'))
            for valeurEnfoncé,_ in moniteurDisponibilitéÉtat.select(.1):
                Données=valeurEnfoncé.fileobj.read(4096)
                if Données: transcription.extend(Données)
        return bytes(transcription[lancer:])
    try:
        jusquÀ(b'TERMINAL READY')
        numéroPort=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transcription).group(1))
        with socket.create_connection(('127.0.0.1',numéroPort),timeout=10) as client:
            assert valeurExact(client,12)==b'RFB 003.008\n'; client.sendall(b'RFB 003.008\n')
            assert 1 in valeurExact(client,valeurExact(client,1)[0]); client.sendall(b'\x01'); assert valeurExact(client,4)==b'\0'*4
            client.sendall(b'\x01'); valeurInitialValeur=valeurExact(client,24); assert struct.unpack('>HH',valeurInitialValeur[:4])==(640,480); valeurExact(client,struct.unpack('>I',valeurInitialValeur[20:])[0])
            client.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            client.sendall(struct.pack('>BBHi',2,0,1,0))
            def valeurEnfoncé(valeurSymbole,estEnfoncementEnCours=True): client.sendall(struct.pack('>BBHI',4,int(estEnfoncementEnCours),0,valeurSymbole))
            def caractèreSaisi(texte):
                for donnéesCaractère in texte:
                    symbole=0xff0d if donnéesCaractère=='\n' else ord(donnéesCaractère) if ord(donnéesCaractère)<256 else 0x01000000|ord(donnéesCaractère)
                    valeurEnfoncé(symbole); valeurEnfoncé(symbole,False)
            def toucheEnfoncer(valeurSymbole): valeurEnfoncé(valeurSymbole); valeurEnfoncé(valeurSymbole,False)
            # Start with English keys only, as delivered without a host IME.
            valeurDécalage=len(transcription); caractèreSaisi('echo '); toucheEnfoncer(0xffc6)
            caractèreSaisi('dkssudgktpdy gksrmf'); toucheEnfoncer(0xffc6); caractèreSaisi('\n')
            jusquÀ('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),valeurDécalage)
            valeurDécalage=len(transcription); caractèreSaisi('echo ')
            valeurEnfoncé(0xffe1); toucheEnfoncer(32); valeurEnfoncé(0xffe1,False)
            caractèreSaisi('dlfr'); toucheEnfoncer(0xff08); toucheEnfoncer(0xff08); caractèreSaisi('fr')
            toucheEnfoncer(0xff31); caractèreSaisi(' EN\n')
            jusquÀ('\r\n읽 EN\r\njkoros-native> '.encode(),valeurDécalage)
            valeurDécalage=len(transcription); caractèreSaisi('echo '); toucheEnfoncer(0xff31)
            caractèreSaisi('rhk rkqtk RkRnd'); toucheEnfoncer(0xff31); caractèreSaisi('\n')
            jusquÀ('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),valeurDécalage)
            # The same composition edits UTF-8 text in the native vi editor.
            valeurDécalage=len(transcription); caractèreSaisi('vi entréeHangul.txt\n'); jusquÀ(b'NORMAL',valeurDécalage)
            caractèreSaisi('i'); toucheEnfoncer(0xffc6); caractèreSaisi('gksrmf dlfr'); toucheEnfoncer(0xffc6)
            toucheEnfoncer(0xff1b); caractèreSaisi(':wq\n'); jusquÀ(b'jkoros-native> ',valeurDécalage)
            valeurDécalage=len(transcription); caractèreSaisi('cat entréeHangul.txt\n')
            jusquÀ('한글 읽'.encode(),valeurDécalage); jusquÀ(b'jkoros-native> ',valeurDécalage)
            valeurDécalage=len(transcription); caractèreSaisi('help ko\n')
            jusquÀ('한/opérandeZéro valeurTouche, Shift+Space 또는 F9'.encode(),valeurDécalage); jusquÀ(b'jkoros-native> ',valeurDécalage)
            valeurDécalage=len(transcription); caractèreSaisi('clear\necho "VNC 한글 valeurEntrée 😀"\n'); jusquÀ('VNC 한글 valeurEntrée 😀\r\n'.encode(),valeurDécalage)
            valeurDécalage=len(transcription); valeurEnfoncé(0xffe3); valeurEnfoncé(ord('u')); valeurEnfoncé(ord('u'),False); valeurEnfoncé(0xffe3,False); caractèreSaisi('echo CONTROL_OK\n'); jusquÀ(b'\r\nCONTROL_OK\r\n',valeurDécalage)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            valeurPressePapiers='echo "valeurColler estTerminé"\n'.encode(); valeurDécalage=len(transcription)
            client.sendall(struct.pack('>B3xI',6,len(valeurPressePapiers))+valeurPressePapiers)
            for évènement,_ in moniteurDisponibilitéÉtat.select(.15):
                blocDonnées=évènement.fileobj.read(4096)
                if blocDonnées: transcription.extend(blocDonnées)
            assert 'valeurColler estTerminé'.encode() not in transcription[valeurDécalage:]
            valeurEnfoncé(0xffe3); valeurEnfoncé(0xffe1); valeurEnfoncé(ord('v')); valeurEnfoncé(ord('v'),False); valeurEnfoncé(0xffe1,False); valeurEnfoncé(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            jusquÀ('\r\n붙여넣기 estTerminé\r\njkoros-native> '.encode(),valeurDécalage)
            client.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            couleurRGB=bytearray(640*480*3); entréesListeVu=False
            while not entréesListeVu:
                texteNotification=valeurExact(client,1)[0]
                if texteNotification==2: continue
                if texteNotification==3:
                    taille=struct.unpack('>I',valeurExact(client,7)[3:])[0]; valeurExact(client,taille); continue
                assert texteNotification==0,texteNotification
                listeRectangles=struct.unpack('>H',valeurExact(client,3)[1:])[0]
                for _ in range(listeRectangles):
                    coordonnéeCoordonnéeHorizontale,coordonnéeCoordonnéeVerticale,valeurLargeurDemandé,valeurHauteurDemandé,jeuCaractères=struct.unpack('>HHHHi',valeurExact(client,12)); assert jeuCaractères==0,jeuCaractères
                    listePixels=valeurExact(client,valeurLargeurDemandé*valeurHauteurDemandé*4)
                    for ordinalInterne in range(valeurHauteurDemandé):
                        for indiceOrdinal in range(valeurLargeurDemandé):
                            adresseOriginal=(ordinalInterne*valeurLargeurDemandé+indiceOrdinal)*4; adresseDestination=((coordonnéeCoordonnéeVerticale+ordinalInterne)*640+coordonnéeCoordonnéeHorizontale+indiceOrdinal)*3
                            couleurRGB[adresseDestination:adresseDestination+3]=bytes((listePixels[adresseOriginal+2],listePixels[adresseOriginal+1],listePixels[adresseOriginal]))
                    entréesListeVu=True
            assert couleurRGB[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (sortie/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+couleurRGB)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(couleurRGB)).save(str(sortie/'vnc-terminal.png'))
            valeurDécalage=len(transcription)
            valeurEnfoncé(0xffe3); valeurEnfoncé(0xffe1); valeurEnfoncé(ord('t')); valeurEnfoncé(ord('t'),False); valeurEnfoncé(0xffe1,False); valeurEnfoncé(0xffe3,False)
            jusquÀ(b'TERMINAL FOCUS 2',valeurDécalage)
            valeurDécalage=len(transcription); caractèreSaisi('echo SECOND_VNC_WINDOW\n'); jusquÀ(b'\r\nSECOND_VNC_WINDOW\r\n',valeurDécalage)
            valeurDécalage=len(transcription); client.sendall(struct.pack('>BBHH',5,1,576,81)); client.sendall(struct.pack('>BBHH',5,0,576,81)); jusquÀ(b'TERMINAL FOCUS 1',valeurDécalage)
            valeurDécalage=len(transcription); caractèreSaisi('python -c \'print("x"*9000)\'\n'); jusquÀ(b'\r\njkoros-native> ',valeurDécalage)
            assert len(transcription)-valeurDécalage>8192,'exercise output longer than bridge status buffer'
            valeurDécalage=len(transcription); client.sendall(struct.pack('>BBHH',5,1,560,63)); client.sendall(struct.pack('>BBHH',5,0,560,63)); jusquÀ(b'TERMINAL FOCUS 1',valeurDécalage)
            valeurDécalage=len(transcription); client.sendall(struct.pack('>BBHH',5,1,80,16)); client.sendall(struct.pack('>BBHH',5,0,80,16)); jusquÀ(b'TERMINAL FOCUS 1',valeurDécalage)
            valeurDécalage=len(transcription); caractèreSaisi('echo REOPENED_VNC_WINDOW\n'); jusquÀ(b'\r\nREOPENED_VNC_WINDOW\r\n',valeurDécalage)
            valeurDécalage=len(transcription); caractèreSaisi('gui\n'); jusquÀ(b'GUI READY:',valeurDécalage)
            valeurDécalage=len(transcription); client.sendall(struct.pack('>BBHH',5,1,80,332)); client.sendall(struct.pack('>BBHH',5,0,80,332)); jusquÀ(b'TERMINAL READY',valeurDécalage)
            rapportValidation.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+espace and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if processus.poll() is None:
            processus.terminate()
            try: processus.wait(timeout=8)
            except subprocess.TimeoutExpired: processus.kill(); processus.wait()
        moniteurDisponibilitéÉtat.close(); processus.stdout.close()
        (sortie/'serial.log').write_bytes(transcription)
        (sortie/'report.json').write_text(json.dumps(rapportValidation,indent=2)+'\n')


if __name__=='__main__': lancer()
