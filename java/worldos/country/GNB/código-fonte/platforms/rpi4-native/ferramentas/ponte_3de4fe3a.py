"""Layer-2/SLIP bridge. TCP, UDP and FTP are processed by the guest, not Python.

QEMU's user network supplies NAT/host forwarding. raspi4b has no emulated GENET,
so a second UART carries IPv4 packets to the guest's lwIP stack.
"""
import select
import socket
import struct
import threading
import time
import ipaddress
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, qemu_network

endereço_real = bytes.fromhex('525400123456')
gateway_hardware_email = bytes.fromhex('52550a000202')
endereço_na_Internet_VALOR = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class ponte_3de4fe3a:
    def __init__(자신, transferência_de_arquivo_número_da_porta=2121, 전달규칙들=(), Captura=False, convidado_email=None, ID_do_host='127.0.0.1'):
        if not 1024 <= transferência_de_arquivo_número_da_porta <= 65535 or 50000 <= transferência_de_arquivo_número_da_porta <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.transferência_de_arquivo_número_da_porta = transferência_de_arquivo_número_da_porta
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        convidado_email = convidado_email or 자신.ip_config['IP']
        qemu_network(자신.ip_config, convidado_email)
        Endereço=ipaddress.IPv4Address(convidado_email)
        자신.convidado_email=str(Endereço); 자신.em_dia_email=Endereço.packed
        Endereço=ipaddress.IPv4Address(ID_do_host)
        if Endereço.is_multicast or str(Endereço)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.ID_do_host=str(Endereço)
        자신.Captura = Captura; 자신.log_de_rastreamento = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', transferência_de_arquivo_número_da_porta)} | {('tcp', dados_cargo) for dados_cargo in range(50000,50008)}
        for regra_VALOR in 전달규칙들:
            caminho_componente = regra_VALOR.split(':')
            if len(caminho_componente) != 3 or caminho_componente[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            rede_ABI, host, convidado = caminho_componente[0], int(caminho_componente[1]), int(caminho_componente[2])
            if not 1024 <= host <= 65535 or not 1 <= convidado <= 65535 or (rede_ABI, host) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + regra_VALOR)
            사용중주소.add((rede_ABI, host)); 자신.전달규칙들.append((rede_ABI, host, convidado))
        자신.수신창구들 = []
        for _ in range(2):
            servidor_VALOR = socket.socket()
            servidor_VALOR.bind(('127.0.0.1', 0)); servidor_VALOR.listen(1); servidor_VALOR.setblocking(False)
            자신.수신창구들.append(servidor_VALOR)
        자신.접속자들 = [None, None]
        자신.TI_Pendente = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.TI_inválido = False
        자신.Pausar_Evento = threading.Event(); 자신.erro = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.tarefaSegundoPlano = threading.Thread(target=자신.Ciclo_VALOR, daemon=True)
        자신.tarefaSegundoPlano.start()

    def 전달인수(자신):
        porta_COM_número, porta_de_rede = [cadeia_dados.getsockname()[1] for cadeia_dados in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.convidado_email) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.transferência_de_arquivo_número_da_porta, 자신.convidado_email)
        for número_da_porta in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(número_da_porta, 자신.convidado_email)
        for rede_ABI, host, convidado in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(rede_ABI, host, 자신.convidado_email, convidado)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.ID_do_host+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(porta_COM_número),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(porta_de_rede),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def execução_quadro(자신, pacote_dados):
        자신.TI_Pendente[1] += struct.pack('!I', len(pacote_dados)) + pacote_dados

    def rastrear_pacote(자신, direção, pacote_dados):
        if not 자신.Captura or len(pacote_dados)<20: return
        DESLOC_VALOR=(pacote_dados[0]&15)*4
        entrada_VALOR_962f286b={'time':time.monotonic(),'direction':direção,'bytes':len(pacote_dados),'protocol':pacote_dados[9]}
        if pacote_dados[9]==6 and len(pacote_dados)>=DESLOC_VALOR+20:
            원본자료,destino_dados_email,ordem_número,확인번호,Configuração_BITS,Janela=struct.unpack_from('!HHIIHH',pacote_dados,DESLOC_VALOR)
            entrada_VALOR_962f286b.update(source=원본자료,destination=destino_dados_email,seq=ordem_número,ack=확인번호,flags=Configuração_BITS&255,window=Janela,
                        payload=len(pacote_dados)-DESLOC_VALOR-((pacote_dados[DESLOC_VALOR+12]>>4)*4))
        자신.log_de_rastreamento.append(entrada_VALOR_962f286b)
        if len(자신.log_de_rastreamento)>2048: del 자신.log_de_rastreamento[:1024]

    def protocolo_SLIP_entrada(자신, dados):
        for ponto_de_código in dados:
            if ponto_de_código == 192:
                if 자신.직렬전문 and not 자신.TI_inválido and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        Endereço=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(Endereço)))
                            자신.em_dia_email=Endereço
                        except ValueError:
                            pass
                    자신.rastrear_pacote('from_guest',자신.직렬전문)
                    자신.execução_quadro(gateway_hardware_email + endereço_real + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.TI_inválido = False
            elif ponto_de_código == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if ponto_de_código not in (220, 221): 자신.TI_inválido = True
                    ponto_de_código = 192 if ponto_de_código == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(ponto_de_código)
                else: 자신.TI_inválido = True

    def Ethernet_entrada(자신, dados):
        자신.Ethernet += dados
        while len(자신.Ethernet) >= 4:
            item_CONT_NÚM = struct.unpack_from('!I', 자신.Ethernet)[0]
            if item_CONT_NÚM > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < item_CONT_NÚM + 4: return
            execução_quadro = bytes(자신.Ethernet[4:4+item_CONT_NÚM]); del 자신.Ethernet[:4+item_CONT_NÚM]
            if len(execução_quadro) < 14: continue
            if execução_quadro[12:14] == b'\x08\x06' and len(execução_quadro) >= 42:
                resolução_de_endereço_pacote = execução_quadro[14:42]
                if resolução_de_endereço_pacote[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and resolução_de_endereço_pacote[24:28] == 자신.em_dia_email:
                    réplica = resolução_de_endereço_pacote[:6] + b'\x00\x02' + endereço_real + 자신.em_dia_email + resolução_de_endereço_pacote[8:18]
                    자신.execução_quadro(execução_quadro[6:12] + endereço_real + b'\x08\x06' + réplica)
            elif execução_quadro[12:14] == b'\x08\x00':
                pacote_dados = execução_quadro[14:]
                자신.rastrear_pacote('to_guest',pacote_dados)
                자신.TI_Pendente[0] += b'\xc0' + pacote_dados.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Ciclo_VALOR(자신):
        try:
            while not 자신.Pausar_Evento.is_set():
                읽기대상들 = [cadeia_dados for 순번, cadeia_dados in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [cadeia_dados for cadeia_dados in 자신.접속자들 if cadeia_dados is not None]
                쓰기대상들 = [cadeia_dados for 순번, cadeia_dados in enumerate(자신.접속자들) if cadeia_dados is not None and 자신.TI_Pendente[순번]]
                읽을수있음, gravável, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for cadeia_dados in 읽을수있음:
                    if cadeia_dados in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(cadeia_dados); 자신.접속자들[순번], _ = cadeia_dados.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(cadeia_dados); dados = cadeia_dados.recv(16384)
                        if not dados: return
                        (자신.protocolo_SLIP_entrada if 순번 == 0 else 자신.Ethernet_entrada)(dados)
                for cadeia_dados in gravável:
                    순번 = 자신.접속자들.index(cadeia_dados)
                    try: item_CONT_NÚM = cadeia_dados.send(자신.TI_Pendente[순번])
                    except BlockingIOError: continue
                    del 자신.TI_Pendente[순번][:item_CONT_NÚM]
                if any(len(SEGUNDO_VALOR) > 1024 * 1024 for SEGUNDO_VALOR in 자신.TI_Pendente):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Pausar_Evento.is_set(): 자신.erro = str(보조항목)

    def Fechar(자신):
        자신.Pausar_Evento.set(); 자신.tarefaSegundoPlano.join(timeout=2)
        for cadeia_dados in 자신.수신창구들 + 자신.접속자들:
            if cadeia_dados is not None: cadeia_dados.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argumento_MATRIZ): 자신.Fechar()
