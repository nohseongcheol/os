#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from exécuterCommande import racineProjet,commande

def lancer():
    positionValeurDestination=racineProjet/'build/verification/windows';positionValeurDestination.mkdir(parents=True,exist_ok=True)
    rapportValidation={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((racineProjet/'build/kernel8.img').read_bytes()).hexdigest()};enregistrementJournal=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as cheminTravailEnCours:
        connexionContrôleSimulacre=Path(cheminTravailEnCours)/'qmp.sock'
        positionDonnées=subprocess.Popen(commande()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(connexionContrôleSimulacre)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        Sélecteur=selectors.DefaultSelector();Sélecteur.register(positionDonnées.stdout,selectors.EVENT_READ)
        def évènementPoignée(unitéSecondes=.1):
            for valeurEnfoncé,_ in Sélecteur.select(unitéSecondes):
                valeurDeuxième=valeurEnfoncé.fileobj.read(65536)
                if valeurDeuxième:enregistrementJournal.extend(valeurDeuxième)
            assert b'PANIC:' not in enregistrementJournal and b'HALTED' not in enregistrementJournal,enregistrementJournal[-2048:]
        def attendreFin(marqueur,positionActuel,unitéSecondes=50):
            décalageFin=time.monotonic()+unitéSecondes
            while marqueur not in enregistrementJournal[positionActuel:]:
                if time.monotonic()>décalageFin or positionDonnées.poll() is not None:raise AssertionError(enregistrementJournal[positionActuel:].decode('utf-8','replace'))
                évènementPoignée()
            return bytes(enregistrementJournal[positionActuel:])
        def envoyer(valeurDeuxième,marqueur=b'jkoros-native> '):
            positionActuel=len(enregistrementJournal);positionDonnées.stdin.write(valeurDeuxième);positionDonnées.stdin.flush();return attendreFin(marqueur,positionActuel)
        def interpréteurCommandes(donnéesChaîne):return envoyer((donnéesChaîne+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def valeurRaccourci(indiceTroisième):return bytes([30,2,indiceTroisième,0,0,0,0])
        def boutonCliquer(coordonnéeCoordonnéeHorizontale,coordonnéeCoordonnéeVerticale):return bytes([30,1,1,coordonnéeCoordonnéeHorizontale&255,coordonnéeCoordonnéeHorizontale>>8,coordonnéeCoordonnéeVerticale&255,coordonnéeCoordonnéeVerticale>>8,30,1,0,coordonnéeCoordonnéeHorizontale&255,coordonnéeCoordonnéeHorizontale>>8,coordonnéeCoordonnéeVerticale&255,coordonnéeCoordonnéeVerticale>>8])
        def modeCommande():
            positionDonnées.stdin.write(b'\x1b');positionDonnées.stdin.flush();décalageFin=time.monotonic()+.2
            while time.monotonic()<décalageFin:évènementPoignée(.03)
        try:
            attendreFin(b'jkoros-native> ',0)
            interpréteurCommandes('terminal');évènementPoignée(.3)
            interpréteurCommandes('mkdir first; cd first; export NAME=one')
            envoyer('vi ordinalPremier.py\n'.encode(),b'NORMAL')
            envoyer('i값 = 21\nprint(valeur * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            décalageFin=time.monotonic()+3
            while time.monotonic()<décalageFin:évènementPoignée(.1)
            envoyer(valeurRaccourci(1),b'TERMINAL FOCUS 2');évènementPoignée(.2)
            assert b'/\r\n' in interpréteurCommandes('pwd')
            interpréteurCommandes('export NAME=two')
            envoyer('vi ordinalDeuxième.txt\n'.encode(),b'NORMAL')
            envoyer('i두 번째 fenêtre\n'.encode(),b'INSERT')
            envoyer(boutonCliquer(180,12),b'TERMINAL FOCUS 1');évènementPoignée(.2)
            modeCommande();envoyer(b':wq\r')
            assert b'one:/first' in interpréteurCommandes('echo "$NAME:$PWD"')
            assert 'valeur = 21\r\nprint(valeur * 2)'.encode() in interpréteurCommandes('cat ordinalPremier.py')
            résultat=interpréteurCommandes('python ordinalPremier.py');assert b'42\r\n' in résultat,résultat
            # Close the first shell with its actual title-bar X; second editor resumes.
            envoyer(boutonCliquer(560,63),b'TERMINAL FOCUS 2');évènementPoignée(.2)
            modeCommande();envoyer(b':wq\r')
            assert b'two:/' in interpréteurCommandes('echo "$NAME:$PWD"')
            assert '두 번째 fenêtre'.encode() in interpréteurCommandes('cat ordinalDeuxième.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            envoyer('vi ordinalDeuxième.txt\n'.encode(),b'NORMAL');envoyer(b'xu',b'NORMAL')
            envoyer(b'iX',b'INSERT');modeCommande();envoyer(b':q\r',b'Unsaved')
            envoyer(b':q!\r');assert '두 번째 fenêtre'.encode() in interpréteurCommandes('cat ordinalDeuxième.txt')
            envoyer(valeurRaccourci(1),b'TERMINAL FOCUS 1');évènementPoignée(.2)
            envoyer(valeurRaccourci(1),b'TERMINAL FOCUS 3');évènementPoignée(.2)
            envoyer(valeurRaccourci(1),b'TERMINAL FOCUS 4');évènementPoignée(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            positionDonnées.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));positionDonnées.stdin.flush()
            interpréteurCommandes('echo DRAGGED_OK')
            envoyer('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            envoyer('i저장하지 않은 Données'.encode(),b'INSERT')
            envoyer(boutonCliquer(578,97),b'TERMINAL FOCUS 3');évènementPoignée(.2)
            assert '버릴문서.txt'.encode() not in interpréteurCommandes('ls')
            envoyer(valeurRaccourci(1),b'TERMINAL FOCUS 4');évènementPoignée(.2)
            interpréteurCommandes('echo REUSED_WINDOW_OK')
            montantAchevé=enregistrementJournal.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            attendreFin(b'jkoros-native> ',montantAchevé)
            # UART completion precedes the next QEMU display refresh.
            décalageFin=time.monotonic()+.3
            while time.monotonic()<décalageFin:évènementPoignée(.05)
            with socket.socket(socket.AF_UNIX) as codeCaractère:
                codeCaractère.settimeout(10);codeCaractère.connect(str(connexionContrôleSimulacre))
                with codeCaractère.makefile('rwb') as entréeÉlémentFichier:
                    json.loads(entréeÉlémentFichier.readline())
                    for valeurRequête in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(positionValeurDestination/'four-terminals.png'),'format':'png'}}):
                        entréeÉlémentFichier.write((json.dumps(valeurRequête)+'\n').encode());entréeÉlémentFichier.flush()
                        while True:
                            valeurRetourné=json.loads(entréeÉlémentFichier.readline())
                            if 'error' in valeurRetourné:raise AssertionError(valeurRetourné)
                            if 'return' in valeurRetourné:break
            from PIL import Image
            listePixels=Image.open(str(positionValeurDestination/'four-terminals.png')).convert('RGB')
            for paireCoordonnée,couleurPixel in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert listePixels.getpixel(paireCoordonnée)==couleurPixel,(paireCoordonnée,listePixels.getpixel(paireCoordonnée))
            interpréteurCommandes('echo FOUR_WINDOWS_OK')
            rapportValidation.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if positionDonnées.poll() is None:positionDonnées.terminate()
            try:positionDonnées.wait(timeout=5)
            except subprocess.TimeoutExpired:positionDonnées.kill();positionDonnées.wait()
            Sélecteur.close();positionDonnées.stdin.close();positionDonnées.stdout.close();(positionValeurDestination/'serial.log').write_bytes(enregistrementJournal);(positionValeurDestination/'report.json').write_text(json.dumps(rapportValidation,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':lancer()
