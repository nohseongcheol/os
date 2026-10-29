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

adresă_reală = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
adresă_internet_VALUE = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class punte_3de4fe3a:
    def __init__(자신, transfer_de_fișiere_număr_port=2121, 전달규칙들=(), captura=False, invitat_adresa=None, gazdă_adresa='127.0.0.1'):
        if not 1024 <= transfer_de_fișiere_număr_port <= 65535 or 50000 <= transfer_de_fișiere_număr_port <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.transfer_de_fișiere_număr_port = transfer_de_fișiere_număr_port
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        invitat_adresa = invitat_adresa or 자신.ip_config['IP']
        qemu_network(자신.ip_config, invitat_adresa)
        adresa=ipaddress.IPv4Address(invitat_adresa)
        자신.invitat_adresa=str(adresa); 자신.curent_adresa=adresa.packed
        adresa=ipaddress.IPv4Address(gazdă_adresa)
        if adresa.is_multicast or str(adresa)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.gazdă_adresa=str(adresa)
        자신.captura = captura; 자신.jurnal_de_urmărire = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', transfer_de_fișiere_număr_port)} | {('tcp', date_poziție) for date_poziție in range(50000,50008)}
        for filtru_VALUE in 전달규칙들:
            cale_componentă = filtru_VALUE.split(':')
            if len(cale_componentă) != 3 or cale_componentă[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, gazdă, invitat = cale_componentă[0], int(cale_componentă[1]), int(cale_componentă[2])
            if not 1024 <= gazdă <= 65535 or not 1 <= invitat <= 65535 or (통신규약, gazdă) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + filtru_VALUE)
            사용중주소.add((통신규약, gazdă)); 자신.전달규칙들.append((통신규약, gazdă, invitat))
        자신.수신창구들 = []
        for _ in range(2):
            server_VALUE = socket.socket()
            server_VALUE.bind(('127.0.0.1', 0)); server_VALUE.listen(1); server_VALUE.setblocking(False)
            자신.수신창구들.append(server_VALUE)
        자신.접속자들 = [None, None]
        자신.sisteme_de_informații_în_așteptare = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.sisteme_de_informații_nul = False
        자신.Pauză_eveniment = threading.Event(); 자신.eroare = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Ciclu_VALUE, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, port_Ethernet = [șir_date.getsockname()[1] for șir_date in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.invitat_adresa) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.transfer_de_fișiere_număr_port, 자신.invitat_adresa)
        for număr_port in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(număr_port, 자신.invitat_adresa)
        for 통신규약, gazdă, invitat in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, gazdă, 자신.invitat_adresa, invitat)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.gazdă_adresa+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(port_Ethernet),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def executare_cadru(자신, pachet_date):
        자신.sisteme_de_informații_în_așteptare[1] += struct.pack('!I', len(pachet_date)) + pachet_date

    def urmă_pachet(자신, 방향, pachet_date):
        if not 자신.captura or len(pachet_date)<20: return
        OFFSET_VALUE=(pachet_date[0]&15)*4
        intrare_VALUE={'time':time.monotonic(),'direction':방향,'bytes':len(pachet_date),'protocol':pachet_date[9]}
        if pachet_date[9]==6 and len(pachet_date)>=OFFSET_VALUE+20:
            원본자료,destinație_date_adresa,순서번호,확인번호,configurație_Serviciu_de_transfer_inteligent_în_fundal,Fereastră=struct.unpack_from('!HHIIHH',pachet_date,OFFSET_VALUE)
            intrare_VALUE.update(source=원본자료,destination=destinație_date_adresa,seq=순서번호,ack=확인번호,flags=configurație_Serviciu_de_transfer_inteligent_în_fundal&255,window=Fereastră,
                        payload=len(pachet_date)-OFFSET_VALUE-((pachet_date[OFFSET_VALUE+12]>>4)*4))
        자신.jurnal_de_urmărire.append(intrare_VALUE)
        if len(자신.jurnal_de_urmărire)>2048: del 자신.jurnal_de_urmărire[:1024]

    def 직렬전문입력(자신, date):
        for cod_caracter in date:
            if cod_caracter == 192:
                if 자신.직렬전문 and not 자신.sisteme_de_informații_nul and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        adresa=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(adresa)))
                            자신.curent_adresa=adresa
                        except ValueError:
                            pass
                    자신.urmă_pachet('from_guest',자신.직렬전문)
                    자신.executare_cadru(관문기계주소 + adresă_reală + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.sisteme_de_informații_nul = False
            elif cod_caracter == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if cod_caracter not in (220, 221): 자신.sisteme_de_informații_nul = True
                    cod_caracter = 192 if cod_caracter == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(cod_caracter)
                else: 자신.sisteme_de_informații_nul = True

    def 이더넷입력(자신, date):
        자신.Ethernet += date
        while len(자신.Ethernet) >= 4:
            element_COUNT = struct.unpack_from('!I', 자신.Ethernet)[0]
            if element_COUNT > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < element_COUNT + 4: return
            executare_cadru = bytes(자신.Ethernet[4:4+element_COUNT]); del 자신.Ethernet[:4+element_COUNT]
            if len(executare_cadru) < 14: continue
            if executare_cadru[12:14] == b'\x08\x06' and len(executare_cadru) >= 42:
                adresa_rezoluție_pachet = executare_cadru[14:42]
                if adresa_rezoluție_pachet[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and adresa_rezoluție_pachet[24:28] == 자신.curent_adresa:
                    răspuns = adresa_rezoluție_pachet[:6] + b'\x00\x02' + adresă_reală + 자신.curent_adresa + adresa_rezoluție_pachet[8:18]
                    자신.executare_cadru(executare_cadru[6:12] + adresă_reală + b'\x08\x06' + răspuns)
            elif executare_cadru[12:14] == b'\x08\x00':
                pachet_date = executare_cadru[14:]
                자신.urmă_pachet('to_guest',pachet_date)
                자신.sisteme_de_informații_în_așteptare[0] += b'\xc0' + pachet_date.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Ciclu_VALUE(자신):
        try:
            while not 자신.Pauză_eveniment.is_set():
                읽기대상들 = [șir_date for 순번, șir_date in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [șir_date for șir_date in 자신.접속자들 if șir_date is not None]
                쓰기대상들 = [șir_date for 순번, șir_date in enumerate(자신.접속자들) if șir_date is not None and 자신.sisteme_de_informații_în_așteptare[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for șir_date in 읽을수있음:
                    if șir_date in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(șir_date); 자신.접속자들[순번], _ = șir_date.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(șir_date); date = șir_date.recv(16384)
                        if not date: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(date)
                for șir_date in 쓸수있음:
                    순번 = 자신.접속자들.index(șir_date)
                    try: element_COUNT = șir_date.send(자신.sisteme_de_informații_în_așteptare[순번])
                    except BlockingIOError: continue
                    del 자신.sisteme_de_informații_în_așteptare[순번][:element_COUNT]
                if any(len(SECOND_VALUE) > 1024 * 1024 for SECOND_VALUE in 자신.sisteme_de_informații_în_așteptare):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Pauză_eveniment.is_set(): 자신.eroare = str(보조항목)

    def Închide(자신):
        자신.Pauză_eveniment.set(); 자신.작업가닥.join(timeout=2)
        for șir_date in 자신.수신창구들 + 자신.접속자들:
            if șir_date is not None: șir_date.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argument_ARRAY): 자신.Închide()
