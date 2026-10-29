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

adres_bezwzględny = bytes.fromhex('525400123456')
brama_sprzęt_ADRES = bytes.fromhex('52550a000202')
adres_internetowy_WARTOŚĆ = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class mostek_3de4fe3a:
    def __init__(자신, transfer_plików_numer_portu=2121, 전달규칙들=(), Capture=False, gość_ADRES=None, host_ADRES='127.0.0.1'):
        if not 1024 <= transfer_plików_numer_portu <= 65535 or 50000 <= transfer_plików_numer_portu <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.transfer_plików_numer_portu = transfer_plików_numer_portu
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        gość_ADRES = gość_ADRES or 자신.ip_config['IP']
        qemu_network(자신.ip_config, gość_ADRES)
        Adres=ipaddress.IPv4Address(gość_ADRES)
        자신.gość_ADRES=str(Adres); 자신.bieżący_ADRES=Adres.packed
        Adres=ipaddress.IPv4Address(host_ADRES)
        if Adres.is_multicast or str(Adres)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.host_ADRES=str(Adres)
        자신.Capture = Capture; 자신.dziennik_śledzenia = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', transfer_plików_numer_portu)} | {('tcp', dane_stanowisko) for dane_stanowisko in range(50000,50008)}
        for filtr_WARTOŚĆ in 전달규칙들:
            ścieżka_składnik = filtr_WARTOŚĆ.split(':')
            if len(ścieżka_składnik) != 3 or ścieżka_składnik[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            sieć_ABI, host, gość = ścieżka_składnik[0], int(ścieżka_składnik[1]), int(ścieżka_składnik[2])
            if not 1024 <= host <= 65535 or not 1 <= gość <= 65535 or (sieć_ABI, host) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + filtr_WARTOŚĆ)
            사용중주소.add((sieć_ABI, host)); 자신.전달규칙들.append((sieć_ABI, host, gość))
        자신.수신창구들 = []
        for _ in range(2):
            serwer_WARTOŚĆ = socket.socket()
            serwer_WARTOŚĆ.bind(('127.0.0.1', 0)); serwer_WARTOŚĆ.listen(1); serwer_WARTOŚĆ.setblocking(False)
            자신.수신창구들.append(serwer_WARTOŚĆ)
        자신.접속자들 = [None, None]
        자신.systemy_informacyjne_oczekujący = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.systemy_informacyjne_nieważny = False
        자신.Wstrzymaj_konkurs = threading.Event(); 자신.błąd = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.pracownik = threading.Thread(target=자신.Cykl_WARTOŚĆ, daemon=True)
        자신.pracownik.start()

    def 전달인수(자신):
        port_COM_identyfikator, port_Ethernet = [ciąg_dane.getsockname()[1] for ciąg_dane in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.gość_ADRES) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.transfer_plików_numer_portu, 자신.gość_ADRES)
        for numer_portu in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(numer_portu, 자신.gość_ADRES)
        for sieć_ABI, host, gość in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(sieć_ABI, host, 자신.gość_ADRES, gość)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.host_ADRES+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(port_COM_identyfikator),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(port_Ethernet),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def wykonanie_kadr(자신, pakiet_dane):
        자신.systemy_informacyjne_oczekujący[1] += struct.pack('!I', len(pakiet_dane)) + pakiet_dane

    def ślad_pakiet(자신, 방향, pakiet_dane):
        if not 자신.Capture or len(pakiet_dane)<20: return
        przesunąć_WARTOŚĆ_450fc799=(pakiet_dane[0]&15)*4
        wpis_WARTOŚĆ={'time':time.monotonic(),'direction':방향,'bytes':len(pakiet_dane),'protocol':pakiet_dane[9]}
        if pakiet_dane[9]==6 and len(pakiet_dane)>=przesunąć_WARTOŚĆ_450fc799+20:
            원본자료,cel_dane_ADRES,zamówić_identyfikator,확인번호,konfiguracja_BITS,Okno=struct.unpack_from('!HHIIHH',pakiet_dane,przesunąć_WARTOŚĆ_450fc799)
            wpis_WARTOŚĆ.update(source=원본자료,destination=cel_dane_ADRES,seq=zamówić_identyfikator,ack=확인번호,flags=konfiguracja_BITS&255,window=Okno,
                        payload=len(pakiet_dane)-przesunąć_WARTOŚĆ_450fc799-((pakiet_dane[przesunąć_WARTOŚĆ_450fc799+12]>>4)*4))
        자신.dziennik_śledzenia.append(wpis_WARTOŚĆ)
        if len(자신.dziennik_śledzenia)>2048: del 자신.dziennik_śledzenia[:1024]

    def 직렬전문입력(자신, dane):
        for kod_znaku in dane:
            if kod_znaku == 192:
                if 자신.직렬전문 and not 자신.systemy_informacyjne_nieważny and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        Adres=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(Adres)))
                            자신.bieżący_ADRES=Adres
                        except ValueError:
                            pass
                    자신.ślad_pakiet('from_guest',자신.직렬전문)
                    자신.wykonanie_kadr(brama_sprzęt_ADRES + adres_bezwzględny + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.systemy_informacyjne_nieważny = False
            elif kod_znaku == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if kod_znaku not in (220, 221): 자신.systemy_informacyjne_nieważny = True
                    kod_znaku = 192 if kod_znaku == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(kod_znaku)
                else: 자신.systemy_informacyjne_nieważny = True

    def Ethernet_wejście(자신, dane):
        자신.Ethernet += dane
        while len(자신.Ethernet) >= 4:
            towar_ILE_LICZB = struct.unpack_from('!I', 자신.Ethernet)[0]
            if towar_ILE_LICZB > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < towar_ILE_LICZB + 4: return
            wykonanie_kadr = bytes(자신.Ethernet[4:4+towar_ILE_LICZB]); del 자신.Ethernet[:4+towar_ILE_LICZB]
            if len(wykonanie_kadr) < 14: continue
            if wykonanie_kadr[12:14] == b'\x08\x06' and len(wykonanie_kadr) >= 42:
                ADRES_rozdzielczość_pakiet = wykonanie_kadr[14:42]
                if ADRES_rozdzielczość_pakiet[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and ADRES_rozdzielczość_pakiet[24:28] == 자신.bieżący_ADRES:
                    odpowiedź_1262b476 = ADRES_rozdzielczość_pakiet[:6] + b'\x00\x02' + adres_bezwzględny + 자신.bieżący_ADRES + ADRES_rozdzielczość_pakiet[8:18]
                    자신.wykonanie_kadr(wykonanie_kadr[6:12] + adres_bezwzględny + b'\x08\x06' + odpowiedź_1262b476)
            elif wykonanie_kadr[12:14] == b'\x08\x00':
                pakiet_dane = wykonanie_kadr[14:]
                자신.ślad_pakiet('to_guest',pakiet_dane)
                자신.systemy_informacyjne_oczekujący[0] += b'\xc0' + pakiet_dane.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Cykl_WARTOŚĆ(자신):
        try:
            while not 자신.Wstrzymaj_konkurs.is_set():
                읽기대상들 = [ciąg_dane for 순번, ciąg_dane in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [ciąg_dane for ciąg_dane in 자신.접속자들 if ciąg_dane is not None]
                쓰기대상들 = [ciąg_dane for 순번, ciąg_dane in enumerate(자신.접속자들) if ciąg_dane is not None and 자신.systemy_informacyjne_oczekujący[순번]]
                읽을수있음, zapisywalny, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for ciąg_dane in 읽을수있음:
                    if ciąg_dane in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(ciąg_dane); 자신.접속자들[순번], _ = ciąg_dane.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(ciąg_dane); dane = ciąg_dane.recv(16384)
                        if not dane: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.Ethernet_wejście)(dane)
                for ciąg_dane in zapisywalny:
                    순번 = 자신.접속자들.index(ciąg_dane)
                    try: towar_ILE_LICZB = ciąg_dane.send(자신.systemy_informacyjne_oczekujący[순번])
                    except BlockingIOError: continue
                    del 자신.systemy_informacyjne_oczekujący[순번][:towar_ILE_LICZB]
                if any(len(SEKUNDA_WARTOŚĆ) > 1024 * 1024 for SEKUNDA_WARTOŚĆ in 자신.systemy_informacyjne_oczekujący):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Wstrzymaj_konkurs.is_set(): 자신.błąd = str(보조항목)

    def Zamknięte(자신):
        자신.Wstrzymaj_konkurs.set(); 자신.pracownik.join(timeout=2)
        for ciąg_dane in 자신.수신창구들 + 자신.접속자들:
            if ciąg_dane is not None: ciąg_dane.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argument_TABLICA): 자신.Zamknięte()
