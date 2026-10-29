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

valódi_cím = bytes.fromhex('525400123456')
átjáró_hardver_CÍM = bytes.fromhex('52550a000202')
internetcím_ÉRTÉK = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class híd_3de4fe3a:
    def __init__(자신, fájlátvitel_portszám=2121, 전달규칙들=(), kioszt=False, vendég_CÍM=None, gazda_CÍM='127.0.0.1'):
        if not 1024 <= fájlátvitel_portszám <= 65535 or 50000 <= fájlátvitel_portszám <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.fájlátvitel_portszám = fájlátvitel_portszám
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        vendég_CÍM = vendég_CÍM or 자신.ip_config['IP']
        qemu_network(자신.ip_config, vendég_CÍM)
        CÍM=ipaddress.IPv4Address(vendég_CÍM)
        자신.vendég_CÍM=str(CÍM); 자신.aktuális_CÍM=CÍM.packed
        CÍM=ipaddress.IPv4Address(gazda_CÍM)
        if CÍM.is_multicast or str(CÍM)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.gazda_CÍM=str(CÍM)
        자신.kioszt = kioszt; 자신.nyomkövetési_napló = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', fájlátvitel_portszám)} | {('tcp', adat_pozíció) for adat_pozíció in range(50000,50008)}
        for lénia_ÉRTÉK in 전달규칙들:
            útvonal_komponens = lénia_ÉRTÉK.split(':')
            if len(útvonal_komponens) != 3 or útvonal_komponens[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, gazda, vendég = útvonal_komponens[0], int(útvonal_komponens[1]), int(útvonal_komponens[2])
            if not 1024 <= gazda <= 65535 or not 1 <= vendég <= 65535 or (통신규약, gazda) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + lénia_ÉRTÉK)
            사용중주소.add((통신규약, gazda)); 자신.전달규칙들.append((통신규약, gazda, vendég))
        자신.수신창구들 = []
        for _ in range(2):
            kiszolgáló_ÉRTÉK = socket.socket()
            kiszolgáló_ÉRTÉK.bind(('127.0.0.1', 0)); kiszolgáló_ÉRTÉK.listen(1); kiszolgáló_ÉRTÉK.setblocking(False)
            자신.수신창구들.append(kiszolgáló_ÉRTÉK)
        자신.접속자들 = [None, None]
        자신.informatikai_részleg_Függő = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.informatikai_részleg_alaptalan = False
        자신.Szünet_esemény = threading.Event(); 자신.HIBA = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.dolgozó = threading.Thread(target=자신.Ciklus_ÉRTÉK, daemon=True)
        자신.dolgozó.start()

    def 전달인수(자신):
        COM_port_szám, Ethernet_port = [sztring_adat.getsockname()[1] for sztring_adat in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.vendég_CÍM) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.fájlátvitel_portszám, 자신.vendég_CÍM)
        for portszám in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(portszám, 자신.vendég_CÍM)
        for 통신규약, gazda, vendég in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, gazda, 자신.vendég_CÍM, vendég)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.gazda_CÍM+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(COM_port_szám),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethernet_port),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def végrehajtás_doboz(자신, csomag_adat):
        자신.informatikai_részleg_Függő[1] += struct.pack('!I', len(csomag_adat)) + csomag_adat

    def nyom_csomag(자신, 방향, csomag_adat):
        if not 자신.kioszt or len(csomag_adat)<20: return
        Ofszet_ÉRTÉK=(csomag_adat[0]&15)*4
        bejegyzés_ÉRTÉK={'time':time.monotonic(),'direction':방향,'bytes':len(csomag_adat),'protocol':csomag_adat[9]}
        if csomag_adat[9]==6 and len(csomag_adat)>=Ofszet_ÉRTÉK+20:
            원본자료,cél_adat_CÍM,rendel_szám,확인번호,konfiguráció_BITS,Ablak=struct.unpack_from('!HHIIHH',csomag_adat,Ofszet_ÉRTÉK)
            bejegyzés_ÉRTÉK.update(source=원본자료,destination=cél_adat_CÍM,seq=rendel_szám,ack=확인번호,flags=konfiguráció_BITS&255,window=Ablak,
                        payload=len(csomag_adat)-Ofszet_ÉRTÉK-((csomag_adat[Ofszet_ÉRTÉK+12]>>4)*4))
        자신.nyomkövetési_napló.append(bejegyzés_ÉRTÉK)
        if len(자신.nyomkövetési_napló)>2048: del 자신.nyomkövetési_napló[:1024]

    def 직렬전문입력(자신, adat):
        for kódpont in adat:
            if kódpont == 192:
                if 자신.직렬전문 and not 자신.informatikai_részleg_alaptalan and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        CÍM=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(CÍM)))
                            자신.aktuális_CÍM=CÍM
                        except ValueError:
                            pass
                    자신.nyom_csomag('from_guest',자신.직렬전문)
                    자신.végrehajtás_doboz(átjáró_hardver_CÍM + valódi_cím + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.informatikai_részleg_alaptalan = False
            elif kódpont == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if kódpont not in (220, 221): 자신.informatikai_részleg_alaptalan = True
                    kódpont = 192 if kódpont == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(kódpont)
                else: 자신.informatikai_részleg_alaptalan = True

    def Ethernet_bevitel(자신, adat):
        자신.Ethernet += adat
        while len(자신.Ethernet) >= 4:
            cikk_DARAB = struct.unpack_from('!I', 자신.Ethernet)[0]
            if cikk_DARAB > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < cikk_DARAB + 4: return
            végrehajtás_doboz = bytes(자신.Ethernet[4:4+cikk_DARAB]); del 자신.Ethernet[:4+cikk_DARAB]
            if len(végrehajtás_doboz) < 14: continue
            if végrehajtás_doboz[12:14] == b'\x08\x06' and len(végrehajtás_doboz) >= 42:
                CÍM_felbontás_csomag = végrehajtás_doboz[14:42]
                if CÍM_felbontás_csomag[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and CÍM_felbontás_csomag[24:28] == 자신.aktuális_CÍM:
                    válasz_1262b476 = CÍM_felbontás_csomag[:6] + b'\x00\x02' + valódi_cím + 자신.aktuális_CÍM + CÍM_felbontás_csomag[8:18]
                    자신.végrehajtás_doboz(végrehajtás_doboz[6:12] + valódi_cím + b'\x08\x06' + válasz_1262b476)
            elif végrehajtás_doboz[12:14] == b'\x08\x00':
                csomag_adat = végrehajtás_doboz[14:]
                자신.nyom_csomag('to_guest',csomag_adat)
                자신.informatikai_részleg_Függő[0] += b'\xc0' + csomag_adat.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Ciklus_ÉRTÉK(자신):
        try:
            while not 자신.Szünet_esemény.is_set():
                읽기대상들 = [sztring_adat for 순번, sztring_adat in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [sztring_adat for sztring_adat in 자신.접속자들 if sztring_adat is not None]
                쓰기대상들 = [sztring_adat for 순번, sztring_adat in enumerate(자신.접속자들) if sztring_adat is not None and 자신.informatikai_részleg_Függő[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for sztring_adat in 읽을수있음:
                    if sztring_adat in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(sztring_adat); 자신.접속자들[순번], _ = sztring_adat.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(sztring_adat); adat = sztring_adat.recv(16384)
                        if not adat: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.Ethernet_bevitel)(adat)
                for sztring_adat in 쓸수있음:
                    순번 = 자신.접속자들.index(sztring_adat)
                    try: cikk_DARAB = sztring_adat.send(자신.informatikai_részleg_Függő[순번])
                    except BlockingIOError: continue
                    del 자신.informatikai_részleg_Függő[순번][:cikk_DARAB]
                if any(len(MPERC_ÉRTÉK) > 1024 * 1024 for MPERC_ÉRTÉK in 자신.informatikai_részleg_Függő):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Szünet_esemény.is_set(): 자신.HIBA = str(보조항목)

    def Bezárás(자신):
        자신.Szünet_esemény.set(); 자신.dolgozó.join(timeout=2)
        for sztring_adat in 자신.수신창구들 + 자신.접속자들:
            if sztring_adat is not None: sztring_adat.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argumentum_TÖMB): 자신.Bezárás()
