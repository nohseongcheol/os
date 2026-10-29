#!/usr/bin/env python3
"""real_dados nativo 커널의 IP/ICMP, Estado_VALOR consulta_VALOR, 현지어 comando, 게스트 sair_app validar."""
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


def iniciar():
    analisador_48ee4b1b=argparse.ArgumentParser();analisador_48ee4b1b.add_argument('--edition',type=Path);analisador_48ee4b1b.add_argument('--output',type=Path);analisador_48ee4b1b.add_argument('--poweroff-only',action='store_true');argumentos=analisador_48ee4b1b.parse_args()
    ação_raiz=Path(__file__).resolve().parents[1];Definições={};nome_tabela={}
    if argumentos.edition:
        Country_VALOR=argumentos.edition.resolve();Definições=json.loads((Country_VALOR/'native.json').read_text());nome_tabela=Definições['identifiers'];ação_raiz=Country_VALOR/Definições['source']/Definições['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(Country_VALOR/'native-edition.py'),'check'])
        host=Country_VALOR/'host/qemu'
        if host.is_file():os.environ['QEMU_AARCH64']=str(host)
    ferramentas=ação_raiz/Path(Definições.get('runner','ferramentas/Executar_comando.py')).parent
    sys.path.insert(0,str(ferramentas))
    def Leitura(Nome):
        caminho=ferramentas/(nome_tabela.get(Nome,Nome)+'.py');valor_do_contrato=importlib.util.spec_from_file_location('test_'+Nome,str(caminho));módulo_VALOR=importlib.util.module_from_spec(valor_do_contrato);valor_do_contrato.loader.exec_module(módulo_VALOR);return módulo_VALOR
    execução_módulo=Leitura('Executar_comando');rede_módulo=Leitura('ponte_3de4fe3a');comando=getattr(execução_módulo,nome_tabela.get('comando','comando'));ponte_TIPO=getattr(rede_módulo,nome_tabela.get('ponte_3de4fe3a','ponte_3de4fe3a'))
    alias_VALOR=Definições.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'endereço_IP','ping':'teste_réplica','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'전원끄기','help':'mostrar_ajuda'})
    sys.path.insert(0,str(ação_raiz/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(ação_raiz);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    saídaTexto=argumentos.output or ação_raiz/'build/verification/system-tools';saídaTexto.mkdir(parents=True,exist_ok=True)
    relatar_VALOR={'passed':False,'country':Definições.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((ação_raiz/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    LOG_linha=bytearray();SEQUÊNCIA_VALOR=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as 임시:
        visual_caminho=Path(임시)/'qmp.sock'
        while True:
            with socket.socket() as busca_VALOR:busca_VALOR.bind(('127.0.0.1',0));número_da_porta=busca_VALOR.getsockname()[1]
            if not 50000<=número_da_porta<=50007:break
        with ponte_TIPO(número_da_porta,Captura=True,convidado_email=ipTestText('10.0.2.20'),ID_do_host='127.0.0.2') as ponte_VALOR:
            Processo_VALOR=subprocess.Popen(comando()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(visual_caminho)]+ponte_VALOR.전달인수(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            ESCOLHER_item=selectors.DefaultSelector();ESCOLHER_item.register(Processo_VALOR.stdout,selectors.EVENT_READ)
            def receber(mostrar_VALOR,iniciar=0,제한=45):
                끝=time.monotonic()+제한
                while mostrar_VALOR not in LOG_linha[iniciar:]:
                    if time.monotonic()>끝 or Processo_VALOR.poll() is not None:raise AssertionError('Missing '+repr(mostrar_VALOR)+'\n'+LOG_linha[iniciar:].decode('utf-8','replace'))
                    for Chave_VALOR,_ in ESCOLHER_item.select(.1):
                        dados=Chave_VALOR.fileobj.read(65536)
                        if dados:LOG_linha.extend(dados)
                return LOG_linha[iniciar:].decode('utf-8','replace').replace('\r\n','\n')
            def enviar(dados):Processo_VALOR.stdin.write(dados);Processo_VALOR.stdin.flush()
            def shell(texto):
                texto=ipTestText(texto)
                print(relatar_VALOR['country'],texto,flush=True);SEQUÊNCIA_VALOR[0]+=1;mostrar_VALOR='__SYSTEM_DONE_'+str(SEQUÊNCIA_VALOR[0])+'__';iniciar=len(LOG_linha)
                enviar((texto+'; echo; echo '+mostrar_VALOR+'\n').encode())
                encerrar_favorito=('\r\n'+mostrar_VALOR+'\r\n').encode();receber(encerrar_favorito,iniciar)
                encerrar_cargo=LOG_linha.index(encerrar_favorito,iniciar)+len(encerrar_favorito)
                receber(b'jkoros-native> ',encerrar_cargo)
                return LOG_linha[iniciar:].decode('utf-8','replace').replace('\r\n','\n')
            def verificar(texto,*값들):
                resposta=shell(texto)
                for VALOR in 값들:assert ipTestText(VALOR) in resposta,(texto,VALOR,resposta)
                return resposta
            try:
                receber(b'jkoros-native> ')
                if not argumentos.poweroff_only:
                    ajuda_VALOR=verificar('help system','ipconfig','ping','ps','top','df','poweroff')
                    for alternativo_nome in alias_VALOR.values():assert alternativo_nome in ajuda_VALOR,(alternativo_nome,ajuda_VALOR)
                    verificar(alias_VALOR['help']+' system','Network / system')
                    verificar('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    verificar(alias_VALOR['ipconfig'],'inet 10.0.2.15');verificar('ip addr show','sl0: UP');verificar('ifconfig','sl0: UP')
                    for inválido_Configurações in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        erro=verificar('ipconfig set '+inválido_Configurações+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in erro,erro
                        verificar('ipconfig','inet 10.0.2.15')
                    verificar('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    verificar(alias_VALOR['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verificar('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    verificar('ip link set dev sl0 down','sl0: DOWN');verificar('ping -c 1 10.0.2.2; echo STATUS=$?','erro -100','STATUS=1')
                    verificar('ipconfig up','sl0: UP')
                    verificar(alias_VALOR['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    verificar('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verificar('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');verificar(alias_VALOR['route'],'10.0.2.2 sl0')
                    verificar('ftpd start','FTP listening')
                    verificar(alias_VALOR['netstat'],'10.0.2.20:21','LISTEN');verificar('ss','LISTEN')
                    verificar('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','erro -16')
                    with ftplib.FTP() as cliente_VALOR:
                        cliente_VALOR.connect('127.0.0.2',número_da_porta,timeout=20);cliente_VALOR.login();dados=b'Network address was changed in the guest.\n'
                        cliente_VALOR.storbinary('STOR net-state.txt',io.BytesIO(dados));RECEBER_dados=bytearray();cliente_VALOR.retrbinary('RETR net-state.txt',RECEBER_dados.extend);assert RECEBER_dados==dados;cliente_VALOR.delete('net-state.txt')
                    verificar('ftpd stop','FTP stopped');verificar('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    relatar_VALOR['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def 저장값(texto):
                        찾음=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',texto);assert 찾음,texto;return tuple(map(int,찾음.groups()))
                    전=저장값(verificar('df','RAM only'));verificar('echo disk-proof > sys-state.txt');후=저장값(verificar(alias_VALOR['df'],'RAM only'))
                    assert 후[1]-전[1]==16384 and 후[4]-전[4]==1 and 후[3]-전[3]==11,(전,후)
                    verificar('rm sys-state.txt');assert 저장값(shell('df'))==전
                    Memória_VALOR=verificar(alias_VALOR['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');quantidade_VALOR=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Memória_VALOR).groups()));assert 0<quantidade_VALOR[1]<=quantidade_VALOR[0] and quantidade_VALOR[1]+quantidade_VALOR[2]==quantidade_VALOR[0]
                    verificar(alias_VALOR['ps'],'kernel/shell');verificar(alias_VALOR['uptime'],'seconds')
                    Status_informações=verificar(alias_VALOR['top']+' -n 2','kernel/shell');assert Status_informações.count('PID SLOT STATE')==2,Status_informações
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    verificar('terminal','TERMINAL READY');iniciar=len(LOG_linha);enviar(b'vi process.txt\n');receber(b'NORMAL',iniciar)
                    iniciar=len(LOG_linha);enviar(bytes([30,2,1,0,0,0,0]));receber(b'jkoros-native> ',iniciar)
                    entrada_Lista_f07b3200=verificar('ps','SUSPENDED','vi process.txt');찾음=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',entrada_Lista_f07b3200);assert 찾음 and int(찾음.group(2))>0,entrada_Lista_f07b3200
                    verificar('free','EL0 mapped KiB: '+찾음.group(2))
                    iniciar=len(LOG_linha);enviar(b'top\n');receber(b'PID SLOT STATE',iniciar);enviar(b'q');receber(b'jkoros-native> ',iniciar)
                    # Test a multibyte prefix through the real shell completion path.
                    if alias_VALOR['df']!='df':
                        iniciar=len(LOG_linha);enviar((alias_VALOR['df'][:-1]+'\t\n').encode());receber(b'RAM only',iniciar);receber(b'jkoros-native> ',iniciar)
                    relatar_VALOR['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as visual_VALOR:
                    visual_VALOR.settimeout(15);visual_VALOR.connect(str(visual_caminho));fluxo_VALOR=visual_VALOR.makefile('rwb');json.loads(fluxo_VALOR.readline());fluxo_VALOR.write(b'{"execute":"qmp_capabilities"}\n');fluxo_VALOR.flush()
                    while 'return' not in json.loads(fluxo_VALOR.readline()):pass
                    enviar((('poweroff' if argumentos.poweroff_only else alias_VALOR['poweroff'])+'\n').encode())
                    while True:
                        Evento=json.loads(fluxo_VALOR.readline())
                        if Evento.get('event')=='SHUTDOWN':break
                    assert Evento['data']['guest'] and Evento['data']['reason']=='guest-shutdown',Evento
                    assert Processo_VALOR.wait(timeout=15)==0
                    relatar_VALOR['shutdown']=Evento;relatar_VALOR['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                relatar_VALOR['network_trace']=ponte_VALOR.log_de_rastreamento
                assert argumentos.poweroff_only or any(entrada_VALOR_962f286b['protocol']==1 and entrada_VALOR_962f286b['direction']=='from_guest' for entrada_VALOR_962f286b in ponte_VALOR.log_de_rastreamento)
                relatar_VALOR['passed']=True
            finally:
                if Processo_VALOR.poll() is None:os.killpg(Processo_VALOR.pid,signal.SIGTERM)
                try:Processo_VALOR.wait(timeout=10)
                except subprocess.TimeoutExpired:Processo_VALOR.kill();Processo_VALOR.wait()
                ESCOLHER_item.close();(saídaTexto/'serial.log').write_bytes(LOG_linha);(saídaTexto/'report.json').write_text(json.dumps(relatar_VALOR,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({Chave_VALOR:VALOR for Chave_VALOR,VALOR in relatar_VALOR.items() if Chave_VALOR!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':iniciar()
