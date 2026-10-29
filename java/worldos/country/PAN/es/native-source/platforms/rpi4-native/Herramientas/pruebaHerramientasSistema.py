#!/usr/bin/env python3
"""datosEfectivo propio 커널의 IP/ICMP, valorEstadoValor valorConsultar, 현지어 comando, 게스트 programaSalir validar."""
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


def ponerEnMarcha():
    Analizador=argparse.ArgumentParser();Analizador.add_argument('--edition',type=Path);Analizador.add_argument('--output',type=Path);Analizador.add_argument('--poweroff-only',action='store_true');argumentos=Analizador.parse_args()
    raízProyecto=Path(__file__).resolve().parents[1];ajustes={};tablaNombre={}
    if argumentos.edition:
        valorPaís=argumentos.edition.resolve();ajustes=json.loads((valorPaís/'native.json').read_text());tablaNombre=ajustes['identifiers'];raízProyecto=valorPaís/ajustes['source']/ajustes['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(valorPaís/'native-edition.py'),'check'])
        Anfitrión=valorPaís/'host/qemu'
        if Anfitrión.is_file():os.environ['QEMU_AARCH64']=str(Anfitrión)
    Herramientas=raízProyecto/Path(ajustes.get('runner','Herramientas/ejecutarComando.py')).parent
    sys.path.insert(0,str(Herramientas))
    def leer(nombre):
        ruta=Herramientas/(tablaNombre.get(nombre,nombre)+'.py');valorContrato=importlib.util.spec_from_file_location('test_'+nombre,str(ruta));valorMódulo=importlib.util.module_from_spec(valorContrato);valorContrato.loader.exec_module(valorMódulo);return valorMódulo
    móduloEjecución=leer('ejecutarComando');móduloRed=leer('puenteRed');comando=getattr(móduloEjecución,tablaNombre.get('comando','comando'));tipoPuente=getattr(móduloRed,tablaNombre.get('puenteRed','puenteRed'))
    valorAlias=ajustes.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'direcciónIP','ping':'pruebaRespuestaRetorno','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'desactivadoAlimentación','help':'mostrarAyuda'})
    sys.path.insert(0,str(raízProyecto/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(raízProyecto);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    Salida=argumentos.output or raízProyecto/'build/verification/system-tools';Salida.mkdir(parents=True,exist_ok=True)
    valorInforme={'passed':False,'country':ajustes.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((raízProyecto/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    registroEntradaDiario=bytearray();valorSecuencia=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as valorTemporal:
        rutaControl=Path(valorTemporal)/'qmp.sock'
        while True:
            with socket.socket() as buscarCoincidenciaValor:buscarCoincidenciaValor.bind(('127.0.0.1',0));númeroPuerto=buscarCoincidenciaValor.getsockname()[1]
            if not 50000<=númeroPuerto<=50007:break
        with tipoPuente(númeroPuerto,capturarDatos=True,direcciónInvitado=ipTestText('10.0.2.20'),direcciónAnfitrión='127.0.0.2') as valorPuente:
            valorProceso=subprocess.Popen(comando()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(rutaControl)]+valorPuente.argumentoReenviado(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            elementoListaElegir=selectors.DefaultSelector();elementoListaElegir.register(valorProceso.stdout,selectors.EVENT_READ)
            def recibir(mostrarValor,ponerEnMarcha=0,valorLímite=45):
                terminación=time.monotonic()+valorLímite
                while mostrarValor not in registroEntradaDiario[ponerEnMarcha:]:
                    if time.monotonic()>terminación or valorProceso.poll() is not None:raise AssertionError('Missing '+repr(mostrarValor)+'\n'+registroEntradaDiario[ponerEnMarcha:].decode('utf-8','replace'))
                    for valorTecla,_ in elementoListaElegir.select(.1):
                        Datos=valorTecla.fileobj.read(65536)
                        if Datos:registroEntradaDiario.extend(Datos)
                return registroEntradaDiario[ponerEnMarcha:].decode('utf-8','replace').replace('\r\n','\n')
            def enviar(Datos):valorProceso.stdin.write(Datos);valorProceso.stdin.flush()
            def intérpreteComandos(texto):
                texto=ipTestText(texto)
                print(valorInforme['country'],texto,flush=True);valorSecuencia[0]+=1;mostrarValor='__SYSTEM_DONE_'+str(valorSecuencia[0])+'__';ponerEnMarcha=len(registroEntradaDiario)
                enviar((texto+'; echo; echo '+mostrarValor+'\n').encode())
                marcadorFin=('\r\n'+mostrarValor+'\r\n').encode();recibir(marcadorFin,ponerEnMarcha)
                posiciónFin=registroEntradaDiario.index(marcadorFin,ponerEnMarcha)+len(marcadorFin)
                recibir(b'jkoros-native> ',posiciónFin)
                return registroEntradaDiario[ponerEnMarcha:].decode('utf-8','replace').replace('\r\n','\n')
            def verificar(texto,*valores):
                respuesta=intérpreteComandos(texto)
                for valor in valores:assert ipTestText(valor) in respuesta,(texto,valor,respuesta)
                return respuesta
            try:
                recibir(b'jkoros-native> ')
                if not argumentos.poweroff_only:
                    valorAyuda=verificar('help system','ipconfig','ping','ps','top','df','poweroff')
                    for nombreAlternativo in valorAlias.values():assert nombreAlternativo in valorAyuda,(nombreAlternativo,valorAyuda)
                    verificar(valorAlias['help']+' system','Network / system')
                    verificar('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    verificar(valorAlias['ipconfig'],'inet 10.0.2.15');verificar('ip addr show','sl0: UP');verificar('ifconfig','sl0: UP')
                    for ajustesInválido in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        error=verificar('ipconfig set '+ajustesInválido+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in error,error
                        verificar('ipconfig','inet 10.0.2.15')
                    verificar('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    verificar(valorAlias['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verificar('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    verificar('ip link set dev sl0 down','sl0: DOWN');verificar('ping -c 1 10.0.2.2; echo STATUS=$?','error -100','STATUS=1')
                    verificar('ipconfig up','sl0: UP')
                    verificar(valorAlias['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    verificar('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    verificar('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');verificar(valorAlias['route'],'10.0.2.2 sl0')
                    verificar('ftpd start','FTP listening')
                    verificar(valorAlias['netstat'],'10.0.2.20:21','LISTEN');verificar('ss','LISTEN')
                    verificar('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','error -16')
                    with ftplib.FTP() as valorCliente:
                        valorCliente.connect('127.0.0.2',númeroPuerto,timeout=20);valorCliente.login();Datos=b'Network address was changed in the guest.\n'
                        valorCliente.storbinary('STOR net-state.txt',io.BytesIO(Datos));datosRecibido=bytearray();valorCliente.retrbinary('RETR net-state.txt',datosRecibido.extend);assert datosRecibido==Datos;valorCliente.delete('net-state.txt')
                    verificar('ftpd stop','FTP stopped');verificar('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    valorInforme['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def guardado(texto):
                        valorEncontrado=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',texto);assert valorEncontrado,texto;return tuple(map(int,valorEncontrado.groups()))
                    valorAntes=guardado(verificar('df','RAM only'));verificar('echo disk-proof > sys-state.txt');estadoValorDespués=guardado(verificar(valorAlias['df'],'RAM only'))
                    assert estadoValorDespués[1]-valorAntes[1]==16384 and estadoValorDespués[4]-valorAntes[4]==1 and estadoValorDespués[3]-valorAntes[3]==11,(valorAntes,estadoValorDespués)
                    verificar('rm sys-state.txt');assert guardado(intérpreteComandos('df'))==valorAntes
                    Memoria=verificar(valorAlias['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');valorCantidad=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',Memoria).groups()));assert 0<valorCantidad[1]<=valorCantidad[0] and valorCantidad[1]+valorCantidad[2]==valorCantidad[0]
                    verificar(valorAlias['ps'],'kernel/shell');verificar(valorAlias['uptime'],'seconds')
                    informaciónEstado=verificar(valorAlias['top']+' -n 2','kernel/shell');assert informaciónEstado.count('PID SLOT STATE')==2,informaciónEstado
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    verificar('terminal','TERMINAL READY');ponerEnMarcha=len(registroEntradaDiario);enviar(b'vi process.txt\n');recibir(b'NORMAL',ponerEnMarcha)
                    ponerEnMarcha=len(registroEntradaDiario);enviar(bytes([30,2,1,0,0,0,0]));recibir(b'jkoros-native> ',ponerEnMarcha)
                    listaEntradaElemento=verificar('ps','SUSPENDED','vi process.txt');valorEncontrado=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',listaEntradaElemento);assert valorEncontrado and int(valorEncontrado.group(2))>0,listaEntradaElemento
                    verificar('free','EL0 mapped KiB: '+valorEncontrado.group(2))
                    ponerEnMarcha=len(registroEntradaDiario);enviar(b'top\n');recibir(b'PID SLOT STATE',ponerEnMarcha);enviar(b'q');recibir(b'jkoros-native> ',ponerEnMarcha)
                    # Test a multibyte prefix through the real shell completion path.
                    if valorAlias['df']!='df':
                        ponerEnMarcha=len(registroEntradaDiario);enviar((valorAlias['df'][:-1]+'\t\n').encode());recibir(b'RAM only',ponerEnMarcha);recibir(b'jkoros-native> ',ponerEnMarcha)
                    valorInforme['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as valorControl:
                    valorControl.settimeout(15);valorControl.connect(str(rutaControl));valorFlujo=valorControl.makefile('rwb');json.loads(valorFlujo.readline());valorFlujo.write(b'{"execute":"qmp_capabilities"}\n');valorFlujo.flush()
                    while 'return' not in json.loads(valorFlujo.readline()):pass
                    enviar((('poweroff' if argumentos.poweroff_only else valorAlias['poweroff'])+'\n').encode())
                    while True:
                        evento=json.loads(valorFlujo.readline())
                        if evento.get('event')=='SHUTDOWN':break
                    assert evento['data']['guest'] and evento['data']['reason']=='guest-shutdown',evento
                    assert valorProceso.wait(timeout=15)==0
                    valorInforme['shutdown']=evento;valorInforme['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                valorInforme['network_trace']=valorPuente.diarioTraza
                assert argumentos.poweroff_only or any(valorEntradaElemento['protocol']==1 and valorEntradaElemento['direction']=='from_guest' for valorEntradaElemento in valorPuente.diarioTraza)
                valorInforme['passed']=True
            finally:
                if valorProceso.poll() is None:os.killpg(valorProceso.pid,signal.SIGTERM)
                try:valorProceso.wait(timeout=10)
                except subprocess.TimeoutExpired:valorProceso.kill();valorProceso.wait()
                elementoListaElegir.close();(Salida/'serial.log').write_bytes(registroEntradaDiario);(Salida/'report.json').write_text(json.dumps(valorInforme,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({valorTecla:valor for valorTecla,valor in valorInforme.items() if valorTecla!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':ponerEnMarcha()
