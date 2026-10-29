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

absolutt_adresse = bytes.fromhex('525400123456')
gateway_maskinvare_e_post = bytes.fromhex('52550a000202')
Internett_adresse_VERDI = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class bro_3de4fe3a:
    def __init__(자신, filoverføring_portnummer=2121, 전달규칙들=(), hente=False, gjest_e_post=None, vert_e_post='127.0.0.1'):
        if not 1024 <= filoverføring_portnummer <= 65535 or 50000 <= filoverføring_portnummer <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.filoverføring_portnummer = filoverføring_portnummer
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        gjest_e_post = gjest_e_post or 자신.ip_config['IP']
        qemu_network(자신.ip_config, gjest_e_post)
        e_post=ipaddress.IPv4Address(gjest_e_post)
        자신.gjest_e_post=str(e_post); 자신.betalt_e_post=e_post.packed
        e_post=ipaddress.IPv4Address(vert_e_post)
        if e_post.is_multicast or str(e_post)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.vert_e_post=str(e_post)
        자신.hente = hente; 자신.sporingslogg = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', filoverføring_portnummer)} | {('tcp', data_plassere) for data_plassere in range(50000,50008)}
        for regel_VERDI in 전달규칙들:
            bane_komponent = regel_VERDI.split(':')
            if len(bane_komponent) != 3 or bane_komponent[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, vert, gjest = bane_komponent[0], int(bane_komponent[1]), int(bane_komponent[2])
            if not 1024 <= vert <= 65535 or not 1 <= gjest <= 65535 or (통신규약, vert) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + regel_VERDI)
            사용중주소.add((통신규약, vert)); 자신.전달규칙들.append((통신규약, vert, gjest))
        자신.수신창구들 = []
        for _ in range(2):
            server_VERDI = socket.socket()
            server_VERDI.bind(('127.0.0.1', 0)); server_VERDI.listen(1); server_VERDI.setblocking(False)
            자신.수신창구들.append(server_VERDI)
        자신.접속자들 = [None, None]
        자신.informasjonssystemer_Venter = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.informasjonssystemer_ugyldig = False
        자신.Pause_hendelse = threading.Event(); 자신.feil = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.arbeider = threading.Thread(target=자신.Krets_VERDI, daemon=True)
        자신.arbeider.start()

    def 전달인수(자신):
        COM_port_nummer, Ethernet_port = [streng_data.getsockname()[1] for streng_data in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.gjest_e_post) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.filoverføring_portnummer, 자신.gjest_e_post)
        for portnummer in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(portnummer, 자신.gjest_e_post)
        for 통신규약, vert, gjest in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, vert, 자신.gjest_e_post, gjest)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.vert_e_post+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(COM_port_nummer),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethernet_port),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def kjøring_bilde(자신, pakke_data):
        자신.informasjonssystemer_Venter[1] += struct.pack('!I', len(pakke_data)) + pakke_data

    def spor_pakke(자신, 방향, pakke_data):
        if not 자신.hente or len(pakke_data)<20: return
        FORSKYVNING_VERDI=(pakke_data[0]&15)*4
        oppføring_VERDI={'time':time.monotonic(),'direction':방향,'bytes':len(pakke_data),'protocol':pakke_data[9]}
        if pakke_data[9]==6 and len(pakke_data)>=FORSKYVNING_VERDI+20:
            원본자료,mål_data_e_post,ordre_nummer,확인번호,konfigurasjon_BITS,Vindu=struct.unpack_from('!HHIIHH',pakke_data,FORSKYVNING_VERDI)
            oppføring_VERDI.update(source=원본자료,destination=mål_data_e_post,seq=ordre_nummer,ack=확인번호,flags=konfigurasjon_BITS&255,window=Vindu,
                        payload=len(pakke_data)-FORSKYVNING_VERDI-((pakke_data[FORSKYVNING_VERDI+12]>>4)*4))
        자신.sporingslogg.append(oppføring_VERDI)
        if len(자신.sporingslogg)>2048: del 자신.sporingslogg[:1024]

    def 직렬전문입력(자신, data):
        for tegnkode in data:
            if tegnkode == 192:
                if 자신.직렬전문 and not 자신.informasjonssystemer_ugyldig and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        e_post=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(e_post)))
                            자신.betalt_e_post=e_post
                        except ValueError:
                            pass
                    자신.spor_pakke('from_guest',자신.직렬전문)
                    자신.kjøring_bilde(gateway_maskinvare_e_post + absolutt_adresse + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.informasjonssystemer_ugyldig = False
            elif tegnkode == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if tegnkode not in (220, 221): 자신.informasjonssystemer_ugyldig = True
                    tegnkode = 192 if tegnkode == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(tegnkode)
                else: 자신.informasjonssystemer_ugyldig = True

    def Ethernet_inndata(자신, data):
        자신.Ethernet += data
        while len(자신.Ethernet) >= 4:
            vare_ANTALL = struct.unpack_from('!I', 자신.Ethernet)[0]
            if vare_ANTALL > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < vare_ANTALL + 4: return
            kjøring_bilde = bytes(자신.Ethernet[4:4+vare_ANTALL]); del 자신.Ethernet[:4+vare_ANTALL]
            if len(kjøring_bilde) < 14: continue
            if kjøring_bilde[12:14] == b'\x08\x06' and len(kjøring_bilde) >= 42:
                e_post_oppløsning_pakke = kjøring_bilde[14:42]
                if e_post_oppløsning_pakke[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and e_post_oppløsning_pakke[24:28] == 자신.betalt_e_post:
                    svar_1262b476 = e_post_oppløsning_pakke[:6] + b'\x00\x02' + absolutt_adresse + 자신.betalt_e_post + e_post_oppløsning_pakke[8:18]
                    자신.kjøring_bilde(kjøring_bilde[6:12] + absolutt_adresse + b'\x08\x06' + svar_1262b476)
            elif kjøring_bilde[12:14] == b'\x08\x00':
                pakke_data = kjøring_bilde[14:]
                자신.spor_pakke('to_guest',pakke_data)
                자신.informasjonssystemer_Venter[0] += b'\xc0' + pakke_data.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Krets_VERDI(자신):
        try:
            while not 자신.Pause_hendelse.is_set():
                읽기대상들 = [streng_data for 순번, streng_data in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [streng_data for streng_data in 자신.접속자들 if streng_data is not None]
                쓰기대상들 = [streng_data for 순번, streng_data in enumerate(자신.접속자들) if streng_data is not None and 자신.informasjonssystemer_Venter[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for streng_data in 읽을수있음:
                    if streng_data in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(streng_data); 자신.접속자들[순번], _ = streng_data.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(streng_data); data = streng_data.recv(16384)
                        if not data: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.Ethernet_inndata)(data)
                for streng_data in 쓸수있음:
                    순번 = 자신.접속자들.index(streng_data)
                    try: vare_ANTALL = streng_data.send(자신.informasjonssystemer_Venter[순번])
                    except BlockingIOError: continue
                    del 자신.informasjonssystemer_Venter[순번][:vare_ANTALL]
                if any(len(SEKUND_VERDI) > 1024 * 1024 for SEKUND_VERDI in 자신.informasjonssystemer_Venter):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Pause_hendelse.is_set(): 자신.feil = str(보조항목)

    def Lukk(자신):
        자신.Pause_hendelse.set(); 자신.arbeider.join(timeout=2)
        for streng_data in 자신.수신창구들 + 자신.접속자들:
            if streng_data is not None: streng_data.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argument_MATRISE): 자신.Lukk()
