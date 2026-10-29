#!/usr/bin/env python3
"""real_datos 자체 커널의 IP/ICMP, Estado_VALOR consulta_VALOR, 현지어 Orde, 게스트 saír_apl validar."""
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


def Executar_2():
    analizador_48ee4b1b=argparse.ArgumentParser();analizador_48ee4b1b.add_argument('--edition',type=Path);analizador_48ee4b1b.add_argument('--output',type=Path);analizador_48ee4b1b.add_argument('--poweroff-only',action='store_true');Argumentos=analizador_48ee4b1b.parse_args()
    Project_raíz=Path(__file__).resolve().parents[1];Configuración={};nome_táboa={}
    if Argumentos.edition:
        나라=Argumentos.edition.resolve();Configuración=json.loads((나라/'native.json').read_text());nome_táboa=Configuración['identifiers'];Project_raíz=나라/Configuración['source']/Configuración['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(나라/'native-edition.py'),'check'])
        hospedar=나라/'host/qemu'
        if hospedar.is_file():os.environ['QEMU_AARCH64']=str(hospedar)
    Ferramentas=Project_raíz/Path(Configuración.get('runner','Ferramentas/executar_comando.py')).parent
    sys.path.insert(0,str(Ferramentas))
    def Lectura(Nome):
        CAMIÑO=Ferramentas/(nome_táboa.get(Nome,Nome)+'.py');caso_VALOR=importlib.util.spec_from_file_location('test_'+Nome,str(CAMIÑO));módulo_VALOR=importlib.util.module_from_spec(caso_VALOR);caso_VALOR.loader.exec_module(módulo_VALOR);return módulo_VALOR
    실행모듈=Lectura('executar_comando');Rede_módulo=Lectura('Rede_ponte');Orde=getattr(실행모듈,nome_táboa.get('Orde','Orde'));ponte_TIPO=getattr(Rede_módulo,nome_táboa.get('Rede_ponte','Rede_ponte'))
    alias_VALOR=Configuración.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'enderezo_IP','ping':'응답시험','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'mostrar_axuda'})
    sys.path.insert(0,str(Project_raíz/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(Project_raíz);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Saída=Argumentos.output or Project_raíz/'build/verification/system-tools';Saída.mkdir(parents=True,exist_ok=True)
    informe_VALOR={'passed':False,'country':Configuración.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_raíz/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_fila=bytearray();SECUENCIA_VALOR=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        control_camiño=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as ACHAR_VALOR:ACHAR_VALOR.bind(('127.0.0.1',0));número_do_porto=ACHAR_VALOR.getsockname()[1]
            if not 50000<=número_do_porto<=50007:break
        with ponte_TIPO(número_do_porto,capturar=True,convidado_ENDEREZO=ipTestText('10.0.2.20'),hospedar_ENDEREZO='127.0.0.2') as ponte_VALOR:
            Proceso_VALOR=subprocess.Popen(Orde()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(control_camiño)]+ponte_VALOR.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            ESCOLLER_elemento=selectors.DefaultSelector();ESCOLLER_elemento.register(Proceso_VALOR.stdout,selectors.EVENT_READ)
            def 받기(mostrar_VALOR,Executar_2=0,제한=45):
                끝=time.monotonic()+제한
                while mostrar_VALOR not in LOG_fila[Executar_2:]:
                    if time.monotonic()>끝 or Proceso_VALOR.poll() is not None:raise AssertionError('Missing '+repr(mostrar_VALOR)+'\n'+LOG_fila[Executar_2:].decode('utf-8','replace'))
                    for Chave_VALOR,_ in ESCOLLER_elemento.select(.1):
                        datos=Chave_VALOR.fileobj.read(65536)
                        if datos:LOG_fila.extend(datos)
                return LOG_fila[Executar_2:].decode('utf-8','replace').replace('\r\n','\n')
            def enviar(datos):Proceso_VALOR.stdin.write(datos);Proceso_VALOR.stdin.flush()
            def shell(Texto):
                Texto=ipTestText(Texto)
                print(informe_VALOR['country'],Texto,flush=True);SECUENCIA_VALOR[0]+=1;mostrar_VALOR='__SYSTEM_DONE_'+str(SECUENCIA_VALOR[0])+'__';Executar_2=len(LOG_fila)
                enviar((Texto+'; echo; echo '+mostrar_VALOR+'\n').encode())
                끝표시=('\r\n'+mostrar_VALOR+'\r\n').encode();받기(끝표시,Executar_2)
                finalizar_cargo=LOG_fila.index(끝표시,Executar_2)+len(끝표시)
                받기(b'jkoros-native> ',finalizar_cargo)
                return LOG_fila[Executar_2:].decode('utf-8','replace').replace('\r\n','\n')
            def verificar(Texto,*값들):
                resposta=shell(Texto)
                for VALOR in 값들:assert ipTestText(VALOR) in resposta,(Texto,VALOR,resposta)
                return resposta
            try:
                받기(b'jkoros-native> ')
                if not Argumentos.poweroff_only:
                    axuda_VALOR=verificar('help system','ipconfig','ping','ps','top','df','poweroff')
                    for 별칭 in alias_VALOR.values():assert 별칭 in axuda_VALOR,(별칭,axuda_VALOR)
                    verificar(alias_VALOR['help']+' system','Network / system')
                    verificar('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    verificar(alias_VALOR['ipconfig'],'inet 10.0.2.15');verificar('ip addr show','sl0: UP');verificar('ifconfig','sl0: UP')
                    for non_válido_Configuración in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        ERRO=verificar('ipconfig set '+non_válido_Configuración+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in ERRO,ERRO
                        verificar('ipconfig','inet 10.0.2.15')
                    verificar('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    verificar(alias_VALOR['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verificar('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    verificar('ip link set dev sl0 down','sl0: DOWN');verificar('ping -c 1 10.0.2.2; echo STATUS=$?','ERRO -100','STATUS=1')
                    verificar('ipconfig up','sl0: UP')
                    verificar(alias_VALOR['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    verificar('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verificar('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');verificar(alias_VALOR['route'],'10.0.2.2 sl0')
                    verificar('ftpd start','FTP listening')
                    verificar(alias_VALOR['netstat'],'10.0.2.20:21','LISTEN');verificar('ss','LISTEN')
                    verificar('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','ERRO -16')
                    with ftplib.FTP() as cliente_VALOR:
                        cliente_VALOR.connect('127.0.0.2',número_do_porto,timeout=20);cliente_VALOR.login();datos=b'Network address was changed in the guest.\n'
                        cliente_VALOR.storbinary('STOR net-state.txt',io.BytesIO(datos));RECIBIDO_datos=bytearray();cliente_VALOR.retrbinary('RETR net-state.txt',RECIBIDO_datos.extend);assert RECIBIDO_datos==datos;cliente_VALOR.delete('net-state.txt')
                    verificar('ftpd stop','FTP stopped');verificar('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    informe_VALOR['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(Texto):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',Texto);assert 찾음,Texto;return tuple(map(int,찾음.groups()))
                    전=저장값(verificar('df','RAM only'));verificar('echo disk-proof > sys-state.txt');후=저장값(verificar(alias_VALOR['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    verificar('rm sys-state.txt');assert 저장값(shell('df'))==전
                    Memoria_VALOR=verificar(alias_VALOR['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');량=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Memoria_VALOR).groups()));assert 0<량[1]<=량[0] and 량[1]+량[2]==량[0]
                    verificar(alias_VALOR['ps'],'kernel/shell');verificar(alias_VALOR['uptime'],'seconds')
                    estado_información=verificar(alias_VALOR['top']+' -n 2','kernel/shell');assert estado_información.count('PID SLOT STATE')==2,estado_información
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    verificar('terminal','TERMINAL READY');Executar_2=len(LOG_fila);enviar(b'vi process.txt\n');받기(b'NORMAL',Executar_2)
                    Executar_2=len(LOG_fila);enviar(bytes([30,2,1,0,0,0,0]));받기(b'jkoros-native> ',Executar_2)
                    introdución_Lista=verificar('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',introdución_Lista);assert 찾음 and int(찾음.group(2))>0,introdución_Lista
                    verificar('free','EL0 mapped KiB: '+찾음.group(2))
                    Executar_2=len(LOG_fila);enviar(b'top\n');받기(b'PID SLOT STATE',Executar_2);enviar(b'q');받기(b'jkoros-native> ',Executar_2)
                    # Test a multibyte prefix through the real shell completion path.
                    if alias_VALOR['df']!='df':
                        Executar_2=len(LOG_fila);enviar((alias_VALOR['df'][:-1]+'\t\n').encode());받기(b'RAM only',Executar_2);받기(b'jkoros-native> ',Executar_2)
                    informe_VALOR['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as control_VALOR:
                    control_VALOR.settimeout(15);control_VALOR.connect(str(control_camiño));fluxo_VALOR=control_VALOR.makefile('rwb');json.loads(fluxo_VALOR.readline());fluxo_VALOR.write(b'{"execute":"qmp_capabilities"}\n');fluxo_VALOR.flush()
                    while 'return' not in json.loads(fluxo_VALOR.readline()):pass
                    enviar((('poweroff' if Argumentos.poweroff_only else alias_VALOR['poweroff'])+'\n').encode())
                    while True:
                        Evento=json.loads(fluxo_VALOR.readline())
                        if Evento.get('event')=='SHUTDOWN':break
                    assert Evento['data']['guest'] and Evento['data']['reason']=='guest-shutdown',Evento
                    assert Proceso_VALOR.wait(timeout=15)==0
                    informe_VALOR['shutdown']=Evento;informe_VALOR['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                informe_VALOR['network_trace']=ponte_VALOR.traza_LOG
                assert Argumentos.poweroff_only or any(introdución_VALOR['protocol']==1 and introdución_VALOR['direction']=='from_guest' for introdución_VALOR in ponte_VALOR.traza_LOG)
                informe_VALOR['passed']=True
            finally:
                if Proceso_VALOR.poll() is None:os.killpg(Proceso_VALOR.pid,signal.SIGTERM)
                try:Proceso_VALOR.wait(timeout=10)
                except subprocess.TimeoutExpired:Proceso_VALOR.kill();Proceso_VALOR.wait()
                ESCOLLER_elemento.close();(Saída/'serial.log').write_bytes(LOG_fila);(Saída/'report.json').write_text(json.dumps(informe_VALOR,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Chave_VALOR:VALOR for Chave_VALOR,VALOR in informe_VALOR.items() if Chave_VALOR!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':Executar_2()
