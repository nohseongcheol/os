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

absolutni_naslov = bytes.fromhex('525400123456')
prehod_strojna_oprema_naslov = bytes.fromhex('52550a000202')
internetni_račun_VALUE = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class most_3de4fe3a:
    def __init__(자신, prenos_datotek_številka_vrat=2121, 전달규칙들=(), snemati=False, gost_naslov=None, gostiti_naslov='127.0.0.1'):
        if not 1024 <= prenos_datotek_številka_vrat <= 65535 or 50000 <= prenos_datotek_številka_vrat <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.prenos_datotek_številka_vrat = prenos_datotek_številka_vrat
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        gost_naslov = gost_naslov or 자신.ip_config['IP']
        qemu_network(자신.ip_config, gost_naslov)
        naslov=ipaddress.IPv4Address(gost_naslov)
        자신.gost_naslov=str(naslov); 자신.sprotno_naslov=naslov.packed
        naslov=ipaddress.IPv4Address(gostiti_naslov)
        if naslov.is_multicast or str(naslov)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.gostiti_naslov=str(naslov)
        자신.snemati = snemati; 자신.dnevnik_sledenja = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', prenos_datotek_številka_vrat)} | {('tcp', podatki_položaj) for podatki_položaj in range(50000,50008)}
        for filter_VALUE in 전달규칙들:
            pot_komponenta = filter_VALUE.split(':')
            if len(pot_komponenta) != 3 or pot_komponenta[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, gostiti, gost = pot_komponenta[0], int(pot_komponenta[1]), int(pot_komponenta[2])
            if not 1024 <= gostiti <= 65535 or not 1 <= gost <= 65535 or (통신규약, gostiti) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + filter_VALUE)
            사용중주소.add((통신규약, gostiti)); 자신.전달규칙들.append((통신규약, gostiti, gost))
        자신.수신창구들 = []
        for _ in range(2):
            strežnik_VALUE = socket.socket()
            strežnik_VALUE.bind(('127.0.0.1', 0)); strežnik_VALUE.listen(1); strežnik_VALUE.setblocking(False)
            자신.수신창구들.append(strežnik_VALUE)
        자신.접속자들 = [None, None]
        자신.informacijska_tehnologija_čakajoče = [bytearray(), bytearray()]
        자신.ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.informacijska_tehnologija_neveljaven = False
        자신.Premor_dogodek = threading.Event(); 자신.NAPAKA = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Krog_VALUE, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, vrata_za_ethernet = [niz_podatki.getsockname()[1] for niz_podatki in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.gost_naslov) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.prenos_datotek_številka_vrat, 자신.gost_naslov)
        for številka_vrat in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(številka_vrat, 자신.gost_naslov)
        for 통신규약, gostiti, gost in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, gostiti, 자신.gost_naslov, gost)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.gostiti_naslov+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(vrata_za_ethernet),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, paket_podatki):
        자신.informacijska_tehnologija_čakajoče[1] += struct.pack('!I', len(paket_podatki)) + paket_podatki

    def sled_paket(자신, 방향, paket_podatki):
        if not 자신.snemati or len(paket_podatki)<20: return
        odmik_VALUE=(paket_podatki[0]&15)*4
        vnos_VALUE={'time':time.monotonic(),'direction':방향,'bytes':len(paket_podatki),'protocol':paket_podatki[9]}
        if paket_podatki[9]==6 and len(paket_podatki)>=odmik_VALUE+20:
            원본자료,cilj_podatki_naslov,순서번호,확인번호,konfiguracija_storitev_Background_Intelligent_Transfer_Service,okno=struct.unpack_from('!HHIIHH',paket_podatki,odmik_VALUE)
            vnos_VALUE.update(source=원본자료,destination=cilj_podatki_naslov,seq=순서번호,ack=확인번호,flags=konfiguracija_storitev_Background_Intelligent_Transfer_Service&255,window=okno,
                        payload=len(paket_podatki)-odmik_VALUE-((paket_podatki[odmik_VALUE+12]>>4)*4))
        자신.dnevnik_sledenja.append(vnos_VALUE)
        if len(자신.dnevnik_sledenja)>2048: del 자신.dnevnik_sledenja[:1024]

    def 직렬전문입력(자신, podatki):
        for koda_znaka in podatki:
            if koda_znaka == 192:
                if 자신.직렬전문 and not 자신.informacijska_tehnologija_neveljaven and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        naslov=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(naslov)))
                            자신.sprotno_naslov=naslov
                        except ValueError:
                            pass
                    자신.sled_paket('from_guest',자신.직렬전문)
                    자신.실행틀(prehod_strojna_oprema_naslov + absolutni_naslov + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.informacijska_tehnologija_neveljaven = False
            elif koda_znaka == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if koda_znaka not in (220, 221): 자신.informacijska_tehnologija_neveljaven = True
                    koda_znaka = 192 if koda_znaka == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(koda_znaka)
                else: 자신.informacijska_tehnologija_neveljaven = True

    def 이더넷입력(자신, podatki):
        자신.ethernet += podatki
        while len(자신.ethernet) >= 4:
            element_COUNT = struct.unpack_from('!I', 자신.ethernet)[0]
            if element_COUNT > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.ethernet) < element_COUNT + 4: return
            실행틀 = bytes(자신.ethernet[4:4+element_COUNT]); del 자신.ethernet[:4+element_COUNT]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                naslov_ločljivost_paket = 실행틀[14:42]
                if naslov_ločljivost_paket[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and naslov_ločljivost_paket[24:28] == 자신.sprotno_naslov:
                    odziv = naslov_ločljivost_paket[:6] + b'\x00\x02' + absolutni_naslov + 자신.sprotno_naslov + naslov_ločljivost_paket[8:18]
                    자신.실행틀(실행틀[6:12] + absolutni_naslov + b'\x08\x06' + odziv)
            elif 실행틀[12:14] == b'\x08\x00':
                paket_podatki = 실행틀[14:]
                자신.sled_paket('to_guest',paket_podatki)
                자신.informacijska_tehnologija_čakajoče[0] += b'\xc0' + paket_podatki.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Krog_VALUE(자신):
        try:
            while not 자신.Premor_dogodek.is_set():
                읽기대상들 = [niz_podatki for 순번, niz_podatki in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [niz_podatki for niz_podatki in 자신.접속자들 if niz_podatki is not None]
                쓰기대상들 = [niz_podatki for 순번, niz_podatki in enumerate(자신.접속자들) if niz_podatki is not None and 자신.informacijska_tehnologija_čakajoče[순번]]
                읽을수있음, zapisljiv, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for niz_podatki in 읽을수있음:
                    if niz_podatki in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(niz_podatki); 자신.접속자들[순번], _ = niz_podatki.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(niz_podatki); podatki = niz_podatki.recv(16384)
                        if not podatki: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(podatki)
                for niz_podatki in zapisljiv:
                    순번 = 자신.접속자들.index(niz_podatki)
                    try: element_COUNT = niz_podatki.send(자신.informacijska_tehnologija_čakajoče[순번])
                    except BlockingIOError: continue
                    del 자신.informacijska_tehnologija_čakajoče[순번][:element_COUNT]
                if any(len(SECOND_VALUE) > 1024 * 1024 for SECOND_VALUE in 자신.informacijska_tehnologija_čakajoče):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Premor_dogodek.is_set(): 자신.NAPAKA = str(보조항목)

    def Zapri(자신):
        자신.Premor_dogodek.set(); 자신.작업가닥.join(timeout=2)
        for niz_podatki in 자신.수신창구들 + 자신.접속자들:
            if niz_podatki is not None: niz_podatki.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argument_ARRAY): 자신.Zapri()
