#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from exécuterCommande import racineProjet,commande

def lancer():
    positionValeurDestination=racineProjet/'build/verification/swing';positionValeurDestination.mkdir(parents=True,exist_ok=True)
    cheminClasse=racineProjet/'build/verification/new-java';cheminClasse.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(racineProjet/'dist/jkoros-native-korean.jar'),'-d',str(cheminClasse),str(racineProjet/'Tests/Java/TestSwing.java'),str(racineProjet/'Tests/Java/testFenêtreHangul.java')])
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
            Données=(racineProjet/'build/verification/new-java/TestSwing.class').read_bytes()
            envoyer('load TestSwing.class\n'.encode(),b'hex> ')
            for indiceOrdinal in range(0,len(Données),64):envoyer(Données[indiceOrdinal:indiceOrdinal+64].hex().encode()+b'\n',b'hex> ')
            envoyer(b'.\n')
            envoyer('java TestSwing\n'.encode(),b'SWING READY')
            décalageFin=time.monotonic()+3
            while time.monotonic()<décalageFin:évènementPoignée(.1)
            # JFrame centered at (120,100), content at y=130.
            envoyer(boutonCliquer(200,210),b'',)  # focus JTextField
            positionDonnées.stdin.write('누리'.encode());positionDonnées.stdin.flush()
            décalageFin=time.monotonic()+.3
            while time.monotonic()<décalageFin:évènementPoignée(.05)
            résultat=envoyer(boutonCliquer(200,255),'SWING CLICK 이름누리'.encode())
            attendreFin(b'true',len(enregistrementJournal)-len(résultat))
            envoyer(valeurRaccourci(1),b'TERMINAL FOCUS 2')
            résultat=interpréteurCommandes('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in résultat
            envoyer(boutonCliquer(180,12),b'TERMINAL FOCUS 1')
            décalageFin=time.monotonic()+.3
            while time.monotonic()<décalageFin:évènementPoignée(.05)
            with socket.socket(socket.AF_UNIX) as codeCaractère:
                codeCaractère.settimeout(10);codeCaractère.connect(str(connexionContrôleSimulacre))
                with codeCaractère.makefile('rwb') as entréeÉlémentFichier:
                    json.loads(entréeÉlémentFichier.readline())
                    for valeurRequête in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(positionValeurDestination/'native-swing.png'),'format':'png'}}):
                        entréeÉlémentFichier.write((json.dumps(valeurRequête)+'\n').encode());entréeÉlémentFichier.flush()
                        while True:
                            valeurRetourné=json.loads(entréeÉlémentFichier.readline())
                            if 'error' in valeurRetourné:raise AssertionError(valeurRetourné)
                            if 'return' in valeurRetourné:break
            envoyer(boutonCliquer(505,115))
            interpréteurCommandes('echo SWING_CLOSED_OK')
            Données=(cheminClasse/'testFenêtreHangul.class').read_bytes()
            envoyer('load testFenêtreHangul.class\n'.encode(),b'hex> ')
            for indiceOrdinal in range(0,len(Données),64):envoyer(Données[indiceOrdinal:indiceOrdinal+64].hex().encode()+b'\n',b'hex> ')
            envoyer(b'.\n')
            envoyer('java testFenêtreHangul\n'.encode(),b'KOREAN SWING READY')
            envoyer(boutonCliquer(200,255),'KOREAN SWING CLICK nom'.encode())
            envoyer(boutonCliquer(505,115))
            interpréteurCommandes('echo KOREAN_SWING_CLOSED_OK')
            rapportValidation.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','français fenêtre/bouton/NotificationAction/FileAttenteÉvènement directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if positionDonnées.poll() is None:positionDonnées.terminate()
            try:positionDonnées.wait(timeout=5)
            except subprocess.TimeoutExpired:positionDonnées.kill();positionDonnées.wait()
            Sélecteur.close();positionDonnées.stdin.close();positionDonnées.stdout.close();(positionValeurDestination/'serial.log').write_bytes(enregistrementJournal);(positionValeurDestination/'report.json').write_text(json.dumps(rapportValidation,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':lancer()
