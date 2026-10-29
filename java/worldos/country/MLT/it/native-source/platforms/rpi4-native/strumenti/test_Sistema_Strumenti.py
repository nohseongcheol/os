#!/usr/bin/env python3
"""effettivo_dati nativo 커널의 IP/ICMP, Stato_VALORE query_VALORE, 현지어 comando, 게스트 Esci_app convalidare."""
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


def avvia():
    parser_48ee4b1b=argparse.ArgumentParser();parser_48ee4b1b.add_argument('--edition',type=Path);parser_48ee4b1b.add_argument('--output',type=Path);parser_48ee4b1b.add_argument('--poweroff-only',action='store_true');argomenti=parser_48ee4b1b.parse_args()
    azione_radice=Path(__file__).resolve().parents[1];Impostazioni={};nome_tabella={}
    if argomenti.edition:
        Country_VALORE=argomenti.edition.resolve();Impostazioni=json.loads((Country_VALORE/'native.json').read_text());nome_tabella=Impostazioni['identifiers'];azione_radice=Country_VALORE/Impostazioni['source']/Impostazioni['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(Country_VALORE/'native-edition.py'),'check'])
        host=Country_VALORE/'host/qemu'
        if host.is_file():os.environ['QEMU_AARCH64']=str(host)
    strumenti=azione_radice/Path(Impostazioni.get('runner','strumenti/Esegui_comando.py')).parent
    sys.path.insert(0,str(strumenti))
    def Lettura(Nome):
        percorso=strumenti/(nome_tabella.get(Nome,Nome)+'.py');valore_di_contratto=importlib.util.spec_from_file_location('test_'+Nome,str(percorso));modulo_VALORE=importlib.util.module_from_spec(valore_di_contratto);valore_di_contratto.loader.exec_module(modulo_VALORE);return modulo_VALORE
    esecuzione_modulo=Lettura('Esegui_comando');rete_modulo=Lettura('bridge_3de4fe3a');comando=getattr(esecuzione_modulo,nome_tabella.get('comando','comando'));bridge_TIPO=getattr(rete_modulo,nome_tabella.get('bridge_3de4fe3a','bridge_3de4fe3a'))
    alias_VALORE=Impostazioni.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'indirizzo_IP','ping':'test_risposta','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'mostra_aiuto'})
    sys.path.insert(0,str(azione_radice/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(azione_radice);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    uscitaTesto=argomenti.output or azione_radice/'build/verification/system-tools';uscitaTesto.mkdir(parents=True,exist_ok=True)
    Report_VALORE={'passed':False,'country':Impostazioni.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((azione_radice/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_riga=bytearray();SEQUENZA_VALORE=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        controllo_percorso=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Cerca_VALORE:Cerca_VALORE.bind(('127.0.0.1',0));numero_di_porta=Cerca_VALORE.getsockname()[1]
            if not 50000<=numero_di_porta<=50007:break
        with bridge_TIPO(numero_di_porta,acquisire=True,guest_e_mail=ipTestText('10.0.2.20'),ID_host='127.0.0.2') as bridge_VALORE:
            Processi_VALORE=subprocess.Popen(comando()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(controllo_percorso)]+bridge_VALORE.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            SCEGLI_articolo=selectors.DefaultSelector();SCEGLI_articolo.register(Processi_VALORE.stdout,selectors.EVENT_READ)
            def ricevere(mostrare_VALORE,avvia=0,제한=45):
                끝=time.monotonic()+제한
                while mostrare_VALORE not in LOG_riga[avvia:]:
                    if time.monotonic()>끝 or Processi_VALORE.poll() is not None:raise AssertionError('Missing '+repr(mostrare_VALORE)+'\n'+LOG_riga[avvia:].decode('utf-8','replace'))
                    for tasto_VALORE,_ in SCEGLI_articolo.select(.1):
                        dati=tasto_VALORE.fileobj.read(65536)
                        if dati:LOG_riga.extend(dati)
                return LOG_riga[avvia:].decode('utf-8','replace').replace('\r\n','\n')
            def inviare(dati):Processi_VALORE.stdin.write(dati);Processi_VALORE.stdin.flush()
            def Shell(testo):
                testo=ipTestText(testo)
                print(Report_VALORE['country'],testo,flush=True);SEQUENZA_VALORE[0]+=1;mostrare_VALORE='__SYSTEM_DONE_'+str(SEQUENZA_VALORE[0])+'__';avvia=len(LOG_riga)
                inviare((testo+'; echo; echo '+mostrare_VALORE+'\n').encode())
                chiudere_marcatore=('\r\n'+mostrare_VALORE+'\r\n').encode();ricevere(chiudere_marcatore,avvia)
                chiudere_funzione=LOG_riga.index(chiudere_marcatore,avvia)+len(chiudere_marcatore)
                ricevere(b'jkoros-native> ',chiudere_funzione)
                return LOG_riga[avvia:].decode('utf-8','replace').replace('\r\n','\n')
            def verificare(testo,*값들):
                replica=Shell(testo)
                for VALORE in 값들:assert ipTestText(VALORE) in replica,(testo,VALORE,replica)
                return replica
            try:
                ricevere(b'jkoros-native> ')
                if not argomenti.poweroff_only:
                    Guida_VALORE=verificare('help system','ipconfig','ping','ps','top','df','poweroff')
                    for alternativa_nome in alias_VALORE.values():assert alternativa_nome in Guida_VALORE,(alternativa_nome,Guida_VALORE)
                    verificare(alias_VALORE['help']+' system','Network / system')
                    verificare('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    verificare(alias_VALORE['ipconfig'],'inet 10.0.2.15');verificare('ip addr show','sl0: UP');verificare('ifconfig','sl0: UP')
                    for non_valida_Impostazioni in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        errore=verificare('ipconfig set '+non_valida_Impostazioni+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in errore,errore
                        verificare('ipconfig','inet 10.0.2.15')
                    verificare('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    verificare(alias_VALORE['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verificare('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    verificare('ip link set dev sl0 down','sl0: DOWN');verificare('ping -c 1 10.0.2.2; echo STATUS=$?','errore -100','STATUS=1')
                    verificare('ipconfig up','sl0: UP')
                    verificare(alias_VALORE['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    verificare('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verificare('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');verificare(alias_VALORE['route'],'10.0.2.2 sl0')
                    verificare('ftpd start','FTP listening')
                    verificare(alias_VALORE['netstat'],'10.0.2.20:21','LISTEN');verificare('ss','LISTEN')
                    verificare('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','errore -16')
                    with ftplib.FTP() as client_VALORE:
                        client_VALORE.connect('127.0.0.2',numero_di_porta,timeout=20);client_VALORE.login();dati=b'Network address was changed in the guest.\n'
                        client_VALORE.storbinary('STOR net-state.txt',io.BytesIO(dati));RICEV_SCAD_dati=bytearray();client_VALORE.retrbinary('RETR net-state.txt',RICEV_SCAD_dati.extend);assert RICEV_SCAD_dati==dati;client_VALORE.delete('net-state.txt')
                    verificare('ftpd stop','FTP stopped');verificare('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    Report_VALORE['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(testo):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',testo);assert 찾음,testo;return tuple(map(int,찾음.groups()))
                    전=저장값(verificare('df','RAM only'));verificare('echo disk-proof > sys-state.txt');후=저장값(verificare(alias_VALORE['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    verificare('rm sys-state.txt');assert 저장값(Shell('df'))==전
                    Memoria_VALORE=verificare(alias_VALORE['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');quantità_VALORE=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Memoria_VALORE).groups()));assert 0<quantità_VALORE[1]<=quantità_VALORE[0] and quantità_VALORE[1]+quantità_VALORE[2]==quantità_VALORE[0]
                    verificare(alias_VALORE['ps'],'kernel/shell');verificare(alias_VALORE['uptime'],'seconds')
                    stato_info=verificare(alias_VALORE['top']+' -n 2','kernel/shell');assert stato_info.count('PID SLOT STATE')==2,stato_info
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    verificare('terminal','TERMINAL READY');avvia=len(LOG_riga);inviare(b'vi process.txt\n');ricevere(b'NORMAL',avvia)
                    avvia=len(LOG_riga);inviare(bytes([30,2,1,0,0,0,0]));ricevere(b'jkoros-native> ',avvia)
                    voce_elenco=verificare('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',voce_elenco);assert 찾음 and int(찾음.group(2))>0,voce_elenco
                    verificare('free','EL0 mapped KiB: '+찾음.group(2))
                    avvia=len(LOG_riga);inviare(b'top\n');ricevere(b'PID SLOT STATE',avvia);inviare(b'q');ricevere(b'jkoros-native> ',avvia)
                    # Test a multibyte prefix through the real shell completion path.
                    if alias_VALORE['df']!='df':
                        avvia=len(LOG_riga);inviare((alias_VALORE['df'][:-1]+'\t\n').encode());ricevere(b'RAM only',avvia);ricevere(b'jkoros-native> ',avvia)
                    Report_VALORE['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as controllo_VALORE:
                    controllo_VALORE.settimeout(15);controllo_VALORE.connect(str(controllo_percorso));Stream_VALORE=controllo_VALORE.makefile('rwb');json.loads(Stream_VALORE.readline());Stream_VALORE.write(b'{"execute":"qmp_capabilities"}\n');Stream_VALORE.flush()
                    while 'return' not in json.loads(Stream_VALORE.readline()):pass
                    inviare((('poweroff' if argomenti.poweroff_only else alias_VALORE['poweroff'])+'\n').encode())
                    while True:
                        Evento=json.loads(Stream_VALORE.readline())
                        if Evento.get('event')=='SHUTDOWN':break
                    assert Evento['data']['guest'] and Evento['data']['reason']=='guest-shutdown',Evento
                    assert Processi_VALORE.wait(timeout=15)==0
                    Report_VALORE['shutdown']=Evento;Report_VALORE['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                Report_VALORE['network_trace']=bridge_VALORE.log_di_analisi
                assert argomenti.poweroff_only or any(voce_VALORE['protocol']==1 and voce_VALORE['direction']=='from_guest' for voce_VALORE in bridge_VALORE.log_di_analisi)
                Report_VALORE['passed']=True
            finally:
                if Processi_VALORE.poll() is None:os.killpg(Processi_VALORE.pid,signal.SIGTERM)
                try:Processi_VALORE.wait(timeout=10)
                except subprocess.TimeoutExpired:Processi_VALORE.kill();Processi_VALORE.wait()
                SCEGLI_articolo.close();(uscitaTesto/'serial.log').write_bytes(LOG_riga);(uscitaTesto/'report.json').write_text(json.dumps(Report_VALORE,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({tasto_VALORE:VALORE for tasto_VALORE,VALORE in Report_VALORE.items() if tasto_VALORE!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':avvia()
