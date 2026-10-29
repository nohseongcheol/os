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

apsolutna_adresa = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
internetska_adresa_VALUE = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class most_3de4fe3a:
    def __init__(자신, prijenos_datoteka_broj_priključka=2121, 전달규칙들=(), snimiti=False, gost_adresa=None, domaćin_adresa='127.0.0.1'):
        if not 1024 <= prijenos_datoteka_broj_priključka <= 65535 or 50000 <= prijenos_datoteka_broj_priključka <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.prijenos_datoteka_broj_priključka = prijenos_datoteka_broj_priključka
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        gost_adresa = gost_adresa or 자신.ip_config['IP']
        qemu_network(자신.ip_config, gost_adresa)
        adresa=ipaddress.IPv4Address(gost_adresa)
        자신.gost_adresa=str(adresa); 자신.redovno_adresa=adresa.packed
        adresa=ipaddress.IPv4Address(domaćin_adresa)
        if adresa.is_multicast or str(adresa)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.domaćin_adresa=str(adresa)
        자신.snimiti = snimiti; 자신.zapis_praćenja = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', prijenos_datoteka_broj_priključka)} | {('tcp', podaci_položaj) for podaci_položaj in range(50000,50008)}
        for filtar_VALUE in 전달규칙들:
            put_komponenta = filtar_VALUE.split(':')
            if len(put_komponenta) != 3 or put_komponenta[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, domaćin, gost = put_komponenta[0], int(put_komponenta[1]), int(put_komponenta[2])
            if not 1024 <= domaćin <= 65535 or not 1 <= gost <= 65535 or (통신규약, domaćin) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + filtar_VALUE)
            사용중주소.add((통신규약, domaćin)); 자신.전달규칙들.append((통신규약, domaćin, gost))
        자신.수신창구들 = []
        for _ in range(2):
            server_VALUE = socket.socket()
            server_VALUE.bind(('127.0.0.1', 0)); server_VALUE.listen(1); server_VALUE.setblocking(False)
            자신.수신창구들.append(server_VALUE)
        자신.접속자들 = [None, None]
        자신.odjel_informacijske_tehnologije_na_čekanju = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.odjel_informacijske_tehnologije_nevaljan = False
        자신.Pauziraj_događaj = threading.Event(); 자신.GREŠKA = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.Ciklus_VALUE, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, priključak_za_Ethernet = [niz_podaci.getsockname()[1] for niz_podaci in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.gost_adresa) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.prijenos_datoteka_broj_priključka, 자신.gost_adresa)
        for broj_priključka in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(broj_priključka, 자신.gost_adresa)
        for 통신규약, domaćin, gost in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, domaćin, 자신.gost_adresa, gost)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.domaćin_adresa+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(priključak_za_Ethernet),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, paket_podaci):
        자신.odjel_informacijske_tehnologije_na_čekanju[1] += struct.pack('!I', len(paket_podaci)) + paket_podaci

    def trag_paket(자신, 방향, paket_podaci):
        if not 자신.snimiti or len(paket_podaci)<20: return
        pomak_VALUE=(paket_podaci[0]&15)*4
        unos_VALUE={'time':time.monotonic(),'direction':방향,'bytes':len(paket_podaci),'protocol':paket_podaci[9]}
        if paket_podaci[9]==6 and len(paket_podaci)>=pomak_VALUE+20:
            원본자료,odredište_podaci_adresa,순서번호,확인번호,konfiguracija_Pozadinski_pametni_servis_za_transfer,Prozor=struct.unpack_from('!HHIIHH',paket_podaci,pomak_VALUE)
            unos_VALUE.update(source=원본자료,destination=odredište_podaci_adresa,seq=순서번호,ack=확인번호,flags=konfiguracija_Pozadinski_pametni_servis_za_transfer&255,window=Prozor,
                        payload=len(paket_podaci)-pomak_VALUE-((paket_podaci[pomak_VALUE+12]>>4)*4))
        자신.zapis_praćenja.append(unos_VALUE)
        if len(자신.zapis_praćenja)>2048: del 자신.zapis_praćenja[:1024]

    def 직렬전문입력(자신, podaci):
        for kodna_točka in podaci:
            if kodna_točka == 192:
                if 자신.직렬전문 and not 자신.odjel_informacijske_tehnologije_nevaljan and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        adresa=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(adresa)))
                            자신.redovno_adresa=adresa
                        except ValueError:
                            pass
                    자신.trag_paket('from_guest',자신.직렬전문)
                    자신.실행틀(관문기계주소 + apsolutna_adresa + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.odjel_informacijske_tehnologije_nevaljan = False
            elif kodna_točka == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if kodna_točka not in (220, 221): 자신.odjel_informacijske_tehnologije_nevaljan = True
                    kodna_točka = 192 if kodna_točka == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(kodna_točka)
                else: 자신.odjel_informacijske_tehnologije_nevaljan = True

    def 이더넷입력(자신, podaci):
        자신.Ethernet += podaci
        while len(자신.Ethernet) >= 4:
            artikl_COUNT = struct.unpack_from('!I', 자신.Ethernet)[0]
            if artikl_COUNT > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < artikl_COUNT + 4: return
            실행틀 = bytes(자신.Ethernet[4:4+artikl_COUNT]); del 자신.Ethernet[:4+artikl_COUNT]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                adresa_razlučivost_paket = 실행틀[14:42]
                if adresa_razlučivost_paket[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and adresa_razlučivost_paket[24:28] == 자신.redovno_adresa:
                    odgovor_1262b476 = adresa_razlučivost_paket[:6] + b'\x00\x02' + apsolutna_adresa + 자신.redovno_adresa + adresa_razlučivost_paket[8:18]
                    자신.실행틀(실행틀[6:12] + apsolutna_adresa + b'\x08\x06' + odgovor_1262b476)
            elif 실행틀[12:14] == b'\x08\x00':
                paket_podaci = 실행틀[14:]
                자신.trag_paket('to_guest',paket_podaci)
                자신.odjel_informacijske_tehnologije_na_čekanju[0] += b'\xc0' + paket_podaci.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Ciklus_VALUE(자신):
        try:
            while not 자신.Pauziraj_događaj.is_set():
                읽기대상들 = [niz_podaci for 순번, niz_podaci in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [niz_podaci for niz_podaci in 자신.접속자들 if niz_podaci is not None]
                쓰기대상들 = [niz_podaci for 순번, niz_podaci in enumerate(자신.접속자들) if niz_podaci is not None and 자신.odjel_informacijske_tehnologije_na_čekanju[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for niz_podaci in 읽을수있음:
                    if niz_podaci in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(niz_podaci); 자신.접속자들[순번], _ = niz_podaci.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(niz_podaci); podaci = niz_podaci.recv(16384)
                        if not podaci: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(podaci)
                for niz_podaci in 쓸수있음:
                    순번 = 자신.접속자들.index(niz_podaci)
                    try: artikl_COUNT = niz_podaci.send(자신.odjel_informacijske_tehnologije_na_čekanju[순번])
                    except BlockingIOError: continue
                    del 자신.odjel_informacijske_tehnologije_na_čekanju[순번][:artikl_COUNT]
                if any(len(SECOND_VALUE) > 1024 * 1024 for SECOND_VALUE in 자신.odjel_informacijske_tehnologije_na_čekanju):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Pauziraj_događaj.is_set(): 자신.GREŠKA = str(보조항목)

    def Zatvori(자신):
        자신.Pauziraj_događaj.set(); 자신.작업가닥.join(timeout=2)
        for niz_podaci in 자신.수신창구들 + 자신.접속자들:
            if niz_podaci is not None: niz_podaci.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argument_ARRAY): 자신.Zatvori()
