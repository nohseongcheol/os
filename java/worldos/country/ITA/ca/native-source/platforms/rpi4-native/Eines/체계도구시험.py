#!/usr/bin/env python3
"""real_dades propi 커널의 IP/ICMP, Estat_VALOR cerca_VALOR, 현지어 Ordre, 게스트 Surt_programa validar."""
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


def Executa_2():
    analitzador_48ee4b1b=argparse.ArgumentParser();analitzador_48ee4b1b.add_argument('--edition',type=Path);analitzador_48ee4b1b.add_argument('--output',type=Path);analitzador_48ee4b1b.add_argument('--poweroff-only',action='store_true');인수=analitzador_48ee4b1b.parse_args()
    Project_rel=Path(__file__).resolve().parents[1];Ajusts={};nom_taula={}
    if 인수.edition:
        나라=인수.edition.resolve();Ajusts=json.loads((나라/'native.json').read_text());nom_taula=Ajusts['identifiers'];Project_rel=나라/Ajusts['source']/Ajusts['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        allotjar=나라/'host/qemu'
        if allotjar.is_file():os.environ['QEMU_AARCH64']=str(allotjar)
    Eines=Project_rel/Path(Ajusts.get('runner','Eines/Executa_ordre.py')).parent
    sys.path.insert(0,str(Eines))
    def Lectura(Nom):
        Camí=Eines/(nom_taula.get(Nom,Nom)+'.py');cas_VALOR=importlib.util.spec_from_file_location('test_'+Nom,str(Camí));mòdul_VALOR=importlib.util.module_from_spec(cas_VALOR);cas_VALOR.loader.exec_module(mòdul_VALOR);return mòdul_VALOR
    실행모듈=Lectura('Executa_ordre');xarxa_mòdul=Lectura('xarxa_pont');Ordre=getattr(실행모듈,nom_taula.get('Ordre','Ordre'));pont_TIPUS=getattr(xarxa_mòdul,nom_taula.get('xarxa_pont','xarxa_pont'))
    àlies_VALOR=Ajusts.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'adreça_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'mostrar_ajuda'})
    sys.path.insert(0,str(Project_rel/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(Project_rel);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Sortida=인수.output or Project_rel/'build/verification/system-tools';Sortida.mkdir(parents=True,exist_ok=True)
    informe_VALOR={'passed':False,'country':Ajusts.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_rel/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_fila=bytearray();SEQÜÈNCIA_VALOR=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        control_camí=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as Cerca_VALOR:Cerca_VALOR.bind(('127.0.0.1',0));número_de_port=Cerca_VALOR.getsockname()[1]
            if not 50000<=número_de_port<=50007:break
        with pont_TIPUS(número_de_port,capturar=True,convidat_ADREÇA=ipTestText('10.0.2.20'),allotjar_ADREÇA='127.0.0.2') as pont_VALOR:
            Procés_VALOR=subprocess.Popen(Ordre()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(control_camí)]+pont_VALOR.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            TRIA_element=selectors.DefaultSelector();TRIA_element.register(Procés_VALOR.stdout,selectors.EVENT_READ)
            def rebre(mostrar_VALOR,Executa_2=0,제한=45):
                끝=time.monotonic()+제한
                while mostrar_VALOR not in LOG_fila[Executa_2:]:
                    if time.monotonic()>끝 or Procés_VALOR.poll() is not None:raise AssertionError('Missing '+repr(mostrar_VALOR)+'\n'+LOG_fila[Executa_2:].decode('utf-8','replace'))
                    for Clau_VALOR,_ in TRIA_element.select(.1):
                        dades=Clau_VALOR.fileobj.read(65536)
                        if dades:LOG_fila.extend(dades)
                return LOG_fila[Executa_2:].decode('utf-8','replace').replace('\r\n','\n')
            def enviar(dades):Procés_VALOR.stdin.write(dades);Procés_VALOR.stdin.flush()
            def shell(SMS):
                SMS=ipTestText(SMS)
                print(informe_VALOR['country'],SMS,flush=True);SEQÜÈNCIA_VALOR[0]+=1;mostrar_VALOR='__SYSTEM_DONE_'+str(SEQÜÈNCIA_VALOR[0])+'__';Executa_2=len(LOG_fila)
                enviar((SMS+'; echo; echo '+mostrar_VALOR+'\n').encode())
                끝표시=('\r\n'+mostrar_VALOR+'\r\n').encode();rebre(끝표시,Executa_2)
                finalitzar_càrrec=LOG_fila.index(끝표시,Executa_2)+len(끝표시)
                rebre(b'jkoros-native> ',finalitzar_càrrec)
                return LOG_fila[Executa_2:].decode('utf-8','replace').replace('\r\n','\n')
            def verificar(SMS,*값들):
                resposta=shell(SMS)
                for VALOR in 값들:assert ipTestText(VALOR) in resposta,(SMS,VALOR,resposta)
                return resposta
            try:
                rebre(b'jkoros-native> ')
                if not 인수.poweroff_only:
                    ajuda_VALOR=verificar('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in àlies_VALOR.values():assert 별칭 in ajuda_VALOR,(별칭,ajuda_VALOR)
                    verificar(àlies_VALOR['help']+' system','Network / system')
                    verificar('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    verificar(àlies_VALOR['ipconfig'],'inet 10.0.2.15');verificar('ip addr show','sl0: UP');verificar('ifconfig','sl0: UP')
                    for invàlid_Configuració in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        s_ha_produït_un_error=verificar('ipconfig set '+invàlid_Configuració+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in s_ha_produït_un_error,s_ha_produït_un_error
                        verificar('ipconfig','inet 10.0.2.15')
                    verificar('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    verificar(àlies_VALOR['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verificar('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    verificar('ip link set dev sl0 down','sl0: DOWN');verificar('ping -c 1 10.0.2.2; echo STATUS=$?','s_ha_produït_un_error -100','STATUS=1')
                    verificar('ipconfig up','sl0: UP')
                    verificar(àlies_VALOR['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    verificar('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verificar('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');verificar(àlies_VALOR['route'],'10.0.2.2 sl0')
                    verificar('ftpd start','FTP listening')
                    verificar(àlies_VALOR['netstat'],'10.0.2.20:21','LISTEN');verificar('ss','LISTEN')
                    verificar('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','s_ha_produït_un_error -16')
                    with ftplib.FTP() as client_VALOR:
                        client_VALOR.connect('127.0.0.2',número_de_port,timeout=20);client_VALOR.login();dades=b'Network address was changed in the guest.\n'
                        client_VALOR.storbinary('STOR net-state.txt',io.BytesIO(dades));CANTIDAD_RECIBIDA_dades=bytearray();client_VALOR.retrbinary('RETR net-state.txt',CANTIDAD_RECIBIDA_dades.extend);assert CANTIDAD_RECIBIDA_dades==dades;client_VALOR.delete('net-state.txt')
                    verificar('ftpd stop','FTP stopped');verificar('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    informe_VALOR['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(SMS):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',SMS);assert 찾음,SMS;return tuple(map(int,찾음.groups()))
                    전=저장값(verificar('df','RAM only'));verificar('echo disk-proof > sys-state.txt');후=저장값(verificar(àlies_VALOR['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    verificar('rm sys-state.txt');assert 저장값(shell('df'))==전
                    Memòria_VALOR=verificar(àlies_VALOR['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Memòria_VALOR).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    verificar(àlies_VALOR['ps'],'kernel/shell');verificar(àlies_VALOR['uptime'],'seconds')
                    estat_informació=verificar(àlies_VALOR['top']+' -n 2','kernel/shell');assert estat_informació.count('PID SLOT STATE')==2,estat_informació
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    verificar('terminal','TERMINAL READY');Executa_2=len(LOG_fila);enviar(b'vi process.txt\n');rebre(b'NORMAL',Executa_2)
                    Executa_2=len(LOG_fila);enviar(bytes([30,2,1,0,0,0,0]));rebre(b'jkoros-native> ',Executa_2)
                    introducció_Llista=verificar('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',introducció_Llista);assert 찾음 and int(찾음.group(2))>0,introducció_Llista
                    verificar('free','EL0 mapped KiB: '+찾음.group(2))
                    Executa_2=len(LOG_fila);enviar(b'top\n');rebre(b'PID SLOT STATE',Executa_2);enviar(b'q');rebre(b'jkoros-native> ',Executa_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if àlies_VALOR['df']!='df':
                        Executa_2=len(LOG_fila);enviar((àlies_VALOR['df'][:-1]+'\t\n').encode());rebre(b'RAM only',Executa_2);rebre(b'jkoros-native> ',Executa_2)
                    informe_VALOR['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as control_VALOR:
                    control_VALOR.settimeout(15);control_VALOR.connect(str(control_camí));flux_VALOR=control_VALOR.makefile('rwb');json.loads(flux_VALOR.readline());flux_VALOR.write(b'{"execute":"qmp_capabilities"}\n');flux_VALOR.flush()
                    while 'return' not in json.loads(flux_VALOR.readline()):pass
                    enviar((('poweroff' if 인수.poweroff_only else àlies_VALOR['poweroff'])+'\n').encode())
                    while True:
                        Esdeveniment=json.loads(flux_VALOR.readline())
                        if Esdeveniment.get('event')=='SHUTDOWN':break
                    assert Esdeveniment['data']['guest'] and Esdeveniment['data']['reason']=='guest-shutdown',Esdeveniment
                    assert Procés_VALOR.wait(timeout=15)==0
                    informe_VALOR['shutdown']=Esdeveniment;informe_VALOR['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                informe_VALOR['network_trace']=pont_VALOR.traça_LOG
                assert 인수.poweroff_only or any(introducció_VALOR['protocol']==1 and introducció_VALOR['direction']=='from_guest' for introducció_VALOR in pont_VALOR.traça_LOG)
                informe_VALOR['passed']=True
            finally:
                if Procés_VALOR.poll() is None:os.killpg(Procés_VALOR.pid,signal.SIGTERM)
                try:Procés_VALOR.wait(timeout=10)
                except subprocess.TimeoutExpired:Procés_VALOR.kill();Procés_VALOR.wait()
                TRIA_element.close();(Sortida/'serial.log').write_bytes(LOG_fila);(Sortida/'report.json').write_text(json.dumps(informe_VALOR,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Clau_VALOR:VALOR for Clau_VALOR,VALOR in informe_VALOR.items() if Clau_VALOR!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Executa_2()
