#!/usr/bin/env python3
"""Exercise the installed Remmina in an isolated X display and D-Bus session.

Needs Remmina's VNC plugin, xdotool, Xvfb (or the existing ARM64 Xvfb rootfs
and qemu-aarch64), dbus-run-session, and ImageMagick import. Never uses :0.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import shutil
import subprocess
import tempfile
import time
from exécuterCommande import racineProjet


def lancer():
    donnéesRésultat=racineProjet/'build/verification/remmina';donnéesRésultat.mkdir(parents=True,exist_ok=True)
    rapportValidation={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((racineProjet/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as cheminTravailEnCours:
        cheminTravailEnCours=Path(cheminTravailEnCours);processusListeEnExécution=[];sélecteur=selectors.DefaultSelector();entréeSortieSériel=bytearray()
        enregistrementsJournal=[]
        try:
            présenterVirtuel=shutil.which('Xvfb')
            if présenterVirtuel: valeurServeur=[présenterVirtuel]
            else:
                systèmeFichiersRacine=racineProjet.parent/'rpi4/build/rootfs'
                valeurServeur=['qemu-aarch64','-L',str(systèmeFichiersRacine),str(systèmeFichiersRacine/'usr/bin/Xvfb')]
            def lancer(tableauArgument,environnement=None,**argumentNommé):
                enregistrementJournal=(donnéesRésultat/('process-%d.log'%len(enregistrementsJournal))).open('wb');enregistrementsJournal.append(enregistrementJournal)
                positionDonnées=subprocess.Popen(tableauArgument,env=environnement,stdout=enregistrementJournal,stderr=subprocess.STDOUT,**argumentNommé)
                processusListeEnExécution.append(positionDonnées);return positionDonnées
            environnement=dict(os.environ)
            for nom in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):environnement.pop(nom,None)
            environnement.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(cheminTravailEnCours/'config'),XDG_DATA_HOME=str(cheminTravailEnCours/'data'),XDG_CACHE_HOME=str(cheminTravailEnCours/'cache'))
            valeurNumérique=next(nombreÉlémentsÉlémentListe for nombreÉlémentsÉlémentListe in range(80,200) if not Path('/tmp/.X11-unix/X'+str(nombreÉlémentsÉlémentListe)).exists() and not Path('/tmp/.X%d-lock'%nombreÉlémentsÉlémentListe).exists())
            environnement['DISPLAY']=':'+str(valeurNumérique)
            périphériquePrésenter=lancer(valeurServeur+[environnement['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],environnement=environnement)
            tempsÉchéance=time.monotonic()+30
            while True:
                assert périphériquePrésenter.poll() is None and time.monotonic()<tempsÉchéance,'Xvfb failed; see process-0.log'
                terminéPréparation=subprocess.run(['xdotool','getdisplaygeometry'],env=environnement,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if terminéPréparation.returncode==0:break
                time.sleep(.1)
            invité=subprocess.Popen(['python3',str(racineProjet/'Outils/exécuterCommande.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            processusListeEnExécution.append(invité);sélecteur.register(invité.stdout,selectors.EVENT_READ)
            def attendreFin(marqueur,valeurDécalage=0):
                tempsÉchéance=time.monotonic()+45
                while marqueur not in entréeSortieSériel[valeurDécalage:]:
                    assert invité.poll() is None and time.monotonic()<tempsÉchéance,entréeSortieSériel[valeurDécalage:].decode('utf-8','replace')
                    for valeurEnfoncé,_ in sélecteur.select(.1):
                        Données=valeurEnfoncé.fileobj.read(65536)
                        if Données:entréeSortieSériel.extend(Données)
            attendreFin(b'TERMINAL READY');attendreFin(b'jkoros-native> ',entréeSortieSériel.rfind(b'TERMINAL READY'))
            numéroPort=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',entréeSortieSériel).group(1))
            profil=cheminTravailEnCours/'test.remmina'
            profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%numéroPort)
            lancer(['dbus-run-session','--','remmina','-c',str(profil)],environnement=environnement,start_new_session=True)
            def outilEntréeVirtuel(*tableauArgument):return subprocess.check_output(['xdotool']+list(tableauArgument),env=environnement,stderr=subprocess.STDOUT)
            tempsÉchéance=time.monotonic()+60;fenêtre=None
            while time.monotonic()<tempsÉchéance:
                chercherRésultat=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=environnement,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if chercherRésultat.returncode==0:
                    candidat=chercherRésultat.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    focalisé=subprocess.run(['xdotool','windowfocus','--sync',candidat],env=environnement,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if focalisé.returncode==0:fenêtre=candidat;break
                time.sleep(.1)
            assert fenêtre,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            outilEntréeVirtuel('mousemove','--window',fenêtre,'280','240','click','1')
            time.sleep(1)
            def caractèreSaisi(texte):outilEntréeVirtuel('type','--clearmodifiers','--delay','50',texte)
            def valeurEnfoncé(*touchesEnfoncé):outilEntréeVirtuel('key','--clearmodifiers',*touchesEnfoncé)
            valeurDécalage=len(entréeSortieSériel);caractèreSaisi('echo ');valeurEnfoncé('F9');caractèreSaisi('dkssudgktpdy gksrmf');valeurEnfoncé('F9','Return')
            attendreFin('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),valeurDécalage)
            valeurDécalage=len(entréeSortieSériel);caractèreSaisi('echo ');valeurEnfoncé('shift+space');caractèreSaisi('rhk rkqtk');valeurEnfoncé('shift+space','Return')
            attendreFin('\r\n과 갑사\r\njkoros-native> '.encode(),valeurDécalage)
            valeurDécalage=len(entréeSortieSériel);caractèreSaisi('help ko');valeurEnfoncé('Return')
            attendreFin('한/opérandeZéro valeurTouche, Shift+Space 또는 F9'.encode(),valeurDécalage);attendreFin(b'jkoros-native> ',valeurDécalage)
            valeurDécalage=len(entréeSortieSériel);caractèreSaisi('echo ');valeurEnfoncé('F9');caractèreSaisi('gksrmf dlfr')
            attendreFin('읽'.encode(),valeurDécalage)
            subprocess.check_call(['import','-display',environnement['DISPLAY'],'-window',fenêtre,str(donnéesRésultat/'remmina-korean.png')])
            valeurEnfoncé('F9','Return')
            attendreFin(b'jkoros-native> ',valeurDécalage)
            # donnéesEffectif Remmina의 Écran 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            Dessin=Image.open(str(donnéesRésultat/'remmina-korean.png')).convert('RGB')
            barreTitre=None
            for positionVertical in range(Dessin.height):
                positionsHorizontal=[positionHorizontal for positionHorizontal in range(Dessin.width) if Dessin.getpixel((positionHorizontal,positionVertical))==(32,80,144)]
                if len(positionsHorizontal)>=500:barreTitre=(min(positionsHorizontal),positionVertical);break
            assert barreTitre,'native terminal title bar not found'
            positionHorizontal,positionVertical=barreTitre[0]+564,barreTitre[1]+356
            outilEntréeVirtuel('mousemove','--window',fenêtre,str(positionHorizontal),str(positionVertical))
            def attendreMatriceBitsPour(nom,listePoints):
                valeurÉchéance=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',environnement['DISPLAY'],'-window',fenêtre,str(donnéesRésultat/nom)])
                    imageMatriceBits=Image.open(str(donnéesRésultat/nom)).convert('RGB')
                    if all(imageMatriceBits.getpixel(position)==Couleur for position,Couleur in listePoints):return
                    assert time.monotonic()<valeurÉchéance,'Remmina framebuffer did not settle: '+nom
                    time.sleep(.1)
            attendreMatriceBitsPour('remmina-resize-cursor.png',[
                ((positionHorizontal-7,positionVertical-7),(255,255,255)),((positionHorizontal+7,positionVertical+7),(255,255,255))])
            outilEntréeVirtuel('mousedown','1','mousemove','--window',fenêtre,str(positionHorizontal-120),str(positionVertical-80),'mouseup','1')
            time.sleep(.4)
            valeurDécalage=len(entréeSortieSériel);caractèreSaisi('terminal size');valeurEnfoncé('Return')
            attendreFin(b'TERMINAL SIZE 53x14\r\n',valeurDécalage)
            outilEntréeVirtuel('mousemove','--window',fenêtre,'500','45')
            attendreMatriceBitsPour('remmina-resized.png',[
                ((barreTitre[0]+447,barreTitre[1]+279),(39,49,64)),((positionHorizontal,positionVertical),(24,32,48))])
            if shutil.which('dpkg-query'):
                numéroVersion=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                numéroVersion=subprocess.check_output(['remmina','--version'],env=environnement,stderr=subprocess.STDOUT).decode('utf-8','replace')
            rapportValidation.update(passed=True,display=environnement['DISPLAY'],remmina_version=numéroVersion,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not rapportValidation['passed'] and 'environnement' in locals() and environnement.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',environnement['DISPLAY'],'-window','root',str(donnéesRésultat/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for positionDonnées in reversed(processusListeEnExécution):
                if positionDonnées.poll() is None:
                    if positionDonnées.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(positionDonnées.pid,signal.SIGTERM)
                    else:positionDonnées.terminate()
                    try:positionDonnées.wait(timeout=5)
                    except subprocess.TimeoutExpired:positionDonnées.kill();positionDonnées.wait()
            sélecteur.close()
            for entréeÉlémentFichier in enregistrementsJournal:entréeÉlémentFichier.close()
            (donnéesRésultat/'serial.log').write_bytes(entréeSortieSériel)
            (donnéesRésultat/'report.json').write_text(json.dumps(rapportValidation,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':lancer()
