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

reālā_adrese = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
interneta_adrese_VALUE = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class tilts_3de4fe3a:
    def __init__(자신, faila_pārsūtīšana_porta_numurs=2121, 전달규칙들=(), tvert=False, viesis_adrese=None, viesot_adrese='127.0.0.1'):
        if not 1024 <= faila_pārsūtīšana_porta_numurs <= 65535 or 50000 <= faila_pārsūtīšana_porta_numurs <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.faila_pārsūtīšana_porta_numurs = faila_pārsūtīšana_porta_numurs
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        viesis_adrese = viesis_adrese or 자신.ip_config['IP']
        qemu_network(자신.ip_config, viesis_adrese)
        adrese=ipaddress.IPv4Address(viesis_adrese)
        자신.viesis_adrese=str(adrese); 자신.pašreizējais_adrese=adrese.packed
        adrese=ipaddress.IPv4Address(viesot_adrese)
        if adrese.is_multicast or str(adrese)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.viesot_adrese=str(adrese)
        자신.tvert = tvert; 자신.trasēšanas_žurnāls = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', faila_pārsūtīšana_porta_numurs)} | {('tcp', dati_amats) for dati_amats in range(50000,50008)}
        for filtrs_VALUE in 전달규칙들:
            ceļš_komponents = filtrs_VALUE.split(':')
            if len(ceļš_komponents) != 3 or ceļš_komponents[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, viesot, viesis = ceļš_komponents[0], int(ceļš_komponents[1]), int(ceļš_komponents[2])
            if not 1024 <= viesot <= 65535 or not 1 <= viesis <= 65535 or (통신규약, viesot) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + filtrs_VALUE)
            사용중주소.add((통신규약, viesot)); 자신.전달규칙들.append((통신규약, viesot, viesis))
        자신.수신창구들 = []
        for _ in range(2):
            serveris_VALUE = socket.socket()
            serveris_VALUE.bind(('127.0.0.1', 0)); serveris_VALUE.listen(1); serveris_VALUE.setblocking(False)
            자신.수신창구들.append(serveris_VALUE)
        자신.접속자들 = [None, None]
        자신.informācijas_tehnoloģija_gaida = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.informācijas_tehnoloģija_nederīgs = False
        자신.Pauze_notikums = threading.Event(); 자신.Kļūda = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.nodarbinātais = threading.Thread(target=자신.Cikls_VALUE, daemon=True)
        자신.nodarbinātais.start()

    def 전달인수(자신):
        COM_ports_numurs, Ethernet_ports = [virkne_dati.getsockname()[1] for virkne_dati in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.viesis_adrese) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.faila_pārsūtīšana_porta_numurs, 자신.viesis_adrese)
        for porta_numurs in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(porta_numurs, 자신.viesis_adrese)
        for 통신규약, viesot, viesis in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, viesot, 자신.viesis_adrese, viesis)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.viesot_adrese+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(COM_ports_numurs),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethernet_ports),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, pakete_dati):
        자신.informācijas_tehnoloģija_gaida[1] += struct.pack('!I', len(pakete_dati)) + pakete_dati

    def pēda_pakete(자신, 방향, pakete_dati):
        if not 자신.tvert or len(pakete_dati)<20: return
        Nobīde_VALUE=(pakete_dati[0]&15)*4
        ievade_VALUE={'time':time.monotonic(),'direction':방향,'bytes':len(pakete_dati),'protocol':pakete_dati[9]}
        if pakete_dati[9]==6 and len(pakete_dati)>=Nobīde_VALUE+20:
            원본자료,mērķis_dati_adrese,secība_numurs,확인번호,konfigurācija_Background_Intelligent_Transfer_Service,Logs=struct.unpack_from('!HHIIHH',pakete_dati,Nobīde_VALUE)
            ievade_VALUE.update(source=원본자료,destination=mērķis_dati_adrese,seq=secība_numurs,ack=확인번호,flags=konfigurācija_Background_Intelligent_Transfer_Service&255,window=Logs,
                        payload=len(pakete_dati)-Nobīde_VALUE-((pakete_dati[Nobīde_VALUE+12]>>4)*4))
        자신.trasēšanas_žurnāls.append(ievade_VALUE)
        if len(자신.trasēšanas_žurnāls)>2048: del 자신.trasēšanas_žurnāls[:1024]

    def 직렬전문입력(자신, dati):
        for koda_punkts in dati:
            if koda_punkts == 192:
                if 자신.직렬전문 and not 자신.informācijas_tehnoloģija_nederīgs and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        adrese=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(adrese)))
                            자신.pašreizējais_adrese=adrese
                        except ValueError:
                            pass
                    자신.pēda_pakete('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + reālā_adrese + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.informācijas_tehnoloģija_nederīgs = False
            elif koda_punkts == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if koda_punkts not in (220, 221): 자신.informācijas_tehnoloģija_nederīgs = True
                    koda_punkts = 192 if koda_punkts == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(koda_punkts)
                else: 자신.informācijas_tehnoloģija_nederīgs = True

    def 이더넷입력(자신, dati):
        자신.Ethernet += dati
        while len(자신.Ethernet) >= 4:
            krājums_COUNT = struct.unpack_from('!I', 자신.Ethernet)[0]
            if krājums_COUNT > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < krājums_COUNT + 4: return
            실행틀 = bytes(자신.Ethernet[4:4+krājums_COUNT]); del 자신.Ethernet[:4+krājums_COUNT]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                adrese_izšķirtspēja_pakete = 실행틀[14:42]
                if adrese_izšķirtspēja_pakete[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and adrese_izšķirtspēja_pakete[24:28] == 자신.pašreizējais_adrese:
                    atbilde_1262b476 = adrese_izšķirtspēja_pakete[:6] + b'\x00\x02' + reālā_adrese + 자신.pašreizējais_adrese + adrese_izšķirtspēja_pakete[8:18]
                    자신.실행틀(실행틀[6:12] + reālā_adrese + b'\x08\x06' + atbilde_1262b476)
            elif 실행틀[12:14] == b'\x08\x00':
                pakete_dati = 실행틀[14:]
                자신.pēda_pakete('to_guest',pakete_dati)
                자신.informācijas_tehnoloģija_gaida[0] += b'\xc0' + pakete_dati.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Cikls_VALUE(자신):
        try:
            while not 자신.Pauze_notikums.is_set():
                읽기대상들 = [virkne_dati for 순번, virkne_dati in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [virkne_dati for virkne_dati in 자신.접속자들 if virkne_dati is not None]
                쓰기대상들 = [virkne_dati for 순번, virkne_dati in enumerate(자신.접속자들) if virkne_dati is not None and 자신.informācijas_tehnoloģija_gaida[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for virkne_dati in 읽을수있음:
                    if virkne_dati in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(virkne_dati); 자신.접속자들[순번], _ = virkne_dati.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(virkne_dati); dati = virkne_dati.recv(16384)
                        if not dati: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(dati)
                for virkne_dati in 쓸수있음:
                    순번 = 자신.접속자들.index(virkne_dati)
                    try: krājums_COUNT = virkne_dati.send(자신.informācijas_tehnoloģija_gaida[순번])
                    except BlockingIOError: continue
                    del 자신.informācijas_tehnoloģija_gaida[순번][:krājums_COUNT]
                if any(len(SECOND_VALUE) > 1024 * 1024 for SECOND_VALUE in 자신.informācijas_tehnoloģija_gaida):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Pauze_notikums.is_set(): 자신.Kļūda = str(보조항목)

    def Aizvērt(자신):
        자신.Pauze_notikums.set(); 자신.nodarbinātais.join(timeout=2)
        for virkne_dati in 자신.수신창구들 + 자신.접속자들:
            if virkne_dati is not None: virkne_dati.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *arg_ARRAY): 자신.Aizvērt()
