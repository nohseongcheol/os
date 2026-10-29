#!/usr/bin/env python3
"""donnéesEffectif interne 커널의 IP/ICMP, valeurÉtatValeur valeurInterroger, 현지어 commande, 게스트 programmeQuitter valider."""
import argparse
import ftplib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import selectors
import signal
import socket
import subprocess
import sys
import tempfile
import time


def lancer():
    Analyseur=argparse.ArgumentParser();Analyseur.add_argument('--edition',type=Path);Analyseur.add_argument('--output',type=Path);Analyseur.add_argument('--poweroff-only',action='store_true');arguments=Analyseur.parse_args()
    racineProjet=Path(__file__).resolve().parents[1];réglages={};tableNom={}
    if arguments.edition:
        valeurPays=arguments.edition.resolve();réglages=json.loads((valeurPays/'native.json').read_text());tableNom=réglages['identifiers'];racineProjet=valeurPays/réglages['source']/réglages['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(valeurPays/'native-edition.py'),'check'])
        Hôte=valeurPays/'host/qemu'
        if Hôte.is_file():os.environ['QEMU_AARCH64']=str(Hôte)
    Outils=racineProjet/Path(réglages.get('runner','Outils/exécuterCommande.py')).parent
    sys.path.insert(0,str(Outils))
    def lire(nom):
        chemin=Outils/(tableNom.get(nom,nom)+'.py');valeurContrat=importlib.util.spec_from_file_location('test_'+nom,str(chemin));valeurModule=importlib.util.module_from_spec(valeurContrat);valeurContrat.loader.exec_module(valeurModule);return valeurModule
    moduleExécution=lire('exécuterCommande');moduleRéseau=lire('pontRéseau');commande=getattr(moduleExécution,tableNom.get('commande','commande'));typePont=getattr(moduleRéseau,tableNom.get('pontRéseau','pontRéseau'))
    valeurAlias=réglages.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'adresseIP','ping':'testRéponseRetour','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'désactivéAlimentation','help':'afficherAide'})
    sys.path.insert(0,str(racineProjet/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(racineProjet);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Sortie=arguments.output or racineProjet/'build/verification/system-tools';Sortie.mkdir(parents=True,exist_ok=True)
    valeurRapport={'passed':False,'country':réglages.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((racineProjet/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    enregistrementJournal=bytearray();valeurSéquence=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as valeurTemporaire:
        cheminContrôle=Path(valeurTemporaire)/'qmp.sock'
        while True:
            with socket.socket() as chercherValeur:chercherValeur.bind(('127.0.0.1',0));numéroPort=chercherValeur.getsockname()[1]
            if not 50000<=numéroPort<=50007:break
        with typePont(numéroPort,capturer=True,adresseInvité=ipTestText('10.0.2.20'),adresseHôte='127.0.0.2') as valeurPont:
            valeurProcessus=subprocess.Popen(commande()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(cheminContrôle)]+valeurPont.argumentTransféré(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            élémentListeChoisir=selectors.DefaultSelector();élémentListeChoisir.register(valeurProcessus.stdout,selectors.EVENT_READ)
            def recevoir(afficherValeur,lancer=0,valeurLimite=45):
                terminaison=time.monotonic()+valeurLimite
                while afficherValeur not in enregistrementJournal[lancer:]:
                    if time.monotonic()>terminaison or valeurProcessus.poll() is not None:raise AssertionError('Missing '+repr(afficherValeur)+'\n'+enregistrementJournal[lancer:].decode('utf-8','replace'))
                    for valeurTouche,_ in élémentListeChoisir.select(.1):
                        Données=valeurTouche.fileobj.read(65536)
                        if Données:enregistrementJournal.extend(Données)
                return enregistrementJournal[lancer:].decode('utf-8','replace').replace('\r\n','\n')
            def envoyer(Données):valeurProcessus.stdin.write(Données);valeurProcessus.stdin.flush()
            def interpréteurCommandes(texte):
                texte=ipTestText(texte)
                print(valeurRapport['country'],texte,flush=True);valeurSéquence[0]+=1;afficherValeur='__SYSTEM_DONE_'+str(valeurSéquence[0])+'__';lancer=len(enregistrementJournal)
                envoyer((texte+'; echo; echo '+afficherValeur+'\n').encode())
                marqueurFin=('\r\n'+afficherValeur+'\r\n').encode();recevoir(marqueurFin,lancer)
                positionFin=enregistrementJournal.index(marqueurFin,lancer)+len(marqueurFin)
                recevoir(b'jkoros-native> ',positionFin)
                return enregistrementJournal[lancer:].decode('utf-8','replace').replace('\r\n','\n')
            def vérifier(texte,*valeurs):
                réponse=interpréteurCommandes(texte)
                for valeur in valeurs:assert ipTestText(valeur) in réponse,(texte,valeur,réponse)
                return réponse
            try:
                recevoir(b'jkoros-native> ')
                if not arguments.poweroff_only:
                    valeurAide=vérifier('help system','ipconfig','ping','ps','top','df','poweroff')
                    for nomAlternatif in valeurAlias.values():assert nomAlternatif in valeurAide,(nomAlternatif,valeurAide)
                    vérifier(valeurAlias['help']+' system','Network / system')
                    vérifier('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    vérifier(valeurAlias['ipconfig'],'inet 10.0.2.15');vérifier('ip addr show','sl0: UP');vérifier('ifconfig','sl0: UP')
                    for réglagesInvalide in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        erreur=vérifier('ipconfig set '+réglagesInvalide+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in erreur,erreur
                        vérifier('ipconfig','inet 10.0.2.15')
                    vérifier('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    vérifier(valeurAlias['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    vérifier('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    vérifier('ip link set dev sl0 down','sl0: DOWN');vérifier('ping -c 1 10.0.2.2; echo STATUS=$?','erreur -100','STATUS=1')
                    vérifier('ipconfig up','sl0: UP')
                    vérifier(valeurAlias['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    vérifier('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    vérifier('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');vérifier(valeurAlias['route'],'10.0.2.2 sl0')
                    vérifier('ftpd start','FTP listening')
                    vérifier(valeurAlias['netstat'],'10.0.2.20:21','LISTEN');vérifier('ss','LISTEN')
                    vérifier('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','erreur -16')
                    with ftplib.FTP() as valeurClient:
                        valeurClient.connect('127.0.0.2',numéroPort,timeout=20);valeurClient.login();Données=b'Network address was changed in the guest.\n'
                        valeurClient.storbinary('STOR net-state.txt',io.BytesIO(Données));donnéesReçu=bytearray();valeurClient.retrbinary('RETR net-state.txt',donnéesReçu.extend);assert donnéesReçu==Données;valeurClient.delete('net-state.txt')
                    vérifier('ftpd stop','FTP stopped');vérifier('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    valeurRapport['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def enregistré(texte):
                        valeurTrouvé=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',texte);assert valeurTrouvé,texte;return tuple(map(int,valeurTrouvé.groups()))
                    valeurAvant=enregistré(vérifier('df','RAM only'));vérifier('echo disk-proof > sys-state.txt');étatValeurAprès=enregistré(vérifier(valeurAlias['df'],'RAM only'))
                    assert étatValeurAprès[1]-valeurAvant[1]==16384 and étatValeurAprès[4]-valeurAvant[4]==1 and étatValeurAprès[3]-valeurAvant[3]==11,(valeurAvant,étatValeurAprès)
                    vérifier('rm sys-state.txt');assert enregistré(interpréteurCommandes('df'))==valeurAvant
                    Mémoire=vérifier(valeurAlias['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');valeurQuantité=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Mémoire).groups()));assert 0<valeurQuantité[1]<=valeurQuantité[0] and valeurQuantité[1]+valeurQuantité[2]==valeurQuantité[0]
                    vérifier(valeurAlias['ps'],'kernel/shell');vérifier(valeurAlias['uptime'],'seconds')
                    informationÉtat=vérifier(valeurAlias['top']+' -n 2','kernel/shell');assert informationÉtat.count('PID SLOT STATE')==2,informationÉtat
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    vérifier('terminal','TERMINAL READY');lancer=len(enregistrementJournal);envoyer(b'vi process.txt\n');recevoir(b'NORMAL',lancer)
                    lancer=len(enregistrementJournal);envoyer(bytes([30,2,1,0,0,0,0]));recevoir(b'jkoros-native> ',lancer)
                    listeEntréeÉlément=vérifier('ps','SUSPENDED','vi process.txt');valeurTrouvé=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',listeEntréeÉlément);assert valeurTrouvé and int(valeurTrouvé.group(2))>0,listeEntréeÉlément
                    vérifier('free','EL0 mapped KiB: '+valeurTrouvé.group(2))
                    lancer=len(enregistrementJournal);envoyer(b'top\n');recevoir(b'PID SLOT STATE',lancer);envoyer(b'q');recevoir(b'jkoros-native> ',lancer)
                    # Test a multibyte prefix through the real shell completion path.
                    if valeurAlias['df']!='df':
                        lancer=len(enregistrementJournal);envoyer((valeurAlias['df'][:-1]+'\t\n').encode());recevoir(b'RAM only',lancer);recevoir(b'jkoros-native> ',lancer)
                    valeurRapport['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as valeurContrôle:
                    valeurContrôle.settimeout(15);valeurContrôle.connect(str(cheminContrôle));valeurFlux=valeurContrôle.makefile('rwb');json.loads(valeurFlux.readline());valeurFlux.write(b'{"execute":"qmp_capabilities"}\n');valeurFlux.flush()
                    while 'return' not in json.loads(valeurFlux.readline()):pass
                    envoyer((('poweroff' if arguments.poweroff_only else valeurAlias['poweroff'])+'\n').encode())
                    while True:
                        évènement=json.loads(valeurFlux.readline())
                        if évènement.get('event')=='SHUTDOWN':break
                    assert évènement['data']['guest'] and évènement['data']['reason']=='guest-shutdown',évènement
                    assert valeurProcessus.wait(timeout=15)==0
                    valeurRapport['shutdown']=évènement;valeurRapport['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                valeurRapport['network_trace']=valeurPont.journalTrace
                assert arguments.poweroff_only or any(valeurEntréeÉlément['protocol']==1 and valeurEntréeÉlément['direction']=='from_guest' for valeurEntréeÉlément in valeurPont.journalTrace)
                valeurRapport['passed']=True
            finally:
                if valeurProcessus.poll() is None:os.killpg(valeurProcessus.pid,signal.SIGTERM)
                try:valeurProcessus.wait(timeout=10)
                except subprocess.TimeoutExpired:valeurProcessus.kill();valeurProcessus.wait()
                élémentListeChoisir.close();(Sortie/'serial.log').write_bytes(enregistrementJournal);(Sortie/'report.json').write_text(json.dumps(valeurRapport,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({valeurTouche:valeur for valeurTouche,valeur in valeurRapport.items() if valeurTouche!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':lancer()
