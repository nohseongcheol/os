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

absolutní_adresa = bytes.fromhex('525400123456')
brána_hardware_ODKAZ = bytes.fromhex('52550a000202')
internetová_adresa_HODNOTA = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class most_3de4fe3a:
    def __init__(자신, přenos_souborů_číslo_portu=2121, 전달규칙들=(), čerpat=False, host_ODKAZ=None, hostit_ODKAZ='127.0.0.1'):
        if not 1024 <= přenos_souborů_číslo_portu <= 65535 or 50000 <= přenos_souborů_číslo_portu <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.přenos_souborů_číslo_portu = přenos_souborů_číslo_portu
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        host_ODKAZ = host_ODKAZ or 자신.ip_config['IP']
        qemu_network(자신.ip_config, host_ODKAZ)
        Adresa=ipaddress.IPv4Address(host_ODKAZ)
        자신.host_ODKAZ=str(Adresa); 자신.dobrá_ODKAZ=Adresa.packed
        Adresa=ipaddress.IPv4Address(hostit_ODKAZ)
        if Adresa.is_multicast or str(Adresa)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.hostit_ODKAZ=str(Adresa)
        자신.čerpat = čerpat; 자신.protokol_trasování = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', přenos_souborů_číslo_portu)} | {('tcp', data_pozice) for data_pozice in range(50000,50008)}
        for filtr_HODNOTA in 전달규칙들:
            cesta_součást = filtr_HODNOTA.split(':')
            if len(cesta_součást) != 3 or cesta_součást[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            síť_ABI, hostit, host = cesta_součást[0], int(cesta_součást[1]), int(cesta_součást[2])
            if not 1024 <= hostit <= 65535 or not 1 <= host <= 65535 or (síť_ABI, hostit) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + filtr_HODNOTA)
            사용중주소.add((síť_ABI, hostit)); 자신.전달규칙들.append((síť_ABI, hostit, host))
        자신.수신창구들 = []
        for _ in range(2):
            server_HODNOTA = socket.socket()
            server_HODNOTA.bind(('127.0.0.1', 0)); server_HODNOTA.listen(1); server_HODNOTA.setblocking(False)
            자신.수신창구들.append(server_HODNOTA)
        자신.접속자들 = [None, None]
        자신.informační_systémy_probíhá = [bytearray(), bytearray()]
        자신.síť_Ethernet = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.informační_systémy_neplatný = False
        자신.Pozastavit_událost = threading.Event(); 자신.chyba = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.pracovník = threading.Thread(target=자신.Cyklus_HODNOTA, daemon=True)
        자신.pracovník.start()

    def 전달인수(자신):
        port_COM_číslo, port_sítě_Ethernet = [řetězec_data.getsockname()[1] for řetězec_data in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.host_ODKAZ) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.přenos_souborů_číslo_portu, 자신.host_ODKAZ)
        for číslo_portu in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(číslo_portu, 자신.host_ODKAZ)
        for síť_ABI, hostit, host in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(síť_ABI, hostit, 자신.host_ODKAZ, host)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.hostit_ODKAZ+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(port_COM_číslo),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(port_sítě_Ethernet),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def spuštění_rámec(자신, paket_data):
        자신.informační_systémy_probíhá[1] += struct.pack('!I', len(paket_data)) + paket_data

    def stopa_paket(자신, 방향, paket_data):
        if not 자신.čerpat or len(paket_data)<20: return
        POSUN_HODNOTA=(paket_data[0]&15)*4
        položka_HODNOTA={'time':time.monotonic(),'direction':방향,'bytes':len(paket_data),'protocol':paket_data[9]}
        if paket_data[9]==6 and len(paket_data)>=POSUN_HODNOTA+20:
            원본자료,cíl_data_ODKAZ,pořadí_číslo,확인번호,konfigurace_BITS,Okno=struct.unpack_from('!HHIIHH',paket_data,POSUN_HODNOTA)
            položka_HODNOTA.update(source=원본자료,destination=cíl_data_ODKAZ,seq=pořadí_číslo,ack=확인번호,flags=konfigurace_BITS&255,window=Okno,
                        payload=len(paket_data)-POSUN_HODNOTA-((paket_data[POSUN_HODNOTA+12]>>4)*4))
        자신.protokol_trasování.append(položka_HODNOTA)
        if len(자신.protokol_trasování)>2048: del 자신.protokol_trasování[:1024]

    def protokol_SLIP_vstup(자신, data):
        for bod_kódu in data:
            if bod_kódu == 192:
                if 자신.직렬전문 and not 자신.informační_systémy_neplatný and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        Adresa=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(Adresa)))
                            자신.dobrá_ODKAZ=Adresa
                        except ValueError:
                            pass
                    자신.stopa_paket('from_guest',자신.직렬전문)
                    자신.spuštění_rámec(brána_hardware_ODKAZ + absolutní_adresa + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.informační_systémy_neplatný = False
            elif bod_kódu == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if bod_kódu not in (220, 221): 자신.informační_systémy_neplatný = True
                    bod_kódu = 192 if bod_kódu == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(bod_kódu)
                else: 자신.informační_systémy_neplatný = True

    def síť_Ethernet_vstup(자신, data):
        자신.síť_Ethernet += data
        while len(자신.síť_Ethernet) >= 4:
            zboží_POČET = struct.unpack_from('!I', 자신.síť_Ethernet)[0]
            if zboží_POČET > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.síť_Ethernet) < zboží_POČET + 4: return
            spuštění_rámec = bytes(자신.síť_Ethernet[4:4+zboží_POČET]); del 자신.síť_Ethernet[:4+zboží_POČET]
            if len(spuštění_rámec) < 14: continue
            if spuštění_rámec[12:14] == b'\x08\x06' and len(spuštění_rámec) >= 42:
                ODKAZ_řešení_paket = spuštění_rámec[14:42]
                if ODKAZ_řešení_paket[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and ODKAZ_řešení_paket[24:28] == 자신.dobrá_ODKAZ:
                    odpověď = ODKAZ_řešení_paket[:6] + b'\x00\x02' + absolutní_adresa + 자신.dobrá_ODKAZ + ODKAZ_řešení_paket[8:18]
                    자신.spuštění_rámec(spuštění_rámec[6:12] + absolutní_adresa + b'\x08\x06' + odpověď)
            elif spuštění_rámec[12:14] == b'\x08\x00':
                paket_data = spuštění_rámec[14:]
                자신.stopa_paket('to_guest',paket_data)
                자신.informační_systémy_probíhá[0] += b'\xc0' + paket_data.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Cyklus_HODNOTA(자신):
        try:
            while not 자신.Pozastavit_událost.is_set():
                읽기대상들 = [řetězec_data for 순번, řetězec_data in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [řetězec_data for řetězec_data in 자신.접속자들 if řetězec_data is not None]
                쓰기대상들 = [řetězec_data for 순번, řetězec_data in enumerate(자신.접속자들) if řetězec_data is not None and 자신.informační_systémy_probíhá[순번]]
                읽을수있음, zapisovatelný, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for řetězec_data in 읽을수있음:
                    if řetězec_data in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(řetězec_data); 자신.접속자들[순번], _ = řetězec_data.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(řetězec_data); data = řetězec_data.recv(16384)
                        if not data: return
                        (자신.protokol_SLIP_vstup if 순번 == 0 else 자신.síť_Ethernet_vstup)(data)
                for řetězec_data in zapisovatelný:
                    순번 = 자신.접속자들.index(řetězec_data)
                    try: zboží_POČET = řetězec_data.send(자신.informační_systémy_probíhá[순번])
                    except BlockingIOError: continue
                    del 자신.informační_systémy_probíhá[순번][:zboží_POČET]
                if any(len(SEKUNDA_HODNOTA) > 1024 * 1024 for SEKUNDA_HODNOTA in 자신.informační_systémy_probíhá):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Pozastavit_událost.is_set(): 자신.chyba = str(보조항목)

    def Zavřené(자신):
        자신.Pozastavit_událost.set(); 자신.pracovník.join(timeout=2)
        for řetězec_data in 자신.수신창구들 + 자신.접속자들:
            if řetězec_data is not None: řetězec_data.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argument_pole): 자신.Zavřené()
