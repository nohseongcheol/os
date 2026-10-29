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

absolútna_adresa = bytes.fromhex('525400123456')
brána_hardvér_adresa = bytes.fromhex('52550a000202')
internetová_adresa_VALUE = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class sieťový_most:
    def __init__(자신, prenos_súborov_číslo_portu=2121, 전달규칙들=(), snímať=False, hosť_adresa=None, hostiteľ_adresa='127.0.0.1'):
        if not 1024 <= prenos_súborov_číslo_portu <= 65535 or 50000 <= prenos_súborov_číslo_portu <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.prenos_súborov_číslo_portu = prenos_súborov_číslo_portu
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        hosť_adresa = hosť_adresa or 자신.ip_config['IP']
        qemu_network(자신.ip_config, hosť_adresa)
        adresa=ipaddress.IPv4Address(hosť_adresa)
        자신.hosť_adresa=str(adresa); 자신.v_termíne_splatnosti_adresa=adresa.packed
        adresa=ipaddress.IPv4Address(hostiteľ_adresa)
        if adresa.is_multicast or str(adresa)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.hostiteľ_adresa=str(adresa)
        자신.snímať = snímať; 자신.denník_sledovania = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', prenos_súborov_číslo_portu)} | {('tcp', údaje_pozícia) for údaje_pozícia in range(50000,50008)}
        for filter_VALUE in 전달규칙들:
            cesta_súčasť = filter_VALUE.split(':')
            if len(cesta_súčasť) != 3 or cesta_súčasť[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, hostiteľ, hosť = cesta_súčasť[0], int(cesta_súčasť[1]), int(cesta_súčasť[2])
            if not 1024 <= hostiteľ <= 65535 or not 1 <= hosť <= 65535 or (통신규약, hostiteľ) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + filter_VALUE)
            사용중주소.add((통신규약, hostiteľ)); 자신.전달규칙들.append((통신규약, hostiteľ, hosť))
        자신.수신창구들 = []
        for _ in range(2):
            server_VALUE = socket.socket()
            server_VALUE.bind(('127.0.0.1', 0)); server_VALUE.listen(1); server_VALUE.setblocking(False)
            자신.수신창구들.append(server_VALUE)
        자신.접속자들 = [None, None]
        자신.Informačné_systémy_čakajúci = [bytearray(), bytearray()]
        자신.sieť_Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.Informačné_systémy_neplatné = False
        자신.Pozastaviť_udalosť = threading.Event(); 자신.chyba = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Cyklus_VALUE, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, port_Ehternet = [reťazec_údaje.getsockname()[1] for reťazec_údaje in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.hosť_adresa) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.prenos_súborov_číslo_portu, 자신.hosť_adresa)
        for číslo_portu in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(číslo_portu, 자신.hosť_adresa)
        for 통신규약, hostiteľ, hosť in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, hostiteľ, 자신.hosť_adresa, hosť)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.hostiteľ_adresa+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(port_Ehternet),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, paket_údaje):
        자신.Informačné_systémy_čakajúci[1] += struct.pack('!I', len(paket_údaje)) + paket_údaje

    def sledovať_paket(자신, 방향, paket_údaje):
        if not 자신.snímať or len(paket_údaje)<20: return
        Posun_VALUE=(paket_údaje[0]&15)*4
        položka_VALUE={'time':time.monotonic(),'direction':방향,'bytes':len(paket_údaje),'protocol':paket_údaje[9]}
        if paket_údaje[9]==6 and len(paket_údaje)>=Posun_VALUE+20:
            원본자료,cieľ_údaje_adresa,순서번호,확인번호,konfigurácia_Background_Intelligent_Transfer_Service,Okno=struct.unpack_from('!HHIIHH',paket_údaje,Posun_VALUE)
            položka_VALUE.update(source=원본자료,destination=cieľ_údaje_adresa,seq=순서번호,ack=확인번호,flags=konfigurácia_Background_Intelligent_Transfer_Service&255,window=Okno,
                        payload=len(paket_údaje)-Posun_VALUE-((paket_údaje[Posun_VALUE+12]>>4)*4))
        자신.denník_sledovania.append(položka_VALUE)
        if len(자신.denník_sledovania)>2048: del 자신.denník_sledovania[:1024]

    def 직렬전문입력(자신, údaje):
        for bod_kódu in údaje:
            if bod_kódu == 192:
                if 자신.직렬전문 and not 자신.Informačné_systémy_neplatné and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        adresa=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(adresa)))
                            자신.v_termíne_splatnosti_adresa=adresa
                        except ValueError:
                            pass
                    자신.sledovať_paket('from_guest',자신.직렬전문)
                    자신.실행틀(brána_hardvér_adresa + absolútna_adresa + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.Informačné_systémy_neplatné = False
            elif bod_kódu == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if bod_kódu not in (220, 221): 자신.Informačné_systémy_neplatné = True
                    bod_kódu = 192 if bod_kódu == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(bod_kódu)
                else: 자신.Informačné_systémy_neplatné = True

    def sieť_Ethernet_vstup(자신, údaje):
        자신.sieť_Ethernet += údaje
        while len(자신.sieť_Ethernet) >= 4:
            položka_COUNT = struct.unpack_from('!I', 자신.sieť_Ethernet)[0]
            if položka_COUNT > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.sieť_Ethernet) < položka_COUNT + 4: return
            실행틀 = bytes(자신.sieť_Ethernet[4:4+položka_COUNT]); del 자신.sieť_Ethernet[:4+položka_COUNT]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                adresa_rozlíšenie_paket = 실행틀[14:42]
                if adresa_rozlíšenie_paket[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and adresa_rozlíšenie_paket[24:28] == 자신.v_termíne_splatnosti_adresa:
                    odpoveď = adresa_rozlíšenie_paket[:6] + b'\x00\x02' + absolútna_adresa + 자신.v_termíne_splatnosti_adresa + adresa_rozlíšenie_paket[8:18]
                    자신.실행틀(실행틀[6:12] + absolútna_adresa + b'\x08\x06' + odpoveď)
            elif 실행틀[12:14] == b'\x08\x00':
                paket_údaje = 실행틀[14:]
                자신.sledovať_paket('to_guest',paket_údaje)
                자신.Informačné_systémy_čakajúci[0] += b'\xc0' + paket_údaje.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Cyklus_VALUE(자신):
        try:
            while not 자신.Pozastaviť_udalosť.is_set():
                읽기대상들 = [reťazec_údaje for 순번, reťazec_údaje in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [reťazec_údaje for reťazec_údaje in 자신.접속자들 if reťazec_údaje is not None]
                쓰기대상들 = [reťazec_údaje for 순번, reťazec_údaje in enumerate(자신.접속자들) if reťazec_údaje is not None and 자신.Informačné_systémy_čakajúci[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for reťazec_údaje in 읽을수있음:
                    if reťazec_údaje in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(reťazec_údaje); 자신.접속자들[순번], _ = reťazec_údaje.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(reťazec_údaje); údaje = reťazec_údaje.recv(16384)
                        if not údaje: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.sieť_Ethernet_vstup)(údaje)
                for reťazec_údaje in 쓸수있음:
                    순번 = 자신.접속자들.index(reťazec_údaje)
                    try: položka_COUNT = reťazec_údaje.send(자신.Informačné_systémy_čakajúci[순번])
                    except BlockingIOError: continue
                    del 자신.Informačné_systémy_čakajúci[순번][:položka_COUNT]
                if any(len(SECOND_VALUE) > 1024 * 1024 for SECOND_VALUE in 자신.Informačné_systémy_čakajúci):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Pozastaviť_udalosť.is_set(): 자신.chyba = str(보조항목)

    def Zatvoriť(자신):
        자신.Pozastaviť_udalosť.set(); 자신.작업가닥.join(timeout=2)
        for reťazec_údaje in 자신.수신창구들 + 자신.접속자들:
            if reťazec_údaje is not None: reťazec_údaje.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argument_pole): 자신.Zatvoriť()
