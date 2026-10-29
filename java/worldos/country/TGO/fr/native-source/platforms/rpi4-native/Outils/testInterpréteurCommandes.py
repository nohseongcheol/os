#!/usr/bin/env python3
"""interne 커널의 interpréteurCommandes, 프로세스 sortieEntrée, Unicode GUI 터미널을 donnéesEffectif raspi4b에서 Tests."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from exécuterCommande import racineProjet, commande


def lancer():
    sortie = racineProjet / 'build/verification/shell'; sortie.mkdir(parents=True, exist_ok=True)
    rapportValidation = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((racineProjet / 'build/kernel8.img').read_bytes()).hexdigest()}
    transcription = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as cheminTravailEnCours:
        connexionContrôleSimulacre = Path(cheminTravailEnCours) / 'qmp.sock'
        processus = subprocess.Popen(commande()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(connexionContrôleSimulacre)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        moniteurDisponibilitéÉtat=selectors.DefaultSelector(); moniteurDisponibilitéÉtat.register(processus.stdout,selectors.EVENT_READ)
        def recevoirMessage(marqueur, délaiExpirationExécution=45):
            Données=bytearray(); décalageFin=time.monotonic()+délaiExpirationExécution
            while marqueur not in Données:
                if time.monotonic()>décalageFin or processus.poll() is not None: raise AssertionError('UART timeout/exit: '+Données.decode('utf-8','replace'))
                for valeurEnfoncé,_ in moniteurDisponibilitéÉtat.select(.1):
                    valeurFragment=valeurEnfoncé.fileobj.read(4096)
                    if valeurFragment: Données.extend(valeurFragment); transcription.extend(valeurFragment)
                if b'PANIC:' in Données or b'FAIL ' in Données: raise AssertionError(Données)
            return Données.decode('utf-8','replace').replace('\r\n','\n')
        def envoyer(Données, marqueur=b'jkoros-native> '):
            processus.stdin.write(Données); processus.stdin.flush(); return recevoirMessage(marqueur)
        def interpréteurCommandes(ligne, *attendu):
            résultat=envoyer(ligne.encode()+b'\n')
            for valeur in attendu: assert valeur in résultat, (ligne,valeur,résultat)
            return résultat
        def Fichier(nom):
            texte=interpréteurCommandes('hex '+nom,'HEX BEGIN','HEX END'); chercherRésultat=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',texte,re.S)
            Données=bytes.fromhex(''.join(chercherRésultat.group(2).split())); assert len(Données)==int(chercherRésultat.group(1)); return Données
        try:
            recevoirMessage(b'jkoros-native> ')
            interpréteurCommandes('mkdir Tâche; cd Tâche; pwd','/Tâche')
            interpréteurCommandes('mkdir 하위; echo "한글 Données 😀" > Salutation.txt')
            assert Fichier('Salutation.txt')=='한글 Données 😀\n'.encode()
            interpréteurCommandes('cp Salutation.txt copierValeur.txt; mv copierValeur.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 Données 😀')
            interpréteurCommandes('cd 하위; cat ../Salutation.txt; cat /Tâche/Salutation.txt; pwd','한글 Données 😀','/Tâche/하위')
            interpréteurCommandes('cd ..; rmdir 하위; echo $?','1\n')
            interpréteurCommandes('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            interpréteurCommandes('cp Salutation.txt Salutation.txt; echo $?','1\n'); assert Fichier('Salutation.txt')=='한글 Données 😀\n'.encode()
            interpréteurCommandes('export Salutation=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/Tâche','GOOD')
            assert b'BAD\n' not in Fichier('Salutation.txt')
            interpréteurCommandes("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Fichier('리터럴')=='$인사\n누리\n'.encode()
            interpréteurCommandes('echo one > valeurInstruction; echo two >> valeurInstruction; echo three >> valeurInstruction')
            interpréteurCommandes('cat < valeurInstruction | grep t | tee 추림 | wc -l','2\n'); assert Fichier('추림')==b'two\nthree\n'
            interpréteurCommandes('head -n 1 valeurInstruction > valeurAvantCôté; tail -n 1 valeurInstruction > valeurRetourArrièreCôté'); assert Fichier('앞')==b'one\n'; assert Fichier('뒤')==b'three\n'
            interpréteurCommandes('grep absent valeurInstruction; echo $?','1\n')
            interpréteurCommandes('echo untouched > protégerValeur')
            interpréteurCommandes('echo destroyed > protégerValeur |','명령이 빠졌습니다'); assert Fichier('protégerValeur')==b'untouched\n'
            interpréteurCommandes('echo "oops','따옴표가 닫히지 않았습니다')
            interpréteurCommandes('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            interpréteurCommandes('echo bad 2> protégerValeur','번호를 지정한 Fichier entréeÉlémentDescripteur sortieEntrée modeCommuter'); assert Fichier('protégerValeur')==b'untouched\n'
            interpréteurCommandes('rm 빈파일 리터럴 valeurInstruction 추림 valeurAvantCôté valeurRetourArrièreCôté protégerValeur')
            rapportValidation['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            interpréteurCommandes("python -c 'print(123)' | wc -c",'4\n')
            interpréteurCommandes("python -c 'print(456)' > Programme.txt"); assert Fichier('Programme.txt')==b'456\n'
            interpréteurCommandes("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            interpréteurCommandes("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < Programme.txt", "b'456\\n'", "b''")
            interpréteurCommandes("python -c 'print(\"x\"*17000)' | wc -c", 'erreur -28')
            interpréteurCommandes('echo recovered | wc -c','10\n')
            interpréteurCommandes("python -c 'import jkoros; print(jkoros.read("+'"/Tâche/Programme.txt"'+"))'",'456','exit 0')
            interpréteurCommandes('cd /; javac Hello.java','Compiled:','exit 0')
            interpréteurCommandes('java Hello > /Tâche/Java.txt'); assert '안녕하세요'.encode() in Fichier('/Tâche/Java.txt')
            interpréteurCommandes('cd Tâche; echo "echo script > résultatExécution" > commande.sh; echo "false || echo recovered >> résultatExécution" >> commande.sh; sh commande.sh')
            assert Fichier('résultatExécution')==b'script\nrecovered\n'
            interpréteurCommandes('rm résultatExécution; echo "exit 7" > programmeQuitter.sh; sh programmeQuitter.sh; echo $?','7\n')
            interpréteurCommandes('rm programmeQuitter.sh commande.sh Programme.txt Java.txt Salutation.txt; cd /; rmdir Tâche')
            rapportValidation['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            interpréteurCommandes('echo history-proof','history-proof')
            résultat=envoyer(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert résultat.count('history-proof')>=2, résultat
            envoyer(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            résultat=envoyer(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in résultat, résultat
            résultat=envoyer(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in résultat,résultat
            résultat=envoyer('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in résultat,résultat
            texteLong='한글'*50
            résultat=envoyer(('echo '+texteLong+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+texteLong+'\r\njkoros-native> ').encode()); assert '\n'+texteLong+'\n' in résultat
            interpréteurCommandes('terminal','TERMINAL READY')
            interpréteurCommandes('clear')
            interpréteurCommandes('echo "한글 terminal ABC xyz 012 😀"','한글 terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as client:
                client.settimeout(10); client.connect(str(connexionContrôleSimulacre))
                with client.makefile('rwb') as valeurFlux:
                    json.loads(valeurFlux.readline())
                    def invoquer(nom,tableauArgument=None):
                        messageRéseau={'execute':nom}
                        if tableauArgument: messageRéseau['arguments']=tableauArgument
                        valeurFlux.write((json.dumps(messageRéseau)+'\n').encode()); valeurFlux.flush()
                        while True:
                            réponse=json.loads(valeurFlux.readline())
                            if 'error' in réponse: raise AssertionError(réponse)
                            if 'return' in réponse: return réponse['return']
                    invoquer('qmp_capabilities')
                    image=sortie/'terminal.ppm'; invoquer('screendump',{'filename':str(image),'format':'ppm'})
                    invoquer('screendump',{'filename':str(sortie/'terminal.png'),'format':'png'})
                    Données=image.read_bytes().split(b'\n',3)[3]
                    def pixel(coordonnéeCoordonnéeHorizontale,coordonnéeCoordonnéeVerticale): return tuple(Données[(coordonnéeCoordonnéeVerticale*640+coordonnéeCoordonnéeHorizontale)*3:(coordonnéeCoordonnéeVerticale*640+coordonnéeCoordonnéeHorizontale)*3+3])
                    assert pixel(12,48)==(32,80,144),pixel(12,48)
                    assert len(set(pixel(coordonnéeCoordonnéeHorizontale,coordonnéeCoordonnéeVerticale) for coordonnéeCoordonnéeVerticale in range(100,116) for coordonnéeCoordonnéeHorizontale in range(24,56)))>1,'Hangul glyphs missing'
                    interpréteurCommandes('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    interpréteurCommandes("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    invoquer('screendump',{'filename':str(image),'format':'ppm'})
                    donnéesRestauré=image.read_bytes().split(b'\n',3)[3]
                    assert tuple(donnéesRestauré[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    interpréteurCommandes('echo test > visible.txt; cat visible.txt','test')
                    for indiceOrdinal in range(27): interpréteurCommandes('echo scroll-'+str(indiceOrdinal),'scroll-'+str(indiceOrdinal))
                    envoyer(b'\x1b[5~\x1b[6~\n')
                    invoquer('screendump',{'filename':str(sortie/'terminal-scroll.png'),'format':'png'})
                    résultat=envoyer(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in résultat,résultat
                    interpréteurCommandes('rm visible.txt')
                    invoquer('quit')
            processus.wait(timeout=5)
            rapportValidation['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            rapportValidation['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if processus.poll() is None:
                processus.terminate()
                try: processus.wait(timeout=5)
                except subprocess.TimeoutExpired: processus.kill(); processus.wait()
            moniteurDisponibilitéÉtat.close(); processus.stdin.close(); processus.stdout.close()
            (sortie/'serial.log').write_bytes(transcription)
            (sortie/'report.json').write_text(json.dumps(rapportValidation,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': lancer()
