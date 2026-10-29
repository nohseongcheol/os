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

máquina_ENDEREZO = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
enderezo_de_internet_VALOR = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class Rede_ponte:
    def __init__(자신, transferencia_de_ficheiros_número_do_porto=2121, 전달규칙들=(), capturar=False, convidado_ENDEREZO=None, hospedar_ENDEREZO='127.0.0.1'):
        if not 1024 <= transferencia_de_ficheiros_número_do_porto <= 65535 or 50000 <= transferencia_de_ficheiros_número_do_porto <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.transferencia_de_ficheiros_número_do_porto = transferencia_de_ficheiros_número_do_porto
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        convidado_ENDEREZO = convidado_ENDEREZO or 자신.ip_config['IP']
        qemu_network(자신.ip_config, convidado_ENDEREZO)
        ENDEREZO=ipaddress.IPv4Address(convidado_ENDEREZO)
        자신.convidado_ENDEREZO=str(ENDEREZO); 자신.ao_corrente_ENDEREZO=ENDEREZO.packed
        ENDEREZO=ipaddress.IPv4Address(hospedar_ENDEREZO)
        if ENDEREZO.is_multicast or str(ENDEREZO)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.hospedar_ENDEREZO=str(ENDEREZO)
        자신.capturar = capturar; 자신.traza_LOG = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', transferencia_de_ficheiros_número_do_porto)} | {('tcp', datos_cargo) for datos_cargo in range(50000,50008)}
        for regra_VALOR in 전달규칙들:
            camiño_compoñente = regra_VALOR.split(':')
            if len(camiño_compoñente) != 3 or camiño_compoñente[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, hospedar, convidado = camiño_compoñente[0], int(camiño_compoñente[1]), int(camiño_compoñente[2])
            if not 1024 <= hospedar <= 65535 or not 1 <= convidado <= 65535 or (통신규약, hospedar) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + regra_VALOR)
            사용중주소.add((통신규약, hospedar)); 자신.전달규칙들.append((통신규약, hospedar, convidado))
        자신.수신창구들 = []
        for _ in range(2):
            servidor_VALOR = socket.socket()
            servidor_VALOR.bind(('127.0.0.1', 0)); servidor_VALOR.listen(1); servidor_VALOR.setblocking(False)
            자신.수신창구들.append(servidor_VALOR)
        자신.접속자들 = [None, None]
        자신.Tecnoloxía_da_información_TI_pendente = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.Tecnoloxía_da_información_TI_non_válido = False
        자신.Pausa_evento = threading.Event(); 자신.ERRO = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Ciclo_VALOR, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, porto_Ethernet = [cadea_datos.getsockname()[1] for cadea_datos in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.convidado_ENDEREZO) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.transferencia_de_ficheiros_número_do_porto, 자신.convidado_ENDEREZO)
        for número_do_porto in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(número_do_porto, 자신.convidado_ENDEREZO)
        for 통신규약, hospedar, convidado in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, hospedar, 자신.convidado_ENDEREZO, convidado)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.hospedar_ENDEREZO+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(porto_Ethernet),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, paquete_datos):
        자신.Tecnoloxía_da_información_TI_pendente[1] += struct.pack('!I', len(paquete_datos)) + paquete_datos

    def traza_paquete(자신, 방향, paquete_datos):
        if not 자신.capturar or len(paquete_datos)<20: return
        DESPRAZAMENTO_VALOR=(paquete_datos[0]&15)*4
        introdución_VALOR={'time':time.monotonic(),'direction':방향,'bytes':len(paquete_datos),'protocol':paquete_datos[9]}
        if paquete_datos[9]==6 and len(paquete_datos)>=DESPRAZAMENTO_VALOR+20:
            원본자료,destino_datos_ENDEREZO,순서번호,확인번호,configuración_Servizo_de_transferencia_intelixente_en_segundo_plano,Xanela=struct.unpack_from('!HHIIHH',paquete_datos,DESPRAZAMENTO_VALOR)
            introdución_VALOR.update(source=원본자료,destination=destino_datos_ENDEREZO,seq=순서번호,ack=확인번호,flags=configuración_Servizo_de_transferencia_intelixente_en_segundo_plano&255,window=Xanela,
                        payload=len(paquete_datos)-DESPRAZAMENTO_VALOR-((paquete_datos[DESPRAZAMENTO_VALOR+12]>>4)*4))
        자신.traza_LOG.append(introdución_VALOR)
        if len(자신.traza_LOG)>2048: del 자신.traza_LOG[:1024]

    def 직렬전문입력(자신, datos):
        for código_de_carácter in datos:
            if código_de_carácter == 192:
                if 자신.직렬전문 and not 자신.Tecnoloxía_da_información_TI_non_válido and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        ENDEREZO=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(ENDEREZO)))
                            자신.ao_corrente_ENDEREZO=ENDEREZO
                        except ValueError:
                            pass
                    자신.traza_paquete('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + máquina_ENDEREZO + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.Tecnoloxía_da_información_TI_non_válido = False
            elif código_de_carácter == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if código_de_carácter not in (220, 221): 자신.Tecnoloxía_da_información_TI_non_válido = True
                    código_de_carácter = 192 if código_de_carácter == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(código_de_carácter)
                else: 자신.Tecnoloxía_da_información_TI_non_válido = True

    def 이더넷입력(자신, datos):
        자신.Ethernet += datos
        while len(자신.Ethernet) >= 4:
            elemento_CONTAR = struct.unpack_from('!I', 자신.Ethernet)[0]
            if elemento_CONTAR > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < elemento_CONTAR + 4: return
            실행틀 = bytes(자신.Ethernet[4:4+elemento_CONTAR]); del 자신.Ethernet[:4+elemento_CONTAR]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                ENDEREZO_resolución_paquete = 실행틀[14:42]
                if ENDEREZO_resolución_paquete[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and ENDEREZO_resolución_paquete[24:28] == 자신.ao_corrente_ENDEREZO:
                    resposta_1262b476 = ENDEREZO_resolución_paquete[:6] + b'\x00\x02' + máquina_ENDEREZO + 자신.ao_corrente_ENDEREZO + ENDEREZO_resolución_paquete[8:18]
                    자신.실행틀(실행틀[6:12] + máquina_ENDEREZO + b'\x08\x06' + resposta_1262b476)
            elif 실행틀[12:14] == b'\x08\x00':
                paquete_datos = 실행틀[14:]
                자신.traza_paquete('to_guest',paquete_datos)
                자신.Tecnoloxía_da_información_TI_pendente[0] += b'\xc0' + paquete_datos.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Ciclo_VALOR(자신):
        try:
            while not 자신.Pausa_evento.is_set():
                읽기대상들 = [cadea_datos for 순번, cadea_datos in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [cadea_datos for cadea_datos in 자신.접속자들 if cadea_datos is not None]
                쓰기대상들 = [cadea_datos for 순번, cadea_datos in enumerate(자신.접속자들) if cadea_datos is not None and 자신.Tecnoloxía_da_información_TI_pendente[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for cadea_datos in 읽을수있음:
                    if cadea_datos in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(cadea_datos); 자신.접속자들[순번], _ = cadea_datos.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(cadea_datos); datos = cadea_datos.recv(16384)
                        if not datos: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(datos)
                for cadea_datos in 쓸수있음:
                    순번 = 자신.접속자들.index(cadea_datos)
                    try: elemento_CONTAR = cadea_datos.send(자신.Tecnoloxía_da_información_TI_pendente[순번])
                    except BlockingIOError: continue
                    del 자신.Tecnoloxía_da_información_TI_pendente[순번][:elemento_CONTAR]
                if any(len(SEGUNDO_VALOR) > 1024 * 1024 for SEGUNDO_VALOR in 자신.Tecnoloxía_da_información_TI_pendente):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Pausa_evento.is_set(): 자신.ERRO = str(보조항목)

    def Pechar(자신):
        자신.Pausa_evento.set(); 자신.작업가닥.join(timeout=2)
        for cadea_datos in 자신.수신창구들 + 자신.접속자들:
            if cadea_datos is not None: cadea_datos.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argumento_MATRIZ): 자신.Pechar()
