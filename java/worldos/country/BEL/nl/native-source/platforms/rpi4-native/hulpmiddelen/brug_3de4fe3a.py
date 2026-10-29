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

absoluut_adres = bytes.fromhex('525400123456')
gateway_hardware_ADRES = bytes.fromhex('52550a000202')
internetadres_WAARDE = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class brug_3de4fe3a:
    def __init__(자신, bestandsoverdracht_poortnummer=2121, 전달규칙들=(), Capture=False, gast_ADRES=None, host_ADRES='127.0.0.1'):
        if not 1024 <= bestandsoverdracht_poortnummer <= 65535 or 50000 <= bestandsoverdracht_poortnummer <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.bestandsoverdracht_poortnummer = bestandsoverdracht_poortnummer
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        gast_ADRES = gast_ADRES or 자신.ip_config['IP']
        qemu_network(자신.ip_config, gast_ADRES)
        ADRES=ipaddress.IPv4Address(gast_ADRES)
        자신.gast_ADRES=str(ADRES); 자신.actueel_ADRES=ADRES.packed
        ADRES=ipaddress.IPv4Address(host_ADRES)
        if ADRES.is_multicast or str(ADRES)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.host_ADRES=str(ADRES)
        자신.Capture = Capture; 자신.traceerlogboek = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', bestandsoverdracht_poortnummer)} | {('tcp', gegevens_functie) for gegevens_functie in range(50000,50008)}
        for regel_WAARDE in 전달규칙들:
            pad_onderdeel = regel_WAARDE.split(':')
            if len(pad_onderdeel) != 3 or pad_onderdeel[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, host, gast = pad_onderdeel[0], int(pad_onderdeel[1]), int(pad_onderdeel[2])
            if not 1024 <= host <= 65535 or not 1 <= gast <= 65535 or (통신규약, host) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + regel_WAARDE)
            사용중주소.add((통신규약, host)); 자신.전달규칙들.append((통신규약, host, gast))
        자신.수신창구들 = []
        for _ in range(2):
            server_WAARDE = socket.socket()
            server_WAARDE.bind(('127.0.0.1', 0)); server_WAARDE.listen(1); server_WAARDE.setblocking(False)
            자신.수신창구들.append(server_WAARDE)
        자신.접속자들 = [None, None]
        자신.informatie_In_behandeling = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.informatie_nietig = False
        자신.Onderbreken_gebeurtenis = threading.Event(); 자신.fout = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.achtergrondwerker = threading.Thread(target=자신.cyclus_WAARDE, daemon=True)
        자신.achtergrondwerker.start()

    def 전달인수(자신):
        COM_poort_nummer, ethernet_poort = [tekenreeks_gegevens.getsockname()[1] for tekenreeks_gegevens in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.gast_ADRES) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.bestandsoverdracht_poortnummer, 자신.gast_ADRES)
        for poortnummer in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(poortnummer, 자신.gast_ADRES)
        for 통신규약, host, gast in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, host, 자신.gast_ADRES, gast)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.host_ADRES+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(COM_poort_nummer),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(ethernet_poort),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def uitvoerbewerking_frame(자신, pakket_gegevens):
        자신.informatie_In_behandeling[1] += struct.pack('!I', len(pakket_gegevens)) + pakket_gegevens

    def spoor_pakket(자신, 방향, pakket_gegevens):
        if not 자신.Capture or len(pakket_gegevens)<20: return
        VERSCHUIVING_WAARDE=(pakket_gegevens[0]&15)*4
        invoer_WAARDE_962f286b={'time':time.monotonic(),'direction':방향,'bytes':len(pakket_gegevens),'protocol':pakket_gegevens[9]}
        if pakket_gegevens[9]==6 and len(pakket_gegevens)>=VERSCHUIVING_WAARDE+20:
            원본자료,doel_gegevens_ADRES,order_nummer,확인번호,configuratie_BITS,Venster=struct.unpack_from('!HHIIHH',pakket_gegevens,VERSCHUIVING_WAARDE)
            invoer_WAARDE_962f286b.update(source=원본자료,destination=doel_gegevens_ADRES,seq=order_nummer,ack=확인번호,flags=configuratie_BITS&255,window=Venster,
                        payload=len(pakket_gegevens)-VERSCHUIVING_WAARDE-((pakket_gegevens[VERSCHUIVING_WAARDE+12]>>4)*4))
        자신.traceerlogboek.append(invoer_WAARDE_962f286b)
        if len(자신.traceerlogboek)>2048: del 자신.traceerlogboek[:1024]

    def Serial_Line_Internet_Protocol_invoer(자신, gegevens):
        for codepoint in gegevens:
            if codepoint == 192:
                if 자신.직렬전문 and not 자신.informatie_nietig and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        ADRES=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(ADRES)))
                            자신.actueel_ADRES=ADRES
                        except ValueError:
                            pass
                    자신.spoor_pakket('from_guest',자신.직렬전문)
                    자신.uitvoerbewerking_frame(gateway_hardware_ADRES + absoluut_adres + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.informatie_nietig = False
            elif codepoint == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if codepoint not in (220, 221): 자신.informatie_nietig = True
                    codepoint = 192 if codepoint == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(codepoint)
                else: 자신.informatie_nietig = True

    def Ethernet_invoer(자신, gegevens):
        자신.Ethernet += gegevens
        while len(자신.Ethernet) >= 4:
            item_AANTAL = struct.unpack_from('!I', 자신.Ethernet)[0]
            if item_AANTAL > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < item_AANTAL + 4: return
            uitvoerbewerking_frame = bytes(자신.Ethernet[4:4+item_AANTAL]); del 자신.Ethernet[:4+item_AANTAL]
            if len(uitvoerbewerking_frame) < 14: continue
            if uitvoerbewerking_frame[12:14] == b'\x08\x06' and len(uitvoerbewerking_frame) >= 42:
                ADRES_resolutie_pakket = uitvoerbewerking_frame[14:42]
                if ADRES_resolutie_pakket[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and ADRES_resolutie_pakket[24:28] == 자신.actueel_ADRES:
                    reactie_1262b476 = ADRES_resolutie_pakket[:6] + b'\x00\x02' + absoluut_adres + 자신.actueel_ADRES + ADRES_resolutie_pakket[8:18]
                    자신.uitvoerbewerking_frame(uitvoerbewerking_frame[6:12] + absoluut_adres + b'\x08\x06' + reactie_1262b476)
            elif uitvoerbewerking_frame[12:14] == b'\x08\x00':
                pakket_gegevens = uitvoerbewerking_frame[14:]
                자신.spoor_pakket('to_guest',pakket_gegevens)
                자신.informatie_In_behandeling[0] += b'\xc0' + pakket_gegevens.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def cyclus_WAARDE(자신):
        try:
            while not 자신.Onderbreken_gebeurtenis.is_set():
                읽기대상들 = [tekenreeks_gegevens for 순번, tekenreeks_gegevens in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [tekenreeks_gegevens for tekenreeks_gegevens in 자신.접속자들 if tekenreeks_gegevens is not None]
                쓰기대상들 = [tekenreeks_gegevens for 순번, tekenreeks_gegevens in enumerate(자신.접속자들) if tekenreeks_gegevens is not None and 자신.informatie_In_behandeling[순번]]
                읽을수있음, schrijfbaar, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for tekenreeks_gegevens in 읽을수있음:
                    if tekenreeks_gegevens in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(tekenreeks_gegevens); 자신.접속자들[순번], _ = tekenreeks_gegevens.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(tekenreeks_gegevens); gegevens = tekenreeks_gegevens.recv(16384)
                        if not gegevens: return
                        (자신.Serial_Line_Internet_Protocol_invoer if 순번 == 0 else 자신.Ethernet_invoer)(gegevens)
                for tekenreeks_gegevens in schrijfbaar:
                    순번 = 자신.접속자들.index(tekenreeks_gegevens)
                    try: item_AANTAL = tekenreeks_gegevens.send(자신.informatie_In_behandeling[순번])
                    except BlockingIOError: continue
                    del 자신.informatie_In_behandeling[순번][:item_AANTAL]
                if any(len(SECONDE_WAARDE) > 1024 * 1024 for SECONDE_WAARDE in 자신.informatie_In_behandeling):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Onderbreken_gebeurtenis.is_set(): 자신.fout = str(보조항목)

    def Sluiten(자신):
        자신.Onderbreken_gebeurtenis.set(); 자신.achtergrondwerker.join(timeout=2)
        for tekenreeks_gegevens in 자신.수신창구들 + 자신.접속자들:
            if tekenreeks_gegevens is not None: tekenreeks_gegevens.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argument_MATRIX): 자신.Sluiten()
