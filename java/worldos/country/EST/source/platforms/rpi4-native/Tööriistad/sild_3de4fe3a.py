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

absoluutaadress = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
Interneti_aadress_VALUE = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class sild_3de4fe3a:
    def __init__(자신, failiedastus_pordinumber=2121, 전달규칙들=(), hõivama=False, külaline_ADDRESS=None, host_ADDRESS='127.0.0.1'):
        if not 1024 <= failiedastus_pordinumber <= 65535 or 50000 <= failiedastus_pordinumber <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.failiedastus_pordinumber = failiedastus_pordinumber
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        külaline_ADDRESS = külaline_ADDRESS or 자신.ip_config['IP']
        qemu_network(자신.ip_config, külaline_ADDRESS)
        ADDRESS=ipaddress.IPv4Address(külaline_ADDRESS)
        자신.külaline_ADDRESS=str(ADDRESS); 자신.tähtaja_piires_ADDRESS=ADDRESS.packed
        ADDRESS=ipaddress.IPv4Address(host_ADDRESS)
        if ADDRESS.is_multicast or str(ADDRESS)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.host_ADDRESS=str(ADDRESS)
        자신.hõivama = hõivama; 자신.jälituslogi = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', failiedastus_pordinumber)} | {('tcp', andmed_ametikoht) for andmed_ametikoht in range(50000,50008)}
        for filter_VALUE in 전달규칙들:
            tee_komponent = filter_VALUE.split(':')
            if len(tee_komponent) != 3 or tee_komponent[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, host, külaline = tee_komponent[0], int(tee_komponent[1]), int(tee_komponent[2])
            if not 1024 <= host <= 65535 or not 1 <= külaline <= 65535 or (통신규약, host) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + filter_VALUE)
            사용중주소.add((통신규약, host)); 자신.전달규칙들.append((통신규약, host, külaline))
        자신.수신창구들 = []
        for _ in range(2):
            server_VALUE = socket.socket()
            server_VALUE.bind(('127.0.0.1', 0)); server_VALUE.listen(1); server_VALUE.setblocking(False)
            자신.수신창구들.append(server_VALUE)
        자신.접속자들 = [None, None]
        자신.infotehnoloogia_ootel = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.infotehnoloogia_kehtetu = False
        자신.Peata_sündmus = threading.Event(); 자신.VIGA = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.töötaja = threading.Thread(target=자신.tsükkel_VALUE, daemon=True)
        자신.töötaja.start()

    def 전달인수(자신):
        COM_port_number, Etherneti_liides = [string_andmed.getsockname()[1] for string_andmed in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.külaline_ADDRESS) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.failiedastus_pordinumber, 자신.külaline_ADDRESS)
        for pordinumber in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(pordinumber, 자신.külaline_ADDRESS)
        for 통신규약, host, külaline in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, host, 자신.külaline_ADDRESS, külaline)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.host_ADDRESS+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(COM_port_number),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Etherneti_liides),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, pakett_andmed):
        자신.infotehnoloogia_ootel[1] += struct.pack('!I', len(pakett_andmed)) + pakett_andmed

    def jälg_pakett(자신, 방향, pakett_andmed):
        if not 자신.hõivama or len(pakett_andmed)<20: return
        nihe_VALUE=(pakett_andmed[0]&15)*4
        kirje_VALUE={'time':time.monotonic(),'direction':방향,'bytes':len(pakett_andmed),'protocol':pakett_andmed[9]}
        if pakett_andmed[9]==6 and len(pakett_andmed)>=nihe_VALUE+20:
            원본자료,sihtkoht_andmed_ADDRESS,tellimus_number,확인번호,konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus,aken=struct.unpack_from('!HHIIHH',pakett_andmed,nihe_VALUE)
            kirje_VALUE.update(source=원본자료,destination=sihtkoht_andmed_ADDRESS,seq=tellimus_number,ack=확인번호,flags=konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus&255,window=aken,
                        payload=len(pakett_andmed)-nihe_VALUE-((pakett_andmed[nihe_VALUE+12]>>4)*4))
        자신.jälituslogi.append(kirje_VALUE)
        if len(자신.jälituslogi)>2048: del 자신.jälituslogi[:1024]

    def 직렬전문입력(자신, andmed):
        for koodipunkt in andmed:
            if koodipunkt == 192:
                if 자신.직렬전문 and not 자신.infotehnoloogia_kehtetu and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        ADDRESS=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(ADDRESS)))
                            자신.tähtaja_piires_ADDRESS=ADDRESS
                        except ValueError:
                            pass
                    자신.jälg_pakett('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + absoluutaadress + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.infotehnoloogia_kehtetu = False
            elif koodipunkt == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if koodipunkt not in (220, 221): 자신.infotehnoloogia_kehtetu = True
                    koodipunkt = 192 if koodipunkt == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(koodipunkt)
                else: 자신.infotehnoloogia_kehtetu = True

    def 이더넷입력(자신, andmed):
        자신.Ethernet += andmed
        while len(자신.Ethernet) >= 4:
            kaup_COUNT = struct.unpack_from('!I', 자신.Ethernet)[0]
            if kaup_COUNT > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < kaup_COUNT + 4: return
            실행틀 = bytes(자신.Ethernet[4:4+kaup_COUNT]); del 자신.Ethernet[:4+kaup_COUNT]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                ADDRESS_eraldusvõime_pakett = 실행틀[14:42]
                if ADDRESS_eraldusvõime_pakett[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and ADDRESS_eraldusvõime_pakett[24:28] == 자신.tähtaja_piires_ADDRESS:
                    vastus_1262b476 = ADDRESS_eraldusvõime_pakett[:6] + b'\x00\x02' + absoluutaadress + 자신.tähtaja_piires_ADDRESS + ADDRESS_eraldusvõime_pakett[8:18]
                    자신.실행틀(실행틀[6:12] + absoluutaadress + b'\x08\x06' + vastus_1262b476)
            elif 실행틀[12:14] == b'\x08\x00':
                pakett_andmed = 실행틀[14:]
                자신.jälg_pakett('to_guest',pakett_andmed)
                자신.infotehnoloogia_ootel[0] += b'\xc0' + pakett_andmed.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def tsükkel_VALUE(자신):
        try:
            while not 자신.Peata_sündmus.is_set():
                읽기대상들 = [string_andmed for 순번, string_andmed in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [string_andmed for string_andmed in 자신.접속자들 if string_andmed is not None]
                쓰기대상들 = [string_andmed for 순번, string_andmed in enumerate(자신.접속자들) if string_andmed is not None and 자신.infotehnoloogia_ootel[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for string_andmed in 읽을수있음:
                    if string_andmed in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(string_andmed); 자신.접속자들[순번], _ = string_andmed.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(string_andmed); andmed = string_andmed.recv(16384)
                        if not andmed: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(andmed)
                for string_andmed in 쓸수있음:
                    순번 = 자신.접속자들.index(string_andmed)
                    try: kaup_COUNT = string_andmed.send(자신.infotehnoloogia_ootel[순번])
                    except BlockingIOError: continue
                    del 자신.infotehnoloogia_ootel[순번][:kaup_COUNT]
                if any(len(SECOND_VALUE) > 1024 * 1024 for SECOND_VALUE in 자신.infotehnoloogia_ootel):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Peata_sündmus.is_set(): 자신.VIGA = str(보조항목)

    def Suletud(자신):
        자신.Peata_sündmus.set(); 자신.töötaja.join(timeout=2)
        for string_andmed in 자신.수신창구들 + 자신.접속자들:
            if string_andmed is not None: string_andmed.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argument_ARRAY): 자신.Suletud()
