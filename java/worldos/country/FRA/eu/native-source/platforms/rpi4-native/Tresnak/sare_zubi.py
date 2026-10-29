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

gailu_helbide = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
Internet_helbide_balio = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class sare_zubi:
    def __init__(자신, fitxategi_transferitu_ataka_zenbaki=2121, 전달규칙들=(), atera_ba7b8054=False, gonbidatu_helbide=None, Ostalari_helbide='127.0.0.1'):
        if not 1024 <= fitxategi_transferitu_ataka_zenbaki <= 65535 or 50000 <= fitxategi_transferitu_ataka_zenbaki <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.fitxategi_transferitu_ataka_zenbaki = fitxategi_transferitu_ataka_zenbaki
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        gonbidatu_helbide = gonbidatu_helbide or 자신.ip_config['IP']
        qemu_network(자신.ip_config, gonbidatu_helbide)
        helbide=ipaddress.IPv4Address(gonbidatu_helbide)
        자신.gonbidatu_helbide=str(helbide); 자신.현재주소=helbide.packed
        helbide=ipaddress.IPv4Address(Ostalari_helbide)
        if helbide.is_multicast or str(helbide)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.Ostalari_helbide=str(helbide)
        자신.atera_ba7b8054 = atera_ba7b8054; 자신.balio_diagonalen_batura_LOG = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', fitxategi_transferitu_ataka_zenbaki)} | {('tcp', datuak_kargu) for datuak_kargu in range(50000,50008)}
        for arau_balio in 전달규칙들:
            bide_izen_osagai = arau_balio.split(':')
            if len(bide_izen_osagai) != 3 or bide_izen_osagai[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, Ostalari, gonbidatu = bide_izen_osagai[0], int(bide_izen_osagai[1]), int(bide_izen_osagai[2])
            if not 1024 <= Ostalari <= 65535 or not 1 <= gonbidatu <= 65535 or (통신규약, Ostalari) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + arau_balio)
            사용중주소.add((통신규약, Ostalari)); 자신.전달규칙들.append((통신규약, Ostalari, gonbidatu))
        자신.수신창구들 = []
        for _ in range(2):
            zerbitzari_balio = socket.socket()
            zerbitzari_balio.bind(('127.0.0.1', 0)); zerbitzari_balio.listen(1); zerbitzari_balio.setblocking(False)
            자신.수신창구들.append(zerbitzari_balio)
        자신.접속자들 = [None, None]
        자신.informatika_zain = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.informatika_baliogabe = False
        자신.pausatu_gertaera = threading.Event(); 자신.errorea = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Zikloa_balio, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, Ethernet_ataka = [kate_datuak.getsockname()[1] for kate_datuak in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.gonbidatu_helbide) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.fitxategi_transferitu_ataka_zenbaki, 자신.gonbidatu_helbide)
        for ataka_zenbaki in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(ataka_zenbaki, 자신.gonbidatu_helbide)
        for 통신규약, Ostalari, gonbidatu in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, Ostalari, 자신.gonbidatu_helbide, gonbidatu)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.Ostalari_helbide+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethernet_ataka),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, pakete_datuak):
        자신.informatika_zain[1] += struct.pack('!I', len(pakete_datuak)) + pakete_datuak

    def balio_diagonalen_batura_pakete(자신, 방향, pakete_datuak):
        if not 자신.atera_ba7b8054 or len(pakete_datuak)<20: return
        Geruzak_balio=(pakete_datuak[0]&15)*4
        sarrera_balio={'time':time.monotonic(),'direction':방향,'bytes':len(pakete_datuak),'protocol':pakete_datuak[9]}
        if pakete_datuak[9]==6 and len(pakete_datuak)>=Geruzak_balio+20:
            원본자료,helburu_datuak_helbide,순서번호,확인번호,konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna,Leihoa=struct.unpack_from('!HHIIHH',pakete_datuak,Geruzak_balio)
            sarrera_balio.update(source=원본자료,destination=helburu_datuak_helbide,seq=순서번호,ack=확인번호,flags=konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna&255,window=Leihoa,
                        payload=len(pakete_datuak)-Geruzak_balio-((pakete_datuak[Geruzak_balio+12]>>4)*4))
        자신.balio_diagonalen_batura_LOG.append(sarrera_balio)
        if len(자신.balio_diagonalen_batura_LOG)>2048: del 자신.balio_diagonalen_batura_LOG[:1024]

    def 직렬전문입력(자신, datuak):
        for karaktere_kode in datuak:
            if karaktere_kode == 192:
                if 자신.직렬전문 and not 자신.informatika_baliogabe and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        helbide=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(helbide)))
                            자신.현재주소=helbide
                        except ValueError:
                            pass
                    자신.balio_diagonalen_batura_pakete('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + gailu_helbide + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.informatika_baliogabe = False
            elif karaktere_kode == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if karaktere_kode not in (220, 221): 자신.informatika_baliogabe = True
                    karaktere_kode = 192 if karaktere_kode == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(karaktere_kode)
                else: 자신.informatika_baliogabe = True

    def 이더넷입력(자신, datuak):
        자신.Ethernet += datuak
        while len(자신.Ethernet) >= 4:
            elementu_ZENBATU = struct.unpack_from('!I', 자신.Ethernet)[0]
            if elementu_ZENBATU > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < elementu_ZENBATU + 4: return
            실행틀 = bytes(자신.Ethernet[4:4+elementu_ZENBATU]); del 자신.Ethernet[:4+elementu_ZENBATU]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                helbide_bereizmen_pakete = 실행틀[14:42]
                if helbide_bereizmen_pakete[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and helbide_bereizmen_pakete[24:28] == 자신.현재주소:
                    erantzun_1262b476 = helbide_bereizmen_pakete[:6] + b'\x00\x02' + gailu_helbide + 자신.현재주소 + helbide_bereizmen_pakete[8:18]
                    자신.실행틀(실행틀[6:12] + gailu_helbide + b'\x08\x06' + erantzun_1262b476)
            elif 실행틀[12:14] == b'\x08\x00':
                pakete_datuak = 실행틀[14:]
                자신.balio_diagonalen_batura_pakete('to_guest',pakete_datuak)
                자신.informatika_zain[0] += b'\xc0' + pakete_datuak.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Zikloa_balio(자신):
        try:
            while not 자신.pausatu_gertaera.is_set():
                읽기대상들 = [kate_datuak for 순번, kate_datuak in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [kate_datuak for kate_datuak in 자신.접속자들 if kate_datuak is not None]
                쓰기대상들 = [kate_datuak for 순번, kate_datuak in enumerate(자신.접속자들) if kate_datuak is not None and 자신.informatika_zain[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for kate_datuak in 읽을수있음:
                    if kate_datuak in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(kate_datuak); 자신.접속자들[순번], _ = kate_datuak.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(kate_datuak); datuak = kate_datuak.recv(16384)
                        if not datuak: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(datuak)
                for kate_datuak in 쓸수있음:
                    순번 = 자신.접속자들.index(kate_datuak)
                    try: elementu_ZENBATU = kate_datuak.send(자신.informatika_zain[순번])
                    except BlockingIOError: continue
                    del 자신.informatika_zain[순번][:elementu_ZENBATU]
                if any(len(SEGUNDOA_balio) > 1024 * 1024 for SEGUNDOA_balio in 자신.informatika_zain):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.pausatu_gertaera.is_set(): 자신.errorea = str(보조항목)

    def Itxi(자신):
        자신.pausatu_gertaera.set(); 자신.작업가닥.join(timeout=2)
        for kate_datuak in 자신.수신창구들 + 자신.접속자들:
            if kate_datuak is not None: kate_datuak.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *arg_matrize): 자신.Itxi()
