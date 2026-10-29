#!/usr/bin/env python3
import hashlib,json,subprocess
from exécuterCommande import racineProjet

def lancer():
    donnéesRésultat=racineProjet/'build/verification/stream';donnéesRésultat.mkdir(parents=True,exist_ok=True)
    rapportValidation={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((racineProjet/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(donnéesRésultat),str(racineProjet/'Tests/Java/testFlux.java')])
        positionDonnées=subprocess.run(['python3',str(racineProjet/'Outils/exécuterFichier.py'),str(donnéesRésultat/'testFlux.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (donnéesRésultat/'serial.log').write_bytes(positionDonnées.stdout);assert positionDonnées.returncode==0,positionDonnées.stdout.decode('utf-8','replace')
        texte=positionDonnées.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 valeurLimite\nDNS estNonPrisEnCharge\nSTREAM PASS\nexit 0\n' in texte,texte
        rapportValidation.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(donnéesRésultat/'report.json').write_text(json.dumps(rapportValidation,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':lancer()
