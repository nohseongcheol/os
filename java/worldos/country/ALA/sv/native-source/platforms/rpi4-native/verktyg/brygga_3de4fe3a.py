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

absolut_adress = bytes.fromhex('525400123456')
gateway_maskinvara_ADRESS = bytes.fromhex('52550a000202')
Internetadress_värde = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class brygga_3de4fe3a:
    def __init__(자신, filöverföring_portnummer=2121, 전달규칙들=(), Capture=False, gäst_ADRESS=None, värd_ADRESS='127.0.0.1'):
        if not 1024 <= filöverföring_portnummer <= 65535 or 50000 <= filöverföring_portnummer <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.filöverföring_portnummer = filöverföring_portnummer
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        gäst_ADRESS = gäst_ADRESS or 자신.ip_config['IP']
        qemu_network(자신.ip_config, gäst_ADRESS)
        Adress=ipaddress.IPv4Address(gäst_ADRESS)
        자신.gäst_ADRESS=str(Adress); 자신.aktuellt_ADRESS=Adress.packed
        Adress=ipaddress.IPv4Address(värd_ADRESS)
        if Adress.is_multicast or str(Adress)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.värd_ADRESS=str(Adress)
        자신.Capture = Capture; 자신.spårningslogg = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', filöverföring_portnummer)} | {('tcp', data_placera) for data_placera in range(50000,50008)}
        for linje_värde in 전달규칙들:
            väg_komponent = linje_värde.split(':')
            if len(väg_komponent) != 3 or väg_komponent[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, värd, gäst = väg_komponent[0], int(väg_komponent[1]), int(väg_komponent[2])
            if not 1024 <= värd <= 65535 or not 1 <= gäst <= 65535 or (통신규약, värd) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + linje_värde)
            사용중주소.add((통신규약, värd)); 자신.전달규칙들.append((통신규약, värd, gäst))
        자신.수신창구들 = []
        for _ in range(2):
            server_värde = socket.socket()
            server_värde.bind(('127.0.0.1', 0)); server_värde.listen(1); server_värde.setblocking(False)
            자신.수신창구들.append(server_värde)
        자신.접속자들 = [None, None]
        자신.informationsteknik_väntar = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.informationsteknik_ogiltig = False
        자신.Pausa_händelse = threading.Event(); 자신.fel = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.arbete = threading.Thread(target=자신.cykel_värde, daemon=True)
        자신.arbete.start()

    def 전달인수(자신):
        seriell_port_nummer, Ethernet_port = [sträng_data.getsockname()[1] for sträng_data in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.gäst_ADRESS) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.filöverföring_portnummer, 자신.gäst_ADRESS)
        for portnummer in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(portnummer, 자신.gäst_ADRESS)
        for 통신규약, värd, gäst in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, värd, 자신.gäst_ADRESS, gäst)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.värd_ADRESS+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(seriell_port_nummer),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethernet_port),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def körning_ram(자신, paket_data):
        자신.informationsteknik_väntar[1] += struct.pack('!I', len(paket_data)) + paket_data

    def spår_paket(자신, 방향, paket_data):
        if not 자신.Capture or len(paket_data)<20: return
        FÖRSKJUTNING_värde=(paket_data[0]&15)*4
        post_värde={'time':time.monotonic(),'direction':방향,'bytes':len(paket_data),'protocol':paket_data[9]}
        if paket_data[9]==6 and len(paket_data)>=FÖRSKJUTNING_värde+20:
            원본자료,mål_data_ADRESS,order_nummer,확인번호,konfiguration_BITS,Fönster=struct.unpack_from('!HHIIHH',paket_data,FÖRSKJUTNING_värde)
            post_värde.update(source=원본자료,destination=mål_data_ADRESS,seq=order_nummer,ack=확인번호,flags=konfiguration_BITS&255,window=Fönster,
                        payload=len(paket_data)-FÖRSKJUTNING_värde-((paket_data[FÖRSKJUTNING_värde+12]>>4)*4))
        자신.spårningslogg.append(post_värde)
        if len(자신.spårningslogg)>2048: del 자신.spårningslogg[:1024]

    def Serial_Line_Internet_Protocol_indata(자신, data):
        for kodpunkt in data:
            if kodpunkt == 192:
                if 자신.직렬전문 and not 자신.informationsteknik_ogiltig and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        Adress=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(Adress)))
                            자신.aktuellt_ADRESS=Adress
                        except ValueError:
                            pass
                    자신.spår_paket('from_guest',자신.직렬전문)
                    자신.körning_ram(gateway_maskinvara_ADRESS + absolut_adress + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.informationsteknik_ogiltig = False
            elif kodpunkt == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if kodpunkt not in (220, 221): 자신.informationsteknik_ogiltig = True
                    kodpunkt = 192 if kodpunkt == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(kodpunkt)
                else: 자신.informationsteknik_ogiltig = True

    def Ethernet_indata(자신, data):
        자신.Ethernet += data
        while len(자신.Ethernet) >= 4:
            objekt_ANTAL = struct.unpack_from('!I', 자신.Ethernet)[0]
            if objekt_ANTAL > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < objekt_ANTAL + 4: return
            körning_ram = bytes(자신.Ethernet[4:4+objekt_ANTAL]); del 자신.Ethernet[:4+objekt_ANTAL]
            if len(körning_ram) < 14: continue
            if körning_ram[12:14] == b'\x08\x06' and len(körning_ram) >= 42:
                ADRESS_upplösning_paket = körning_ram[14:42]
                if ADRESS_upplösning_paket[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and ADRESS_upplösning_paket[24:28] == 자신.aktuellt_ADRESS:
                    svar = ADRESS_upplösning_paket[:6] + b'\x00\x02' + absolut_adress + 자신.aktuellt_ADRESS + ADRESS_upplösning_paket[8:18]
                    자신.körning_ram(körning_ram[6:12] + absolut_adress + b'\x08\x06' + svar)
            elif körning_ram[12:14] == b'\x08\x00':
                paket_data = körning_ram[14:]
                자신.spår_paket('to_guest',paket_data)
                자신.informationsteknik_väntar[0] += b'\xc0' + paket_data.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def cykel_värde(자신):
        try:
            while not 자신.Pausa_händelse.is_set():
                읽기대상들 = [sträng_data for 순번, sträng_data in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [sträng_data for sträng_data in 자신.접속자들 if sträng_data is not None]
                쓰기대상들 = [sträng_data for 순번, sträng_data in enumerate(자신.접속자들) if sträng_data is not None and 자신.informationsteknik_väntar[순번]]
                읽을수있음, skrivbar, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for sträng_data in 읽을수있음:
                    if sträng_data in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(sträng_data); 자신.접속자들[순번], _ = sträng_data.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(sträng_data); data = sträng_data.recv(16384)
                        if not data: return
                        (자신.Serial_Line_Internet_Protocol_indata if 순번 == 0 else 자신.Ethernet_indata)(data)
                for sträng_data in skrivbar:
                    순번 = 자신.접속자들.index(sträng_data)
                    try: objekt_ANTAL = sträng_data.send(자신.informationsteknik_väntar[순번])
                    except BlockingIOError: continue
                    del 자신.informationsteknik_väntar[순번][:objekt_ANTAL]
                if any(len(SEKUND_värde) > 1024 * 1024 for SEKUND_värde in 자신.informationsteknik_väntar):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Pausa_händelse.is_set(): 자신.fel = str(보조항목)

    def Stäng(자신):
        자신.Pausa_händelse.set(); 자신.arbete.join(timeout=2)
        for sträng_data in 자신.수신창구들 + 자신.접속자들:
            if sträng_data is not None: sträng_data.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argument_MATRIS): 자신.Stäng()
