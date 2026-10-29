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

maskin_ADDRESS = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
Internett_adresse_VALUE = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class Nettverk_bru:
    def __init__(자신, fil_Overfør_portnummer=2121, 전달규칙들=(), ta_opp=False, gjest_ADDRESS=None, vert_ADDRESS='127.0.0.1'):
        if not 1024 <= fil_Overfør_portnummer <= 65535 or 50000 <= fil_Overfør_portnummer <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.fil_Overfør_portnummer = fil_Overfør_portnummer
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        gjest_ADDRESS = gjest_ADDRESS or 자신.ip_config['IP']
        qemu_network(자신.ip_config, gjest_ADDRESS)
        ADDRESS=ipaddress.IPv4Address(gjest_ADDRESS)
        자신.gjest_ADDRESS=str(ADDRESS); 자신.betalt_ADDRESS=ADDRESS.packed
        ADDRESS=ipaddress.IPv4Address(vert_ADDRESS)
        if ADDRESS.is_multicast or str(ADDRESS)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.vert_ADDRESS=str(ADDRESS)
        자신.ta_opp = ta_opp; 자신.spor_LOG = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', fil_Overfør_portnummer)} | {('tcp', data_plassere) for data_plassere in range(50000,50008)}
        for regel_VALUE in 전달규칙들:
            bane_komponent = regel_VALUE.split(':')
            if len(bane_komponent) != 3 or bane_komponent[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, vert, gjest = bane_komponent[0], int(bane_komponent[1]), int(bane_komponent[2])
            if not 1024 <= vert <= 65535 or not 1 <= gjest <= 65535 or (통신규약, vert) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + regel_VALUE)
            사용중주소.add((통신규약, vert)); 자신.전달규칙들.append((통신규약, vert, gjest))
        자신.수신창구들 = []
        for _ in range(2):
            tenar_VALUE = socket.socket()
            tenar_VALUE.bind(('127.0.0.1', 0)); tenar_VALUE.listen(1); tenar_VALUE.setblocking(False)
            자신.수신창구들.append(tenar_VALUE)
        자신.접속자들 = [None, None]
        자신.informasjonsteknologi_ventande = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.informasjonsteknologi_ugyldig = False
        자신.Pause_hending = threading.Event(); 자신.FEIL = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Syklus_VALUE, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, Ethernet_port = [streng_data.getsockname()[1] for streng_data in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.gjest_ADDRESS) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.fil_Overfør_portnummer, 자신.gjest_ADDRESS)
        for portnummer in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(portnummer, 자신.gjest_ADDRESS)
        for 통신규약, vert, gjest in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, vert, 자신.gjest_ADDRESS, gjest)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.vert_ADDRESS+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethernet_port),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, pakke_data):
        자신.informasjonsteknologi_ventande[1] += struct.pack('!I', len(pakke_data)) + pakke_data

    def spor_pakke(자신, 방향, pakke_data):
        if not 자신.ta_opp or len(pakke_data)<20: return
        OFFSET_VALUE=(pakke_data[0]&15)*4
        oppføring_VALUE={'time':time.monotonic(),'direction':방향,'bytes':len(pakke_data),'protocol':pakke_data[9]}
        if pakke_data[9]==6 and len(pakke_data)>=OFFSET_VALUE+20:
            원본자료,mål_data_ADDRESS,순서번호,확인번호,설정비트,vindauge=struct.unpack_from('!HHIIHH',pakke_data,OFFSET_VALUE)
            oppføring_VALUE.update(source=원본자료,destination=mål_data_ADDRESS,seq=순서번호,ack=확인번호,flags=설정비트&255,window=vindauge,
                        payload=len(pakke_data)-OFFSET_VALUE-((pakke_data[OFFSET_VALUE+12]>>4)*4))
        자신.spor_LOG.append(oppføring_VALUE)
        if len(자신.spor_LOG)>2048: del 자신.spor_LOG[:1024]

    def 직렬전문입력(자신, data):
        for teiknkode in data:
            if teiknkode == 192:
                if 자신.직렬전문 and not 자신.informasjonsteknologi_ugyldig and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        ADDRESS=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(ADDRESS)))
                            자신.betalt_ADDRESS=ADDRESS
                        except ValueError:
                            pass
                    자신.spor_pakke('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + maskin_ADDRESS + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.informasjonsteknologi_ugyldig = False
            elif teiknkode == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if teiknkode not in (220, 221): 자신.informasjonsteknologi_ugyldig = True
                    teiknkode = 192 if teiknkode == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(teiknkode)
                else: 자신.informasjonsteknologi_ugyldig = True

    def 이더넷입력(자신, data):
        자신.Ethernet += data
        while len(자신.Ethernet) >= 4:
            vare_COUNT = struct.unpack_from('!I', 자신.Ethernet)[0]
            if vare_COUNT > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < vare_COUNT + 4: return
            실행틀 = bytes(자신.Ethernet[4:4+vare_COUNT]); del 자신.Ethernet[:4+vare_COUNT]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                ADDRESS_oppløysing_pakke = 실행틀[14:42]
                if ADDRESS_oppløysing_pakke[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and ADDRESS_oppløysing_pakke[24:28] == 자신.betalt_ADDRESS:
                    응답자료 = ADDRESS_oppløysing_pakke[:6] + b'\x00\x02' + maskin_ADDRESS + 자신.betalt_ADDRESS + ADDRESS_oppløysing_pakke[8:18]
                    자신.실행틀(실행틀[6:12] + maskin_ADDRESS + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                pakke_data = 실행틀[14:]
                자신.spor_pakke('to_guest',pakke_data)
                자신.informasjonsteknologi_ventande[0] += b'\xc0' + pakke_data.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Syklus_VALUE(자신):
        try:
            while not 자신.Pause_hending.is_set():
                읽기대상들 = [streng_data for 순번, streng_data in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [streng_data for streng_data in 자신.접속자들 if streng_data is not None]
                쓰기대상들 = [streng_data for 순번, streng_data in enumerate(자신.접속자들) if streng_data is not None and 자신.informasjonsteknologi_ventande[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for streng_data in 읽을수있음:
                    if streng_data in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(streng_data); 자신.접속자들[순번], _ = streng_data.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(streng_data); data = streng_data.recv(16384)
                        if not data: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(data)
                for streng_data in 쓸수있음:
                    순번 = 자신.접속자들.index(streng_data)
                    try: vare_COUNT = streng_data.send(자신.informasjonsteknologi_ventande[순번])
                    except BlockingIOError: continue
                    del 자신.informasjonsteknologi_ventande[순번][:vare_COUNT]
                if any(len(SECOND_VALUE) > 1024 * 1024 for SECOND_VALUE in 자신.informasjonsteknologi_ventande):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Pause_hending.is_set(): 자신.FEIL = str(보조항목)

    def Lukk(자신):
        자신.Pause_hending.set(); 자신.작업가닥.join(timeout=2)
        for streng_data in 자신.수신창구들 + 자신.접속자들:
            if streng_data is not None: streng_data.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argument_ARRAY): 자신.Lukk()
