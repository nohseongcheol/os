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

màquina_ADREÇA = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
adreça_d_Internet_VALOR = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class xarxa_pont:
    def __init__(자신, transferència_de_fitxers_número_de_port=2121, 전달규칙들=(), capturar=False, convidat_ADREÇA=None, allotjar_ADREÇA='127.0.0.1'):
        if not 1024 <= transferència_de_fitxers_número_de_port <= 65535 or 50000 <= transferència_de_fitxers_número_de_port <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.transferència_de_fitxers_número_de_port = transferència_de_fitxers_número_de_port
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        convidat_ADREÇA = convidat_ADREÇA or 자신.ip_config['IP']
        qemu_network(자신.ip_config, convidat_ADREÇA)
        Adreça=ipaddress.IPv4Address(convidat_ADREÇA)
        자신.convidat_ADREÇA=str(Adreça); 자신.현재주소=Adreça.packed
        Adreça=ipaddress.IPv4Address(allotjar_ADREÇA)
        if Adreça.is_multicast or str(Adreça)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.allotjar_ADREÇA=str(Adreça)
        자신.capturar = capturar; 자신.traça_LOG = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', transferència_de_fitxers_número_de_port)} | {('tcp', dades_càrrec) for dades_càrrec in range(50000,50008)}
        for regla_VALOR in 전달규칙들:
            camí_component = regla_VALOR.split(':')
            if len(camí_component) != 3 or camí_component[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, allotjar, convidat = camí_component[0], int(camí_component[1]), int(camí_component[2])
            if not 1024 <= allotjar <= 65535 or not 1 <= convidat <= 65535 or (통신규약, allotjar) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + regla_VALOR)
            사용중주소.add((통신규약, allotjar)); 자신.전달규칙들.append((통신규약, allotjar, convidat))
        자신.수신창구들 = []
        for _ in range(2):
            servidor_VALOR = socket.socket()
            servidor_VALOR.bind(('127.0.0.1', 0)); servidor_VALOR.listen(1); servidor_VALOR.setblocking(False)
            자신.수신창구들.append(servidor_VALOR)
        자신.접속자들 = [None, None]
        자신.tecnologies_de_la_informació_pendent = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.tecnologies_de_la_informació_invàlid = False
        자신.Pausa_incidència = threading.Event(); 자신.s_ha_produït_un_error = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Cicle_VALOR, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, port_Ethernet = [cadena_dades.getsockname()[1] for cadena_dades in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.convidat_ADREÇA) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.transferència_de_fitxers_número_de_port, 자신.convidat_ADREÇA)
        for número_de_port in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(número_de_port, 자신.convidat_ADREÇA)
        for 통신규약, allotjar, convidat in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, allotjar, 자신.convidat_ADREÇA, convidat)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.allotjar_ADREÇA+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(port_Ethernet),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, paquet_dades):
        자신.tecnologies_de_la_informació_pendent[1] += struct.pack('!I', len(paquet_dades)) + paquet_dades

    def traça_paquet(자신, 방향, paquet_dades):
        if not 자신.capturar or len(paquet_dades)<20: return
        DESPLAÇAMENT_VALOR=(paquet_dades[0]&15)*4
        introducció_VALOR={'time':time.monotonic(),'direction':방향,'bytes':len(paquet_dades),'protocol':paquet_dades[9]}
        if paquet_dades[9]==6 and len(paquet_dades)>=DESPLAÇAMENT_VALOR+20:
            원본자료,destinació_dades_ADREÇA,순서번호,확인번호,configuració_Servei_de_transferència_intel_ligent_en_segon_terme,Finestra=struct.unpack_from('!HHIIHH',paquet_dades,DESPLAÇAMENT_VALOR)
            introducció_VALOR.update(source=원본자료,destination=destinació_dades_ADREÇA,seq=순서번호,ack=확인번호,flags=configuració_Servei_de_transferència_intel_ligent_en_segon_terme&255,window=Finestra,
                        payload=len(paquet_dades)-DESPLAÇAMENT_VALOR-((paquet_dades[DESPLAÇAMENT_VALOR+12]>>4)*4))
        자신.traça_LOG.append(introducció_VALOR)
        if len(자신.traça_LOG)>2048: del 자신.traça_LOG[:1024]

    def 직렬전문입력(자신, dades):
        for codi_de_caràcter in dades:
            if codi_de_caràcter == 192:
                if 자신.직렬전문 and not 자신.tecnologies_de_la_informació_invàlid and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        Adreça=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(Adreça)))
                            자신.현재주소=Adreça
                        except ValueError:
                            pass
                    자신.traça_paquet('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + màquina_ADREÇA + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.tecnologies_de_la_informació_invàlid = False
            elif codi_de_caràcter == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if codi_de_caràcter not in (220, 221): 자신.tecnologies_de_la_informació_invàlid = True
                    codi_de_caràcter = 192 if codi_de_caràcter == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(codi_de_caràcter)
                else: 자신.tecnologies_de_la_informació_invàlid = True

    def 이더넷입력(자신, dades):
        자신.Ethernet += dades
        while len(자신.Ethernet) >= 4:
            element_COMPT = struct.unpack_from('!I', 자신.Ethernet)[0]
            if element_COMPT > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < element_COMPT + 4: return
            실행틀 = bytes(자신.Ethernet[4:4+element_COMPT]); del 자신.Ethernet[:4+element_COMPT]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                ADREÇA_resolució_paquet = 실행틀[14:42]
                if ADREÇA_resolució_paquet[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and ADREÇA_resolució_paquet[24:28] == 자신.현재주소:
                    resposta_1262b476 = ADREÇA_resolució_paquet[:6] + b'\x00\x02' + màquina_ADREÇA + 자신.현재주소 + ADREÇA_resolució_paquet[8:18]
                    자신.실행틀(실행틀[6:12] + màquina_ADREÇA + b'\x08\x06' + resposta_1262b476)
            elif 실행틀[12:14] == b'\x08\x00':
                paquet_dades = 실행틀[14:]
                자신.traça_paquet('to_guest',paquet_dades)
                자신.tecnologies_de_la_informació_pendent[0] += b'\xc0' + paquet_dades.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Cicle_VALOR(자신):
        try:
            while not 자신.Pausa_incidència.is_set():
                읽기대상들 = [cadena_dades for 순번, cadena_dades in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [cadena_dades for cadena_dades in 자신.접속자들 if cadena_dades is not None]
                쓰기대상들 = [cadena_dades for 순번, cadena_dades in enumerate(자신.접속자들) if cadena_dades is not None and 자신.tecnologies_de_la_informació_pendent[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for cadena_dades in 읽을수있음:
                    if cadena_dades in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(cadena_dades); 자신.접속자들[순번], _ = cadena_dades.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(cadena_dades); dades = cadena_dades.recv(16384)
                        if not dades: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(dades)
                for cadena_dades in 쓸수있음:
                    순번 = 자신.접속자들.index(cadena_dades)
                    try: element_COMPT = cadena_dades.send(자신.tecnologies_de_la_informació_pendent[순번])
                    except BlockingIOError: continue
                    del 자신.tecnologies_de_la_informació_pendent[순번][:element_COMPT]
                if any(len(SEGON_VALOR) > 1024 * 1024 for SEGON_VALOR in 자신.tecnologies_de_la_informació_pendent):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Pausa_incidència.is_set(): 자신.s_ha_produït_un_error = str(보조항목)

    def Tanca(자신):
        자신.Pausa_incidència.set(); 자신.작업가닥.join(timeout=2)
        for cadena_dades in 자신.수신창구들 + 자신.접속자들:
            if cadena_dades is not None: cadena_dades.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *arg_MATRIU): 자신.Tanca()
